/* FounderNexus executive equity calculator.
   Client-side only. No tracking, no network, no "Join now".
   Bands are cited public figures; this file does not invent ranges.
   Bound to #equity-calc (build.py calculator layout).
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

  var form = document.getElementById("equity-calc");
  if (!form) return;

  var result = document.getElementById("equity-result");
  var errorEl = document.getElementById("equity-error");

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

  function showError(msg) {
    if (!errorEl) return;
    errorEl.hidden = !msg;
    errorEl.textContent = msg || "";
  }

  function row(label, value) {
    return "<div><dt>" + label + "</dt><dd>" + value + "</dd></div>";
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    showError("");

    var stage = form.stage.value;
    var role = form.role.value;
    var pool = parsePct(form.pool.value);
    var grant = parsePct(form.grant.value);
    var cashRaw = String(form.cash.value || "").trim();
    var cash = cashRaw === "" ? null : Number(String(cashRaw).replace(/[$,]/g, ""));

    if (!stage) {
      showError("Choose Seed, Series A, or Series B.");
      form.stage.focus();
      return;
    }
    if (!role) {
      showError("Choose the role you are granting into.");
      form.role.focus();
      return;
    }
    if (pool == null || grant == null) {
      showError("Enter unallocated pool % and this grant % as numbers.");
      form.pool.focus();
      return;
    }
    if (pool < 0 || pool > 100) {
      showError("Unallocated pool must be between 0 and 100.");
      form.pool.focus();
      return;
    }
    if (grant <= 0 || grant >= 100) {
      showError("This grant % must be greater than 0 and less than 100.");
      form.grant.focus();
      return;
    }
    if (cashRaw !== "" && (!Number.isFinite(cash) || cash < 0)) {
      showError("Cash, if entered, must be a positive USD amount.");
      form.cash.focus();
      return;
    }

    var remaining = pool - grant;
    var ofPool = pool > 0 ? (grant / pool) * 100 : null;
    var band = BANDS[stage][role];

    var html = '<dl class="result-dl">';
    html += row("Stage", escapeHtml(stage) + " (Stage 1 $0–2M Pre-Seed/Seed · Stage 2 $2–10M Series A · Stage 3 $10–50M Series B/C)");
    html += row("Role", escapeHtml(role));
    html += row("Cited equity band", escapeHtml(band.equity));
    html += row("Cited cash / OTE", escapeHtml(band.cash));
    html += row("Vest (cited)", escapeHtml(band.vest));
    html += row("This grant", fmtPct(grant) + " of the company, fully diluted");
    html += row(
      "Unallocated pool remaining",
      remaining < 0
        ? fmtPct(remaining) + " — this grant is larger than remaining pool."
        : fmtPct(remaining) + " of the company"
    );
    html += row(
      "This grant as share of starting pool",
      ofPool == null ? "Pool was 0." : fmtPct(ofPool) + " of the unallocated pool you entered"
    );
    if (cash != null) {
      html += row(
        "Cash you entered",
        "$" + Math.round(cash).toLocaleString("en-US") +
          ". Compare only to the cited cash line above; there is no FounderNexus cash band."
      );
    }
    html += "</dl>";

    var warn =
      remaining < 0
        ? "This grant exceeds remaining unallocated pool. Resize the grant, recycle cancelled options, or top up the pool (that top-up is a dilution event — Carta, Kruze)."
        : remaining < grant
          ? "Pool remaining after this grant is smaller than the grant itself. Check the rest of the 12–18 month hiring plan (Carta) before you sign."
          : "Carta: size the pool from a 12–18 month hiring plan, not a default 10%. Index: the ESOP should cover talent needs through the next round.";

    html += '<p class="small" style="margin-top:16px">' + escapeHtml(warn) + "</p>";
    html += '<p class="small">' + escapeHtml(NINE_A) + "</p>";
    html += '<p class="small">This is not legal, tax, or compensation advice. Confirm grants with counsel and your 409A provider.</p>';

    result.innerHTML = html;
    result.classList.remove("result-placeholder");
    result.focus();
  });

  form.addEventListener("reset", function () {
    showError("");
    result.classList.add("result-placeholder");
    result.innerHTML =
      '<p class="muted">Results land here. Bands are cited public figures, not FounderNexus data. Conflicting sources are shown separately.</p>';
  });
})();
