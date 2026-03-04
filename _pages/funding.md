---
layout: page
permalink: /funding/
title: Funding
nav: true
nav_order: 5
---

<div class="funders-grid">
  {% for f in site.data.funders %}
    <a class="funder-card" href="{{ f.url }}" target="_blank" rel="noopener">
      <img src="{{ f.logo | relative_url }}" alt="{{ f.name }} logo" loading="lazy">
    </a>
  {% endfor %}
</div>

<style>
  .funders-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 18px;
    margin-top: 16px;
  }
  .funder-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 16px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
  }
  .funder-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.12);
  }
  .funder-card img {
    max-height: 70px;
    max-width: 100%;
    width: auto;
    height: auto;
  }
</style>
