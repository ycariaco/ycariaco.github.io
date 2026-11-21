---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 5
---

<section class="publication-garden" aria-labelledby="publication-garden-title">
  <div class="publication-garden-heading">
    <h2 id="publication-garden-title">Publications by year</h2>
    <button id="publication-motion" class="publication-garden-button" type="button" aria-pressed="false" disabled>Pause animation</button>
  </div>
  <p id="publication-garden-help" class="publication-garden-help">Each year is a flower center, with a paper on every petal. Hover to explore or click a petal to open the paper. Dashed petals are preprints.</p>
  <div id="cytoscape" role="img" aria-label="Publication flowers grouped by year" aria-describedby="publication-garden-help"></div>
  <label for="publication-picker" class="publication-garden-picker">Explore a publication</label>
  <select id="publication-picker" class="publication-garden-select" disabled>
    <option>Loading publications…</option>
  </select>
  <div id="publication-garden-detail" class="publication-garden-detail" aria-live="polite">
    Select a publication to see its details.
  </div>
</section>

<hr style="margin:40px 0;">

<h2>Full list of publications</h2>

<div id="pub-citation-summary" class="pub-citation-summary" aria-live="polite"></div>
<div id="pub-list" class="pub-list"></div>

<style>
  .pub-list { margin-top: 16px; }
  .pub-item { padding: 14px 0; border-bottom: 1px solid var(--global-divider-color, #eee); }
  .pub-title { font-weight: 600; }
  .pub-meta { color: var(--global-text-color, #555); opacity: .8; margin-top: 4px; }
  .pub-links { margin-top: 6px; }
  .pub-links a { margin-right: 10px; text-decoration: none; }
  .pub-citation-summary { margin-bottom: 18px; }
  .pub-citation-summary strong { font-size: 1.15rem; }
  .pub-citation-note { font-size: .85rem; opacity: .75; margin-top: 4px; }
  .publication-garden { margin: 0 0 24px; }
  .publication-garden-heading { display: flex; align-items: center; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  .publication-garden-heading h2 { margin: 0; }
  .publication-garden-help { margin: 12px 0 18px; font-size: .9rem; opacity: .8; }
  .publication-garden-button { border: 1px solid currentColor; border-radius: 20px; background: transparent; color: inherit; padding: 6px 14px; font: inherit; font-size: .85rem; cursor: pointer; }
  .publication-garden-button:focus-visible, .publication-garden-select:focus-visible { outline: 2px solid var(--global-theme-color, #e91e63); outline-offset: 3px; }
  .publication-garden-button:disabled { opacity: .5; cursor: default; }
  #cytoscape { width: 100%; min-height: 220px; border: 1px solid rgba(148, 163, 184, .3); border-radius: 16px; background: rgba(148, 163, 184, .035); }
  .publication-garden-picker { display: block; margin: 18px 0 6px; font-size: .85rem; }
  .publication-garden-select { width: 100%; min-width: 0; max-width: 100%; padding: 8px 10px; border: 1px solid rgba(148, 163, 184, .6); border-radius: 6px; font: inherit; font-size: .9rem; color: var(--global-text-color, #333); background: var(--global-bg-color, #fff); }
  .publication-garden-detail { min-height: 100px; margin-top: 12px; padding: 14px 16px; border-left: 3px solid var(--global-theme-color, #e91e63); background: rgba(148, 163, 184, .07); border-radius: 0 8px 8px 0; }
  .publication-garden-detail-title { font-weight: 600; }
  .publication-garden-detail-meta { margin: 6px 0; font-size: .88rem; opacity: .8; }
  @media (max-width: 480px) { .publication-garden-heading h2 { font-size: 1.4rem; } }
</style>

<script>
  function publicationDoiUrl(value) {
    const doi = String(value || "").trim().replace(/^https?:\/\/(?:dx\.)?doi\.org\//i, "");
    if (!/^10\.\d{4,9}\/[^\s<>"']+$/i.test(doi)) return "";
    return `https://doi.org/${encodeURIComponent(doi).replace(/%2F/gi, "/")}`;
  }

  function publicationPmidUrl(value) {
    const pmid = String(value || "").trim();
    return /^\d+$/.test(pmid) ? `https://pubmed.ncbi.nlm.nih.gov/${pmid}/` : "";
  }

  function publicationCitationCount(pub) {
    return pub.citation_source === "Crossref" && Number.isSafeInteger(pub.citation_count) && pub.citation_count >= 0
      ? pub.citation_count
      : null;
  }

  function publicationCitationText(pub) {
    const count = publicationCitationCount(pub);
    return count === null ? "" : `${count.toLocaleString()} Crossref ${count === 1 ? "citation" : "citations"}`;
  }

  fetch("/assets/json/publications.json")
    .then((r) => {
      if (!r.ok) throw new Error("Failed to load publications.json");
      return r.json();
    })
    .then((data) => {
      data.sort((a, b) => (b.year || 0) - (a.year || 0));
      const container = document.getElementById("pub-list");
      const citationCounts = data.map(publicationCitationCount).filter((count) => count !== null);
      const summary = document.getElementById("pub-citation-summary");
      if (citationCounts.length) {
        const total = citationCounts.reduce((sum, count) => sum + count, 0);
        const countText = document.createElement("strong");
        countText.textContent = `${total.toLocaleString()} ${total === 1 ? "citation" : "citations"}`;
        const source = document.createElement("a");
        source.href = "https://www.crossref.org/services/cited-by/";
        source.textContent = "Crossref";
        source.target = "_blank";
        source.rel = "noopener";
        const note = document.createElement("div");
        note.className = "pub-citation-note";
        note.textContent = "Counts reflect references indexed by Crossref and may differ from other databases.";
        if (citationCounts.length < data.length) {
          note.textContent += ` Counts are available for ${citationCounts.length} of ${data.length} publications.`;
        }
        summary.replaceChildren(countText, " · ", source, note);
      }
      const items = data.map((pub) => {
        const item = document.createElement("div");
        item.className = "pub-item";
        const title = document.createElement("div");
        title.className = "pub-title";
        title.textContent = `${pub.title || "Untitled"}${pub.year ? ` (${pub.year})` : ""}`;
        const metadata = document.createElement("div");
        metadata.className = "pub-meta";
        metadata.textContent = Array.isArray(pub.authors) ? pub.authors.join(", ") : "";
        if (pub.journal) {
          const journal = document.createElement("em");
          journal.textContent = pub.journal;
          metadata.append(" ", journal);
        }
        item.append(title, metadata);
        if (pub.kind === "preprint") {
          const status = document.createElement("div");
          status.className = "pub-meta";
          status.textContent = "Preprint · Not peer reviewed";
          item.append(status);
        }

        const citationText = publicationCitationText(pub);
        if (citationText) {
          const citations = document.createElement("div");
          citations.className = "pub-meta";
          citations.textContent = citationText;
          item.append(citations);
        }

        const urls = [
          ["DOI", publicationDoiUrl(pub.doi)],
          ["PMID", publicationPmidUrl(pub.pmid)],
          ...(pub.kind !== "preprint" && Array.isArray(pub.preprint_dois)
            ? pub.preprint_dois.map((doi, index) => [
                pub.preprint_dois.length > 1 ? `Preprint ${index + 1}` : "Preprint",
                publicationDoiUrl(doi),
              ])
            : []),
        ].filter(([, url]) => url);
        if (urls.length) {
          const links = document.createElement("div");
          links.className = "pub-links";
          urls.forEach(([label, url], index) => {
            if (index) links.append(" · ");
            const link = document.createElement("a");
            link.href = url;
            link.target = "_blank";
            link.rel = "noopener";
            link.textContent = label;
            links.append(link);
          });
          item.append(links);
        }
        return item;
      });
      container.replaceChildren(...items);
    })
    .catch((err) => {
      console.error(err);
      document.getElementById("pub-list").textContent = "Publications are temporarily unavailable. Please try again later.";
    });
</script>

<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>

<script>
  (() => {
    const garden = document.getElementById("cytoscape");
    const motionButton = document.getElementById("publication-motion");
    const picker = document.getElementById("publication-picker");
    const detail = document.getElementById("publication-garden-detail");

    fetch("/assets/json/publications.json")
      .then((response) => {
        if (!response.ok) throw new Error("Failed to load publications.json");
        return response.json();
      })
      .then((data) => {
        const publications = [...data].sort((a, b) => (b.year || 0) - (a.year || 0));
        if (!publications.length) {
          garden.textContent = "Publications will appear here as they are added.";
          picker.replaceChildren(new Option("No publications yet", ""));
          return;
        }
        const byId = new Map(publications.map((pub) => [pub.id, pub]));
        const years = [...new Set(publications.map((pub) => pub.year))].sort((a, b) => b - a);
        const palette = ["#F8BBD0", "#BBDEFB", "#C8E6C9", "#FFE0B2", "#D1C4E9", "#B2EBF2", "#FFCDD2", "#DCEDC8", "#FFF9C4", "#E1BEE7"];
        const flowers = years.map((year, index) => ({
          year,
          color: palette[index % palette.length],
          papers: publications.filter((pub) => pub.year === year),
          angle: index * .7,
          speed: (index % 2 ? -1 : 1) * (.085 + (index % 3) * .012),
          center: { x: 0, y: 0 },
        }));
        const elements = [];
        flowers.forEach((flower) => {
          elements.push({
            data: { id: `year-${flower.year}`, label: String(flower.year), color: flower.color },
            classes: "year-center",
          });
          flower.papers.forEach((pub) => {
            elements.push({
              data: { id: pub.id, color: flower.color, year: flower.year },
              classes: pub.kind === "preprint" ? "paper preprint" : "paper",
            });
            elements.push({ data: { source: `year-${flower.year}`, target: pub.id, color: flower.color } });
          });
        });

        const cy = cytoscape({
          container: garden,
          elements,
          layout: { name: "preset", fit: false },
          zoom: 1,
          pan: { x: 0, y: 0 },
          userZoomingEnabled: false,
          userPanningEnabled: false,
          boxSelectionEnabled: false,
          autoungrabify: true,
          autounselectify: true,
          style: [
            {
              selector: "node",
              style: { "background-color": "data(color)", width: 30, height: 30, "border-width": 1.5, "border-color": "#64748b", "overlay-opacity": 0 },
            },
            {
              selector: ".year-center",
              style: { width: 48, height: 48, label: "data(label)", color: "#263245", "font-size": 13, "font-weight": 600, "text-valign": "center", "text-halign": "center", "border-width": 2, "border-color": "#64748b" },
            },
            {
              selector: ".preprint",
              style: { "border-style": "dashed", "border-width": 2.5 },
            },
            {
              selector: ".paper.highlighted",
              style: { "border-width": 3, "border-color": "#d81b60", "underlay-color": "#e91e63", "underlay-opacity": .12, "underlay-padding": 5 },
            },
            {
              selector: "edge",
              style: { width: 2, "line-color": "data(color)", opacity: .8, "curve-style": "straight", "events": "no", "overlay-opacity": 0 },
            },
          ],
        });

        function showPublication(pub) {
          picker.value = pub.id;
          cy.nodes(".highlighted").removeClass("highlighted");
          cy.getElementById(pub.id).addClass("highlighted");
          const title = document.createElement("div");
          title.className = "publication-garden-detail-title";
          title.textContent = pub.title;
          const meta = document.createElement("div");
          meta.className = "publication-garden-detail-meta";
          meta.textContent = [pub.year, pub.journal, pub.kind === "preprint" ? "Preprint · Not peer reviewed" : "", publicationCitationText(pub)].filter(Boolean).join(" · ");
          const url = publicationDoiUrl(pub.doi) || publicationPmidUrl(pub.pmid);
          const children = [title, meta];
          if (url) {
            const link = document.createElement("a");
            link.href = url;
            link.target = "_blank";
            link.rel = "noopener";
            link.textContent = "Open publication ↗";
            children.push(link);
          }
          detail.replaceChildren(...children);
        }

        picker.replaceChildren(...publications.map((pub) => new Option(`${pub.year} · ${pub.title}${pub.kind === "preprint" ? " (Preprint)" : ""}`, pub.id)));
        picker.disabled = false;
        picker.addEventListener("change", () => showPublication(byId.get(picker.value)));
        showPublication(publications[0]);

        let cellWidth = 220;
        let heldYear = null;
        let lastWidth = 0;
        function positionPetals() {
          cy.batch(() => {
            flowers.forEach((flower) => {
              if (!flower.rings) return;
              cy.getElementById(`year-${flower.year}`).position(flower.center);
              let paperIndex = 0;
              flower.rings.forEach((ring, ringIndex) => {
                for (let i = 0; i < ring.count; i++) {
                  const angle = flower.angle * (ringIndex % 2 ? -.7 : 1) + i * 2 * Math.PI / ring.count - Math.PI / 2;
                  const pub = flower.papers[paperIndex++];
                  cy.getElementById(pub.id).position({ x: flower.center.x + ring.radius * flower.scale * Math.cos(angle), y: flower.center.y + ring.radius * flower.scale * Math.sin(angle) });
                }
              });
            });
          });
        }

        function arrangeFlowers() {
          const width = garden.clientWidth;
          if (!width || Math.abs(width - lastWidth) < 1) return;
          lastWidth = width;
          // Add rings for prolific years; scale each flower to fit even narrow screens.
          flowers.forEach((flower) => {
            flower.rings = [];
            let remaining = flower.papers.length;
            let radius = 62;
            while (remaining > 0) {
              const count = Math.min(remaining, Math.floor(2 * Math.PI * radius / 38));
              flower.rings.push({ radius, count });
              remaining -= count;
              radius += 38;
            }
          });
          const outerRadius = Math.max(...flowers.map((flower) => flower.rings[flower.rings.length - 1].radius));
          const desiredCell = Math.max(210, (outerRadius + 28) * 2);
          const columns = Math.max(1, Math.min(4, Math.floor(width / desiredCell)));
          cellWidth = width / columns;
          const cellHeight = Math.max(190, Math.min(outerRadius, cellWidth / 2 - 28) * 2 + 56);
          const rows = Math.ceil(flowers.length / columns);
          garden.style.height = `${rows * cellHeight + 24}px`;
          flowers.forEach((flower, index) => {
            const row = Math.floor(index / columns);
            const flowersInRow = Math.min(columns, flowers.length - row * columns);
            const rowOffset = (width - flowersInRow * cellWidth) / 2;
            flower.center = { x: rowOffset + (index % columns + .5) * cellWidth, y: 12 + (row + .5) * cellHeight };
            const radius = flower.rings[flower.rings.length - 1].radius;
            flower.scale = Math.min(1, Math.max(30, cellWidth / 2 - 28) / radius);
            flower.papers.forEach((pub) => cy.getElementById(pub.id).style({ width: 30 * flower.scale, height: 30 * flower.scale }));
            cy.getElementById(`year-${flower.year}`).style({ width: Math.max(32, 48 * flower.scale), height: Math.max(32, 48 * flower.scale) });
          });
          cy.resize();
          positionPetals();
        }

        const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
        let paused = reducedMotion.matches;
        let visible = true;
        let frame = 0;
        let lastTime = null;
        function updateMotionButton() {
          motionButton.textContent = paused ? "Resume animation" : "Pause animation";
          motionButton.setAttribute("aria-pressed", String(paused));
        }
        function tick(time) {
          frame = 0;
          if (paused || !visible || document.hidden) { lastTime = null; return; }
          if (lastTime !== null) {
            const elapsed = Math.min((time - lastTime) / 1000, .05);
            flowers.forEach((flower) => { if (flower.year !== heldYear) flower.angle += elapsed * flower.speed; });
            positionPetals();
          }
          lastTime = time;
          frame = requestAnimationFrame(tick);
        }
        function syncAnimation() {
          if (frame) cancelAnimationFrame(frame);
          frame = 0;
          lastTime = null;
          if (!paused && visible && !document.hidden) frame = requestAnimationFrame(tick);
          updateMotionButton();
        }
        motionButton.disabled = false;
        motionButton.addEventListener("click", () => { paused = !paused; syncAnimation(); });
        reducedMotion.addEventListener("change", (event) => { paused = event.matches; syncAnimation(); });
        document.addEventListener("visibilitychange", syncAnimation);
        const intersectionObserver = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; syncAnimation(); });
        intersectionObserver.observe(garden);
        const resizeObserver = new ResizeObserver(arrangeFlowers);
        resizeObserver.observe(garden);

        cy.on("mouseover", ".paper", (event) => {
          const pub = byId.get(event.target.id());
          heldYear = pub.year;
          garden.style.cursor = "pointer";
          showPublication(pub);
        });
        cy.on("mouseout", ".paper", () => { heldYear = null; garden.style.cursor = "default"; });
        cy.on("tap", ".paper", (event) => {
          const pub = byId.get(event.target.id());
          showPublication(pub);
          const url = publicationDoiUrl(pub.doi) || publicationPmidUrl(pub.pmid);
          if (url) window.open(url, "_blank", "noopener,noreferrer");
        });
        window.addEventListener("pagehide", () => {
          if (frame) cancelAnimationFrame(frame);
          frame = 0;
          lastTime = null;
        });
        window.addEventListener("pageshow", syncAnimation);
        arrangeFlowers();
        syncAnimation();
      })
      .catch((error) => {
        console.error("Error loading publication flowers:", error);
        garden.textContent = "The publication map is temporarily unavailable. All publication links are listed above.";
        picker.replaceChildren(new Option("Map unavailable", ""));
        detail.textContent = "You can browse every publication in the list above.";
      });
  })();
</script>
