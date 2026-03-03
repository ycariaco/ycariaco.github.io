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

      const pastel = [
        "#F8BBD0",
        "#BBDEFB",
        "#C8E6C9",
        "#FFE0B2",
        "#D1C4E9",
        "#B2EBF2",
        "#FFCDD2",
        "#DCEDC8",
        "#FFF9C4",
        "#E1BEE7",
      ];

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

      const yearsSorted = Array.from(years).sort((a, b) => a - b);
      const yearColor = {};
      yearsSorted.forEach((year, i) => {
        yearColor[year] = pastel[i % pastel.length];
      });

      nodes.forEach((n) => {
        if (!n.data.id.startsWith("year-")) {
          n.data.color = yearColor[n.data.year];
        }
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
        "background-color": "data(color)",
        label: "",
        "text-opacity": 0,
        "font-size": 9,
        "text-valign": "center",
        "text-halign": "center",
        "text-background-color": "rgba(255,255,255,0.9)",
        "text-background-opacity": 1,
        "text-background-padding": 3,
        "text-background-shape": "round-rectangle",
        width: 22,
        height: 22,
        "border-width": 1,
        "border-color": "#94a3b8",
      },
    },
    {
      selector: 'node[id ^= "year"]',
      style: {
        "background-color": "#94a3b8",
        label: "data(label)",
        "text-opacity": 1,
        width: 42,
        height: 42,
        "font-size": 12,
        "font-weight": "bold",
        "border-width": 2,
        "border-color": "#475569",
      },
    },
    {
      selector: "node:hover",
      style: {
        label: "data(label)",
        "text-opacity": 1,
        "border-width": 2,
        "border-color": "#64748b",
      },
    },
    {
      selector: "edge",
      style: {
        "line-color": "#cbd5e1",
        width: "mapData(weight, 1, 5, 1, 3)",
        opacity: 0.5,
        "curve-style": "bezier",
      },
    },
  ],
  layout: {
    name: "cose",
    directed: false,
    animate: true,
    animationDuration: 600,
    avoidOverlap: true,
    nodeSpacing: 40,
    nodeRepulsion: 9000,
    idealEdgeLength: 160,
    edgeElasticity: 0.2,
    gravity: 0.08,
    numIter: 2000,
    randomize: true,
  },
});
      const floatSpeed = 0.08;
const jitter = 0.015;

const floating = cy.nodes().filter((n) => !n.id().startsWith("year-"));

floating.forEach((n) => {
  n.scratch("_v", {
    vx: (Math.random() - 0.5) * floatSpeed,
    vy: (Math.random() - 0.5) * floatSpeed,
  });
});

function floatTick() {
  const w = cy.width();
  const h = cy.height();

  cy.batch(() => {
    floating.forEach((n) => {
      const v = n.scratch("_v");
      v.vx += (Math.random() - 0.5) * jitter;
      v.vy += (Math.random() - 0.5) * jitter;

      let x = n.position("x") + v.vx;
      let y = n.position("y") + v.vy;

      if (x < 0 || x > w) v.vx *= -1;
      if (y < 0 || y > h) v.vy *= -1;

      n.position({ x, y });
    });
  });

  requestAnimationFrame(floatTick);
}

floatTick();
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
