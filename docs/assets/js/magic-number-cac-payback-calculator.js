/* Magic number & CAC payback calculator.
   Client-side only. No tracking, no network.
   Classic magic number follows Scale VP framing ((CQ−PQ)×4)/PQ S&M.
   Optional GM-adjusted variant is labeled separately (not Scale's classic).
   CAC payback follows ChartMogul: CAC ÷ (ARPA × gross margin %).
   Defaults are a labeled hypothetical. Not legal, tax, or investment advice.
*/
(function () {
  "use strict";

  var DEFAULTS = {
    priorArr: "2000000",
    currentArr: "2400000",
    priorSm: "2000000",
    gmPct: "75",
    cac: "12000",
    arpa: "1000",
  };

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

  function parseNum(value) {
    if (value == null) return null;
    var s = String(value).trim().replace(/[$,%\s]/g, "");
    if (s === "") return null;
    var n = Number(s);
    if (!Number.isFinite(n)) return null;
    return n;
  }

  function fmtMoney(n) {
    if (!Number.isFinite(n)) return "—";
    var sign = n < 0 ? "-" : "";
    var abs = Math.abs(n);
    return sign + "$" + Math.round(abs).toLocaleString("en-US");
  }

  function fmtRatio(n) {
    if (!Number.isFinite(n)) return "—";
    return n.toFixed(2);
  }

  function fmtMonths(n) {
    if (!Number.isFinite(n)) return "—";
    if (n === Infinity) return "∞ (no gross-margin contribution)";
    return n.toFixed(1) + " mo";
  }

  function moneyInput(id, value, placeholder) {
    return el("input", {
      type: "text",
      inputmode: "decimal",
      id: id,
      name: id,
      value: value,
      placeholder: placeholder || "",
      autocomplete: "off",
      spellcheck: "false",
    });
  }

  function field(id, label, input, hint) {
    var kids = [el("label", { htmlFor: id }, [label]), input];
    if (hint) kids.push(el("p", { className: "eq-hint" }, [hint]));
    return el("div", { className: "eq-field" }, kids);
  }

  function summaryCard(label, value, tone) {
    var cls = "eq-summary-card" + (tone ? " eq-summary-card--" + tone : "");
    return el("div", { className: cls }, [
      el("dt", null, [label]),
      el("dd", null, [value]),
    ]);
  }

  function magicRead(classic) {
    if (!Number.isFinite(classic)) return { tone: null, text: "" };
    if (classic >= 0.75) {
      return {
        tone: "good",
        text:
          "Classic magic number is at or above ChartMogul’s ~0.75 “invest more” line. Scale’s long-term median is 0.7 — a separate publisher baseline.",
      };
    }
    if (classic >= 0.5) {
      return {
        tone: "mid",
        text:
          "Classic magic number sits between ChartMogul’s ~0.5 pull-back line and ~0.75 invest line. Scale’s long-term median is 0.7.",
      };
    }
    return {
      tone: "warn",
      text:
        "Classic magic number is below ChartMogul’s ~0.5 pull-back line. Compare next to Scale’s 0.7 median only as a separate baseline.",
    };
  }

  function paybackRead(months) {
    if (!Number.isFinite(months) || months === Infinity) {
      return {
        tone: "warn",
        text: "No payback on these inputs (gross-margin contribution is zero or negative).",
      };
    }
    if (months < 12) {
      return {
        tone: "good",
        text:
          "Under 12 months clears Bessemer’s SMB target and sits inside their State of the Cloud 2023 “better” (6–12) or “best” (0–6) ladders depending on the exact number.",
      };
    }
    if (months < 18) {
      return {
        tone: "mid",
        text:
          "Between 12 and 18 months: outside Bessemer’s SMB <12 target, inside mid-market <18. Their $1–10M ARR portfolio average was about 15 months.",
      };
    }
    if (months < 24) {
      return {
        tone: "mid",
        text:
          "Between 18 and 24 months: outside mid-market <18, inside enterprise <24 (Bessemer Scaling to $100 Million).",
      };
    }
    return {
      tone: "warn",
      text:
        "At or above 24 months: outside Bessemer’s enterprise <24 target on this labeled read.",
    };
  }

  function compute(inputs) {
    var delta = inputs.currentArr - inputs.priorArr;
    var classic =
      inputs.priorSm === 0 ? null : (delta * 4) / inputs.priorSm;
    var gm = inputs.gmPct / 100;
    var gmAdj =
      inputs.priorSm === 0 ? null : (delta * gm * 4) / inputs.priorSm;
    var monthlyGp = inputs.arpa * gm;
    var payback =
      monthlyGp <= 0 ? Infinity : inputs.cac / monthlyGp;
    return {
      delta: delta,
      classic: classic,
      gmAdj: gmAdj,
      monthlyGp: monthlyGp,
      payback: payback,
      annualizedNew: delta * 4,
    };
  }

  function mount(root) {
    var priorArrInput = moneyInput("mn-prior-arr", DEFAULTS.priorArr, "e.g. 2000000");
    var currentArrInput = moneyInput(
      "mn-current-arr",
      DEFAULTS.currentArr,
      "e.g. 2400000"
    );
    var priorSmInput = moneyInput("mn-prior-sm", DEFAULTS.priorSm, "e.g. 2000000");
    var gmInput = moneyInput("mn-gm", DEFAULTS.gmPct, "e.g. 75");
    var cacInput = moneyInput("mn-cac", DEFAULTS.cac, "e.g. 12000");
    var arpaInput = moneyInput("mn-arpa", DEFAULTS.arpa, "e.g. 1000");

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

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";

      var priorArr = parseNum(priorArrInput.value);
      var currentArr = parseNum(currentArrInput.value);
      var priorSm = parseNum(priorSmInput.value);
      var gmPct = parseNum(gmInput.value);
      var cac = parseNum(cacInput.value);
      var arpa = parseNum(arpaInput.value);

      if (
        priorArr == null ||
        currentArr == null ||
        priorSm == null ||
        gmPct == null ||
        cac == null ||
        arpa == null
      ) {
        setError("Enter every field as a number.");
        return;
      }
      if (priorArr < 0 || currentArr < 0) {
        setError("Quarterly recurring revenue cannot be negative.");
        return;
      }
      if (priorSm < 0) {
        setError("Prior-quarter S&M cannot be negative.");
        return;
      }
      if (priorSm === 0) {
        setError("Prior-quarter S&M must be greater than zero to compute a magic number.");
        return;
      }
      if (gmPct < 0 || gmPct > 100) {
        setError("Gross margin % should be between 0 and 100.");
        return;
      }
      if (cac < 0) {
        setError("CAC cannot be negative.");
        return;
      }
      if (arpa < 0) {
        setError("Monthly ARPA cannot be negative.");
        return;
      }

      var r = compute({
        priorArr: priorArr,
        currentArr: currentArr,
        priorSm: priorSm,
        gmPct: gmPct,
        cac: cac,
        arpa: arpa,
      });

      var mRead = magicRead(r.classic);
      var pRead = paybackRead(r.payback);

      var summary = el("dl", { className: "eq-summary" }, [
        summaryCard("Classic magic number (Scale-style)", fmtRatio(r.classic), mRead.tone),
        summaryCard(
          "GM-adjusted magic number (optional)",
          fmtRatio(r.gmAdj),
          null
        ),
        summaryCard("CAC payback", fmtMonths(r.payback), pRead.tone),
        summaryCard("Quarterly ARR change", fmtMoney(r.delta), null),
        summaryCard("Annualized net new (×4)", fmtMoney(r.annualizedNew), null),
        summaryCard("Monthly gross profit / account", fmtMoney(r.monthlyGp), null),
      ]);

      var magicNote = el("div", { className: "eq-note" }, [
        el("strong", null, ["Magic number read. "]),
        document.createTextNode(mRead.text),
      ]);
      var payNote = el("div", { className: "eq-note" }, [
        el("strong", null, ["Payback read. "]),
        document.createTextNode(pRead.text),
      ]);

      var formulas = el("div", { className: "eq-note" }, [
        el("strong", null, ["Formulas. "]),
        document.createTextNode(
          "Classic magic number = ((current-quarter ARR − prior-quarter ARR) × 4) ÷ prior-quarter S&M (Scale framing). GM-adjusted variant = ((current − prior) × gross margin × 4) ÷ prior S&M — labeled separately; not Scale’s classic. CAC payback (months) = CAC ÷ (monthly ARPA × gross margin %) (ChartMogul). Bessemer segment targets and Scale’s 0.7 median are cited on the page, not averaged into one threshold."
        ),
      ]);

      outEl.appendChild(
        el("p", { className: "eq-lede", style: "margin-top:0" }, [
          "Labeled hypothetical on the numbers you typed. Not a company. Not legal, tax, or investment advice.",
        ])
      );
      outEl.appendChild(summary);
      outEl.appendChild(magicNote);
      outEl.appendChild(payNote);
      outEl.appendChild(formulas);
      outEl.hidden = false;
      outEl.focus();
    }

    var form = el("form", { id: "mn-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults: prior ARR $2.0M → current $2.4M, prior S&M $2.0M (classic magic number 0.80), CAC $12k, ARPA $1k/mo, gross margin 75% (16.0 mo payback). Change every field.",
      ]),
      el("h3", { className: "eq-subhead" }, ["Magic number inputs"]),
      el("div", { className: "eq-fields" }, [
        field(
          "mn-prior-arr",
          "Prior-quarter recurring revenue / ARR ($)",
          priorArrInput
        ),
        field(
          "mn-current-arr",
          "Current-quarter recurring revenue / ARR ($)",
          currentArrInput
        ),
        field(
          "mn-prior-sm",
          "Prior-quarter sales & marketing spend ($)",
          priorSmInput,
          "Denominator is prior quarter, not current."
        ),
        field(
          "mn-gm",
          "Gross margin %",
          gmInput,
          "Used for GM-adjusted magic number and for CAC payback."
        ),
      ]),
      el("h3", { className: "eq-subhead" }, ["CAC payback inputs"]),
      el("div", { className: "eq-fields" }, [
        field(
          "mn-cac",
          "CAC per new customer ($)",
          cacInput,
          "Period S&M (acquisition) ÷ new customers in that period."
        ),
        field(
          "mn-arpa",
          "Monthly ARPA ($)",
          arpaInput,
          "Average monthly recurring revenue per account."
        ),
      ]),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, [
          "Reset to hypothetical",
        ]),
      ]),
    ]);

    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (ev) {
      ev.preventDefault();
      priorArrInput.value = DEFAULTS.priorArr;
      currentArrInput.value = DEFAULTS.currentArr;
      priorSmInput.value = DEFAULTS.priorSm;
      gmInput.value = DEFAULTS.gmPct;
      cacInput.value = DEFAULTS.cac;
      arpaInput.value = DEFAULTS.arpa;
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    root.appendChild(form);
    root.appendChild(outEl);
  }

  function boot() {
    var root = document.getElementById("magic-number-cac-payback-calculator");
    if (root) mount(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
