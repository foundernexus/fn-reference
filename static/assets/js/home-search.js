/* Homepage finder: filters an inline page index as you type. No network calls. */
(function () {
  var input = document.getElementById("home-q");
  var list = document.getElementById("home-results");
  var dataEl = document.getElementById("fd-index");
  if (!input || !list || !dataEl) return;
  var items;
  try { items = JSON.parse(dataEl.textContent); } catch (e) { return; }
  var synonyms = { vp: "vp executive", ceo: "ceo", arr: "arr revenue", gtm: "customers sales", safe: "safe", pool: "pool option", options: "option equity", raise: "raise round fundraising", hire: "hire hiring" };
  items.forEach(function (it) {
    it.hay = (it.t + " " + it.d + " " + it.k).toLowerCase();
    it.tl = it.t.toLowerCase();
    it.flat = it.hay.replace(/[^a-z0-9]/g, "");
    it.words = it.hay.split(/[^a-z0-9]+/).filter(function (w) { return w.length > 2; });
    it.twords = it.tl.split(/[^a-z0-9]+/).filter(function (w) { return w.length > 2; });
  });

  // Typo tolerance: edit distance with an early exit once it passes max.
  function near(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return false;
    var prev = [], cur, i, j;
    for (j = 0; j <= b.length; j++) prev[j] = j;
    for (i = 1; i <= a.length; i++) {
      cur = [i];
      var low = i;
      for (j = 1; j <= b.length; j++) {
        cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
        if (cur[j] < low) low = cur[j];
      }
      if (low > max) return false;
      prev = cur;
    }
    return prev[b.length] <= max;
  }
  function fuzzy(it, tok) {
    if (tok.length < 4) return 0;
    if (tok.length >= 5 && it.flat.indexOf(tok) !== -1) return 1; // "seriesa" -> "series a"
    var max = tok.length >= 7 ? 2 : 1;
    for (var t = 0; t < it.twords.length; t++) {
      if (near(tok, it.twords[t], max)) return 2;
    }
    for (var w = 0; w < it.words.length; w++) {
      if (near(tok, it.words[w], max)) return 1;
    }
    return 0;
  }
  var active = -1, shown = [];

  function render(q) {
    var toks = q.toLowerCase().split(/[^a-z0-9$%]+/).filter(Boolean);
    list.innerHTML = "";
    active = -1;
    if (!toks.length) { list.hidden = true; shown = []; return; }
    shown = items.map(function (it) {
      var score = 0;
      for (var i = 0; i < toks.length; i++) {
        var alts = (synonyms[toks[i]] || toks[i]).split(" ");
        var hit = 0;
        for (var j = 0; j < alts.length; j++) {
          if (it.tl.indexOf(alts[j]) !== -1) { hit = 3; break; }
          if (it.hay.indexOf(alts[j]) !== -1) hit = Math.max(hit, 1);
        }
        if (!hit) hit = fuzzy(it, toks[i]);
        if (!hit) return null;
        score += hit;
      }
      return { it: it, score: score };
    }).filter(Boolean).sort(function (a, b) { return b.score - a.score; }).slice(0, 7);
    if (!shown.length) {
      var li = document.createElement("li");
      li.className = "home-results-empty";
      li.textContent = "No page matches yet. Try a shorter word, or browse the topics below.";
      list.appendChild(li);
    }
    shown.forEach(function (r, idx) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = r.it.u;
      a.id = "home-r-" + idx;
      var t = document.createElement("span"); t.className = "r-title"; t.textContent = r.it.t;
      var k = document.createElement("span"); k.className = "r-topic"; k.textContent = r.it.k;
      a.appendChild(t); a.appendChild(k);
      li.appendChild(a); list.appendChild(li);
    });
    list.hidden = false;
  }

  function setActive(n) {
    var links = list.querySelectorAll("a");
    if (!links.length) return;
    active = (n + links.length) % links.length;
    links.forEach(function (a, i) { a.classList.toggle("is-active", i === active); });
    input.setAttribute("aria-activedescendant", links[active].id);
  }

  input.addEventListener("input", function () { render(input.value); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
    else if (e.key === "Escape") { list.hidden = true; }
  });
  input.form.addEventListener("submit", function (e) {
    var links = list.querySelectorAll("a");
    if (links.length) { e.preventDefault(); location.href = links[Math.max(active, 0)].href; }
  });
})();
