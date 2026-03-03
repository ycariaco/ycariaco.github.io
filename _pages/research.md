---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Interactive visualization grouped by **research theme**. **Drag nodes** around—they'll push and pull based on connections. **Zoom** and **hover** to read titles, **click** a node to view details and open PubMed/DOI.

<div id="cytoscape"></div>

<div id="info-panel">
  <h4 id="info-title"></h4>
  <p id="info-details"></p>
  <a id="info-link" target="_blank" rel="noopener noreferrer">View on PubMed / DOI</a>
</div>

<style>
  #cytoscape {
    width: 100%;
    height: 900px;
    border: 1px solid #e2e8f0;
    margin: 20px 0;
    background: radial-gradient(circle at 10% 20%, #f8fafc 0%, #e2e8f0 40%, #cbd5e1 100%);
    border-radius: 12px;
  }

  #info-panel {
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    margin-top: 20px;
    display: none;
    border-left: 4px solid #3b82f6;
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.08);
  }

  #info-panel h4 {
    margin-top: 0;
  }

  #info-link {
    display: inline-block;
    margin-top: 10px;
    padding: 8px 16px;
    background: #3b82f6;
    color: white;
    border-radius: 6px;
    text-decoration: none;
  }
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>
<script src="https://unpkg.com/webcola/WebCola/cola.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape.js-cola/2.3.0/cytoscape-cola.min.js"></script>

<script>
  const themeColors = {
    Preeclampsia: "#ef4444",
    Malaria: "#f97316",
    Toxoplasmosis: "#8b5cf6",
    Pregnancy: "#ec4899",
    Immunity: "#06b6d4",
    "Natural Products": "#22c55e",
    Parasites: "#eab308",
    Metabolism: "#3b82f6",
    Other: "#64748b",
  };

  function getColorForTags(tags) {
    if (!tags || tags.length === 0) return themeColors.Other;
    for (const tag of tags) {
      if (themeColors[tag]) return themeColors[tag];
    }
    return themeColors.Other;
  }

  function extractMainTheme(tags) {
    if (!tags || tags.length === 0) return "Other";
    for (const tag of tags) {
      if (themeColors[tag]) return tag;
    }
    return "Other";
  }

  function slugify(value) {
    return value
      .toLowerCase()
      .trim()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");
  }

  fetch("/assets/json/publications.json")
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load publications.json");
      return response.json();
    })
    .then((data) => {
      const container = document.getElementById("cytoscape");
      const width = container.clientWidth || 1200;
      const height = container.clientHeight || 900;

      const nodes = [];
      const edges = [];
      const themesInData = new Set();

      data.forEach((pub) => {
        const label =
          pub.title.length > 45 ? pub.title.substring(0, 45) + "…" : pub.title;
        const mainTheme = extractMainTheme(pub.tags);
        const color = getColorForTags(pub.tags);

        themesInData.add(mainTheme);

        nodes.push({
          data: {
            id: pub.id,
            label,
            fullTitle: pub.title,
            year: pub.year,
            journal: pub.journal,
            doi: pub.doi,
            pmid: pub.pmid,
            authors: pub.authors || [],
            tags: pub.tags || [],
            theme: mainTheme,
            color,
          },
          classes: "pub",
        });
      });

      const themes = Array.from(themesInData);
      const themeIdMap = {};

      themes.forEach((theme) => {
        const themeId = `theme-${slugify(theme)}`;
        themeIdMap[theme] = themeId;

        nodes.push({
          data: {
            id: themeId,
            label: theme,
            color: themeColors[theme] || themeColors.Other,
          },
          classes: "theme",
          selectable: false,
          grabbable: false,
        });
      });

      const cols = Math.ceil(Math.sqrt(themes.length));
      const rows = Math.ceil(themes.length / cols);
      const padding = 120;
      const gapX = cols > 1 ? (width - padding * 2) / (cols - 1) : 0;
      const gapY = rows > 1 ? (height - padding * 2) / (rows - 1) : 0;

      themes.forEach((theme, index) => {
        const themeId = themeIdMap[theme];
        const col = index % cols;
        const row = Math.floor(index / cols);
        const center = {
          x: padding + gapX * col,
          y: padding + gapY * row,
        };

        const themeNode = nodes.find((n) => n.data.id === themeId);
        themeNode.position = center;
        themeNode.locked = true;

        nodes.forEach((n) => {
          if (n.classes !== "pub") return;
          if (n.data.theme !== theme) return;

          n.position = {
            x: center.x + (Math.random() - 0.5) * 220,
            y: center.y + (Math.random() - 0.5) * 220,
          };

          edges.push({
            data: {
              source: themeId,
              target: n.data.id,
              type: "theme-anchor",
            },
          });
        });
      });

      for (let i = 0; i < data.length; i++) {
        for (let j = i + 1; j < data.length; j++) {
          const pubA = data[i];
          const pubB = data[j];

          if (!Array.isArray(pubA.authors) || !Array.isArray(pubB.authors)) {
            continue;
          }

          const commonAuthors = pubA.authors.filter((a) =>
            pubB.authors.some(
              (b) =>
                a.toLowerCase().includes(b.toLowerCase()) ||
                b.toLowerCase().includes(a.toLowerCase())
            )
          );

          if (commonAuthors.length > 0) {
            edges.push({
              data: {
                source: pubA.id,
                target: pubB.id,
                weight: commonAuthors.length,
                type: "co-author",
              },
            });
          }
        }
      }

      const cy = cytoscape({
        container,
        elements: [...nodes, ...edges],
        style: [
          {
            selector: "node.pub",
            style: {
              label: "",
              width: 22,
              height: 22,
              "background-color": "data(color)",
              "background-opacity": 0.95,
              "border-width": 1.5,
              "border-color": "#0f172a",
              "text-valign": "bottom",
              "text-margin-y": 6,
              "font-size": 9,
              color: "#0f172a",
              "text-opacity": 0.9,
            },
          },
          {
            selector: "node.theme",
            style: {
              label: "data(label)",
              shape: "round-rectangle",
              width: 140,
              height: 60,
              "background-color": "data(color)",
              "background-opacity": 0.12,
              "border-width": 2,
              "border-color": "data(color)",
              "font-size": 12,
              "font-weight": 600,
              color: "#0f172a",
              "text-valign": "center",
              "text-halign": "center",
            },
          },
          {
            selector: "node.pub:hover, node.pub:selected",
            style: {
              label: "data(label)",
              "text-wrap": "wrap",
              "text-max-width": 110,
              "text-background-color": "#ffffff",
              "text-background-opacity": 0.85,
              "text-background-padding": 3,
              "text-background-shape": "round-rectangle",
              "border-width": 3,
              "border-color": "#f59e0b",
            },
          },
          {
            selector: "edge",
            style: {
              width: 1.5,
              opacity: 0.35,
              "curve-style": "bezier",
              "line-color": "#94a3b8",
            },
          },
          {
            selector: 'edge[type = "co-author"]',
            style: {
              width: "mapData(weight, 1, 5, 1.5, 3.5)",
              "line-color": "#0ea5e9",
              opacity: 0.45,
            },
          },
          {
            selector: 'edge[type = "theme-anchor"]',
            style: {
              opacity: 0,
            },
          },
        ],
        layout: {
          name: "cola",
          animate: true,
          animationDuration: 800,
          avoidOverlap: true,
          nodeDimensionsIncludeLabels: false,
          handleDisconnected: true,
          randomize: false,
          nodeSpacing: 20,
          edgeLength: (edge) =>
            edge.data("type") === "theme-anchor" ? 220 : 120,
        },
      });

      cy.one("layoutstop", () => {
        cy.fit(cy.elements(), 60);
      });

      cy.on("tap", "node.pub", function (evt) {
        const node = evt.target;
        const data = node.data();

        const pmid = data.pmid || "";
        const doi = data.doi || "";

        let url = "";
        if (pmid && pmid.length > 0) {
          url = `https://pubmed.ncbi.nlm.nih.gov/${pmid}/`;
        } else if (doi && doi.length > 0) {
          url = `https://doi.org/${doi}`;
        }

        const infoPanel = document.getElementById("info-panel");
        document.getElementById("info-title").textContent = data.fullTitle;
        document.getElementById("info-details").innerHTML = `
          <strong>Theme:</strong> <span style="color: ${getColorForTags(
            data.tags
          )}">●</span> ${data.theme}<br>
          <strong>Authors:</strong> ${data.authors.slice(0, 3).join(", ")}$
          {data.authors.length > 3 ? ` +${data.authors.length - 3} more` : ""}<br>
          <strong>Journal:</strong> ${data.journal}<br>
          <strong>Year:</strong> ${data.year}<br>
          <strong>Tags:</strong> ${data.tags.join(", ")}
        `;

        if (pmid && pmid.length > 0) {
          document.getElementById("info-link").href =
            `https://pubmed.ncbi.nlm.nih.gov/${pmid}/`;
          document.getElementById("info-link").textContent = "View on PubMed";
          document.getElementById("info-link").style.display = "inline-block";
        } else if (doi && doi.length > 0) {
          document.getElementById("info-link").href = `https://doi.org/${doi}`;
          document.getElementById("info-link").textContent = "View on DOI";
          document.getElementById("info-link").style.display = "inline-block";
        } else {
          document.getElementById("info-link").style.display = "none";
        }

        infoPanel.style.display = "block";

        if (url) {
          window.open(url, "_blank");
        }
      });

      cy.on("tap", (evt) => {
        if (evt.target === cy) {
          document.getElementById("info-panel").style.display = "none";
        }
      });
    })
    .catch((err) => console.error("Error loading publications:", err));
</script>
