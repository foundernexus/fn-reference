/* Option pool shuffle calculator.
   Client-side only. No tracking, no network.
   Mechanics follow Kruze (pre- vs post-money pool) and Carta (same contrast).
   Worked numbers are hypothetical. Not legal advice.
*/
(function () {
  "use strict";

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "className") node.className = attrs[k];
        else if (k === "htmlFor") node.htmlFor = attrs[k];
        else if (k === "innerHTML") node.innerHTML = attrs[k];
        else if (k.slice(0, 2) === "on" && typeof attrs[k] === "function") {
          node.addEventListener(k.slice(2).toLowerCase(), attrs[k]);
        } else if (attrs[k] === true) node.setAttribute(k, k);
        else if (attrs[k] !== false && attrs[k] != null)
          node.setAttribute(k, String(attrs[k]));
      });
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function parseMoney(value) {
    if (value == null) return null;
    var s = String(value).trim().replace(/[$,\s]/g, "");
    if (s === "") return null;
    var n = Number(s);
    if (!Number.isFinite(n)) return null;
    return n;
  }

  function parsePct(value) {
    if (value == null) return null;
    var s = String(value).trim().replace(/%/g, "").replace(/,/g, "");
    if (s === "") return null;
    var n = Number(s);
    if (!Number.isFinite(n)) return null;
    return n;
  }

  function fmtPct(n, digits) {
    if (!Number.isFinite(n)) return "—";
    var d = digits == null ? 2 : digits;
    return n.toFixed(d) + "%";
  }

  function fmtMoney(n) {
    if (!Number.isFinite(n)) return "—";
    var abs = Math.abs(n);
    var opts =
      abs >= 1e6
        ? { maximumFractionDigits: 2 }
        : abs >= 1
          ? { maximumFractionDigits: 0 }
          : { maximumFractionDigits: 2 };
    return "$" + Math.round(n).toLocaleString("en-US", opts);
  }

  function field(id, label, input, hint) {
    var kids = [el("label", { htmlFor: id }, [label]), input];
    if (hint) kids.push(el("p", { className: "eq-hint" }, [hint]));
    return el("div", { className: "eq-field" }, kids);
  }

  /** Normalize current FD share count to 100. */
  function compute(pre, invest, poolCurPct, targetPct) {
    var inv = invest / (pre + invest); // investor headline ownership of post-money
    var H = 100 - poolCurPct; // existing holders excl. unallocated pool
    var P0 = poolCurPct;

    // --- Pre-money placement (shuffle / VC-friendly) ---
    // Target pool = targetPct of post-money FD; investor keeps inv of post-money.
    var holdersEndPre = 1 - inv - targetPct / 100;
    var preMoney = null;
    if (holdersEndPre > 0 && targetPct / 100 + inv < 1) {
      var sPostPre = H / holdersEndPre;
      var poolSharesPre = (targetPct / 100) * sPostPre;
      var invSharesPre = inv * sPostPre;
      var topUpPre = poolSharesPre - P0;
      if (topUpPre < -1e-9) {
        preMoney = { impossible: "topup_negative", topUpPre: topUpPre };
      } else {
        if (topUpPre < 0) topUpPre = 0;
        var sPre = H + poolSharesPre;
        preMoney = {
          topUpShares: topUpPre,
          topUpPtsOfStart: topUpPre, // since start total = 100
          poolPreClosePct: (poolSharesPre / sPre) * 100, // = target/(1-inv)
          holdersPreClosePct: (H / sPre) * 100,
          holdersPostPct: (H / sPostPre) * 100,
          poolPostPct: (poolSharesPre / sPostPre) * 100,
          investorPostPct: (invSharesPre / sPostPre) * 100,
          effectivePre: pre * (H / sPre), // economics on existing issued stack
          priceFactor: 100 / sPre, // vs $1 notionally on 100 shares
          sPre: sPre,
          sPost: sPostPre,
        };
      }
    }

    // --- Post-money placement (founder-friendlier) ---
    // Invest first at inv of current FD, then expand pool to targetPct of new total.
    var postMoney = null;
    var invSharesPost = (100 * inv) / (1 - inv);
    var s1 = 100 + invSharesPost;
    var denom = 1 - targetPct / 100;
    if (denom > 0 && inv < 1) {
      var delta = ((targetPct / 100) * s1 - P0) / denom;
      if (delta < -1e-9) {
        postMoney = { impossible: "topup_negative", delta: delta };
      } else {
        if (delta < 0) delta = 0;
        var sPostPost = s1 + delta;
        var poolSharesPost = P0 + delta;
        postMoney = {
          topUpShares: delta,
          topUpPtsOfStart: delta,
          holdersPostPct: (H / sPostPost) * 100,
          poolPostPct: (poolSharesPost / sPostPost) * 100,
          investorPostPct: (invSharesPost / sPostPost) * 100,
          holdersAfterInvestBeforePool: (H / s1) * 100,
          investorAfterInvestBeforePool: (invSharesPost / s1) * 100,
          s1: s1,
          sPost: sPostPost,
        };
      }
    }

    return {
      invPct: inv * 100,
      postMoneyVal: pre + invest,
      H: H,
      P0: P0,
      preMoney: preMoney,
      postMoney: postMoney,
    };
  }

  function mount(root) {
    if (root.getAttribute("data-ops-ready") === "true") return;
    root.setAttribute("data-ops-ready", "true");

    var preInput = el("input", {
      id: "ops-pre",
      name: "pre",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      required: true,
      value: "40000000",
      placeholder: "e.g. 40000000",
    });
    var investInput = el("input", {
      id: "ops-invest",
      name: "invest",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      required: true,
      value: "10000000",
      placeholder: "e.g. 10000000",
    });
    var poolInput = el("input", {
      id: "ops-pool",
      name: "pool",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      required: true,
      value: "5",
      placeholder: "e.g. 5",
    });
    var targetInput = el("input", {
      id: "ops-target",
      name: "target",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      required: true,
      value: "15",
      placeholder: "e.g. 15",
    });
    var errorEl = el("p", { className: "eq-error", hidden: true });
    var outEl = el("div", { className: "eq-out", hidden: true, tabindex: "-1" });

    function setError(msg) {
      if (msg) {
        errorEl.hidden = false;
        errorEl.textContent = msg;
      } else {
        errorEl.hidden = true;
        errorEl.textContent = "";
      }
    }

    function header(cols) {
      return el(
        "tr",
        null,
        cols.map(function (t) {
          return el("th", { scope: "col" }, [t]);
        })
      );
    }

    function dataRow(cells) {
      return el(
        "tr",
        null,
        cells.map(function (t, i) {
          return el(i === 0 ? "th" : "td", i === 0 ? { scope: "row" } : null, [
            String(t),
          ]);
        })
      );
    }

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";

      var pre = parseMoney(preInput.value);
      var invest = parseMoney(investInput.value);
      var poolCur = parsePct(poolInput.value);
      var target = parsePct(targetInput.value);

      if (pre == null || invest == null || poolCur == null || target == null) {
        setError("Enter pre-money, new investment, current pool %, and target pool % as numbers.");
        return;
      }
      if (pre <= 0) {
        setError("Pre-money valuation must be greater than 0.");
        return;
      }
      if (invest <= 0) {
        setError("New investment must be greater than 0.");
        return;
      }
      if (poolCur < 0 || poolCur >= 100) {
        setError("Current unallocated pool must be between 0 and 100.");
        return;
      }
      if (target <= 0 || target >= 100) {
        setError("Target option pool must be greater than 0 and less than 100.");
        return;
      }
      if (target <= poolCur) {
        setError(
          "Target pool is not above current unallocated. Raise the target, or you do not need a top-up for this comparison."
        );
        return;
      }

      var inv = invest / (pre + invest);
      if (target / 100 + inv >= 1) {
        setError(
          "Target pool plus investor ownership would exceed 100% of post-money. Lower the target or the raise relative to pre-money."
        );
        return;
      }

      var r = compute(pre, invest, poolCur, target);
      var pm = r.preMoney;
      var po = r.postMoney;

      if (!pm || pm.impossible || !po || po.impossible) {
        setError(
          "These inputs cannot reach the target pool under standard pre/post placement. Check that target plus investor ownership stays under 100%."
        );
        return;
      }

      var holdersBefore = r.H; // % of company today (excl. unallocated)

      var table = el("table", null, [
        el("thead", null, [
          header([
            "After the round",
            "Pre-money pool (shuffle)",
            "Post-money pool",
          ]),
        ]),
        el("tbody", null, [
          dataRow([
            "Existing holders (excl. unallocated pool)",
            fmtPct(pm.holdersPostPct),
            fmtPct(po.holdersPostPct),
          ]),
          dataRow([
            "Unallocated option pool",
            fmtPct(pm.poolPostPct),
            fmtPct(po.poolPostPct),
          ]),
          dataRow([
            "New investor",
            fmtPct(pm.investorPostPct),
            fmtPct(po.investorPostPct),
          ]),
          dataRow([
            "Pool top-up (share units on a 100-share start)",
            pm.topUpShares.toFixed(2),
            po.topUpShares.toFixed(2),
          ]),
        ]),
      ]);

      var gap = po.holdersPostPct - pm.holdersPostPct;
      var read =
        "Existing holders start at " +
        fmtPct(holdersBefore) +
        " of the company (everything except the " +
        fmtPct(poolCur, 1) +
        " unallocated pool). Under pre-money placement they finish at " +
        fmtPct(pm.holdersPostPct) +
        ". Under post-money placement they finish at " +
        fmtPct(po.holdersPostPct) +
        ". That is " +
        fmtPct(gap) +
        " of the company kept when the top-up dilutes the new investor too. The new investor owns " +
        fmtPct(pm.investorPostPct) +
        " when the pool is carved pre-money, and " +
        fmtPct(po.investorPostPct) +
        " when it is carved post-money. Headline investor ownership on cash alone is " +
        fmtPct(r.invPct) +
        " of a " +
        fmtMoney(r.postMoneyVal) +
        " post-money.";

      var formulas = el("div", { className: "eq-note" }, [
        el("strong", null, ["Formulas (normalized to 100 fully diluted shares today). "]),
        document.createTextNode(
          "Investor headline % = investment ÷ (pre-money + investment) = " +
            fmtPct(r.invPct) +
            ". Pre-money placement: existing-holder shares stay fixed; post-money total = holders ÷ (1 − investor% − target%); pool shares = target% × that total; top-up = pool shares − current pool. Before close, pool as % of pre-money FD = target% ÷ (1 − investor%) = " +
            fmtPct(pm.poolPreClosePct) +
            ". Post-money placement: issue investor shares first so they own the headline % of the then-current FD; then add pool shares Δ where (current pool + Δ) ÷ (shares after invest + Δ) = target%."
        ),
      ]);

      var econ =
        "On the pre-money path, the effective claim of today's existing stack against the headline pre-money is about " +
        fmtMoney(pm.effectivePre) +
        " (headline pre × existing shares ÷ pre-close FD after top-up). That is the economic haircut Kruze walks in their shuffle examples. Confirm with counsel and your cap table software.";

      outEl.appendChild(
        el("p", { className: "eq-lede", style: "margin-top:0" }, [
          "Side-by-side on your inputs. Pre-money pool is the usual term-sheet path (Kruze; Carta).",
        ])
      );
      outEl.appendChild(table);
      outEl.appendChild(el("p", { className: "eq-note" }, [read]));
      outEl.appendChild(el("p", { className: "eq-note" }, [econ]));
      outEl.appendChild(formulas);
      outEl.appendChild(
        el("p", { className: "eq-note" }, [
          "Hypothetical arithmetic on the numbers you typed. Ignores SAFEs, converts, warrants, multiple share classes, and promised-but-ungranted IOUs. Not legal, tax, or compensation advice.",
        ])
      );
      outEl.hidden = false;
      outEl.focus();
    }

    var form = el("form", { id: "ops-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults match the labeled hub sketch: $40M pre, $10M in, 5% → 15% pool. Change them. Target % is of post-round fully diluted shares.",
      ]),
      field("ops-pre", "Pre-money valuation ($)", preInput),
      field("ops-invest", "New investment ($)", investInput),
      field("ops-pool", "Current unallocated pool %", poolInput),
      field("ops-target", "Target option pool % (post-round FD)", targetInput),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Reset to hub sketch"]),
      ]),
    ]);

    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (e) {
      e.preventDefault();
      preInput.value = "40000000";
      investInput.value = "10000000";
      poolInput.value = "5";
      targetInput.value = "15";
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    root.appendChild(form);
    root.appendChild(outEl);
  }

  function boot() {
    var root = document.getElementById("option-pool-shuffle-calculator");
    if (root) mount(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
