---
layout: page
title: Research Hub
permalink: /research/
nav: true
nav_order: 3
---

<div id="pub-network" style="height:700px;"></div>

<script>
fetch("/assets/json/publications.json")
  .then(response => response.json())
  .then(data => {

    var chart = echarts.init(document.getElementById('pub-network'));

    var nodes = data.map(p => ({
      id: p.id,
      name: p.title,
      value: p.year,
      symbolSize: 12
    }));

    var links = [];
    // Simple year-based grouping for now
    data.forEach(p => {
      links.push({
        source: p.year,
        target: p.id
      });
    });

    // Add year nodes
    var years = [...new Set(data.map(p => p.year))];
    years.forEach(y => {
      nodes.push({
        id: y,
        name: y,
        symbolSize: 40
      });
    });

    var option = {
      tooltip: { trigger: 'item' },
      series: [{
        type: 'graph',
        layout: 'force',
        roam: true,
        label: { show: false },
        force: { repulsion: 120 },
        data: nodes,
        links: links
      }]
    };

    chart.setOption(option);
  });
</script>
