---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Interactive visualization of my research publications organized by research theme. **Drag nodes**, **zoom**, and **hover** for details. **Click** any article to visit PubMed or DOI.

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
      const themeClusters = {}; // Track nodes by theme

      // Initialize theme clusters
      Object.keys(themeColors).forEach((theme) => {
        themeClusters[theme] = [];
      });

      // Create publication nodes
      data.forEach((pub) => {
        const title =
          pub.title.length > 60
            ? pub.title.substring(0, 60) + "..."
            : pub.title;
        const mainTheme = extractMainTheme(pub.tags);
        const color = getColorForTags(pub.tags);

        if (!themeClusters[mainTheme]) {
          themeClusters[mainTheme] = [];
        }
        themeClusters[mainTheme].push(pub.id);

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
            parent: `cluster-${mainTheme}`,
          },
          style: {
            "background-color": color,
          },
        });
      });

      // Create invisible cluster nodes for spatial organization
      Object.entries(themeClusters).forEach(([theme, pubIds]) => {
        if (pubIds.length > 0) {
          nodes.push({
            data: {
              id: `cluster-${theme}`,
              label: theme,
            },
            style: {
              "background-opacity": 0,
              "border-opacity": 0,
              width: 150,
              height: 150,
            },
            isCluster: true,
          });
        }
      });

      // Create edges between co-authored papers
      for (let i = 0; i < data.length; i++) {
        for (let j = i + 1; j < data.length; j++) {
          const pubA = data[i];
          const pubB = data[j];

          if (
            !Array.isArray(pubA.authors) ||
            !Array.isArray(pubB.authors)
          ) {
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

          if (
            !Array.isArray(pubA.tags) ||
            !Array.isArray(pubB.tags)
          ) {
            continue;
          }

          const commonTags = pubA.tags.filter((tag) =>
            pubB.tags.includes(tag)
          );

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

      console.log("Nodes:", nodes.length, "Edges:", edges.length);

      const cy = cytoscape({
        container: document.getElementById("cytoscape"),
        elements: [...nodes, ...edges],
        style: [
          {
            selector: "node",
            style: {
              label: "data(label)",
              "text-opacity": 0.9,
              "font-size": 11,
              "text-valign": "center",
              "text-halign": "center",
              width: 45,
              height: 45,
              "border-width": 2,
              "border-color": "#000",
              "background-opacity": 0.85,
              cursor: "pointer",
            },
          },
          {
            selector: "edge",
            style: {
              width: "mapData(weight, 1, 5, 2, 5)",
              opacity: 0.5,
              "curve-style": "bezier",
              "line-color": "#cbd5e1",
            },
          },
          {
            selector: 'edge[type = "theme-link"]',
            style: {
              "line-color": "#f59e0b",
              "line-style": "dashed",
              opacity: 0.4,
            },
          },
          {
            selector: 'edge[type = "co-author"]',
            style: {
              "line-color": "#06b6d4",
              opacity: 0.6,
            },
          },
          {
            selector: "node:hover",
            style: {
              "border-width": 3,
              "background-opacity": 1,
              "box-shadow":
                "0 0 20px 2px rgba(59, 130, 246, 0.5)",
            },
          },
          {
            selector: "node:selected",
            style: {
              "border-width": 4,
              "border-color": "#fbbf24",
              "background-opacity": 1,
              "box-shadow":
                "0 0 25px 3px rgba(251, 191, 36, 0.6)",
            },
          },
        ],
        layout: {
          name: "cose-bilkent",
          directed: false,
          animate: true,
          animationDuration: 500,
          avoidOverlap: true,
          nodeSpacing: 20,
          gravity: 0.5,
          gravityRange: 200,
          numIter: 2500,
          tile: true,
          tilingPaddingVertical: 10,
          tilingPaddingHorizontal: 10,
          randomize: false,
        },
      });

      // Click to open PubMed/DOI
      cy.on("tap", "node", function (evt) {
        const node = evt.target;
        if (node.isNode() && !node.isParent()) {
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
          document.getElementById("info-title").textContent =
            data.fullTitle;
          document.getElementById("info-details").innerHTML = `
            <strong>Theme:</strong> ${data.theme}<br>
            <strong>Authors:</strong> ${data.authors.join(
              ", "
            )}<br>
            <strong>Journal:</strong> ${data.journal}<br>
            <strong>Year:</strong> ${data.year}<br>
            <strong>Tags:</strong> ${data.tags.join(", ")}
          `;

          if (pmid) {
            document.getElementById("info-link").href =
              `https://pubmed.ncbi.nlm.nih.gov/${pmid}/`;
            document.getElementById("info-link").textContent =
              "View on PubMed";
          } else if (doi) {
            document.getElementById("info-link").href =
              `https://doi.org/${doi}`;
            document.getElementById("info-link").textContent =
              "View on DOI";
          }

          infoPanel.style.display = "block";
        }
      });

      // Hover tooltip
      cy.on("mouseover", "node", function (evt) {
        const node = evt.target;
        if (node.isNode() && !node.isParent()) {
          const data = node.data();
          node.style(
            "label",
            data.fullTitle.substring(0, 40) + "..."
          );
        }
      });

      cy.on("mouseout", "node", function (evt) {
        const node = evt.target;
        if (node.isNode() && !node.isParent()) {
          node.style("label", "data(label)");
        }
      });
    })
    .catch((err) => console.error("Error loading publications:", err));
</script>
