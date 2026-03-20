(function () {
  const input = document.getElementById("search");
  const meta = document.getElementById("search-meta");
  const sections = Array.from(document.querySelectorAll("article.section"));
  const parts = Array.from(document.querySelectorAll("section.part"));
  const tocParts = Array.from(document.querySelectorAll(".toc-part"));
  const tocLeaves = Array.from(document.querySelectorAll(".toc-leaf"));
  if (!input || !sections.length) return;

  function clearHighlights() {
    sections.forEach(function (sec) {
      sec.querySelectorAll("mark.search-hit").forEach(function (m) {
        const parent = m.parentNode;
        while (m.firstChild) parent.insertBefore(m.firstChild, m);
        parent.removeChild(m);
        parent.normalize();
      });
    });
  }

  function highlightText(node, query) {
    if (!query || query.length < 2) return 0;
    let hits = 0;
    const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        let el = n.parentElement;
        while (el) {
          if (el.tagName === "MARK" || el.tagName === "SCRIPT") return NodeFilter.FILTER_REJECT;
          el = el.parentElement;
        }
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    const toProcess = [];
    while (walker.nextNode()) toProcess.push(walker.currentNode);

    const lowerQ = query.toLowerCase();
    toProcess.forEach(function (textNode) {
      const text = textNode.nodeValue;
      const lower = text.toLowerCase();
      let idx = lower.indexOf(lowerQ);
      if (idx < 0) return;
      const frag = document.createDocumentFragment();
      let pos = 0;
      while (idx >= 0) {
        if (idx > pos) frag.appendChild(document.createTextNode(text.slice(pos, idx)));
        const mark = document.createElement("mark");
        mark.className = "search-hit";
        mark.appendChild(document.createTextNode(text.slice(idx, idx + query.length)));
        frag.appendChild(mark);
        hits += 1;
        pos = idx + query.length;
        idx = lower.indexOf(lowerQ, pos);
      }
      if (pos < text.length) frag.appendChild(document.createTextNode(text.slice(pos)));
      textNode.parentNode.replaceChild(frag, textNode);
    });
    return hits;
  }

  function sectionIdFromHash(href) {
    if (!href || href.charAt(0) !== "#") return "";
    try {
      return decodeURIComponent(href.slice(1));
    } catch (e) {
      return href.slice(1);
    }
  }

  function syncPartVisibility() {
    parts.forEach(function (part) {
      const arts = part.querySelectorAll("article.section");
      const anyVisible = Array.from(arts).some(function (a) {
        return !a.classList.contains("section--hidden");
      });
      part.classList.toggle("part--hidden", !anyVisible);
    });
    tocParts.forEach(function (li) {
      const links = li.querySelectorAll('a[href^="#"]');
      const anyVisible = Array.from(links).some(function (a) {
        const id = sectionIdFromHash(a.getAttribute("href"));
        const el = id ? document.getElementById(id) : null;
        return el && !el.classList.contains("section--hidden");
      });
      li.classList.toggle("toc-part--hidden", !anyVisible);
    });
    tocLeaves.forEach(function (li) {
      const a = li.querySelector('a[href^="#"]');
      if (!a) return;
      const id = sectionIdFromHash(a.getAttribute("href"));
      const el = id ? document.getElementById(id) : null;
      const visible = el && !el.classList.contains("section--hidden");
      li.classList.toggle("toc-leaf--hidden", !visible);
    });
  }

  function runSearch() {
    const q = input.value.trim();
    clearHighlights();

    if (!q) {
      sections.forEach(function (s) {
        s.classList.remove("section--hidden");
      });
      parts.forEach(function (p) {
        p.classList.remove("part--hidden");
      });
      tocParts.forEach(function (li) {
        li.classList.remove("toc-part--hidden");
      });
      tocLeaves.forEach(function (li) {
        li.classList.remove("toc-leaf--hidden");
      });
      if (meta) meta.textContent = "";
      return;
    }

    const lower = q.toLowerCase();
    let visible = 0;
    let marks = 0;
    sections.forEach(function (sec) {
      const body = sec.querySelector(".section-body");
      const title = (sec.dataset.title || sec.querySelector("h2")?.textContent || "").toLowerCase();
      const haystack = (body ? body.textContent : "").toLowerCase();
      const match = haystack.includes(lower) || title.includes(lower);
      if (match) {
        sec.classList.remove("section--hidden");
        visible += 1;
        if (body) marks += highlightText(body, q);
      } else {
        sec.classList.add("section--hidden");
      }
    });

    syncPartVisibility();

    if (meta) {
      if (visible === 0) meta.textContent = "No sections match.";
      else meta.textContent = marks ? visible + " section(s), " + marks + " highlight(s)" : visible + " section(s)";
    }
  }

  let t = null;
  input.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(runSearch, 120);
  });
  input.addEventListener("search", runSearch);
})();
