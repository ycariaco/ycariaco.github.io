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

/* Hero wrapper */
.hero-container {
  position: relative;
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  margin-top: 0;
  overflow: hidden;
}

/* Hero image */
.hero-image {
  display: block;
  width: 100%;
  height: 72vh;
  min-height: 420px;
  object-fit: cover;
  border-radius: 0;
}

/* Hero text card (desktop) */
.hero-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255,255,255,0.78);
  padding: 40px 50px;
  border-radius: 12px;
  text-align: center;
  max-width: 700px;
}

.hero-text p {
  font-size: 26px;
  font-style: italic;
  line-height: 1.6;
  margin: 0;
}

.hero-text,
.hero-text * { color: #111827 !important; }

/* Mobile fix: stack text below image */
@media (max-width: 768px) {
  .hero-image {
    height: 48vh;
    min-height: 260px;
  }

  .hero-text {
    position: static;
    transform: none;
    margin: -40px 16px 20px;
    padding: 18px 20px;
    max-width: 100%;
  }

  .hero-text p {
    font-size: 18px;
    line-height: 1.4;
  }
}
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
