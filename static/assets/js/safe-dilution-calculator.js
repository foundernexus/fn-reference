/* SAFE dilution calculator.
   Client-side only. No tracking, no network.
   Mechanics follow the Y Combinator post-money safe user guide: each safe converts at the
   lower of (post-money cap / Company Capitalization) and the round price times the discount
   rate (or the round price itself). Company Capitalization counts today's fully diluted shares
   and every converting safe, but not the new money or the pool increase for the round.
   The pool increase sits in the pre-money. Not legal or tax advice.
*/
(function () {
  "use strict";

  var MAX_SAFES = 8;
  var DEFAULTS = {
    shares: "10000000",
    founders: "92.5",
    pool: "1",
    pre: "15000000",
    newMoney: "5000000",
    target: "10",
    safes: [
      { amount: "200000", cap: "4000000", discount: "" },
      { amount: "800000", cap: "8000000", discount: "" },
    ],
  };

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "className") node.className = attrs[k];
        else if (k === "htmlFor") node.htmlFor = attrs[k];
        else if (k.slice(0, 2) === "on" && typeof attrs[k] === "function") {
          node.addEventListener(k.slice(2).toLowerCase(), attrs[k]);
        } else if (attrs[k] === true) node.setAttribute(k, k);
        else if (attrs[k] !== false && attrs[k] != null) node.setAttribute(k, String(attrs[k]));
      });
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  function parseNum(value) {
    if (value == null) return null;
    var s = String(value).trim().replace(/[$,%\s]/g, "");
    if (s === "") return null;
    var n = Number(s);
    return Number.isFinite(n) ? n : NaN;
  }

  function fmtPct(n) {
    return Number.isFinite(n) ? n.toFixed(2) + "%" : "n/a";
  }
  function fmtMoney(n) {
    if (!Number.isFinite(n)) return "n/a";
    return "$" + Math.round(n).toLocaleString("en-US");
  }
  function fmtPrice(n) {
    return Number.isFinite(n) ? "$" + n.toFixed(4) : "n/a";
  }
  function fmtShares(n) {
    return Number.isFinite(n) ? Math.round(n).toLocaleString("en-US") : "n/a";
  }

  /* Solve the conversion. Fixed-point on Company Capitalization (K) and round price (p).
     safes: [{amount, cap|null, discount 0..<100}] */
  function compute(inp) {
    var C0 = inp.shares;
    var F = (C0 * inp.founders) / 100;
    var U0 = (C0 * inp.pool) / 100;
    var O = C0 - F - U0;
    var inv = inp.newMoney / (inp.pre + inp.newMoney);
    var t = inp.target / 100;

    var K = C0;
    var p = inp.pre / C0;
    var s = inp.safes.map(function () { return 0; });
    var basis = inp.safes.map(function () { return ""; });
    var D = 0, T = 0, S = 0;
    for (var iter = 0; iter < 5000; iter++) {
      var sum = 0;
      for (var i = 0; i < inp.safes.length; i++) {
        var sf = inp.safes[i];
        var price = p, b = "round price";
        if (sf.discount > 0) {
          var dp = p * (1 - sf.discount / 100);
          if (dp < price) { price = dp; b = "discount"; }
        }
        if (sf.cap) {
          var cp = sf.cap / K;
          if (cp < price) { price = cp; b = "cap"; }
        }
        s[i] = sf.amount / price;
        basis[i] = b;
        sum += s[i];
      }
      var Knew = C0 + sum;
      T = (Knew - U0) / (1 - inv - t);
      D = t * T - U0;
      if (D < 0) { D = 0; T = Knew / (1 - inv); }
      S = Knew + D;
      var pNew = inp.pre / S;
      var dk = Math.abs(Knew - K) / Knew, dpr = Math.abs(pNew - p) / pNew;
      K = 0.5 * K + 0.5 * Knew;
      p = 0.5 * p + 0.5 * pNew;
      if (dk < 1e-13 && dpr < 1e-13) { K = Knew; p = pNew; break; }
    }
    var nShares = inp.newMoney / p;
    T = S + nShares;
    return {
      K: K, p: p, D: D, T: T, S: S, F: F, O: O, U0: U0, C0: C0,
      inv: inv, newShares: nShares, safeShares: s, basis: basis,
      safePrices: s.map(function (x, i) { return inp.safes[i].amount / x; }),
    };
  }

  function input(id, value, placeholder) {
    return el("input", {
      id: id, name: id, type: "text", inputmode: "decimal", autocomplete: "off",
      value: value, placeholder: placeholder,
    });
  }

  function field(id, label, inp, hint) {
    var kids = [el("label", { htmlFor: id }, [label]), inp];
    if (hint) kids.push(el("p", { className: "eq-hint" }, [hint]));
    return el("div", { className: "eq-field" }, kids);
  }

  function mount(root) {
    if (root.getAttribute("data-sdc-ready") === "true") return;
    root.setAttribute("data-sdc-ready", "true");

    var sharesIn = input("sdc-shares", DEFAULTS.shares, "e.g. 10000000");
    var foundersIn = input("sdc-founders", DEFAULTS.founders, "e.g. 92.5");
    var poolIn = input("sdc-pool", DEFAULTS.pool, "e.g. 1");
    var preIn = input("sdc-pre", DEFAULTS.pre, "e.g. 15000000");
    var newIn = input("sdc-new", DEFAULTS.newMoney, "e.g. 5000000");
    var targetIn = input("sdc-target", DEFAULTS.target, "e.g. 10");

    var safeList = el("div", { className: "sdc-safes" });
    var addBtn = el("button", { type: "button", className: "btn btn-secondary", id: "sdc-add" }, ["Add a SAFE"]);
    var errorEl = el("p", { className: "eq-error", hidden: true, role: "alert" });
    var outEl = el("div", { className: "eq-out", hidden: true, tabindex: "-1", id: "sdc-out" });

    function renumber() {
      var rows = safeList.querySelectorAll(".sdc-safe");
      for (var i = 0; i < rows.length; i++) {
        rows[i].querySelector(".sdc-safe-title").textContent = "SAFE " + (i + 1);
        rows[i].setAttribute("data-index", String(i + 1));
      }
      addBtn.hidden = rows.length >= MAX_SAFES;
    }

    var uid = 0;
    function addSafe(v) {
      v = v || { amount: "", cap: "", discount: "" };
      uid++;
      var a = input("sdc-amount-" + uid, v.amount, "e.g. 500000");
      var c = input("sdc-cap-" + uid, v.cap, "blank if none");
      var d = input("sdc-discount-" + uid, v.discount, "blank if none");
      a.className = "sdc-amount"; c.className = "sdc-cap"; d.className = "sdc-discount";
      var row = el("fieldset", { className: "sdc-safe" }, [
        el("legend", { className: "sdc-safe-title" }, ["SAFE"]),
        el("div", { className: "sdc-safe-grid" }, [
          field(a.id, "Amount ($)", a),
          field(c.id, "Post-money cap ($)", c),
          field(d.id, "Discount %", d),
        ]),
      ]);
      var rm = el("button", { type: "button", className: "sdc-remove", "aria-label": "Remove this SAFE" }, ["Remove"]);
      rm.addEventListener("click", function () {
        if (safeList.querySelectorAll(".sdc-safe").length <= 1) return;
        row.parentNode.removeChild(row);
        renumber();
      });
      row.appendChild(rm);
      safeList.appendChild(row);
      renumber();
    }

    addBtn.addEventListener("click", function () { addSafe(); });

    function setError(msg) {
      errorEl.hidden = !msg;
      errorEl.textContent = msg || "";
    }

    function row(cells, cls) {
      return el("tr", cls ? { className: cls } : null, cells.map(function (t, i) {
        return el(i === 0 ? "th" : "td", i === 0 ? { scope: "row" } : null, [String(t)]);
      }));
    }
    function table(head, rows) {
      return el("div", { className: "sdc-table" }, [el("table", null, [
        el("thead", null, [el("tr", null, head.map(function (h) { return el("th", { scope: "col" }, [h]); }))]),
        el("tbody", null, rows),
      ])]);
    }

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";

      var shares = parseNum(sharesIn.value);
      var founders = parseNum(foundersIn.value);
      var pool = parseNum(poolIn.value);
      var pre = parseNum(preIn.value);
      var newMoney = parseNum(newIn.value);
      var target = parseNum(targetIn.value);
      if ([shares, founders, pool, pre, newMoney, target].some(function (x) { return x == null || Number.isNaN(x); })) {
        return setError("Fill every round field with a number.");
      }
      if (shares <= 0) return setError("Fully diluted shares today must be greater than 0.");
      if (founders <= 0 || founders > 100) return setError("Founders % must be above 0 and at most 100.");
      if (pool < 0 || founders + pool > 100) return setError("Founders % plus unissued pool % cannot exceed 100.");
      if (pre <= 0 || newMoney <= 0) return setError("Pre-money and new money must both be greater than 0.");
      if (target < 0 || target >= 100) return setError("Target pool must be between 0 and 100.");
      var inv = newMoney / (pre + newMoney);
      if (inv + target / 100 >= 1) return setError("New investor % plus the target pool reaches 100%. Lower the target pool or the raise.");

      var safes = [];
      var rows = safeList.querySelectorAll(".sdc-safe");
      for (var i = 0; i < rows.length; i++) {
        var a = parseNum(rows[i].querySelector(".sdc-amount").value);
        var c = parseNum(rows[i].querySelector(".sdc-cap").value);
        var d = parseNum(rows[i].querySelector(".sdc-discount").value);
        var label = "SAFE " + (i + 1);
        if (a == null && c == null && d == null) continue;
        if (a == null || Number.isNaN(a) || a <= 0) return setError(label + ": enter an amount above 0.");
        if (Number.isNaN(c) || (c != null && c <= 0)) return setError(label + ": the cap must be a positive number or blank.");
        if (Number.isNaN(d) || (d != null && (d < 0 || d >= 100))) return setError(label + ": the discount must be between 0 and 99, or blank.");
        if (c == null && !d) return setError(label + ": give it a cap, a discount, or both. This tool does not model uncapped MFN SAFEs.");
        safes.push({ amount: a, cap: c || null, discount: d || 0, label: label });
      }
      var capShare = safes.reduce(function (acc, sf) { return acc + (sf.cap ? sf.amount / sf.cap : 0); }, 0);
      if (capShare >= 0.95) return setError("SAFE amounts divided by their caps add to 95% or more. Check the caps.");

      var r = compute({ shares: shares, founders: founders, pool: pool, pre: pre, newMoney: newMoney, target: target, safes: safes });
      if (![r.p, r.T, r.K].every(Number.isFinite) || r.p <= 0) return setError("These inputs do not converge. Check the caps and discounts.");

      var pct = function (x) { return (x / r.T) * 100; };
      var others = 100 - founders - pool;
      var safeSum = r.safeShares.reduce(function (acc, x) { return acc + x; }, 0);

      var ownRows = [
        row(["Founders", fmtPct(founders), fmtPct(pct(r.F))], "sdc-founders"),
      ];
      if (others > 1e-9) ownRows.push(row(["Other existing holders (issued options, other common)", fmtPct(others), fmtPct(pct(r.O))]));
      ownRows.push(row(["Unissued option pool", fmtPct(pool), fmtPct(pct(r.U0 + r.D))], "sdc-pool"));
      safes.forEach(function (sf, i) {
        ownRows.push(row([sf.label + " (" + fmtMoney(sf.amount) + ")", "0.00%", fmtPct(pct(r.safeShares[i]))], "sdc-safe-row"));
      });
      ownRows.push(row(["New investors (" + fmtMoney(newMoney) + ")", "0.00%", fmtPct(pct(r.newShares))], "sdc-new"));

      var convRows = safes.map(function (sf, i) {
        return row([sf.label, fmtPrice(r.safePrices[i]), r.basis[i], fmtShares(r.safeShares[i]), fmtPct((r.safeShares[i] / r.K) * 100)]);
      });

      var foundersAfter = pct(r.F);
      var summary = el("dl", { className: "eq-summary" }, [
        el("div", { className: "eq-summary-card eq-summary-card--good" }, [
          el("dt", null, ["Founders after the round"]),
          el("dd", { id: "sdc-founders-after" }, [fmtPct(foundersAfter) + " (from " + fmtPct(founders) + ")"]),
        ]),
        el("div", { className: "eq-summary-card" }, [
          el("dt", null, ["All SAFE holders after the round"]),
          el("dd", null, [fmtPct(pct(safeSum))]),
        ]),
        el("div", { className: "eq-summary-card" }, [
          el("dt", null, ["Round price per share"]),
          el("dd", null, [fmtPrice(r.p)]),
        ]),
        el("div", { className: "eq-summary-card" }, [
          el("dt", null, ["Pool increase in the pre-money"]),
          el("dd", null, [fmtShares(r.D) + " shares"]),
        ]),
      ]);

      var read =
        "Founders go from " + fmtPct(founders) + " today to " + fmtPct((r.F / r.K) * 100) +
        " once the SAFEs convert, then to " + fmtPct(foundersAfter) +
        " after the new money and the pool increase. New investors own " + fmtPct(pct(r.newShares)) +
        " of a " + fmtMoney(pre + newMoney) + " post-money. The pool increase and the SAFE shares sit in the pre-money, so the new investors do not pay for either.";
      if (r.D === 0) read += " Your unissued pool already meets the target, so there is no increase.";

      var formulas = el("div", { className: "eq-note sdc-formulas" }, [
        el("strong", null, ["How this is calculated. "]),
        document.createTextNode(
          "Company Capitalization (K) = today's fully diluted shares + all SAFE conversion shares. It leaves out the new money and the round's pool increase (YC post-money safe user guide). " +
          "Cap price = post-money cap ÷ K. Discount price = round price × (1 − discount). Each SAFE takes the lowest of cap price, discount price, and round price, which gives the most shares (YC; Carta). " +
          "Round price = pre-money ÷ (K + pool increase). Pool increase = target % × post-round shares − unissued pool today. New investor % = new money ÷ (pre-money + new money). " +
          "On your inputs: K = " + fmtShares(r.K) + ", post-round shares = " + fmtShares(r.T) + "."
        ),
      ]);

      outEl.appendChild(summary);
      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["Ownership, fully diluted"]));
      outEl.appendChild(table(["Holder", "Today", "After the round"], ownRows));
      outEl.appendChild(el("p", { className: "eq-note" }, [read]));
      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["How each SAFE converted"]));
      outEl.appendChild(table(["SAFE", "Price", "Term used", "Shares", "% of K"], convRows));
      outEl.appendChild(formulas);
      outEl.appendChild(el("p", { className: "eq-note" }, [
        "Assumptions: YC post-money SAFEs, one class of common, no promised options above the unissued pool, no notes, no pro rata side letters (any pro rata money is inside new money). Pre-money includes the SAFE shares and the pool increase, as in YC's worked examples. Your numbers stay in this browser tab. Not legal or tax advice.",
      ]));
      outEl.hidden = false;
      outEl.focus();
    }

    function loadDefaults() {
      sharesIn.value = DEFAULTS.shares;
      foundersIn.value = DEFAULTS.founders;
      poolIn.value = DEFAULTS.pool;
      preIn.value = DEFAULTS.pre;
      newIn.value = DEFAULTS.newMoney;
      targetIn.value = DEFAULTS.target;
      safeList.innerHTML = "";
      DEFAULTS.safes.forEach(addSafe);
    }

    var form = el("form", { id: "sdc-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults are YC's own worked example: two post-money SAFEs, then a $5M round at $15M pre with a 10% pool. Change them to your cap table.",
      ]),
      el("h3", { className: "eq-subhead" }, ["Your cap table today"]),
      el("div", { className: "eq-fields" }, [
        field("sdc-shares", "Fully diluted shares today", sharesIn, "Issued shares, options, and the unissued pool."),
        field("sdc-founders", "Founders % of fully diluted", foundersIn),
        field("sdc-pool", "Unissued option pool %", poolIn, "Granted options count as other holders."),
      ]),
      el("h3", { className: "eq-subhead" }, ["SAFEs outstanding"]),
      safeList,
      el("div", { className: "eq-actions", style: "margin:0 0 20px" }, [addBtn]),
      el("h3", { className: "eq-subhead" }, ["The priced round"]),
      el("div", { className: "eq-fields" }, [
        field("sdc-pre", "Pre-money valuation ($)", preIn),
        field("sdc-new", "New money ($)", newIn),
        field("sdc-target", "Target unissued pool % after the round", targetIn, "As a % of post-round fully diluted shares."),
      ]),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary", id: "sdc-calc" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Reset to YC example"]),
      ]),
    ]);
    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (e) {
      e.preventDefault();
      loadDefaults();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    loadDefaults();
    root.appendChild(form);
    root.appendChild(outEl);
    root.__sdcCompute = compute;
  }

  function boot() {
    var root = document.getElementById("safe-dilution-calculator");
    if (root) mount(root);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
