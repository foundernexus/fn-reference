/* Cap table waterfall calculator.
   Client-side only. No tracking, no network.
   Who gets what when the company sells. Preferred series take their liquidation preference
   (multiple x amount invested) first, either stacked (newest series paid first) or pari passu
   (all series share pro rata to their preference). What is left goes to common, options, and any
   participating preferred on an as-converted basis, up to each capped series' cap.
   Non-participating preferred takes the greater of its preference or its as-converted share
   (Feld, NVCA model charter). Capped participating preferred can also convert when common is
   worth more than the cap. Conversion choices interact, so the tool lets each series pick its
   better option given the others' choices and repeats until no series wants to switch.
   Assumptions: 1:1 conversion, no declared dividends, options treated as common with exercise
   prices ignored, exit value is net proceeds to stockholders. Not legal or tax advice.
*/
(function () {
  "use strict";

  var MAX_SERIES = 6;
  var DEFAULTS = {
    exit: "25000000",
    founders: "6000000",
    other: "",
    options: "1000000",
    seniority: "pari",
    series: [
      { name: "Seed", shares: "2000000", invested: "2000000", mult: "1", part: "none", cap: "" },
      { name: "Series A", shares: "3000000", invested: "9000000", mult: "1", part: "none", cap: "" },
    ],
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

  // Accepts 25000000, 25,000,000, $25M, 450k, 1x.
  function parseNum(value) {
    if (value == null) return null;
    var s = String(value).trim().toLowerCase().replace(/[$,\s×]/g, "");
    if (s === "") return null;
    if (s.charAt(s.length - 1) === "x") s = s.slice(0, -1);
    var mult = 1;
    var last = s.charAt(s.length - 1);
    if (last === "k") mult = 1e3;
    else if (last === "m") mult = 1e6;
    else if (last === "b") mult = 1e9;
    if (mult !== 1) s = s.slice(0, -1);
    if (!/^-?\d*\.?\d+$/.test(s)) return NaN;
    var n = Number(s) * mult;
    return Number.isFinite(n) ? n : NaN;
  }

  function fmtMoney(n) {
    if (!Number.isFinite(n)) return "n/a";
    return "$" + Math.round(n).toLocaleString("en-US");
  }
  function fmtPrice(n) {
    return Number.isFinite(n) ? "$" + n.toFixed(2) : "n/a";
  }
  function fmtPct(n) {
    return Number.isFinite(n) ? n.toFixed(2) + "%" : "n/a";
  }
  function fmtShares(n) {
    return Number.isFinite(n) ? Math.round(n).toLocaleString("en-US") : "n/a";
  }
  function fmtX(n) {
    return (Math.round(n * 100) / 100).toString() + "x";
  }

  /* One pass of the waterfall for a fixed set of conversion choices.
     inp: {exit, common, series:[{shares, invested, mult, part:'none'|'full'|'capped', cap}], seniority}
     conv: array of booleans (true = series converts to common). */
  function waterfall(inp, conv) {
    var n = inp.series.length;
    var pref = new Array(n), part = new Array(n), remaining = inp.exit;
    for (var i = 0; i < n; i++) { pref[i] = 0; part[i] = 0; }

    // Preference tiers, most senior first.
    var tiers = [];
    if (inp.seniority === "stacked") {
      for (var t = n - 1; t >= 0; t--) tiers.push([t]);
    } else {
      var all = [];
      for (var a = 0; a < n; a++) all.push(a);
      tiers.push(all);
    }
    tiers.forEach(function (tier) {
      var members = tier.filter(function (k) { return !conv[k]; });
      var demand = members.reduce(function (acc, k) { return acc + inp.series[k].mult * inp.series[k].invested; }, 0);
      if (demand <= 0) return;
      if (remaining >= demand) {
        members.forEach(function (k) { pref[k] = inp.series[k].mult * inp.series[k].invested; });
        remaining -= demand;
      } else {
        members.forEach(function (k) { pref[k] = remaining * (inp.series[k].mult * inp.series[k].invested) / demand; });
        remaining = 0;
      }
    });

    // Residual: common + converted series + participating series, capped ones up to their cap.
    var totalShares = inp.common;
    var capped = [];
    for (var j = 0; j < n; j++) {
      var s = inp.series[j];
      if (conv[j] || s.part === "full") totalShares += s.shares;
      else if (s.part === "capped") {
        var head = Math.max(0, s.cap * s.invested - pref[j]);
        totalShares += s.shares;
        capped.push({ k: j, t: head / s.shares });
      }
    }
    capped.sort(function (x, y) { return x.t - y.t; });
    var perShare = 0, R = remaining, filled = {};
    for (var c = 0; c < capped.length; c++) {
      var need = (capped[c].t - perShare) * totalShares;
      if (R >= need) {
        R -= need;
        perShare = capped[c].t;
        filled[capped[c].k] = true;
        totalShares -= inp.series[capped[c].k].shares;
      } else break;
    }
    if (totalShares > 0) perShare += R / totalShares;
    for (var q = 0; q < n; q++) {
      var sq = inp.series[q];
      if (conv[q] || sq.part === "full") part[q] = sq.shares * perShare;
      else if (sq.part === "capped") {
        part[q] = filled[q] ? Math.max(0, sq.cap * sq.invested - pref[q]) : sq.shares * perShare;
      }
    }
    var pay = pref.map(function (p, k) { return p + part[k]; });
    return { pref: pref, part: part, pay: pay, perShare: perShare, commonPay: inp.common * perShare };
  }

  /* Each convertible series (non-participating or capped participating) picks the better of
     converting or not, given the others' current choices. Repeat until stable. */
  function compute(inp) {
    var n = inp.series.length;
    var conv = inp.series.map(function () { return false; });
    var order = inp.series.map(function (s, i) { return i; }).sort(function (a, b) {
      var pa = inp.series[a].mult * inp.series[a].invested / inp.series[a].shares;
      var pb = inp.series[b].mult * inp.series[b].invested / inp.series[b].shares;
      return pa - pb;
    });
    var stable = false, rounds = 0;
    for (; rounds < 100 && !stable; rounds++) {
      stable = true;
      order.forEach(function (i) {
        if (inp.series[i].part === "full") return;
        var off = conv.slice(); off[i] = false;
        var on = conv.slice(); on[i] = true;
        var want = waterfall(inp, on).pay[i] > waterfall(inp, off).pay[i] + 1e-6;
        if (want !== conv[i]) { conv[i] = want; stable = false; }
      });
    }
    if (!stable && n <= 10) {
      // Fallback: first choice set where no series gains by switching alone.
      for (var m = 0; m < (1 << n); m++) {
        var tryC = inp.series.map(function (s, i) { return s.part !== "full" && !!(m & (1 << i)); });
        var ok = tryC.every(function (ci, i) {
          if (inp.series[i].part === "full") return true;
          var flip = tryC.slice(); flip[i] = !ci;
          return waterfall(inp, flip).pay[i] <= waterfall(inp, tryC).pay[i] + 1e-6;
        });
        if (ok) { conv = tryC; stable = true; break; }
      }
    }
    var r = waterfall(inp, conv);
    r.conv = conv;
    r.stable = stable;
    r.rounds = rounds;
    return r;
  }

  function mount(root) {
    if (root.getAttribute("data-ctw-ready") === "true") return;
    root.setAttribute("data-ctw-ready", "true");

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

    var exitIn = textInput("ctw-exit", DEFAULTS.exit, "e.g. 25000000");
    var foundersIn = textInput("ctw-founders", DEFAULTS.founders, "e.g. 6000000");
    var otherIn = textInput("ctw-other", DEFAULTS.other, "blank if none");
    var optionsIn = textInput("ctw-options", DEFAULTS.options, "e.g. 1000000");
    var seniorityIn = el("select", { id: "ctw-seniority", name: "ctw-seniority" }, [
      el("option", { value: "pari" }, ["Pari passu: all series share pro rata"]),
      el("option", { value: "stacked" }, ["Stacked: newest series paid first"]),
    ]);

    var seriesList = el("div", { className: "sdc-safes ctw-series-list" });
    var addBtn = el("button", { type: "button", className: "btn btn-secondary", id: "ctw-add" }, ["Add a series"]);
    var errorEl = el("p", { className: "eq-error", hidden: true, role: "alert", id: "ctw-error" });
    var outEl = el("div", { className: "eq-out", hidden: true, tabindex: "-1", id: "ctw-out" });

    function renumber() {
      var rows = seriesList.querySelectorAll(".ctw-series");
      for (var i = 0; i < rows.length; i++) {
        rows[i].querySelector(".sdc-safe-title").textContent = "Preferred series " + (i + 1) + (i === rows.length - 1 && rows.length > 1 ? " (newest)" : i === 0 && rows.length > 1 ? " (oldest)" : "");
        rows[i].setAttribute("data-index", String(i + 1));
      }
      addBtn.hidden = rows.length >= MAX_SERIES;
    }

    var uid = 0;
    function addSeries(v) {
      v = v || { name: "", shares: "", invested: "", mult: "1", part: "none", cap: "" };
      uid++;
      var nm = el("input", { type: "text", id: "ctw-name-" + uid, name: "ctw-name-" + uid, value: v.name, placeholder: "e.g. Series B", autocomplete: "off" });
      var sh = textInput("ctw-shares-" + uid, v.shares, "e.g. 2000000");
      var iv = textInput("ctw-invested-" + uid, v.invested, "e.g. 10000000");
      var mu = textInput("ctw-mult-" + uid, v.mult, "1");
      var pa = el("select", { id: "ctw-part-" + uid, name: "ctw-part-" + uid }, [
        el("option", { value: "none" }, ["Non-participating"]),
        el("option", { value: "full" }, ["Participating, no cap"]),
        el("option", { value: "capped" }, ["Participating, capped"]),
      ]);
      pa.value = v.part;
      var cp = textInput("ctw-cap-" + uid, v.cap, "e.g. 3");
      nm.className = "ctw-name"; sh.className = "ctw-shares"; iv.className = "ctw-invested";
      mu.className = "ctw-mult"; pa.className = "ctw-part"; cp.className = "ctw-cap";
      var capField = field(cp.id, "Cap (x invested, total)", cp);
      function syncCap() { capField.hidden = pa.value !== "capped"; }
      pa.addEventListener("change", syncCap);
      syncCap();
      var row = el("fieldset", { className: "sdc-safe ctw-series" }, [
        el("legend", { className: "sdc-safe-title" }, ["Preferred series"]),
        el("div", { className: "sdc-safe-grid ctw-grid" }, [
          field(nm.id, "Name", nm),
          field(sh.id, "Shares", sh),
          field(iv.id, "Amount invested ($)", iv),
          field(mu.id, "Preference multiple", mu),
          field(pa.id, "Participation", pa),
          capField,
        ]),
      ]);
      var rm = el("button", { type: "button", className: "sdc-remove", "aria-label": "Remove this series" }, ["Remove"]);
      rm.addEventListener("click", function () {
        if (seriesList.querySelectorAll(".ctw-series").length <= 1) return;
        row.parentNode.removeChild(row);
        renumber();
      });
      row.appendChild(rm);
      seriesList.appendChild(row);
      renumber();
    }
    addBtn.addEventListener("click", function () { addSeries(); });

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
    function trow(cells, cls) {
      return el("tr", cls ? { className: cls } : null, cells.map(function (t, i) {
        return el(i === 0 ? "th" : "td", i === 0 ? { scope: "row" } : null, [String(t)]);
      }));
    }
    function table(head, rows, extra) {
      return el("div", { className: "sdc-table" + (extra ? " " + extra : "") }, [el("table", null, [
        el("thead", null, [el("tr", null, head.map(function (h) { return el("th", { scope: "col" }, [h]); }))]),
        el("tbody", null, rows),
      ])]);
    }

    function readInputs() {
      var exit = parseNum(exitIn.value);
      var founders = parseNum(foundersIn.value);
      var other = parseNum(otherIn.value);
      var options = parseNum(optionsIn.value);
      if (exit == null || Number.isNaN(exit) || exit < 0) return { err: "Enter the exit value as a number, 0 or more. You can type 25m or 800k." };
      if (founders == null || Number.isNaN(founders) || founders <= 0) return { err: "Founder shares must be a number above 0." };
      if (Number.isNaN(other) || (other != null && other < 0)) return { err: "Other common shares must be a number or blank." };
      if (Number.isNaN(options) || (options != null && options < 0)) return { err: "Option shares must be a number or blank." };
      other = other || 0; options = options || 0;
      var series = [];
      var rows = seriesList.querySelectorAll(".ctw-series");
      for (var i = 0; i < rows.length; i++) {
        var name = rows[i].querySelector(".ctw-name").value.trim() || "Series " + (i + 1);
        var sh = parseNum(rows[i].querySelector(".ctw-shares").value);
        var iv = parseNum(rows[i].querySelector(".ctw-invested").value);
        var mu = parseNum(rows[i].querySelector(".ctw-mult").value);
        var pa = rows[i].querySelector(".ctw-part").value;
        var cp = parseNum(rows[i].querySelector(".ctw-cap").value);
        if (sh == null && iv == null) continue;
        if (sh == null || Number.isNaN(sh) || sh <= 0) return { err: name + ": enter its shares, above 0." };
        if (iv == null || Number.isNaN(iv) || iv <= 0) return { err: name + ": enter the amount invested, above 0." };
        if (mu == null) mu = 1;
        if (Number.isNaN(mu) || mu < 0 || mu > 10) return { err: name + ": the preference multiple must be between 0 and 10." };
        if (pa === "capped") {
          if (cp == null || Number.isNaN(cp) || cp <= 0) return { err: name + ": enter the participation cap as a multiple of the amount invested, for example 3." };
          if (cp < mu) return { err: name + ": the cap counts the preference, so it must be at least the preference multiple." };
        }
        series.push({ name: name, shares: sh, invested: iv, mult: mu, part: pa, cap: pa === "capped" ? cp : null });
      }
      if (!series.length) return { err: "Add at least one preferred series with shares and an amount invested." };
      return {
        inp: { exit: exit, common: founders + other + options, series: series, seniority: seniorityIn.value },
        founders: founders, other: other, options: options,
      };
    }

    function termLabel(s, r, i) {
      if (r.conv[i]) return "Converts to common";
      if (s.part === "none") return "Takes " + fmtX(s.mult) + " preference";
      if (s.part === "full") return "Preference + participation";
      var capAmt = s.cap * s.invested;
      if (r.pay[i] >= capAmt - 0.5) return "Hits " + fmtX(s.cap) + " cap";
      return "Preference + participation (under cap)";
    }

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
      var got = readInputs();
      if (got.err) return setError(got.err);
      var inp = got.inp;
      var r = compute(inp);
      if (!r.stable) return setError("These terms have no stable conversion choice. Check the multiples and caps.");

      var totalShares = inp.common + inp.series.reduce(function (a, s) { return a + s.shares; }, 0);
      var exit = inp.exit;
      var pctOf = function (x) { return exit > 0 ? (x / exit) * 100 : 0; };
      var fd = function (sh) { return (sh / totalShares) * 100; };
      var ps = r.perShare;
      var founderPay = got.founders * ps;
      var prefTotal = r.pref.reduce(function (a, b) { return a + b; }, 0);
      var stackTotal = inp.series.reduce(function (a, s) { return a + s.mult * s.invested; }, 0);

      var rows = [
        trow(["Founders", fmtMoney(founderPay), fmtPrice(ps), fmtPct(pctOf(founderPay)), fmtPct(fd(got.founders)), "Common"], "sdc-founders ctw-founders"),
      ];
      if (got.other > 0) rows.push(trow(["Other common", fmtMoney(got.other * ps), fmtPrice(ps), fmtPct(pctOf(got.other * ps)), fmtPct(fd(got.other)), "Common"]));
      if (got.options > 0) rows.push(trow(["Options", fmtMoney(got.options * ps), fmtPrice(ps), fmtPct(pctOf(got.options * ps)), fmtPct(fd(got.options)), "Common, strike ignored"]));
      inp.series.forEach(function (s, i) {
        rows.push(trow([s.name, fmtMoney(r.pay[i]), fmtPrice(r.pay[i] / s.shares), fmtPct(pctOf(r.pay[i])), fmtPct(fd(s.shares)), termLabel(s, r, i)], "ctw-series-row"));
      });

      outEl.appendChild(el("dl", { className: "eq-summary" }, [
        card("Founders take", fmtMoney(founderPay) + " (" + fmtPct(pctOf(founderPay)) + " of proceeds)", "good", "ctw-founders-out"),
        card("Common per share", fmtPrice(ps), null, "ctw-pps"),
        card("Paid as preference", fmtMoney(prefTotal) + " of a " + fmtMoney(stackTotal) + " stack", null, "ctw-pref"),
        card("Founders own, fully diluted", fmtPct(fd(got.founders)), null, "ctw-fd"),
      ]));
      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["Who gets what at " + fmtMoney(exit)]));
      outEl.appendChild(table(["Holder", "Payout", "$ per share", "% of proceeds", "% owned", "Term used"], rows, "ctw-table"));

      var converted = inp.series.filter(function (s, i) { return r.conv[i]; }).map(function (s) { return s.name; });
      var kept = inp.series.filter(function (s, i) { return !r.conv[i]; }).map(function (s) { return s.name; });
      var read = "Founders own " + fmtPct(fd(got.founders)) + " and take " + fmtPct(pctOf(founderPay)) + " of the proceeds. ";
      if (kept.length) read += kept.join(", ") + (kept.length > 1 ? " take" : " takes") + " the preference" + (converted.length ? ". " : ", because it is worth more than converting. ");
      if (converted.length) read += converted.join(", ") + (converted.length > 1 ? " convert" : " converts") + " to common, because converting pays more than the preference. ";
      if (exit < stackTotal) read += "The exit is below the " + fmtMoney(stackTotal) + " preference stack, so common gets only what is left after preferences" + (ps === 0 ? ", which is nothing." : ".");
      outEl.appendChild(el("p", { className: "eq-note", id: "ctw-read" }, [el("strong", null, ["Read. "]), read]));

      // Same terms at other exit values.
      var mults = [0.25, 0.5, 1, 2, 4];
      var sRows = mults.map(function (m) {
        var alt = compute({ exit: exit * m, common: inp.common, series: inp.series, seniority: inp.seniority });
        var fp = got.founders * alt.perShare;
        return trow([fmtMoney(exit * m), fmtMoney(fp), fmtPct(exit * m > 0 ? (fp / (exit * m)) * 100 : 0), fmtPrice(alt.perShare)], m === 1 ? "bm-current" : null);
      });
      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["Same terms at other exit values"]));
      outEl.appendChild(table(["Exit value", "Founders take", "% of proceeds", "Common per share"], sRows, "bm-table"));

      outEl.appendChild(el("div", { className: "eq-note sdc-formulas" }, [
        el("strong", null, ["How this is calculated. "]),
        document.createTextNode(
          "1. Preferences. Each series that does not convert is owed its multiple × amount invested (Feld). Stacked: the newest series is paid in full first, then the next newest. Pari passu: all series share pro rata to what each is owed. If the exit runs out inside a tier, that tier splits what is left pro rata. " +
          "2. What is left goes to common, options, converted series, and participating series, per share on an as-converted basis. A capped series stops when its preference plus participation reaches its cap × amount invested. The cap counts the preference (Feld), and the excess goes to everyone else. " +
          "3. Conversion. A non-participating series takes the greater of its preference or what it would get as common, not both (Feld; NVCA model charter). A capped series can also convert when common pays more than its cap. One series converting changes what common is worth for the others, so the tool lets each series pick its better option given the others' picks and repeats until none wants to switch. " +
          "On your inputs: " + fmtShares(totalShares) + " fully diluted shares, " + (converted.length ? converted.join(", ") + " converted." : "no series converted.")
        ),
      ]));
      outEl.appendChild(el("p", { className: "eq-note" }, [
        "Assumptions: every preferred share converts 1:1, no declared or accrued dividends, no debt, fees, escrow, earnout, or management carve-out (enter the exit value after those come out), options counted as common with exercise prices ignored, unissued pool left out. Cooley counted a 1x preference in 95.8% and nonparticipating preferred in 96.4% of its Q2 2026 deals. Your numbers stay in this browser tab. Not legal or tax advice.",
      ]));
      outEl.hidden = false;
      outEl.focus();
    }

    function loadDefaults() {
      exitIn.value = DEFAULTS.exit;
      foundersIn.value = DEFAULTS.founders;
      otherIn.value = DEFAULTS.other;
      optionsIn.value = DEFAULTS.options;
      seniorityIn.value = DEFAULTS.seniority;
      seriesList.innerHTML = "";
      DEFAULTS.series.forEach(addSeries);
    }

    var form = el("form", { id: "ctw-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults: a $25M sale, founders with 6M shares, 1M in options, a $2M Seed and a $9M Series A, both 1x non-participating. List series oldest first.",
      ]),
      el("h3", { className: "eq-subhead" }, ["The exit"]),
      el("div", { className: "eq-fields" }, [
        field("ctw-exit", "Exit value to stockholders ($)", exitIn, "Net proceeds after debt, fees, and any carve-out."),
        field("ctw-seniority", "Preference seniority", seniorityIn),
      ]),
      el("h3", { className: "eq-subhead" }, ["Common and options"]),
      el("div", { className: "eq-fields" }, [
        field("ctw-founders", "Founder shares", foundersIn),
        field("ctw-other", "Other common shares", otherIn, "Early employees, advisors. Blank if none."),
        field("ctw-options", "Options that share in the exit", optionsIn, "Granted options. Leave the unissued pool out."),
      ]),
      el("h3", { className: "eq-subhead" }, ["Preferred series, oldest first"]),
      seriesList,
      el("div", { className: "eq-actions", style: "margin:0 0 20px" }, [addBtn]),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary", id: "ctw-calc" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Reset to example"]),
      ]),
    ]);
    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (ev) {
      ev.preventDefault();
      loadDefaults();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    loadDefaults();
    root.appendChild(form);
    root.appendChild(outEl);
    root.__ctwCompute = compute;
  }

  function boot() {
    var root = document.getElementById("cap-table-waterfall");
    if (root) mount(root);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
