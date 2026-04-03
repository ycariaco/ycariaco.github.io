---
layout: page
title: Welcome
permalink: /
nav: false
nav_order: 1
---

<style>
.post-header {
  display: none;
}

.post {
  background: transparent;
  border: 0;
  padding: 0;
}

.post article {
  margin: 0;
}

body {
  padding-bottom: 0;
}

footer.fixed-bottom {
  position: static;
}

.container.mt-5 {
  margin-top: 0 !important;
}

.hero-container {
  position: relative;
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  margin-top: 0;
}

.hero-image {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 0;
}

.hero-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  background: rgba(255,255,255,0.78);
  padding: 40px 50px;
  border-radius: 10px;

  text-align: center;
  max-width: 700px;
}

.hero-text p {
  font-size: 26px;
  font-style: italic;
  line-height: 1.6;
}

.hero-text,
.hero-text * {
  color: #111827 !important;
}

  /* Dark mode fix for hero text */
  html[data-theme="dark"] .hero-text,
  body.dark .hero-text {
    color: #111827 !important;
  }

  html[data-theme="dark"] .hero-text p,
  html[data-theme="dark"] .hero-text em,
  body.dark .hero-text p,
  body.dark .hero-text em {
    color: #111827 !important;
  }
</style>

<div class="hero-container">
<div class="welcome-hero">
  <img class="welcome-hero__img" src="/assets/img/placenta_hero.png" alt="">
  <div class="welcome-hero__card">
    <!-- Our vision is to establish the placenta as an<br>
  adaptive sensor of prenatal exposures,<br>
  whose molecular programs can be decoded<br>
  through integrated multi-omics to explain<br>
  <em><strong>—and ultimately improve—</strong></em><br>
  fetal outcomes. -->
  </div>
</div>
