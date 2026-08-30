/* Executive equity calculator.
   Client-side only. No tracking, no network, no "Join now".
   Bands are cited public figures; this file does not invent ranges.
*/
(function () {
  "use strict";

  var BANDS = {
    Seed: {
      "VP Sales": {
        equity:
          "0.5%–2.0% FD. UltraTalent (July 2026) “first sales hire,” Pre-Seed/Seed. The CRO Report Seed band: 0.5%–2.0%.",
        cash: "UltraTalent: $140k base, $180k median OTE (first sales hire). Index warns this is often not a true VP.",
        vest: "4 years, 1-year cliff (UltraTalent; Index; The CRO Report; Kruze).",
      },
      "VP Eng": {
        equity:
          "Index / Advanced HR VCECS Seed Data (2018): senior engineering 1.00% FD at US seed. Special cases 2%–3% (solo founder skill gap; deep-tech). No seed “VP Eng” band published.",
        cash: "No VP Eng cash band in the fetched sources. Index 2018 US seed senior engineering cash is $120k (IC, not VP) — not used as a VP figure.",
        vest: "4 years, 1-year cliff (Index; Kruze).",
      },
      "CFO / VP Finance": {
        equity:
          "No seed CFO or VP Finance percentage in the fetched sources. Index places first true execs at Series A and finance as a Series B central team. C-level 0.8%–1.5% FDE is a Series A/B figure — not applied here.",
        cash: "No cited cash band.",
        vest: "4 years, 1-year cliff when you do grant (Index; Kruze).",
      },
      "VP Product": {
        equity:
          "Index / Advanced HR VCECS Seed Data (2018): senior product & design 1.00% FD at US seed. Special cases 2%–3%. No seed “VP Product” band published.",
        cash: "No VP Product cash band in the fetched sources. Index 2018 US seed senior product cash is $100k (not VP).",
        vest: "4 years, 1-year cliff (Index; Kruze).",
      },
      "Head of People": {
        equity:
          "No seed Head of People percentage in the fetched sources. Index lists HR with finance and ops as Series B central-team hires.",
        cash: "No cited cash band.",
        vest: "4 years, 1-year cliff when you do grant (Index; Kruze).",
      },
    },
    "Series A": {
      "VP Sales": {
        equity:
          "Index VP rule of thumb: 0.3%–0.8% FDE, sales at the lower end. UltraTalent Head of Sales/Director: 0.30%–0.75%. UltraTalent first VP (Series A to B): 0.60%–1.00%. The CRO Report Series A: 0.25%–1.0%. Not averaged.",
        cash:
          "UltraTalent Head of Sales: $160k base / $260k median OTE. First VP: $200k / $325k. The CRO Report Seed/Series A average base range (57 roles): $188,085–$250,458. Series A/B (154 roles): $147,024–$183,750.",
        vest: "4 years, 1-year cliff.",
      },
      "VP Eng": {
        equity:
          "High end of Index VP 0.3%–0.8% FDE. True non-founding CTO (C-level): Index typical 1% US at Series A or B; C-level range 0.8%–1.5% FDE.",
        cash: "No VP Eng cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
      "CFO / VP Finance": {
        equity:
          "True CFO (C-level): Index 0.8%–1.5% FDE, typical 1%. VP Finance: smaller end of Index VP 0.3%–0.8% FDE. Index: at most three true non-founding C-levels at Series A/B.",
        cash: "No CFO / VP Finance cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
      "VP Product": {
        equity: "High end of Index VP 0.3%–0.8% FDE.",
        cash: "No VP Product cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
      "Head of People": {
        equity: "Smaller end of Index VP 0.3%–0.8% FDE (HR and finance).",
        cash: "No Head of People cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
    },
    "Series B": {
      "VP Sales": {
        equity:
          "Index VP rule of thumb: 0.2%–0.7% FDE, sales lower. UltraTalent Series B: 0.50%–1.50% FD (median 0.75%, attributed to Carta Q1 2026). The CRO Report typical Series B: 0.1%–0.5%. The CRO Report April 2026 update: “average 0.4–0.7%.” Not averaged.",
        cash:
          "UltraTalent: $220k base / $385k median OTE. The CRO Report Series B/C (100 postings): average base $164,466–$226,224; OTE typically 2× base ($328k–$452k).",
        vest: "4 years, 1-year cliff. The CRO Report April 2026: companies increasingly offering 4-year vesting with 1-year cliffs.",
      },
      "VP Eng": {
        equity: "High end of Index VP 0.2%–0.7% FDE. CTO typical 1% US still stated by Index for Series A or B.",
        cash: "No VP Eng cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
      "CFO / VP Finance": {
        equity:
          "True CFO (C-level): Index 0.8%–1.5% FDE in the Series A and B table, typical 1%. VP Finance: smaller end of Index VP 0.2%–0.7% FDE.",
        cash: "No CFO / VP Finance cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
      "VP Product": {
        equity: "High end of Index VP 0.2%–0.7% FDE.",
        cash: "No VP Product cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
      "Head of People": {
        equity: "Smaller end of Index VP 0.2%–0.7% FDE (HR and finance).",
        cash: "No Head of People cash band in the fetched sources.",
        vest: "4 years, 1-year cliff.",
      },
    },
  };

  var NINE_A =
    "A 409A valuation is valid for a maximum of 12 months, and ends sooner after a material event (Carta, 4 August 2026; Kruze). Material events include a priced round, SAFE, convertible note, credible acquisition term sheet, or a major change in projections. Strike price must be at least FMV on the grant date. Do not grant on an expired 409A. Board-approve the new FMV first.";

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

  function parsePct(value) {
    if (value == null) return null;
    var s = String(value).trim().replace(/%/g, "").replace(/,/g, "");
    if (s === "") return null;
    var n = Number(s);
    if (!Number.isFinite(n)) return null;
    return n;
  }

  function fmtPct(n) {
    var abs = Math.abs(n);
    if (abs >= 10) return n.toFixed(1) + "%";
    if (abs >= 1) return n.toFixed(2) + "%";
    return n.toFixed(3) + "%";
  }

  function field(id, label, input) {
    return el("div", { className: "eq-field" }, [
      el("label", { htmlFor: id }, [label]),
      input,
    ]);
  }

  function mount(root) {
    if (root.getAttribute("data-eq-ready") === "true") return;
    root.setAttribute("data-eq-ready", "true");

    var stageSel = el(
      "select",
      { id: "eq-stage", name: "stage", required: true },
      ["Seed", "Series A", "Series B"].map(function (s) {
        return el("option", { value: s }, [s]);
      })
    );
    var roleSel = el(
      "select",
      { id: "eq-role", name: "role", required: true },
      ["VP Sales", "VP Eng", "CFO / VP Finance", "VP Product", "Head of People"].map(
        function (s) {
          return el("option", { value: s }, [s]);
        }
      )
    );
    var poolInput = el("input", {
      id: "eq-pool",
      name: "pool",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      required: true,
      placeholder: "e.g. 8",
    });
    var grantInput = el("input", {
      id: "eq-grant",
      name: "grant",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      required: true,
      placeholder: "e.g. 0.8",
    });
    var cashInput = el("input", {
      id: "eq-cash",
      name: "cash",
      type: "text",
      inputmode: "decimal",
      autocomplete: "off",
      placeholder: "Optional. Base in USD, e.g. 200000",
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

    function row(dt, dd) {
      var wrap = el("div", { className: "eq-row" }, [
        el("dt", null, [dt]),
        el("dd", null, [dd]),
      ]);
      return wrap;
    }

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;

      var stage = stageSel.value;
      var role = roleSel.value;
      var pool = parsePct(poolInput.value);
      var grant = parsePct(grantInput.value);
      var cashRaw = String(cashInput.value || "").trim();
      var cash = cashRaw === "" ? null : Number(String(cashRaw).replace(/[$,]/g, ""));

      if (pool == null || grant == null) {
        setError("Enter unallocated pool % and this grant % as numbers.");
        return;
      }
      if (pool < 0 || pool > 100) {
        setError("Unallocated pool must be between 0 and 100.");
        return;
      }
      if (grant <= 0 || grant >= 100) {
        setError("This grant % must be greater than 0 and less than 100.");
        return;
      }
      if (cashRaw !== "" && (!Number.isFinite(cash) || cash < 0)) {
        setError("Cash, if entered, must be a positive USD amount.");
        return;
      }

      var remaining = pool - grant;
      var ofPool = pool > 0 ? (grant / pool) * 100 : null;
      var band = BANDS[stage][role];

      var dl = el("dl", { className: "eq-dl" }, [
        row("Stage", stage),
        row("Role", role),
        row("Cited equity band", band.equity),
        row("Cited cash / OTE", band.cash),
        row("Vest (cited)", band.vest),
        row("This grant", fmtPct(grant) + " of the company, fully diluted"),
        row(
          "Unallocated pool remaining",
          remaining < 0
            ? fmtPct(remaining) + " — this grant is larger than remaining pool."
            : fmtPct(remaining) + " of the company"
        ),
        row(
          "This grant as share of starting pool",
          ofPool == null ? "Pool was 0." : fmtPct(ofPool) + " of the unallocated pool you entered"
        ),
      ]);

      if (cash != null) {
        dl.appendChild(
          row(
            "Cash you entered",
            "$" +
              Math.round(cash).toLocaleString("en-US") +
              ". Compare only to the cited cash line above."
          )
        );
      }

      var warn =
        remaining < 0
          ? "This grant exceeds remaining unallocated pool. Resize the grant, recycle cancelled options, or top up the pool (that top-up is a dilution event — Carta, Kruze)."
          : remaining < grant
            ? "Pool remaining after this grant is smaller than the grant itself. Check the rest of the 12–18 month hiring plan (Carta) before you sign."
            : "Carta: size the pool from a 12–18 month hiring plan, not a default 10%. Index: the ESOP should cover talent needs through the next round.";

      outEl.innerHTML = "";
      outEl.appendChild(dl);
      outEl.appendChild(el("p", { className: "eq-note" }, [warn]));
      outEl.appendChild(el("p", { className: "eq-note" }, [NINE_A]));
      outEl.appendChild(
        el("p", { className: "eq-note" }, [
          "This is not legal, tax, or compensation advice. Confirm grants with counsel and your 409A provider.",
        ])
      );
      outEl.hidden = false;
      outEl.focus();
    }

    var form = el("form", { id: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Numbers are fully diluted percentages. Bands are cited; blank cash means the sources did not publish a VP cash figure for that seat.",
      ]),
      field("eq-stage", "Stage", stageSel),
      field("eq-role", "Role", roleSel),
      field("eq-pool", "Unallocated pool %", poolInput),
      field("eq-grant", "This grant %", grantInput),
      field("eq-cash", "Cash, optional (USD base)", cashInput),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Clear"]),
      ]),
    ]);

    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function () {
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    root.appendChild(form);
    root.appendChild(outEl);
  }

  function boot() {
    var root = document.getElementById("equity-calculator");
    if (root) mount(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
