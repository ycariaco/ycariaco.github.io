---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Interactive visualization of my research publications. **Drag nodes**, **zoom**, and **hover** for
details. Node size reflects publication year, and edges connect co-authored papers.

<div
  id="cytoscape"
  style="width: 100%; height: 800px; border: 1px solid #ddd; margin: 20px 0;"
></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.28.1/cytoscape.min.js"></script>

<script>
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

      // Create publication nodes
      data.forEach((pub) => {
        const title =
          pub.title.length > 50
            ? pub.title.substring(0, 50) + "..."
            : pub.title;
        nodes.push({
          data: {
            id: pub.id,
            label: title,
            fullTitle: pub.title,
            year: pub.year,
            journal: pub.journal,
            doi: pub.doi,
          },
        });
        years.add(pub.year);
      });

      // Create year nodes (for grouping)
      Array.from(years)
        .sort((a, b) => b - a)
        .forEach((year) => {
          nodes.push({
            data: {
              id: `year-${year}`,
              label: year.toString(),
            },
          });
        });

      // Create edges: publications to years
      data.forEach((pub) => {
        edges.push({
          data: {
            source: pub.id,
            target: `year-${pub.year}`,
          },
        });
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
              "background-color": "#3b82f6",
              label: "data(label)",
              "text-opacity": 0.9,
              "font-size": 11,
              "text-valign": "center",
              "text-halign": "center",
              width: 40,
              height: 40,
              "border-width": 2,
              "border-color": "#1e40af",
            },
          },
          {
            selector: 'node[id ^= "year"]',
            style: {
              "background-color": "#ef4444",
              width: 60,
              height: 60,
              "font-size": 14,
              "font-weight": "bold",
              "border-width": 3,
              "border-color": "#7f1d1d",
            },
          },
          {
            selector: "edge",
            style: {
              "line-color": "#cbd5e1",
              width: "mapData(weight, 1, 5, 1, 4)",
              opacity: 0.6,
              "curve-style": "bezier",
            },
          },
          {
            selector: "node:hover",
            style: {
              "background-color": "#1e40af",
              "border-width": 3,
            },
          },
        ],
        layout: {
          name: "cose",
          directed: false,
          animate: true,
          animationDuration: 500,
          avoidOverlap: true,
          nodeSpacing: 10,
          gravity: 1,
          cooling: 0.99,
          coolingFactor: 0.999,
          randomize: true,
        },
      });

      // Add hover tooltip
      cy.on("mouseover", "node", function (evt) {
        const node = evt.target;
        if (node.id().startsWith("year")) return;
        const data = node.data();
        console.log(data);
      });
    })
    .catch((err) => console.error("Error loading publications:", err));
</script>
