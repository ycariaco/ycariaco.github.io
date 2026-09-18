---
layout: page
permalink: /data-explorer/
title: Data Explorer
description: Explore and visualize research data.
nav: true
nav_order: 8
calendar: false
---

<style>
.container.mt-5 {
  width: 100% !important;
  max-width: none !important;
  padding-right: clamp(16px, 2.5vw, 48px) !important;
  padding-left: clamp(16px, 2.5vw, 48px) !important;
}

.post {
  width: 100% !important;
  max-width: none !important;
  padding: 24px 0 !important;
}

.data-explorer-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 16px;
}

.data-explorer-button {
  display: inline-block;
  padding: 10px 18px;
  color: #ffffff !important;
  font-weight: 600;
  text-decoration: none !important;
  background: var(--global-theme-color);
  border-radius: 8px;
}

.data-explorer-button:hover {
  color: #ffffff !important;
  opacity: 0.88;
}

.data-explorer-frame {
  display: block;
  width: 100%;
  height: calc(100vh - 230px);
  min-height: 850px;
  border: 1px solid var(--global-divider-color);
  border-radius: 16px;
  background: #ffffff;
}

@media (max-width: 768px) {
  .container.mt-5 {
    padding-right: 12px !important;
    padding-left: 12px !important;
  }

  .data-explorer-frame {
    height: 1000px;
    min-height: 1000px;
    border-radius: 10px;
  }
}
</style>

<div class="data-explorer-page">
  <div class="data-explorer-toolbar">
    <a class="data-explorer-button" href="https://cariaco-lab-data-explorer.pages.dev/" target="_blank" rel="noopener noreferrer">Open full-screen version</a>
  </div>

  <iframe class="data-explorer-frame" src="https://cariaco-lab-data-explorer.pages.dev/" title="Cariaco Lab Data Explorer" loading="lazy"></iframe>
</div>
