---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Interactive visualization of my research publications. **Drag nodes**, **zoom**, and **hover** for details. Articles are connected by **shared authors** and **research themes**. **Click** any article to visit PubMed or DOI.

<div
  id="cytoscape"
  style="width: 100%; height: 900px; border: 1px solid #ddd; margin: 20px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);"
></div>

<div
  id="info-panel"
  style="padding: 20px; background: #f8f9fa; border-radius: 8px; margin-top: 20px; display: none;"
>
  <h4 id="info-title"></h4>
  <p id="info-details"></p>
  <a
    id="info-link"
    target="_blank"
    rel="noopener noreferrer"
    style="display: inline-block; margin-top: 10px; padding: 8px 16px; background: #3b82f6; color: white; border-radius: 4px; text-decoration: none;"
  >
    View on PubMed / DOI
  </a>
</div>

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

  fetch("/assets/json/publications.json")
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load publications.json");
      return response.json();
    })
    .then((data) => {
      console.log("Loaded publications:", data.length);

      const nodes = [];
      const edges = [];
      const years = new Set();
      const themeMap = {}; // Track themes for coloring

      // Create publication nodes
      data.forEach((pub) => {
        const title =
          pub.title.length > 60
            ? pub.title.substring(0, 60) + "..."
            : pub.title;
        const mainTheme = extractMainTheme(pub.tags);
        const color = getColorForTags(pub.tags);

        if (!themeMap[mainTheme]) themeMap[mainTheme] = [];
        themeMap[mainTheme].push(pub.id);

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
        years.add(pub.year);
      });

      // Create year nodes
      Array.from(years)
        .sort((a, b) => b - a)
        .forEach((year) => {
          nodes.push({
            data: {
              id: `year-${year}`,
              label: year.toString(),
            },
            classes: "year",
            style: {
              "background-color": "#64748b",
            },
          });
        });

      // Create edges: publications to years
      data.forEach((pub) => {
        edges.push({
          data: {
            source: pub.id,
            target: `year-${pub.year}`,
            type: "year-link",
          },
        });
      });

      // Create edges between co-authored papers
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

      // Create edges between papers sharing research themes
      for (let i = 0; i < data.length; i++) {
        for (let j = i + 1; j < data.length; j++) {
          const pubA = data[i];
          const pubB = data[j];

          if (!Array.isArray(pubA.tags) || !Array.isArray(pubB.tags)) {
            continue;
          }

          const commonTags = pubA.tags.filter((tag) => pubB.tags.includes(tag));

          if (
            commonTags.length > 0 &&
            !edges.some(
              (e) =>
                (e.data.source === pubA.id &&
                  e.data.target === pubB.id) ||
                (e.data.source === pubB.id &&
                  e.data.target === pubA.id)
            )
          ) {
            edges.push({
              data: {
                source: pubA.id,
                target: pubB.id,
                weight: commonTags.length,
                type: "theme-link",
              },
            });
          }
        }
      }

      // Degree (used for spacing + sizing)
      const degreeMap = {};
      edges.forEach((edge) => {
        if (edge.data.type === "year-link") return;
        degreeMap[edge.data.source] = (degreeMap[edge.data.source] || 0) + 1;
        degreeMap[edge.data.target] = (degreeMap[edge.data.target] || 0) + 1;
      });

      nodes.forEach((node) => {
        if (node.classes !== "pub") return;
        node.data.degree = degreeMap[node.data.id] || 0;
      });

      console.log("Nodes:", nodes.length, "Edges:", edges.length);

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
              width: "mapData(degree, 0, 8, 18, 34)",
              height: "mapData(degree, 0, 8, 18, 34)",
              "border-width": 2,
              "border-color": "#000",
              "background-opacity": 0.85,
              cursor: "pointer",
            },
          },
          {
            selector: "node.year",
            style: {
              label: "data(label)",
              width: 60,
              height: 60,
              "font-size": 13,
              "font-weight": "bold",
              "border-width": 2,
              "border-color": "#1e293b",
              "background-opacity": 0.9,
              cursor: "default",
            },
          },
          {
            selector: "node.pub:hover, node.pub:selected",
            style: {
              label: "data(label)",
              "text-opacity": 1,
              "text-wrap": "wrap",
              "text-max-width": 120,
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
              opacity: 0.25,
              "curve-style": "bezier",
              "line-color": "#cbd5e1",
            },
          },
          {
            selector: 'edge[type = "theme-link"]',
            style: {
              "line-color": "#f59e0b",
              "line-style": "dashed",
              opacity: 0.25,
            },
          },
          {
            selector: 'edge[type = "co-author"]',
            style: {
              "line-color": "#06b6d4",
              opacity: 0.45,
            },
          },
          {
            selector: 'edge[type = "year-link"]',
            style: {
              "line-color": "#94a3b8",
              opacity: 0.15,
              width: 1,
            },
          },
          {
            selector: "node:selected",
            style: {
              "border-width": 4,
              "border-color": "#fbbf24",
              "background-opacity": 1,
            },
          },
        ],
        layout: {
          name: "cose",
          directed: false,
          animate: true,
          animationDuration: 800,
          avoidOverlap: true,
          nodeOverlap: 8,
          nodeSpacing: 30,
          nodeRepulsion: (node) => {
            if (node.hasClass("year")) return 9000;
            const degree = node.data("degree") || 0;
            return 6000 + degree * 300;
          },
          idealEdgeLength: (edge) => {
            const type = edge.data("type");
            if (type === "co-author") return 120;
            if (type === "theme-link") return 220;
            if (type === "year-link") return 260;
            return 180;
          },
          edgeElasticity: 0.1,
          gravity: 0.2,
          numIter: 2500,
          initialTemp: 200,
          coolingFactor: 0.99,
          randomize: true,
        },
      });

      // Click to open PubMed/DOI
      cy.on("tap", "node", function (evt) {
        const node = evt.target;
        if (node.hasClass("year")) return;

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

        // Update info panel
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
