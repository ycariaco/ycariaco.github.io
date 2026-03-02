---
layout: page
title: Publications
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Interactive visualization of my research publications.

<div id="network" style="width: 100%; height: 800px; border: 1px solid #ddd;"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
<link
  rel="stylesheet"
  href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css"
/>

<script>
  fetch("/assets/json/publications.json")
    .then((response) => response.json())
    .then((data) => {
      const nodes = new vis.DataSet();
      const edges = new vis.DataSet();
      const years = new Set();

      // Add publication nodes
      data.forEach((pub, idx) => {
        nodes.add({
          id: pub.id,
          label: pub.title.substring(0, 30) + "...",
          title: pub.title,
          group: pub.year.toString(),
          shape: "box",
        });
        years.add(pub.year);
      });

      // Add year nodes for grouping
      years.forEach((year) => {
        nodes.add({
          id: `year-${year}`,
          label: year.toString(),
          group: "year",
          shape: "circle",
          color: "#ff6b6b",
          font: { size: 16, bold: true },
        });
      });

      // Connect publications to their year
      data.forEach((pub) => {
        edges.add({
          from: pub.id,
          to: `year-${pub.year}`,
          color: { color: "rgba(200,200,200,0.3)" },
        });
      });

      // Connect co-authored papers
      for (let i = 0; i < data.length; i++) {
        for (let j = i + 1; j < data.length; j++) {
          const pubA = data[i];
          const pubB = data[j];
          const commonAuthors = pubA.authors.filter((a) =>
            pubB.authors.includes(a)
          );
          if (commonAuthors.length > 0) {
            edges.add({
              from: pubA.id,
              to: pubB.id,
              color: { color: "rgba(100,150,255,0.5)" },
              width: commonAuthors.length,
              title: `${commonAuthors.length} common author(s)`,
            });
          }
        }
      }

      const container = document.getElementById("network");
      const data_obj = { nodes: nodes, edges: edges };
      const options = {
        physics: {
          enabled: true,
          stabilization: { iterations: 200 },
        },
        interaction: { hover: true },
      };

      new vis.Network(container, data_obj, options);
    })
    .catch((err) => console.error("Error loading publications:", err));
</script>
