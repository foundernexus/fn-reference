/* Burn multiple calculator.
   Client-side only. No tracking, no network.
   Burn multiple = net burn / net new ARR (David Sacks, Craft Ventures, 23 April 2020).
   Net new ARR = ending ARR - beginning ARR for the same period (new + expansion - contraction - churn).
   Bands are Sacks' published rules of thumb: under 1 amazing, 1 to 1.5 great, 1.5 to 2 good,
   2 to 3 suspect, over 3 bad. Each band includes its upper edge; "amazing" stops under 1.
   Defaults are a labeled hypothetical. Not legal, tax, or investment advice.
*/
(function () {
  "use strict";

  var DEFAULTS = { burn: "1800000", start: "3000000", end: "4000000", stage: "a" };

  // upper = highest multiple that still sits in the band (null = no upper edge).
  var BANDS = [
    { id: "amazing", label: "Amazing", range: "Under 1×", upper: 1, strict: true, tone: "good" },
    { id: "great", label: "Great", range: "1× to 1.5×", upper: 1.5, tone: "good" },
    { id: "good", label: "Good", range: "1.5× to 2×", upper: 2, tone: "mid" },
    { id: "suspect", label: "Suspect", range: "2× to 3×", upper: 3, tone: "mid" },
    { id: "bad", label: "Bad", range: "Over 3×", upper: null, tone: "warn" },
  ];

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

  // Accepts 1800000, 1,800,000, $1.8M, 450k.
  function parseNum(value) {
    if (value == null) return null;
    var s = String(value).trim().toLowerCase().replace(/[$,\s]/g, "");
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

  function fmtX(n) {
    return n.toFixed(2) + "×";
  }

  function bandFor(x) {
    var r = Math.round(x * 100) / 100;
    for (var i = 0; i < BANDS.length; i++) {
      var b = BANDS[i];
      if (b.upper == null) return b;
      if (b.strict ? r < b.upper : r <= b.upper) return b;
    }
    return BANDS[BANDS.length - 1];
  }

  function compute(inp) {
    var nn = inp.end - inp.start;
    var out = { netNew: nn, burn: inp.burn, multiple: null, band: null, state: "ok" };
    if (nn <= 0) {
      out.state = "no-growth";
      return out;
    }
    if (inp.burn <= 0) {
      out.state = "no-burn";
      return out;
    }
    out.multiple = inp.burn / nn;
    out.band = bandFor(out.multiple);
    return out;
  }

  function stageRead(stage, x) {
    var rel = function (ref) {
      var r = Math.round(x * 100) / 100;
      if (r <= ref) return "You are at or under that.";
      return "You are above that by " + (r - ref).toFixed(2) + "×.";
    };
    if (stage === "seed")
      return "Sacks: a seed company might run a burn multiple of about 3 because sales are only starting. " + rel(3);
    if (stage === "a")
      return "Sacks: after a Series A the multiple might drop to about 2. " + rel(2);
    if (stage === "b")
      return "Sacks: after a Series B the sales team should be operating at scale, so he expects efficiency to improve even more. He gives no number. There is no reliable public benchmark yet for a median burn multiple by stage.";
    return "Sacks: the multiple should improve as the company matures and approach 0 as it nears profitability. There is no reliable public benchmark yet for a median burn multiple by stage.";
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

    var burnIn = textInput("bm-burn", DEFAULTS.burn, "e.g. 1800000");
    var startIn = textInput("bm-start", DEFAULTS.start, "e.g. 3000000");
    var endIn = textInput("bm-end", DEFAULTS.end, "e.g. 4000000");
    var stageIn = el("select", { id: "bm-stage", name: "bm-stage" }, [
      el("option", { value: "seed" }, ["Seed"]),
      el("option", { value: "a" }, ["Series A"]),
      el("option", { value: "b" }, ["Series B or later"]),
      el("option", { value: "na" }, ["Not sure"]),
    ]);
    stageIn.value = DEFAULTS.stage;

    var errorEl = el("p", { className: "eq-error", hidden: true, id: "bm-error" });
    var outEl = el("div", { className: "eq-out", hidden: true, tabindex: "-1", id: "bm-out" });

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

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";

      var burn = parseNum(burnIn.value);
      var start = parseNum(startIn.value);
      var end = parseNum(endIn.value);
      if (burn == null || start == null || end == null) {
        setError("Enter net burn and both ARR figures as numbers. You can type 1.8m or 450k.");
        return;
      }
      if (start < 0 || end < 0) {
        setError("ARR cannot be negative.");
        return;
      }
      var r = compute({ burn: burn, start: start, end: end });

      outEl.appendChild(el("p", { className: "eq-lede", style: "margin-top:0" }, [
        "Labeled hypothetical on the numbers you typed. Not a company. Not legal, tax, or investment advice.",
      ]));

      if (r.state === "no-growth") {
        outEl.appendChild(el("dl", { className: "eq-summary" }, [
          card("Burn multiple", "Does not compute", "warn", "bm-multiple"),
          card("Net new ARR", fmtMoney(r.netNew), "warn", "bm-netnew"),
        ]));
        outEl.appendChild(el("p", { className: "eq-note", id: "bm-read" }, [
          el("strong", null, ["Read. "]),
          "Net new ARR is zero or negative, so the ratio has nothing to divide by. Sacks: for a pre-revenue company the ratio does not compute, and the focus is keeping burn low and getting to first revenue. If you had ARR and it fell, churn and contraction beat new sales. Fix that before you quote any multiple.",
        ]));
      } else if (r.state === "no-burn") {
        outEl.appendChild(el("dl", { className: "eq-summary" }, [
          card("Burn multiple", "No burn to multiply", "good", "bm-multiple"),
          card("Net new ARR", fmtMoney(r.netNew), null, "bm-netnew"),
        ]));
        outEl.appendChild(el("p", { className: "eq-note", id: "bm-read" }, [
          el("strong", null, ["Read. "]),
          "Net burn is zero or negative. You added ARR without losing cash in this period, so Sacks' bands do not apply. Report net burn and net new ARR as two lines.",
        ]));
      } else {
        var b = r.band;
        outEl.appendChild(el("dl", { className: "eq-summary" }, [
          card("Burn multiple", fmtX(r.multiple), b.tone, "bm-multiple"),
          card("Sacks read", b.label, b.tone, "bm-band"),
          card("Net burn", fmtMoney(burn), null, "bm-burn-out"),
          card("Net new ARR", fmtMoney(r.netNew), null, "bm-netnew"),
        ]));
        outEl.appendChild(el("p", { className: "eq-note", id: "bm-read" }, [
          el("strong", null, ["Read. "]),
          "You burned " + fmtMoney(burn) + " to add " + fmtMoney(r.netNew) + " of net new ARR, which is " + fmtX(r.multiple) + ". Sacks' band: " + b.label.toLowerCase() + " (" + b.range + "). ",
          stageRead(stageIn.value, r.multiple),
        ]));

        var rows = BANDS.slice(0, 4).map(function (band) {
          var cur = band.id === b.id;
          var lessThan = band.strict ? "More than " : "At least ";
          var most = band.strict ? "Less than " : "At most ";
          return el("tr", cur ? { className: "bm-current" } : null, [
            el("th", { scope: "row" }, [band.label + (cur ? " (you)" : ""), el("span", { className: "bm-range" }, [band.range])]),
            el("td", null, [lessThan + fmtMoney(burn / band.upper)]),
            el("td", null, [most + fmtMoney(band.upper * r.netNew)]),
          ]);
        });
        outEl.appendChild(el("h3", { className: "eq-subhead" }, ["What it takes to reach each band"]));
        outEl.appendChild(el("div", { className: "sdc-table bm-table" }, [el("table", null, [
          el("thead", null, [el("tr", null, [
            el("th", { scope: "col" }, ["Band"]),
            el("th", { scope: "col" }, ["Net new ARR needed"]),
            el("th", { scope: "col" }, ["Net burn allowed"]),
          ])]),
          el("tbody", null, rows),
        ])]));
      }

      outEl.appendChild(el("p", { className: "eq-note sdc-formulas" }, [
        el("strong", null, ["Formula. "]),
        "Burn multiple = net burn ÷ net new ARR (Sacks, Craft Ventures, 23 April 2020). Net new ARR = ending ARR − beginning ARR for the same period, so new and expansion ARR count and churn and contraction come out. Net burn is cash out minus cash in for that period (Kruze). Bands are Sacks' rules of thumb. Each band includes its upper edge, and amazing stops under 1. The table shows the net new ARR you need at your net burn, and the net burn you can carry at your net new ARR, to sit at the top edge of each band.",
      ]));
      outEl.hidden = false;
      outEl.focus();
    }

    var form = el("form", { id: "bm-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults: $1.8M of net burn in a quarter, ARR from $3.0M to $4.0M. That is 1.80×. Use one period for all three numbers: a month, a quarter, or a year.",
      ]),
      el("div", { className: "eq-fields" }, [
        field("bm-burn", "Net burn in the period ($)", burnIn, "Cash out minus cash in. Do not net a funding round against it."),
        field("bm-start", "ARR at the start of the period ($)", startIn),
        field("bm-end", "ARR at the end of the period ($)", endIn, "Net new ARR is this minus the start figure."),
        field("bm-stage", "Stage", stageIn, "Changes the Sacks stage note only."),
      ]),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary", id: "bm-calc" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Reset to example"]),
      ]),
    ]);
    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (ev) {
      ev.preventDefault();
      burnIn.value = DEFAULTS.burn;
      startIn.value = DEFAULTS.start;
      endIn.value = DEFAULTS.end;
      stageIn.value = DEFAULTS.stage;
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    root.appendChild(form);
    root.appendChild(outEl);
    root.__bmCompute = compute;
  }

  function boot() {
    var root = document.getElementById("burn-multiple-calculator");
    if (root) mount(root);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
