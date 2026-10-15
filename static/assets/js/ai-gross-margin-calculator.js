/* AI gross margin calculator.
   Client-side only. No tracking, no network.
   AI-inclusive gross margin = (revenue − classic COGS − AI delivery COGS) ÷ revenue.
   AI delivery COGS lines follow The SaaS CFO (Murray, 2026): production inference,
   production GPU serving, AI infrastructure layer, AI monitoring, AI support.
   Human review of customer outputs follows a16z (Casado and Bornstein, 2020).
   Band reads use Murray's published bands by product type. Other publishers are
   cited on the page, not averaged into a verdict.
   Defaults are a labeled editorial example. Not legal, tax, or investment advice.
*/
(function () {
  "use strict";

  var DEFAULTS = {
    revenue: "500000",
    classic: "75000",
    inference: "80000",
    gpu: "0",
    infra: "15000",
    monitoring: "5000",
    support: "10000",
    review: "0",
    units: "10000",
    unitLabel: "user",
    cohortRev: "60000",
    cohortAi: "50000",
    devTest: "30000",
    type: "native",
    target: "65",
  };

  var BANDS = {
    native: {
      label: "AI-native (inference is core to delivery)",
      read: function (gm) {
        if (gm >= 65)
          return {
            tone: "good",
            text:
              "At or above the top of Murray’s AI-native band (50–65% at maturity).",
          };
        if (gm >= 50)
          return {
            tone: "good",
            text: "Inside Murray’s AI-native band at maturity (50–65%).",
          };
        if (gm > 30)
          return {
            tone: "mid",
            text:
              "Below Murray’s AI-native maturity band (50–65%) and above the 25–30% he says early-stage AI-native companies often run. Show the path up.",
          };
        if (gm >= 25)
          return {
            tone: "mid",
            text:
              "Inside the 25–30% range Murray says early-stage AI-native companies often run. The board will ask for the path to 50–65%.",
          };
        return {
          tone: "warn",
          text:
            "Below the 25–30% early-stage AI-native range Murray cites. Bessemer’s 2025 Supernovas averaged about 25%, often negative, and Bessemer says many traded margin for distribution. Say which trade you are making.",
        };
      },
    },
    enabled: {
      label: "AI-enabled SaaS (SaaS with AI features added)",
      read: function (gm) {
        if (gm > 85)
          return {
            tone: "good",
            text:
              "Above Murray’s AI-enabled band (72–85%). Check that you mapped all six AI delivery lines to COGS.",
          };
        if (gm >= 72)
          return {
            tone: "good",
            text: "Inside Murray’s AI-enabled band (72–85%).",
          };
        return {
          tone: "warn",
          text:
            "Below Murray’s AI-enabled band (72–85%). If inference is core to delivery, the AI-native band (50–65% at maturity) may be the fair comparison. Pick one and say why.",
        };
      },
    },
    classic: {
      label: "Traditional SaaS (little or no AI in delivery)",
      read: function (gm) {
        if (gm > 80)
          return {
            tone: "good",
            text: "Above Murray’s traditional SaaS benchmark (70–80%).",
          };
        if (gm >= 70)
          return {
            tone: "good",
            text: "Inside Murray’s traditional SaaS benchmark (70–80%).",
          };
        return {
          tone: "warn",
          text:
            "Below Murray’s traditional SaaS benchmark (70–80%). If AI costs drive the gap, read against the AI-enabled or AI-native band instead.",
        };
      },
    },
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
    return Number.isFinite(n) ? n : null;
  }

  function fmtMoney(n, cents) {
    if (!Number.isFinite(n)) return "n/a";
    var sign = n < 0 ? "-" : "";
    var abs = Math.abs(n);
    if (cents)
      return (
        sign +
        "$" +
        abs.toLocaleString("en-US", {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        })
      );
    return sign + "$" + Math.round(abs).toLocaleString("en-US");
  }

  function fmtPct(n) {
    if (!Number.isFinite(n)) return "n/a";
    return n.toFixed(1) + "%";
  }

  function fmtPts(n) {
    if (!Number.isFinite(n)) return "n/a";
    return n.toFixed(1) + " pts";
  }

  function textInput(id, value, placeholder) {
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

  function selectInput(id, options, value) {
    var s = el(
      "select",
      { id: id, name: id },
      options.map(function (o) {
        return el("option", { value: o[0] }, [o[1]]);
      })
    );
    s.value = value;
    return s;
  }

  function field(id, label, input, hint) {
    var kids = [el("label", { htmlFor: id }, [label]), input];
    if (hint) kids.push(el("p", { className: "eq-hint" }, [hint]));
    return el("div", { className: "eq-field" }, kids);
  }

  function card(label, value, tone) {
    var cls = "eq-summary-card" + (tone ? " eq-summary-card--" + tone : "");
    return el("div", { className: cls }, [
      el("dt", null, [label]),
      el("dd", null, [value]),
    ]);
  }

  function note(title, text) {
    return el("div", { className: "eq-note" }, [
      el("strong", null, [title + " "]),
      document.createTextNode(text),
    ]);
  }

  function erosionRead(pts) {
    if (!Number.isFinite(pts)) return "";
    if (pts >= 16)
      return (
        "AI costs take " +
        pts.toFixed(1) +
        " points of margin. In the Mavvrik and Benchmarkit 2025 survey (N=372), 26% of companies reported 16 points or more."
      );
    if (pts > 6)
      return (
        "AI costs take " +
        pts.toFixed(1) +
        " points of margin. In the Mavvrik and Benchmarkit 2025 survey (N=372), 84% reported more than 6 points."
      );
    return (
      "AI costs take " +
      pts.toFixed(1) +
      " points of margin. That is at or under the 6-point line that 84% of Mavvrik and Benchmarkit 2025 respondents (N=372) said they exceeded."
    );
  }

  function compute(v) {
    var ai = v.inference + v.gpu + v.infra + v.monitoring + v.support + v.review;
    var exAi = ((v.revenue - v.classic) / v.revenue) * 100;
    var incl = ((v.revenue - v.classic - ai) / v.revenue) * 100;
    var aiShare = (ai / v.revenue) * 100;
    var perUnit = v.units > 0 ? ai / v.units : null;
    var cohortShare = v.cohortRev > 0 ? (v.cohortAi / v.cohortRev) * 100 : null;
    var withDev =
      ((v.revenue - v.classic - ai - v.devTest) / v.revenue) * 100;
    var t = v.target / 100;
    var aiBudget = v.revenue * (1 - t) - v.classic;
    var gap = ai - aiBudget;
    var perUnitBudget = v.units > 0 ? aiBudget / v.units : null;
    var revNeeded = t < 1 ? (v.classic + ai) / (1 - t) : null;
    var lift = revNeeded != null ? (revNeeded / v.revenue - 1) * 100 : null;
    return {
      ai: ai,
      exAi: exAi,
      incl: incl,
      aiShare: aiShare,
      perUnit: perUnit,
      cohortShare: cohortShare,
      withDev: withDev,
      aiBudget: aiBudget,
      gap: gap,
      perUnitBudget: perUnitBudget,
      revNeeded: revNeeded,
      lift: lift,
    };
  }

  function mount(root) {
    var ids = {
      revenue: "agm-revenue",
      classic: "agm-classic",
      inference: "agm-inference",
      gpu: "agm-gpu",
      infra: "agm-infra",
      monitoring: "agm-monitoring",
      support: "agm-support",
      review: "agm-review",
      units: "agm-units",
      cohortRev: "agm-cohort-rev",
      cohortAi: "agm-cohort-ai",
      devTest: "agm-devtest",
      target: "agm-target",
    };
    var inputs = {};
    Object.keys(ids).forEach(function (k) {
      inputs[k] = textInput(ids[k], DEFAULTS[k]);
    });
    var unitSel = selectInput(
      "agm-unit",
      [
        ["user", "Active users"],
        ["workflow", "Completed workflows"],
      ],
      DEFAULTS.unitLabel
    );
    var typeSel = selectInput(
      "agm-type",
      [
        ["native", BANDS.native.label],
        ["enabled", BANDS.enabled.label],
        ["classic", BANDS.classic.label],
      ],
      DEFAULTS.type
    );

    var errorEl = el("p", { className: "eq-error", hidden: true });
    var outEl = el("div", { className: "eq-out", hidden: true, tabindex: "-1" });

    function setError(msg) {
      errorEl.hidden = !msg;
      errorEl.textContent = msg || "";
    }

    function calculate(e) {
      if (e) e.preventDefault();
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";

      var v = {};
      var missing = false;
      Object.keys(ids).forEach(function (k) {
        v[k] = parseNum(inputs[k].value);
        if (v[k] == null) missing = true;
      });
      if (missing) {
        setError("Enter a number in each field. Use 0 for lines you do not have.");
        return;
      }
      if (v.revenue <= 0) {
        setError("Monthly revenue must be greater than zero.");
        return;
      }
      var neg = Object.keys(ids).some(function (k) {
        return v[k] < 0;
      });
      if (neg) {
        setError("Costs, revenue, and counts cannot be negative.");
        return;
      }
      if (v.target >= 100) {
        setError("Target gross margin should be below 100%.");
        return;
      }
      if (v.cohortRev > v.revenue) {
        setError("Heavy-user cohort revenue cannot exceed total revenue.");
        return;
      }

      var r = compute(v);
      var band = BANDS[typeSel.value] || BANDS.native;
      var bandRead = band.read(r.incl);
      var unitWord = unitSel.value === "workflow" ? "workflow" : "active user";

      var cohortTone = null;
      if (r.cohortShare != null)
        cohortTone = r.cohortShare >= 100 ? "warn" : r.cohortShare >= 50 ? "mid" : null;

      var summary = el("dl", { className: "eq-summary" }, [
        card("AI-inclusive gross margin", fmtPct(r.incl), bandRead.tone),
        card("Software gross margin ex-AI", fmtPct(r.exAi), null),
        card("AI delivery cost % of revenue", fmtPct(r.aiShare), null),
        card(
          "AI COGS per " + unitWord + " (month)",
          r.perUnit == null ? "n/a" : fmtMoney(r.perUnit, true),
          null
        ),
        card(
          "Heavy cohort: AI COGS ÷ cohort revenue",
          r.cohortShare == null ? "n/a" : fmtPct(r.cohortShare),
          cohortTone
        ),
        card("Margin if dev/test sits in COGS", fmtPct(r.withDev), null),
      ]);

      var targetCards = el("dl", { className: "eq-summary" }, [
        card("AI budget at " + v.target + "% target", fmtMoney(r.aiBudget), null),
        card(
          r.gap > 0 ? "AI spend over budget" : "AI spend under budget",
          fmtMoney(Math.abs(r.gap)),
          r.gap > 0 ? "warn" : "good"
        ),
        card(
          "AI COGS per " + unitWord + " at target",
          r.perUnitBudget == null ? "n/a" : fmtMoney(r.perUnitBudget, true),
          null
        ),
        card(
          "Revenue lift to hit target at today’s costs",
          r.lift == null ? "n/a" : r.lift <= 0 ? "None needed" : fmtPct(r.lift),
          null
        ),
      ]);

      var cohortText =
        r.cohortShare == null
          ? "Enter cohort revenue to see whether your heaviest users pay for their own AI costs."
          : r.cohortShare >= 100
          ? "Your heavy-user cohort costs more in AI COGS than it pays you, before classic COGS. Price usage, cap it, or route those requests to cheaper models."
          : "AI COGS takes " +
            fmtPct(r.cohortShare) +
            " of heavy-cohort revenue before classic COGS. Murray cites estimates that heavy users can cost 50 to 100 times more than light users, so track this line monthly.";

      outEl.appendChild(
        el("p", { className: "eq-lede", style: "margin-top:0" }, [
          "Results on the numbers you typed, for your own planning. Not legal, tax, or investment advice.",
        ])
      );
      outEl.appendChild(summary);
      outEl.appendChild(note("Band read (" + band.label + ").", bandRead.text));
      outEl.appendChild(note("Margin points.", erosionRead(r.aiShare)));
      outEl.appendChild(note("Heavy users.", cohortText));
      outEl.appendChild(
        note(
          "Classification swing.",
          "Book all AI spend in R&D and the slide says " +
            fmtPct(r.exAi) +
            ". Book the dev/test inference to COGS and it says " +
            fmtPct(r.withDev) +
            ". The " +
            fmtPct(r.incl) +
            " is the figure a diligence team will rebuild."
        )
      );
      outEl.appendChild(el("h3", { className: "eq-subhead" }, ["Against your target"]));
      outEl.appendChild(targetCards);
      outEl.appendChild(
        note(
          "Formulas.",
          "AI-inclusive gross margin = (revenue − classic COGS − AI delivery COGS) ÷ revenue. Software gross margin ex-AI = (revenue − classic COGS) ÷ revenue. The gap between them equals AI delivery cost ÷ revenue. AI budget at target = revenue × (1 − target) − classic COGS. Revenue lift = (classic COGS + AI delivery COGS) ÷ (1 − target) ÷ revenue − 1, holding costs flat. Bands from The SaaS CFO (Murray, 2026), one publisher. Other publishers are on the page as separate rows."
        )
      );
      outEl.hidden = false;
      outEl.focus();
    }

    function f(k, label, hint) {
      return field(ids[k], label, inputs[k], hint);
    }

    var form = el("form", { id: "agm-form", className: "eq-form", novalidate: true }, [
      el("p", { className: "eq-lede" }, [
        "Defaults are the editorial example on this page: $500k monthly revenue, $75k classic COGS, $110k AI delivery costs, 10,000 active users, a 1,000-user heavy cohort, and $30k of dev/test inference on the production account. Replace each field with your own monthly figures.",
      ]),
      el("h3", { className: "eq-subhead" }, ["Revenue and classic COGS (monthly)"]),
      el("div", { className: "eq-fields" }, [
        f("revenue", "Revenue ($)", "Recognized revenue for the month."),
        f(
          "classic",
          "Classic COGS ($)",
          "Hosting, support, customer success, DevOps. Your pre-AI stack."
        ),
      ]),
      el("h3", { className: "eq-subhead" }, ["AI delivery costs in COGS (monthly)"]),
      el("div", { className: "eq-fields" }, [
        f("inference", "Production inference ($)", "Model API calls that answer customers."),
        f("gpu", "Production GPU serving ($)", "Self-hosted or fine-tuned models served to customers."),
        f(
          "infra",
          "AI infrastructure layer ($)",
          "Vector DB, embeddings, retrieval, orchestration, egress to model providers."
        ),
        f("monitoring", "AI monitoring and evals ($)", "Tracing, evals, guardrails on production traffic."),
        f("support", "AI-related support ($)", "Incremental hours on AI-tagged tickets."),
        f("review", "Human review of outputs ($)", "People who check AI output before the customer sees it."),
      ]),
      el("h3", { className: "eq-subhead" }, ["Units and heavy users"]),
      el("div", { className: "eq-fields" }, [
        field("agm-unit", "Unit for cost per unit", unitSel, "Name the unit on the slide."),
        f("units", "Units this month", "Active users or completed workflows."),
        f("cohortRev", "Heavy-user cohort revenue ($)", "Write the cohort cut down, for example top 10% by usage."),
        f("cohortAi", "Heavy-user cohort AI COGS ($)", "AI delivery costs attributed to that cohort."),
      ]),
      el("h3", { className: "eq-subhead" }, ["Classification check and target"]),
      el("div", { className: "eq-fields" }, [
        f(
          "devTest",
          "Dev/test inference on the production account ($)",
          "Engineering test spend mixed into the production bill. Use 0 if your accounts are split."
        ),
        field("agm-type", "Product type for the band read", typeSel, "Bands from The SaaS CFO (Murray, 2026)."),
        f("target", "Your target gross margin (%)", "Your own goal. The tool solves for the AI budget that hits it."),
      ]),
      errorEl,
      el("div", { className: "eq-actions" }, [
        el("button", { type: "submit", className: "btn btn-primary" }, ["Calculate"]),
        el("button", { type: "reset", className: "btn btn-secondary" }, ["Reset to example"]),
      ]),
    ]);

    form.addEventListener("submit", calculate);
    form.addEventListener("reset", function (ev) {
      ev.preventDefault();
      Object.keys(ids).forEach(function (k) {
        inputs[k].value = DEFAULTS[k];
      });
      unitSel.value = DEFAULTS.unitLabel;
      typeSel.value = DEFAULTS.type;
      setError("");
      outEl.hidden = true;
      outEl.innerHTML = "";
    });

    root.appendChild(form);
    root.appendChild(outEl);
  }

  function boot() {
    var root = document.getElementById("ai-gross-margin-calculator");
    if (root) mount(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
