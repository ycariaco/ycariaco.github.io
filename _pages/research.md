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

<script>
  // Color palette for research themes
  const themeColors = {
    Preeclampsia: "#ef4444",
    Malaria: "#f97316",
    Toxoplasmosis: "#8b5cf6",
    Pregnancy: "#ec4899",
    Immunity: "#06b6d4",
    "Natural Products": "#22c55e",
    Parasites: "#eab308",
    Metabolism: "#3b82f6",
  };

  function getColorForTags(tags) {
    if (!tags || tags.length === 0) return "#6b7280";
    for (const tag of tags) {
      if (themeColors[tag]) return themeColors[tag];
    }
    return "#9ca3af";
  }

  function extractMainTheme(tags) {
    if (!tags || tags.length === 0) return "Other";
    for (const tag of tags) {
      if (themeColors[tag]) return tag;
    }
    return tags[0];
  }

  function slugifyTheme(theme) {
    return theme
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/(^-|-$)/g, "");
  }

  fetch("{{ '/assets/json/publications.json' | relative_url }}")
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load publications.json");
      return response.json();
    })
    .then((data) => {
      const nodes = [];
      const edges = [];
      const themes = new Set();
      const themeIdMap = {};

      // Publication nodes
      data.forEach((pub) => {
        const title =
          pub.title.length > 60
            ? pub.title.substring(0, 60) + "..."
            : pub.title;
        const mainTheme = extractMainTheme(pub.tags);
        const color = getColorForTags(pub.tags);

        themes.add(mainTheme);

        nodes.push({
          data: {
            id: pub.id,
            label: title,
            fullTitle: pub.title,
            year: pub.year,
            journal: pub.journal,
            doi: pub.doi,
            pmid: pub.pmid,
            authors: pub.authors || [],
            tags: pub.tags || [],
            theme: mainTheme,
          },
          classes: "pub",
          style: {
            "background-color": color,
          },
        });
      });

      // Theme hub nodes (cluster anchors)
      Array.from(themes).forEach((theme, index) => {
        const themeId = `theme-${slugifyTheme(theme) || index}`;
        themeIdMap[theme] = themeId;

        nodes.push({
          data: {
            id: themeId,
            label: theme,
            theme,
          },
          classes: "theme",
          style: {
            "background-color": themeColors[theme] || "#9ca3af",
          },
        });
      });

      // Theme edges: pub -> theme hub
      data.forEach((pub) => {
        const mainTheme = extractMainTheme(pub.tags);
        edges.push({
          data: {
            source: pub.id,
            target: themeIdMap[mainTheme],
            type: "theme-link",
          },
        });
      });

      // Co-author edges
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

      // Degree (co-author only)
      const degreeMap = {};
      edges.forEach((edge) => {
        if (edge.data.type !== "co-author") return;
        degreeMap[edge.data.source] = (degreeMap[edge.data.source] || 0) + 1;
        degreeMap[edge.data.target] = (degreeMap[edge.data.target] || 0) + 1;
      });

      nodes.forEach((node) => {
        if (node.classes !== "pub") return;
        node.data.degree = degreeMap[node.data.id] || 0;
      });

      const cy = cytoscape({
        container: document.getElementById("cytoscape"),
        elements: [...nodes, ...edges],
        style: [
          {
            selector: "node.pub",
            style: {
              label: "",
              "text-opacity": 0,
              "font-size": 10,
              "text-valign": "center",
              "text-halign": "center",
              width: "mapData(degree, 0, 8, 20, 36)",
              height: "mapData(degree, 0, 8, 20, 36)",
              "border-width": 2,
              "border-color": "#0f172a",
              "background-opacity": 0.85,
              cursor: "pointer",
            },
          },
          {
            selector: "node.theme",
            style: {
              label: "data(label)",
              "font-size": 13,
              "font-weight": "bold",
              "text-wrap": "wrap",
              "text-max-width": 120,
              "text-valign": "center",
              "text-halign": "center",
              width: 70,
              height: 70,
              "border-width": 2,
              "border-color": "#1f2937",
              "background-opacity": 0.95,
              cursor: "default",
            },
          },
          {
            selector: "node.pub:hover, node.pub:selected",
            style: {
              label: "data(label)",
              "text-opacity": 1,
              "text-wrap": "wrap",
              "text-max-width": 130,
              "text-background-color": "#ffffff",
              "text-background-opacity": 0.9,
              "text-background-padding": 4,
              "text-background-shape": "round-rectangle",
              "border-width": 3,
              "border-color": "#fbbf24",
            },
          },
          {
            selector: "edge",
            style: {
              width: "mapData(weight, 1, 5, 1, 3)",
              opacity: 0.3,
              "curve-style": "bezier",
              "line-color": "#cbd5e1",
            },
          },
          {
            selector: 'edge[type = "theme-link"]',
            style: {
              "line-color": "#94a3b8",
              "line-style": "dashed",
              opacity: 0.25,
              width: 1,
            },
          },
          {
            selector: 'edge[type = "co-author"]',
            style: {
              "line-color": "#06b6d4",
              opacity: 0.5,
            },
          },
        ],
        layout: {
          name: "cose",
          directed: false,
          animate: true,
          animationDuration: 900,
          avoidOverlap: true,
          nodeOverlap: 6,
          nodeSpacing: 35,
          nodeDimensionsIncludeLabels: true,
          nodeRepulsion: (node) => {
            if (node.hasClass("theme")) return 14000;
            const degree = node.data("degree") || 0;
            return 6500 + degree * 350;
          },
          idealEdgeLength: (edge) => {
            const type = edge.data("type");
            if (type === "co-author") return 140;
            if (type === "theme-link") return 260;
            return 180;
          },
          edgeElasticity: 0.1,
          gravity: 0.08,
          numIter: 3000,
          initialTemp: 200,
          coolingFactor: 0.99,
          randomize: true,
          fit: true,
          padding: 50,
        },
      });

      // Click to open PubMed/DOI
      cy.on("tap", "node.pub", function (evt) {
        const node = evt.target;
        const data = node.data();
        const pmid = data.pmid || "";
        const doi = data.doi || "";

        let url = "";
        if (pmid) {
          url = `https://pubmed.ncbi.nlm.nih.gov/${pmid}/`;
        } else if (doi) {
          url = `https://doi.org/${doi}`;
        }

        if (url) {
          window.open(url, "_blank");
        }

        const infoPanel = document.getElementById("info-panel");
        document.getElementById("info-title").textContent = data.fullTitle;
        document.getElementById("info-details").innerHTML = `
          <strong>Authors:</strong> ${data.authors.join(", ")}<br>
          <strong>Journal:</strong> ${data.journal}<br>
          <strong>Year:</strong> ${data.year}<br>
          <strong>Tags:</strong> ${data.tags.join(", ")}
        `;

        if (pmid) {
          document.getElementById("info-link").href =
            `https://pubmed.ncbi.nlm.nih.gov/${pmid}/`;
          document.getElementById("info-link").textContent = "View on PubMed";
        } else if (doi) {
          document.getElementById("info-link").href = `https://doi.org/${doi}`;
          document.getElementById("info-link").textContent = "View on DOI";
        }

        infoPanel.style.display = "block";
      });

      // Hover tooltip (pub nodes only)
      cy.on("mouseover", "node.pub", function (evt) {
        const node = evt.target;
        const data = node.data();
        const label =
          data.fullTitle.length > 70
            ? data.fullTitle.substring(0, 70) + "..."
            : data.fullTitle;
        node.style("label", label);
      });

      cy.on("mouseout", "node.pub", function (evt) {
        const node = evt.target;
        node.style("label", "");
      });
    })
    .catch((err) => console.error("Error loading publications:", err));
</script>
