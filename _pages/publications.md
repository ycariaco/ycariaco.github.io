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
  <p id="publication-garden-help" class="publication-garden-help">Organ icons orbit each year in matching colors. Hover to explore or click an icon to open the paper. A small P badge marks preprints.</p>
  <div id="cytoscape" role="img" aria-label="Publication organ icons orbiting each year" aria-describedby="publication-garden-help"></div>
  <div id="publication-organ-legend" class="publication-organ-legend" aria-label="Publication icon guide"></div>
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
  .publication-organ-legend { display: flex; flex-wrap: wrap; gap: 8px 20px; margin-top: 14px; font-size: .8rem; }
  .publication-organ-legend span { display: inline-flex; align-items: center; gap: 6px; }
  .publication-organ-legend img { width: 28px; height: 28px; }
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
  // Returns an encoded SVG data URI for Cytoscape's background-image.
  // The caller supplies the year color; preprints receive a small vector P badge.
  function publicationOrganSvg(type, color, preprint = false) {
    const fill = /^#[0-9a-f]{6}$/i.test(color) ? color : "#e9b6cc";
    const outline = `#${[1, 3, 5]
      .map((i) => Math.round(parseInt(fill.slice(i, i + 2), 16) * 0.57).toString(16).padStart(2, "0"))
      .join("")}`;
    const organs = {
      placenta: `
        <path d="M32 22C45 20 56 28 56 40C57 52 46 60 33 60C19 61 8 52 8 40C8 29 18 22 32 22Z"/>
        <g fill="none" stroke-width="1.9">
          <path d="M32 33L31 43L24 53M31 43L40 54M32 35L21 32L15 35M21 32L19 27M31 40L18 44L14 41M18 44L18 50M33 35L44 30L49 33M44 30L44 26M33 41L45 45L51 41M45 45L48 51M31 47L33 56"/>
        </g>
        <path d="M32 34C29 26 29 20 35 15C40 11 46 15 48 11C51 6 44 3 40 6" fill="none" stroke-width="6.2"/>
        <path d="M32 34C29 26 29 20 35 15C40 11 46 15 48 11C51 6 44 3 40 6" fill="none" stroke="${fill}" stroke-width="3.1"/>
        <path d="M14 34C17 28 22 27 26 27" class="shine"/>`,
      brain: `
        <path d="M31 12C25 7 17 10 14 16C7 17 5 24 9 30C4 36 7 44 14 46C15 54 25 58 32 53C39 58 49 54 51 47C59 44 61 36 55 30C58 23 54 16 48 16C45 8 37 7 31 12Z"/>
        <g fill="none" stroke-width="1.9">
          <path d="M31 13C28 20 34 25 31 32C28 39 34 47 32 53M14 17C19 17 22 20 20 25M10 30C16 27 21 29 22 34M14 46C13 40 18 37 23 40M25 14C22 19 25 22 28 23M20 49C24 47 25 43 24 40M48 17C42 16 39 20 41 25M54 30C49 27 43 29 42 34M51 46C51 40 46 37 41 40M37 14C41 18 37 22 35 23M44 49C39 47 38 43 40 40"/>
        </g>
        <path d="M12 24C12 21 14 20 16 20M35 14C38 12 42 13 43 15" class="shine"/>`,
      intestine: `
        <path d="M16 56C9 56 7 52 7 45V22C7 13 12 8 20 8H43C52 8 57 13 57 22V45C57 52 53 56 46 56H37V48H46C48 48 49 46 49 43V23C49 19 47 17 43 17H21C17 17 15 19 15 23V45C15 48 17 49 20 49H24V56Z"/>
        <path d="M23 24H39C44 24 44 31 39 31H25C20 31 20 38 25 38H39C44 38 44 45 39 45H31V56" fill="none" stroke-width="6.7"/>
        <path d="M23 24H39C44 24 44 31 39 31H25C20 31 20 38 25 38H39C44 38 44 45 39 45H31V56" fill="none" stroke="${fill}" stroke-width="3.1"/>
        <g fill="none" stroke-width="1.5"><path d="M9 23H14M9 34H14M10 45H14M20 10V15M31 10V15M42 10V15M51 23H55M51 34H55M50 45H54"/></g>
        <path d="M12 18C13 14 16 13 19 13" class="shine"/>`,
      liver: `
        <path d="M7 20C20 11 37 10 52 15C58 17 59 23 54 29L41 42C34 47 24 47 17 52C12 56 7 52 6 45C4 37 3 27 7 20Z"/>
        <path d="M35 14C35 23 30 27 28 36C26 42 22 46 17 49M34 24C40 24 47 23 54 21" fill="none" stroke-width="1.9"/>
        <path d="M35 35C38 36 39 40 36 44C33 47 30 43 31 40Z" fill="${outline}" opacity=".25" stroke-width="1.5"/>
        <path d="M11 24C16 20 22 18 27 18" class="shine"/>`,
      kidney: `
        <path d="M34 8C21 5 11 14 9 28C6 42 13 54 24 56C32 58 39 53 40 46C41 41 38 38 33 36C29 34 29 29 33 27C38 25 42 24 42 18C42 13 39 9 34 8Z"/>
        <path d="M31 18C22 17 17 25 17 33C17 42 22 47 29 47M29 27L24 25M29 35L22 37" fill="none" stroke-width="1.8"/>
        <path d="M35 31C42 31 48 35 48 44V56" fill="none" stroke-width="5.3"/>
        <path d="M35 31C42 31 48 35 48 44V56" fill="none" stroke="${fill}" stroke-width="2.3"/>
        <path d="M15 23C18 16 23 13 28 13" class="shine"/>`,
      uterus: `
        <path d="M26 25C22 16 14 14 9 18C6 20 6 25 9 27M38 25C42 16 50 14 55 18C58 20 58 25 55 27" fill="none" stroke-width="6.4"/>
        <path d="M26 25C22 16 14 14 9 18C6 20 6 25 9 27M38 25C42 16 50 14 55 18C58 20 58 25 55 27" fill="none" stroke="${fill}" stroke-width="3.3"/>
        <path d="M22 25C22 18 42 18 42 25C44 34 37 41 36 48V56H28V48C27 41 20 34 22 25Z"/>
        <path d="M26 28C28 25 36 25 38 28L32 39V50" fill="none" stroke-width="1.9"/>
        <path d="M13 27C17 28 18 33 14 36C10 39 6 35 7 31C8 28 10 26 13 27ZM51 27C47 28 46 33 50 36C54 39 58 35 57 31C56 28 54 26 51 27Z"/>
        <path d="M26 23C29 21 34 21 37 23" class="shine"/>`,
      cell: `
        <path d="M29 8C36 6 39 11 45 13C53 15 57 23 55 30C54 36 59 41 52 48C46 54 39 52 33 56C25 60 20 53 14 49C8 45 7 37 9 30C11 23 8 18 15 13C19 10 24 10 29 8Z"/>
        <path d="M35 23C42 25 44 33 40 38C36 43 27 43 23 37C19 31 23 24 28 23C30 22 33 22 35 23Z" fill="${outline}" fill-opacity=".18" stroke-width="1.8"/>
        <path d="M29 29C32 27 36 29 35 32C34 35 30 34 29 32Z" fill="${outline}" fill-opacity=".35" stroke="none"/>
        <path d="M17 25C20 22 21 25 19 27M44 43C41 46 44 48 47 45M20 43L23 45M43 19L45 22" fill="none" stroke-width="2.2"/>
        <path d="M15 19C18 15 22 15 25 14" class="shine"/>`,
    };
    const badge = preprint
      ? `<rect x="50" y="3" width="13" height="15" rx="4" fill="${outline}" stroke="#fff" stroke-width="1"/>
         <path d="M54 14V7H57C60 7 60 11 57 11H54" fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>`
      : "";
    const svg = `<?xml version="1.0" encoding="UTF-8"?>
      <!DOCTYPE svg>
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">
        <style>.shine{fill:none;stroke:#fff;stroke-width:2.8;opacity:.65}</style>

        <g fill="${fill}" stroke="${outline}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
          ${Object.prototype.hasOwnProperty.call(organs, type) ? organs[type] : organs.cell}
        </g>
        ${badge}
      </svg>`;
    return `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;

}

function publicationOrgan(pub) {
// Reviewed topic choices for titles that do not identify one clear organ.
// Keep these separate from automatically refreshed publication records.
const overrides = {
zurub_microplastics_2023: "cell",
cariaco_ccr5_2023: "placenta",
briceno_effects_2022: "cell",
jahan_comparison_2023: "placenta",
cariaco_inhibition_2022: "uterus",
cristina_borges_araujo_beneficial_2021: "intestine",
coutinho_both_2023: "placenta",
"miranda_anti-parasitic_2021": "cell",
nascimento_ethanolic_2022: "cell",
"duran-rodriguez_macrophage_2025": "uterus",
};
const labels = { placenta: "Placenta", uterus: "Uterus / decidua", brain: "Brain", intestine: "Intestine", liver: "Liver", kidney: "Kidney", cell: "Cells / multiple organs" };
const title = String(pub.title || "");
let type = overrides[pub.id];
if (!type) {
if (/placent|trophoblast|preeclampsia|maternal.fetal/i.test(title)) type = "placenta";
else if (/brain|cerebral/i.test(title)) type = "brain";
else if (/intestin|bowel|ileum|colitis/i.test(title)) type = "intestine";
else if (/uter|decidua|endometr/i.test(title)) type = "uterus";
else if (/liver|hepatic/i.test(title)) type = "liver";
else if (/kidney|renal/i.test(title)) type = "kidney";
else type = "cell";
}
return { type, label: labels[type] };
}

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
              data: { id: pub.id, color: flower.color, year: flower.year, icon: publicationOrganSvg(publicationOrgan(pub).type, flower.color, pub.kind === "preprint") },
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
              selector: ".paper",
              style: { shape: "rectangle", width: 44, height: 44, "background-opacity": 0, "border-width": 0, "background-image": "data(icon)", "background-fit": "contain", "background-clip": "none", "background-image-opacity": 1 },
            },
            {
              selector: ".paper.highlighted",
              style: { "underlay-color": "data(color)", "underlay-opacity": .4, "underlay-padding": 5, "underlay-shape": "round-rectangle" },
            },
            {
              selector: "edge",
              style: { width: 2, "line-color": "data(color)", opacity: .8, "curve-style": "straight", "events": "no", "overlay-opacity": 0 },
            },
          ],
        });

        const legend = document.getElementById("publication-organ-legend");
        const organs = new Map(publications.map((pub) => { const organ = publicationOrgan(pub); return [organ.type, organ]; }));
        legend.replaceChildren(...[...organs.values()].map((organ) => {
          const item = document.createElement("span");
          const icon = document.createElement("img");
          icon.src = publicationOrganSvg(organ.type, "#F8BBD0");
          icon.alt = "";
          item.append(icon, organ.label);
          return item;
        }));

        function showPublication(pub) {
          picker.value = pub.id;
          cy.nodes(".highlighted").removeClass("highlighted");
          cy.getElementById(pub.id).addClass("highlighted");
          const title = document.createElement("div");
          title.className = "publication-garden-detail-title";
          title.textContent = pub.title;
          const meta = document.createElement("div");
          meta.className = "publication-garden-detail-meta";
          meta.textContent = [publicationOrgan(pub).label, pub.year, pub.journal, pub.kind === "preprint" ? "Preprint · Not peer reviewed" : "", publicationCitationText(pub)].filter(Boolean).join(" · ");
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
            let radius = 70;
            while (remaining > 0) {
              const count = Math.min(remaining, Math.floor(2 * Math.PI * radius / 52));
              flower.rings.push({ radius, count });
              remaining -= count;
              radius += 52;
            }
          });
          const outerRadius = Math.max(...flowers.map((flower) => flower.rings[flower.rings.length - 1].radius));
          const desiredCell = Math.max(210, (outerRadius + 34) * 2);
          const columns = Math.max(1, Math.min(4, Math.floor(width / desiredCell)));
          cellWidth = width / columns;
          const cellHeight = Math.max(190, Math.min(outerRadius, cellWidth / 2 - 34) * 2 + 68);
          const rows = Math.ceil(flowers.length / columns);
          garden.style.height = `${rows * cellHeight + 24}px`;
          flowers.forEach((flower, index) => {
            const row = Math.floor(index / columns);
            const flowersInRow = Math.min(columns, flowers.length - row * columns);
            const rowOffset = (width - flowersInRow * cellWidth) / 2;
            flower.center = { x: rowOffset + (index % columns + .5) * cellWidth, y: 12 + (row + .5) * cellHeight };
            const radius = flower.rings[flower.rings.length - 1].radius;
            flower.scale = Math.min(1, Math.max(30, cellWidth / 2 - 34) / radius);
            flower.papers.forEach((pub) => cy.getElementById(pub.id).style({ width: 44 * flower.scale, height: 44 * flower.scale }));
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
        garden.textContent = "The publication map is temporarily unavailable. All publication links are listed below.";
        picker.replaceChildren(new Option("Map unavailable", ""));
        detail.textContent = "You can browse every publication in the list below.";
      });

})();
</script>
