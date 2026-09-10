/* Runway calculator with hiring plan.
   Client-side only. No tracking, no network.
   Snapshot runway follows Kruze (cash ÷ monthly net burn).
   Trajectory + default alive/dead follows Paul Graham's framing with explicit hiring.
   Worked numbers are a labeled hypothetical. Not legal, tax, or investment advice.
*/
(function () {
  "use strict";

  var DEFAULTS = {
    cash: "4200000",
    revenue: "80000",
    growth: "8",
    expenses: "430000",
    hires: "3",
    hireCost: "18000",
    firstStart: "2",
    spacing: "1",
    horizon: "18",
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
    var opts =
      abs >= 1e6
        ? { maximumFractionDigits: 2 }
        : { maximumFractionDigits: 0 };
    return sign + "$" + Math.round(abs).toLocaleString("en-US", opts);
  }

  function fmtMonths(n) {
    if (!Number.isFinite(n)) return "—";
    if (n === Infinity) return "∞ (profitable at current run-rate)";
    return n.toFixed(1) + " mo";
  }

  function field(id, label, input, hint) {
    var kids = [el("label", { htmlFor: id }, [label]), input];
    if (hint) kids.push(el("p", { className: "eq-hint" }, [hint]));
    return el("div", { className: "eq-field" }, kids);
  }

  function hireStarts(count, firstStart, spacing) {
    var starts = [];
    var i;
    for (i = 0; i < count; i++) {
      starts.push(firstStart + i * spacing);
    }
    return starts;
  }

  function hireCostInMonth(t, starts, costPer) {
    var n = 0;
    var i;
    for (i = 0; i < starts.length; i++) {
      if (starts[i] <= t) n += 1;
    }
    return n * costPer;
  }

  function project(inputs) {
    var cash0 = inputs.cash;
    var r = inputs.revenue;
    var g = inputs.growth / 100;
    var e0 = inputs.expenses;
    var starts = hireStarts(inputs.hires, inputs.firstStart, inputs.spacing);
    var costPer = inputs.hireCost;
    var N = inputs.horizon;
    var eps = 1e-9;

    var snapBurn = e0 - inputs.revenue;
    var snapshotRunway =
      snapBurn <= eps ? Infinity : cash0 / Math.max(snapBurn, eps);

    var rows = [];
    var cash = cash0;
    var revenue = inputs.revenue;
    var cashOutMonth = null;
    var crossoverMonth = null;
    var defaultAlive = false;
    var t;

    for (t = 1; t <= N; t++) {
      revenue = revenue * (1 + g);
      var hireCost = hireCostInMonth(t, starts, costPer);
      var expenses = e0 + hireCost;
      var netBurn = expenses - revenue;
      var cashPrev = cash;
      cash = cashPrev - netBurn;

      var hitZero = false;
      if (cashOutMonth == null && cash <= eps) {
        cashOutMonth = t;
        hitZero = true;
      }

      if (crossoverMonth == null && revenue + eps >= expenses) {
        crossoverMonth = t;
        if (cashOutMonth == null || crossoverMonth < cashOutMonth) {
          defaultAlive = true;
        }
      }

      rows.push({
        month: t,
        revenue: revenue,
        expenses: expenses,
        hireCost: hireCost,
        netBurn: netBurn,
        endingCash: cash,
        cashPrev: cashPrev,
        hitZero: hitZero,
      });

      if (cash <= eps && t < N) {
        // Continue filling table for transparency, cash can go more negative.
      }
    }

    // PG-style: default alive if crossover exists before (or without) cash-out.
    if (crossoverMonth != null && (cashOutMonth == null || crossoverMonth < cashOutMonth)) {
      defaultAlive = true;
    } else if (crossoverMonth == null || (cashOutMonth != null && crossoverMonth >= cashOutMonth)) {
      defaultAlive = false;
    }

    // If already revenue >= expenses at month 1 start after growth? handled in loop.
    // Also: if starting net burn already negative and stays so — alive from month 1.
    if (inputs.revenue >= e0 && cash0 > 0) {
      // Before any hire; may still die after hires. Loop handles crossover.
    }

    var runwayWithPlan = cashOutMonth == null ? null : cashOutMonth;
    if (cashOutMonth == null && rows.length && rows[rows.length - 1].endingCash > eps) {
      runwayWithPlan = null; // survived horizon
    }

    return {
      snapshotRunway: snapshotRunway,
      snapBurn: snapBurn,
      rows: rows,
      cashOutMonth: cashOutMonth,
      crossoverMonth: crossoverMonth,
      defaultAlive: defaultAlive,
      runwayWithPlan: runwayWithPlan,
      survivedHorizon: cashOutMonth == null,
      horizon: N,
      starts: starts,
    };
  }

  function mount(root) {
    if (root.getAttribute("data-rw-ready") === "true") return;
    root.setAttribute("data-rw-ready", "true");

    function moneyInput(id, value, placeholder) {
      return el("input", {
        id: id,
        name: id,
        type: "text",
        inputmode: "decimal",
        autocomplete: "off",
        required: true,
        value: value,
        placeholder: placeholder,
      });
    }

    var cashInput = moneyInput("rw-cash", DEFAULTS.cash, "e.g. 4200000");
    var revInput = moneyInput("rw-revenue", DEFAULTS.revenue, "e.g. 80000");
    var growthInput = moneyInput("rw-growth", DEFAULTS.growth, "e.g. 8");
    var expInput = moneyInput("rw-expenses", DEFAULTS.expenses, "e.g. 430000");
    var hiresInput = moneyInput("rw-hires", DEFAULTS.hires, "e.g. 3");
    var hireCostInput = moneyInput("rw-hire-cost", DEFAULTS.hireCost, "e.g. 18000");
    var firstStartInput = moneyInput("rw-first-start", DEFAULTS.firstStart, "e.g. 2");
    var spacingInput = moneyInput("rw-spacing", DEFAULTS.spacing, "e.g. 1");
    var horizonInput = el("select", { id: "rw-horizon", name: "rw-horizon" }, [
      el("option", { value: "12" }, ["12"]),
      el("option", { value: "18", selected: true }, ["18"]),
      el("option", { value: "24" }, ["24"]),
    ]);

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

    function dataRow(cells, opts) {
      opts = opts || {};
      return el(
        "tr",
        opts.className ? { className: opts.className } : null,
        cells.map(function (t, i) {
          return el(i === 0 ? "th" : "td", i === 0 ? { scope: "row" } : null, [
            String(t),
          ]);
        })
      );
    }

    function summaryCard(label, value) {
      return el("div", { className: "eq-summary-card" }, [
        el("dt", null, [label]),
        el("dd", null, [value]),
      ]);
    }

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";

      var cash = parseNum(cashInput.value);
      var revenue = parseNum(revInput.value);
      var growth = parseNum(growthInput.value);
      var expenses = parseNum(expInput.value);
      var hires = parseNum(hiresInput.value);
      var hireCost = parseNum(hireCostInput.value);
      var firstStart = parseNum(firstStartInput.value);
      var spacing = parseNum(spacingInput.value);
      var horizon = parseNum(horizonInput.value);

      if (
        cash == null ||
        revenue == null ||
        growth == null ||
        expenses == null ||
        hires == null ||
        hireCost == null ||
        firstStart == null ||
        spacing == null ||
        horizon == null
      ) {
        setError("Enter every field as a number.");
        return;
      }
      if (cash < 0) {
        setError("Cash on hand cannot be negative.");
        return;
      }
      if (revenue < 0) {
        setError("Monthly revenue cannot be negative.");
        return;
      }
      if (growth < 0 || growth > 100) {
        setError("Monthly revenue growth % should be between 0 and 100.");
        return;
      }
      if (expenses < 0) {
        setError("Monthly expenses cannot be negative.");
        return;
      }
      if (hires < 0 || hires !== Math.floor(hires) || hires > 50) {
        setError("Planned new hires must be a whole number from 0 to 50.");
        return;
      }
      if (hireCost < 0) {
        setError("Fully loaded monthly cost per hire cannot be negative.");
        return;
      }
      if (firstStart < 1 || firstStart > horizon || firstStart !== Math.floor(firstStart)) {
        setError("First hire start month must be a whole number from 1 to the projection horizon.");
        return;
      }
      if (spacing < 0 || spacing !== Math.floor(spacing) || spacing > 24) {
        setError("Hire spacing must be a whole number of months from 0 to 24.");
        return;
      }
      if ([12, 18, 24].indexOf(horizon) === -1) {
        setError("Projection horizon must be 12, 18, or 24 months.");
        return;
      }

      var r = project({
        cash: cash,
        revenue: revenue,
        growth: growth,
        expenses: expenses,
        hires: hires,
        hireCost: hireCost,
        firstStart: firstStart,
        spacing: spacing,
        horizon: horizon,
      });

      var snapLabel =
        r.snapshotRunway === Infinity
          ? "Profitable at current run-rate"
          : fmtMonths(r.snapshotRunway);

      var planLabel;
      if (r.survivedHorizon) {
        planLabel = ">" + r.horizon + " mo (cash still positive at horizon)";
      } else {
        planLabel = r.cashOutMonth + " mo (cash ≤ 0 in month " + r.cashOutMonth + ")";
      }

      var aliveLabel = r.defaultAlive ? "Default alive" : "Default dead";
      var crossLabel =
        r.crossoverMonth == null
          ? "None in horizon"
          : "Month " + r.crossoverMonth;
      var outLabel =
        r.cashOutMonth == null ? "None in horizon" : "Month " + r.cashOutMonth;

      var gapNote = "";
      if (r.crossoverMonth != null && r.cashOutMonth != null) {
        var gap = r.cashOutMonth - r.crossoverMonth;
        if (gap > 0) {
          gapNote =
            " Crossover is " +
            gap +
            " month(s) before cash-out on this model.";
        } else if (gap <= 0) {
          gapNote =
            " Cash hits ≤ 0 in month " +
            r.cashOutMonth +
            " at or before crossover. That is the fatal pinch PG describes.";
        }
      } else if (r.crossoverMonth != null && r.cashOutMonth == null) {
        gapNote = " Revenue covers expenses before cash runs out inside the horizon.";
      } else if (r.crossoverMonth == null && r.cashOutMonth != null) {
        gapNote = " No crossover before cash-out inside the horizon.";
      }

      var summary = el("dl", { className: "eq-summary" }, [
        summaryCard("Snapshot runway (ignore hiring & growth)", snapLabel),
        summaryCard("Runway with hiring plan", planLabel),
        summaryCard("PG-style on this model", aliveLabel),
        summaryCard("Crossover month (rev ≥ exp)", crossLabel),
        summaryCard("Cash-out month", outLabel),
      ]);

      var tbody = r.rows.map(function (row) {
        return dataRow(
          [
            String(row.month),
            fmtMoney(row.revenue),
            fmtMoney(row.expenses),
            fmtMoney(row.netBurn),
            fmtMoney(row.endingCash),
          ],
          { className: row.hitZero ? "eq-row-warn" : null }
        );
      });

      var table = el("div", { className: "table-wrap eq-month-table" }, [
        el("table", null, [
          el("thead", null, [
            header(["Month", "Revenue", "Expenses", "Net burn", "Ending cash"]),
          ]),
          el("tbody", null, tbody),
        ]),
      ]);

      var startsText =
        r.starts.length === 0
          ? "no planned hires"
          : "hire starts in month(s) " + r.starts.join(", ");

      var read =
        "Snapshot net burn (expenses − revenue, no hires, no growth) is " +
        fmtMoney(r.snapBurn) +
        ". With the plan (" +
        startsText +
        "), this model is " +
        aliveLabel.toLowerCase() +
        "." +
        gapNote +
        " Ending cash can go negative in the table so you can see how far short the path is; treat cash-out as the first month ending cash ≤ 0.";

      var formulas = el("div", { className: "eq-note" }, [
        el("strong", null, ["Formulas. "]),
        document.createTextNode(
          "Snapshot runway = cash ÷ max(E0 − R0, ε); if E0 − R0 ≤ 0, show profitable at current run-rate. Each month t=1…N: Rt = R(t−1)×(1+g); hire cost = (hires with start ≤ t) × fully loaded monthly cost; Expenses_t = E0 + hire cost; Net burn_t = Expenses_t − Rt; Cash_t = Cash(t−1) − (Expenses_t − Rt). Default alive if some month has revenue ≥ expenses before cash ≤ 0. Base expenses held constant except the planned hire ladder. Matches PG’s “expenses remain constant” plus an explicit hiring trajectory (Kruze: headcount is most of burn)."
        ),
      ]);

      outEl.appendChild(
        el("p", { className: "eq-lede", style: "margin-top:0" }, [
          "Labeled hypothetical on the numbers you typed. Not a company. Not legal, tax, or investment advice.",
        ])
      );
      outEl.appendChild(summary);
      outEl.appendChild(el("p", { className: "eq-note" }, [read]));
      outEl.appendChild(
        el("h3", { className: "eq-subhead" }, ["Month-by-month (" + horizon + " mo)"])
      );
      outEl.appendChild(table);
      outEl.appendChild(formulas);
      outEl.hidden = false;
      outEl.focus();
    }

    var form = el("form", { id: "rw-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults match a labeled hypothetical at Kruze’s example scale: $4.2M cash, ~$350k starting net burn ($430k expenses − $80k revenue), 8% monthly revenue growth, three hires. Change every field. Projection defaults to 18 months (Kruze rolling forecast).",
      ]),
      el("div", { className: "eq-fields" }, [
        field("rw-cash", "Cash on hand ($)", cashInput),
        field("rw-revenue", "Current monthly revenue ($)", revInput),
        field(
          "rw-growth",
          "Monthly revenue growth %",
          growthInput,
          "Compounded each month."
        ),
        field(
          "rw-expenses",
          "Current monthly expenses before planned hires ($)",
          expInput
        ),
        field("rw-hires", "Planned new hires (count)", hiresInput),
        field(
          "rw-hire-cost",
          "Fully loaded monthly cost per hire ($)",
          hireCostInput,
          "Kruze cites SBA: often ~1.25–1.4× base salary as a rule of thumb."
        ),
        field(
          "rw-first-start",
          "First hire starts in month (1–horizon)",
          firstStartInput,
          "Kruze: assume starts slip a month or two later than hoped."
        ),
        field("rw-spacing", "Hire spacing (months between starts)", spacingInput),
        field("rw-horizon", "Projection horizon (months)", horizonInput),
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
      cashInput.value = DEFAULTS.cash;
      revInput.value = DEFAULTS.revenue;
      growthInput.value = DEFAULTS.growth;
      expInput.value = DEFAULTS.expenses;
      hiresInput.value = DEFAULTS.hires;
      hireCostInput.value = DEFAULTS.hireCost;
      firstStartInput.value = DEFAULTS.firstStart;
      spacingInput.value = DEFAULTS.spacing;
      horizonInput.value = DEFAULTS.horizon;
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    root.appendChild(form);
    root.appendChild(outEl);
  }

  function boot() {
    var root = document.getElementById("runway-calculator");
    if (root) mount(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
