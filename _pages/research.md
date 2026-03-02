---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

## Publications Network

Below is an interactive visualization of my research and publications. The animated
background shows a force-directed network of nodes and edges, while your publication
data (when available) can be integrated with the ECharts overlay below.

<div id="pub-network" style="height: 700px;"></div>

<script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>

<script>
  fetch("/assets/json/publications.json")
    .then((response) => response.json())
    .then((data) => {
      const chart = echarts.init(document.getElementById("pub-network"));

      const nodes = [];
      const links = [];

      data.forEach((p) => {
        nodes.push({
          id: p.id,
          name: p.title,
          value: p.year,
          symbolSize: 12,
        });

        nodes.push({
          id: p.year,
          name: p.year,
          symbolSize: 40,
        });

        links.push({
          source: p.year,
          target: p.id,
        });
      });

      const option = {
        tooltip: { trigger: "item" },
        series: [
          {
            type: "graph",
            layout: "force",
            roam: true,
            label: { show: false },
            force: { repulsion: 120 },
            data: nodes,
            links: links,
          },
        ],
      };

      chart.setOption(option);
    });
</script>
