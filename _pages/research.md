---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Interactive visualization grouped by **research theme**. **Drag nodes** to move them (they repel and attract based on connections), **zoom**, and **click** to view details.

<div
  id="cytoscape"
  style="width: 100%; height: 900px; border: 1px solid #ddd; margin: 20px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);"
></div>

<div
  id="info-panel"
  style="padding: 20px; background: #f8f9fa; border-radius: 8px; margin-top: 20px; display: none; border-left: 4px solid #3b82f6;"
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
      const themeMap = {};

      // Create publication nodes
      data.forEach((pub) => {
        const title =
          pub.title.length > 55
            ? pub.title.substring(0, 55) + "..."
            : pub.title;
        const mainTheme = extractMainTheme(pub.tags);
        const color = getColorForTags(pub.tags);

        if (!themeMap[mainTheme]) themeMap[mainTheme] = 0;
        themeMap[mainTheme]++;

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
          style: {
            "background-color": color,
          },
        });
      });

      // Create edges between co-authored papers (stronger weight)
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
                weight: commonAuthors.length * 2,
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
      console.log("Themes:", themeMap);

      const cy = cytoscape({
        container: document.getElementById("cytoscape"),
        elements: [...nodes, ...edges],
        style: [
          {
            selector: "node",
            style: {
              label: "data(label)",
              "text-opacity": 0.95,
              "font-size": 10,
              "text-valign": "center",
              "text-halign": "center",
              width: 50,
              height: 50,
              "border-width": 2,
              "border-color": "#1a1a1a",
              "background-opacity": 0.9,
              cursor: "grab",
              "overlay-padding": 5,
            },
          },
          {
            selector: "node:active",
            style: {
              cursor: "grabbing",
            },
          },
          {
            selector: "edge",
            style: {
              width: 2,
              opacity: 0.4,
              "curve-style": "bezier",
              "line-color": "#cbd5e1",
            },
          },
          {
            selector: 'edge[type = "theme-link"]',
            style: {
              "line-color": "#f59e0b",
              "line-style": "dashed",
              opacity: 0.35,
              width: 1.5,
            },
          },
          {
            selector: 'edge[type = "co-author"]',
            style: {
              "line-color": "#06b6d4",
              opacity: 0.55,
              width: 2.5,
            },
          },
          {
            selector: "node:hover",
            style: {
              "border-width": 3,
              "border-color": "#fbbf24",
              "background-opacity": 1,
            },
          },
          {
            selector: "node:selected",
            style: {
              "border-width": 4,
              "border-color": "#fbbf24",
              "background-opacity": 1,
              "box-shadow":
                "0 0 30px 3px rgba(251, 191, 36, 0.7)",
            },
          },
        ],
        layout: {
          name: "cose",
          directed: false,
          animate: true,
          animationDuration: 500,
          avoidOverlap: true,
          avoidOverlapPadding: 10,
          nodeSpacing: 5,
          refresh: 20,
          fit: true,
          padding: 30,
          randomize: true,
          componentSpacing: 100,
          nodeRepulsion: (node) => 200000,
          idealEdgeLength: (edge) => {
            if (edge.data("type") === "co-author") return 80;
            if (edge.data("type") === "theme-link") return 120;
            return 150;
          },
          edgeElasticity: (edge) => {
            if (edge.data("type") === "co-author") return 0.45;
            return 0.1;
          },
          nestingFactor: 1.2,
          gravity: 0.25,
          numIter: 2500,
          initialTemp: 200,
          coolingFactor: 0.95,
          minTemp: 1.0,
        },
      });

      // Enable dragging to repel/attract
      cy.on("grabon", "node", function (evt) {
        evt.target.unselectify();
      });

      cy.on("graboff", "node", function (evt) {
        evt.target.selectify();
      });

      // Click to show info and open link
      cy.on("tap", "node", function (evt) {
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

        // Update info panel
        const infoPanel = document.getElementById("info-panel");
        document.getElementById("info-title").textContent =
          data.fullTitle;
        document.getElementById("info-details").innerHTML = `
          <strong>Theme:</strong> <span style="color: ${getColorForTags(
            data.tags
          )}">●</span> ${data.theme}<br>
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
      });

      // Hover tooltip
      cy.on("mouseover", "node", function (evt) {
        const node = evt.target;
        const data = node.data();
        node.style(
          "label",
          data.fullTitle.substring(0, 50) + "..."
        );
      });

      cy.on("mouseout", "node", function (evt) {
        const node = evt.target;
        node.style("label", "data(label)");
      });

      // Fit on load
      setTimeout(() => {
        cy.fit();
      }, 1000);
    })
    .catch((err) => console.error("Error loading publications:", err));
</script>
