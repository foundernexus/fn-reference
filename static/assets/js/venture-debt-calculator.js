/* Venture debt cost and warrant calculator.
   Client-side only. No tracking, no network.
   Cash flows by month: day 0 = loan minus the upfront fee; months 1..IO = interest only;
   then amortization (equal monthly payments, or straight-line principal plus interest);
   last month adds the final payment (end-of-term fee, % of the loan).
   Cash cost = all payments + fees - loan. Effective annual cost = (1 + monthly IRR)^12 - 1.
   Warrant shares = coverage % x loan / strike (the formula in Codexis' 5 Nov 2026 8-K with Trinity).
   Warrant value = shares x (exit price - strike), floored at 0, charged in the exit month for the all-in rate.
   Equity option: new money / (pre-money + new money).
   Defaults are a labeled hypothetical. Not legal, tax, or investment advice.
*/
(function () {
  "use strict";

  var DEFAULTS = {
    loan: "5000000", rate: "12", io: "12", am: "24", style: "equal",
    fee: "1", finalFee: "5", cov: "5", strike: "2.00", fd: "25000000",
    pre: "50000000", exitPrice: "6.00", years: "5", burn: "1000000",
  };

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "className") node.className = attrs[k];
        else if (k === "htmlFor") node.htmlFor = attrs[k];
        else if (attrs[k] === true) node.setAttribute(k, k);
        else if (attrs[k] !== false && attrs[k] != null) node.setAttribute(k, String(attrs[k]));
      });
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      node.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return node;
  }

  // Accepts 5000000, 5,000,000, $5M, 450k, 12%.
  function parseNum(value) {
    if (value == null) return null;
    var s = String(value).trim().toLowerCase().replace(/[$,%\s]/g, "");
    if (s === "") return null;
    var mult = 1;
    var last = s.charAt(s.length - 1);
    if (last === "k") mult = 1e3;
    else if (last === "m") mult = 1e6;
    else if (last === "b") mult = 1e9;
    if (mult !== 1) s = s.slice(0, -1);
    if (!/^-?\d*\.?\d+$/.test(s)) return null;
    var n = Number(s) * mult;
    return Number.isFinite(n) ? n : null;
  }

  function fmtMoney(n) {
    if (!Number.isFinite(n)) return "n/a";
    var sign = n < 0 ? "-" : "";
    return sign + "$" + Math.round(Math.abs(n)).toLocaleString("en-US");
  }
  function fmtPct(n, d) {
    if (!Number.isFinite(n)) return "n/a";
    return n.toFixed(d == null ? 2 : d) + "%";
  }
  function fmtShares(n) {
    return Math.round(n).toLocaleString("en-US");
  }

  // Monthly payment list for the loan (index 0 = month 1).
  function schedule(L, rate, io, am, style) {
    var i = rate / 12;
    var pays = [];
    var m;
    for (m = 0; m < io; m++) pays.push(L * i);
    if (am > 0) {
      if (style === "straight") {
        var p = L / am;
        var bal = L;
        for (m = 0; m < am; m++) {
          pays.push(p + bal * i);
          bal -= p;
        }
      } else {
        var pmt = i === 0 ? L / am : (L * i) / (1 - Math.pow(1 + i, -am));
        for (m = 0; m < am; m++) pays.push(pmt);
      }
    }
    return pays;
  }

  function npv(r, flows) {
    var s = 0;
    for (var t = 0; t < flows.length; t++) s += flows[t] / Math.pow(1 + r, t);
    return s;
  }

  // Monthly IRR by bisection. Flows are one inflow then outflows, so the root is unique.
  function irr(flows) {
    var lo = -0.99, hi = 1;
    if (npv(hi, flows) < 0) return null;
    for (var k = 0; k < 300; k++) {
      var mid = (lo + hi) / 2;
      if (npv(mid, flows) > 0) hi = mid;
      else lo = mid;
    }
    return (lo + hi) / 2;
  }

  function compute(inp) {
    var L = inp.loan;
    var pays = schedule(L, inp.rate / 100, inp.io, inp.am, inp.style);
    var T = inp.io + inp.am;
    var feeAmt = (L * inp.fee) / 100;
    var finalAmt = (L * inp.finalFee) / 100;
    var flows = [L - feeAmt];
    pays.forEach(function (p) { flows.push(-p); });
    flows[T] -= finalAmt;
    var mCash = irr(flows);

    var totalPay = pays.reduce(function (a, b) { return a + b; }, 0);
    var interest = totalPay - L;
    var cashCost = interest + feeAmt + finalAmt;

    var wShares = inp.strike > 0 ? ((inp.cov / 100) * L) / inp.strike : 0;
    var wValue = wShares * Math.max(0, inp.exitPrice - inp.strike);
    var exitMonth = Math.max(0, Math.round(inp.years * 12));
    var flows2 = flows.slice();
    while (flows2.length <= exitMonth) flows2.push(0);
    flows2[exitMonth] -= wValue;
    var mAll = exitMonth === 0 && wValue > 0 ? null : irr(flows2);

    var wPct = (wShares / (inp.fd + wShares)) * 100;
    var eqPct = (L / (inp.pre + L)) * 100;
    var eqPrice = inp.pre / inp.fd;
    var eqShares = L / eqPrice;
    var eqValue = eqShares * inp.exitPrice;

    var peak = pays.length ? Math.max.apply(null, pays) : 0;
    return {
      ioPmt: inp.io > 0 ? pays[0] : null,
      amFirst: inp.am > 0 ? pays[inp.io] : null,
      amLast: inp.am > 0 ? pays[pays.length - 1] : null,
      term: T, interest: interest, feeAmt: feeAmt, finalAmt: finalAmt,
      totalPay: totalPay, cashCost: cashCost,
      cashApr: mCash == null ? null : (Math.pow(1 + mCash, 12) - 1) * 100,
      allApr: mAll == null ? null : (Math.pow(1 + mAll, 12) - 1) * 100,
      wShares: wShares, wValue: wValue, wPct: wPct, allInCost: cashCost + wValue,
      eqPct: eqPct, eqPrice: eqPrice, eqShares: eqShares, eqValue: eqValue,
      peak: peak, burnShare: inp.burn > 0 ? (peak / inp.burn) * 100 : null,
      ioBurnShare: inp.burn > 0 && inp.io > 0 ? (pays[0] / inp.burn) * 100 : null,
      exitMonth: exitMonth,
    };
  }

  function mount(root) {
    function textInput(id, value, placeholder) {
      return el("input", {
        type: "text", inputmode: "decimal", id: id, name: id, value: value,
        placeholder: placeholder || "", autocomplete: "off", spellcheck: "false",
      });
    }
    function field(id, label, input, hint) {
      var kids = [el("label", { htmlFor: id }, [label]), input];
      if (hint) kids.push(el("p", { className: "eq-hint" }, [hint]));
      return el("div", { className: "eq-field" }, kids);
    }

    var inputs = {
      loan: textInput("vd-loan", DEFAULTS.loan, "e.g. 5m"),
      rate: textInput("vd-rate", DEFAULTS.rate, "e.g. 12"),
      io: textInput("vd-io", DEFAULTS.io, "e.g. 12"),
      am: textInput("vd-am", DEFAULTS.am, "e.g. 24"),
      fee: textInput("vd-fee", DEFAULTS.fee, "e.g. 1"),
      finalFee: textInput("vd-final", DEFAULTS.finalFee, "e.g. 5"),
      cov: textInput("vd-cov", DEFAULTS.cov, "e.g. 5"),
      strike: textInput("vd-strike", DEFAULTS.strike, "e.g. 2.00"),
      fd: textInput("vd-fd", DEFAULTS.fd, "e.g. 25m"),
      pre: textInput("vd-pre", DEFAULTS.pre, "e.g. 50m"),
      exitPrice: textInput("vd-exit", DEFAULTS.exitPrice, "e.g. 6.00"),
      years: textInput("vd-years", DEFAULTS.years, "e.g. 5"),
      burn: textInput("vd-burn", DEFAULTS.burn, "optional"),
    };
    var styleIn = el("select", { id: "vd-style", name: "vd-style" }, [
      el("option", { value: "equal" }, ["Equal monthly payments"]),
      el("option", { value: "straight" }, ["Straight-line principal plus interest"]),
    ]);
    styleIn.value = DEFAULTS.style;

    var errorEl = el("p", { className: "eq-error", hidden: true, id: "vd-error" });
    var outEl = el("div", { className: "eq-out", hidden: true, tabindex: "-1", id: "vd-out" });

    function setError(msg) {
      errorEl.hidden = !msg;
      errorEl.textContent = msg || "";
    }
    function card(label, value, tone, id) {
      return el("div", { className: "eq-summary-card" + (tone ? " eq-summary-card--" + tone : "") }, [
        el("dt", null, [label]),
        el("dd", id ? { id: id } : null, [value]),
      ]);
    }
    function row(label, debt, equity, cls) {
      return el("tr", cls ? { className: cls } : null, [
        el("th", { scope: "row" }, [label]),
        el("td", null, [debt]),
        el("td", null, [equity]),
      ]);
    }

    function read() {
      var v = {};
      for (var k in inputs) v[k] = parseNum(inputs[k].value);
      v.style = styleIn.value;
      return v;
    }

    function calculate(e, quiet) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
      var v = read();
      var required = ["loan", "rate", "io", "am", "fee", "finalFee", "cov", "strike", "fd", "pre", "exitPrice", "years"];
      for (var j = 0; j < required.length; j++) {
        if (v[required[j]] == null) {
          setError("Fill every field with a number. You can type 5m, 450k, or 12%. Monthly burn is the only optional field.");
          return;
        }
      }
      if (v.loan <= 0 || v.fd <= 0 || v.pre <= 0 || v.strike <= 0) {
        setError("Loan, shares, pre-money valuation, and strike price must be above zero.");
        return;
      }
      if (v.rate < 0 || v.fee < 0 || v.finalFee < 0 || v.cov < 0 || v.exitPrice < 0 || v.years < 0) {
        setError("Rates, fees, coverage, exit price, and years cannot be negative.");
        return;
      }
      if (v.io < 0 || v.am < 0 || v.io % 1 || v.am % 1 || v.io + v.am < 1 || v.io + v.am > 120) {
        setError("Use whole months, with a total term from 1 to 120 months.");
        return;
      }
      if (v.rate > 60) {
        setError("Enter the annual interest rate as a percent, for example 12 for 12%.");
        return;
      }
      if (v.burn != null && v.burn < 0) v.burn = null;
      var r = compute(v);

      outEl.appendChild(el("p", { className: "eq-lede", style: "margin-top:0" }, [
        "A labeled hypothetical on the numbers you typed, not a lender quote. Not legal, tax, or investment advice.",
      ]));

      outEl.appendChild(el("h3", { className: "eq-subhead", style: "margin-top:0" }, ["Payments"]));
      var payCards = [];
      if (r.ioPmt != null) payCards.push(card("Monthly payment, interest-only (months 1 to " + v.io + ")", fmtMoney(r.ioPmt), null, "vd-io-pmt"));
      if (r.amFirst != null) {
        var amLabel = "Monthly payment, amortizing (months " + (v.io + 1) + " to " + r.term + ")";
        var amVal = v.style === "straight" && Math.abs(r.amFirst - r.amLast) > 0.5
          ? fmtMoney(r.amFirst) + " falling to " + fmtMoney(r.amLast)
          : fmtMoney(r.amFirst);
        payCards.push(card(amLabel, amVal, null, "vd-am-pmt"));
      }
      payCards.push(card("Final payment at month " + r.term, fmtMoney(r.finalAmt), null, "vd-final-amt"));
      payCards.push(card("Upfront fee, taken at funding", fmtMoney(r.feeAmt), null, "vd-fee-amt"));
      outEl.appendChild(el("dl", { className: "eq-summary" }, payCards));

      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["Cost"]));
      outEl.appendChild(el("dl", { className: "eq-summary" }, [
        card("Total cash cost (interest + fees + final payment)", fmtMoney(r.cashCost), null, "vd-cash-cost"),
        card("Effective annual cost, cash only", r.cashApr == null ? "n/a" : fmtPct(r.cashApr), "mid", "vd-cash-apr"),
        card("Warrant value at your exit price", fmtMoney(r.wValue), null, "vd-warrant-value"),
        card("All-in annual cost, with warrants", r.allApr == null ? "n/a" : fmtPct(r.allApr), "warn", "vd-allin-apr"),
      ]));

      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["Ownership: this loan or the same money as equity"]));
      outEl.appendChild(el("dl", { className: "eq-summary" }, [
        card("Ownership given up: warrants", fmtPct(r.wPct), "good", "vd-warrant-pct"),
        card("Ownership given up: " + fmtMoney(v.loan) + " as equity", fmtPct(r.eqPct), "warn", "vd-equity-pct"),
      ]));
      outEl.appendChild(el("div", { className: "sdc-table bm-table" }, [el("table", null, [
        el("thead", null, [el("tr", null, [
          el("th", { scope: "col" }, ["For " + fmtMoney(v.loan)]),
          el("th", { scope: "col" }, ["Venture debt"]),
          el("th", { scope: "col" }, ["Equity"]),
        ])]),
        el("tbody", null, [
          row("Cash in on day one", fmtMoney(v.loan - r.feeAmt), fmtMoney(v.loan)),
          row("Cash paid back", fmtMoney(r.totalPay + r.finalAmt), "$0"),
          row("New shares", fmtShares(r.wShares) + " (warrant)", fmtShares(r.eqShares)),
          row("Ownership given up", fmtPct(r.wPct), fmtPct(r.eqPct), "bm-current"),
          row("Their stake at " + "$" + v.exitPrice.toFixed(2) + " a share", fmtMoney(r.wValue), fmtMoney(r.eqValue)),
          row("Cost beyond the money you got", fmtMoney(r.allInCost), fmtMoney(r.eqValue - v.loan)),
        ]),
      ])]));

      var readParts = [
        el("strong", null, ["Read. "]),
        "The loan costs " + fmtMoney(r.cashCost) + " in cash over " + r.term + " months",
        r.cashApr == null ? ". " : ", an effective " + fmtPct(r.cashApr, 1) + " a year against a " + fmtPct(v.rate, 1) + " headline rate. ",
        "At " + "$" + v.exitPrice.toFixed(2) + " a share the warrant is worth " + fmtMoney(r.wValue),
        r.allApr == null ? ". " : ", which lifts the all-in cost to " + fmtPct(r.allApr, 1) + " a year. ",
        "The warrant takes " + fmtPct(r.wPct) + " of the company. The same money as equity at a " + fmtMoney(v.pre) + " pre-money takes " + fmtPct(r.eqPct) + ".",
      ];
      outEl.appendChild(el("p", { className: "eq-note", id: "vd-read" }, readParts));

      if (r.burnShare != null) {
        var over = r.burnShare >= 25;
        outEl.appendChild(el("p", { className: "eq-note", id: "vd-burn-read" }, [
          el("strong", null, ["Burn check. "]),
          "Peak debt service is " + fmtMoney(r.peak) + " a month, " + fmtPct(r.burnShare, 1) + " of a " + fmtMoney(v.burn) + " monthly net burn",
          r.ioBurnShare != null ? " (" + fmtPct(r.ioBurnShare, 1) + " during interest-only). " : ". ",
          over
            ? "SVB suggests keeping debt service under 25% of net burn. This is above it. A longer interest-only period or a smaller loan brings it down."
            : "SVB suggests keeping debt service under 25% of net burn. This is under it.",
        ]));
      }

      outEl.appendChild(el("p", { className: "eq-note sdc-formulas", id: "vd-formula" }, [
        el("strong", null, ["Formula. "]),
        "Interest-only payment = loan × rate ÷ 12. Equal amortizing payment = loan × i ÷ (1 − (1 + i)^−n), with i = rate ÷ 12 and n = amortization months. Straight-line pays loan ÷ n of principal plus interest on the balance. Cash flows: loan minus the upfront fee in month 0, each payment after that, and the final payment (% of the loan) in the last month. Effective annual cost = (1 + monthly IRR)^12 − 1. Warrant shares = coverage × loan ÷ strike, the formula in Codexis' November 2026 loan filing with Trinity Capital. Warrant value = shares × (exit price − strike), never below zero, charged in the exit month for the all-in rate. Ownership = warrant shares ÷ (shares now + warrant shares). Equity = new money ÷ (pre-money + new money).",
      ]));
      outEl.appendChild(el("p", { className: "eq-note", id: "vd-assumptions" }, [
        el("strong", null, ["Assumptions. "]),
        "Fixed rate, drawn in full on day one, held to maturity, no prepayment fee, no covenant default. Floating loans tied to prime move with it. The tool treats the warrant as vested at funding and exercised in the exit month you set. Your exit price is a guess, not a forecast. Typical terms, each with its source, are in the tables below.",
      ]));

      outEl.hidden = false;
      if (!quiet) outEl.focus();
    }

    var form = el("form", { id: "vd-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults: a $5M loan at 12% with 12 months interest-only and 24 months of amortization, a 1% upfront fee, a 5% final payment, and 5% warrant coverage at $2.00 a share. The fees match two Trinity Capital loans in SEC filings. The rest is a labeled hypothetical.",
      ]),
      el("h3", { className: "eq-subhead" }, ["The loan"]),
      el("div", { className: "eq-fields" }, [
        field("vd-loan", "Loan amount ($)", inputs.loan),
        field("vd-rate", "Annual interest rate (%)", inputs.rate, "Kruze: often 8% to 12%. Hercules: about 7% to 14%."),
        field("vd-io", "Interest-only months", inputs.io, "Mercury: often 12 to 18."),
        field("vd-am", "Amortization months after that", inputs.am, "Term = interest-only + amortization."),
        field("vd-style", "Amortization style", styleIn),
        field("vd-burn", "Monthly net burn ($, optional)", inputs.burn, "For SVB's under-25% debt service check."),
      ]),
      el("h3", { className: "eq-subhead" }, ["Fees"]),
      el("div", { className: "eq-fields" }, [
        field("vd-fee", "Upfront fee (% of loan)", inputs.fee, "Origination or commitment fee."),
        field("vd-final", "Final payment (% of loan)", inputs.finalFee, "End-of-term fee due at maturity."),
      ]),
      el("h3", { className: "eq-subhead" }, ["Warrants and the equity option"]),
      el("div", { className: "eq-fields" }, [
        field("vd-cov", "Warrant coverage (% of loan)", inputs.cov, "Kruze: 2% to 10%. Hercules: 3% to 20%."),
        field("vd-strike", "Warrant strike price ($ a share)", inputs.strike, "Often your last round price (Hercules)."),
        field("vd-fd", "Fully diluted shares now", inputs.fd),
        field("vd-pre", "Pre-money valuation if you raised it as equity ($)", inputs.pre),
        field("vd-exit", "Share price at exit ($)", inputs.exitPrice, "Your guess. Prices the warrant and the equity stake."),
        field("vd-years", "Years until exit", inputs.years, "When the lender exercises. Warrants often run 10 to 12 years (Mercury)."),
      ]),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary", id: "vd-calc" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Reset to example"]),
      ]),
    ]);
    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (ev) {
      ev.preventDefault();
      inputs.loan.value = DEFAULTS.loan; inputs.rate.value = DEFAULTS.rate; inputs.io.value = DEFAULTS.io;
      inputs.am.value = DEFAULTS.am; inputs.fee.value = DEFAULTS.fee; inputs.finalFee.value = DEFAULTS.finalFee;
      inputs.cov.value = DEFAULTS.cov; inputs.strike.value = DEFAULTS.strike; inputs.fd.value = DEFAULTS.fd;
      inputs.pre.value = DEFAULTS.pre; inputs.exitPrice.value = DEFAULTS.exitPrice; inputs.years.value = DEFAULTS.years;
      inputs.burn.value = DEFAULTS.burn; styleIn.value = DEFAULTS.style;
      calculate(null, true);
    });

    root.appendChild(form);
    root.appendChild(outEl);
    root.__vdCompute = compute;
    calculate(null, true);
  }

  function boot() {
    var root = document.getElementById("venture-debt-calculator");
    if (root) mount(root);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
