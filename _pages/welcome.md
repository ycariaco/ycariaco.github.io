---
layout: page
title: Welcome
permalink: /
nav: false
nav_order: 1
---

<style>
.post-header { display: none; }
.post { background: transparent; border: 0; padding: 0; }
.post article { margin: 0; }

body { padding-bottom: 0; }
footer.fixed-bottom { position: static; }
.container.mt-5 { margin-top: 0 !important; }

.hero-container {
  position: relative;
  width: 100vw;
  height: 100vh;
  min-height: 600px;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  overflow: hidden;
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: min(720px, 88vw);
  background: rgba(255,255,255,0.78);
  padding: clamp(18px, 3vw, 40px);
  border-radius: 12px;
  text-align: center;
}

.hero-text p {
  font-size: clamp(16px, 2.1vw, 26px);
  font-style: italic;
  line-height: 1.5;
  margin: 0;
}

.hero-text, .hero-text * { color: #111827 !important; }
</style>

<div class="hero-container">
  <img class="hero-image" src="/assets/img/placenta_hero.png" alt="Placenta image">
  <div class="hero-text">
    <p>
      Our vision is to establish the placenta as an<br>
      adaptive sensor of prenatal exposures,<br>
      whose molecular programs can be decoded<br>
      through integrated multi‑omics to explain<br>
      <em><strong>—and ultimately improve—</strong></em><br>
      fetal outcomes.
    </p>
  </div>
</div>
