---
layout: page
title: "The Placenta: A Dynamic Interface of Pregnancy"
permalink: /research/placenta/
nav: false
---

<style>
.placenta-page {
  font-size: 1.3rem;
  line-height: 1.8;
  width: 100%;
  display: flow-root;

  --pl-theme: var(--global-theme-color, #e83e8c);
  --pl-text: var(--global-text-color, #2b2b2b);
  --pl-border: #f2a1c3;
  --pl-soft-bg: rgba(242, 161, 195, 0.16);
  --pl-card-bg: rgba(242, 161, 195, 0.10);
  --pl-box-bg: #fff7fb;
  --pl-figure-bg: #ffe9f2;
}

.placenta-page p {
  margin: 0 0 1.25rem 0;
  color: var(--pl-text);
}

.placenta-page h2 {
  margin-top: 1.9rem;
  margin-bottom: 0.85rem;
  font-size: 1.65rem;
  line-height: 1.35;
  color: var(--pl-theme);
}

.placenta-page .placenta-callout {
  border-left: 5px solid var(--pl-border);
  background: var(--pl-soft-bg);
  color: var(--pl-text);
  padding: 1rem 1.25rem;
  margin: 1.35rem 0;
  border-radius: 0 14px 14px 0;
}

.placenta-page .placenta-callout p {
  margin-bottom: 0;
  color: inherit;
}

.placenta-page .placenta-callout strong {
  color: inherit;
}

.placenta-page .placenta-figure-slot {
  clear: both;
  width: min(94%, 980px);
  margin: 1.6rem auto 1.9rem auto;
  padding: 0;
  box-sizing: border-box;
}

.placenta-page .figure-placeholder {
  min-height: 280px;
  border: 2px dashed var(--pl-border);
  border-radius: 18px;
  background: var(--pl-figure-bg);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 1.4rem;
  color: var(--pl-text);
}

.placenta-page .figure-placeholder strong {
  display: block;
  color: var(--pl-theme);
  font-size: 1.15rem;
  margin-bottom: 0.35rem;
}

.placenta-page .figure-placeholder span {
  font-size: 1rem;
  line-height: 1.45;
  max-width: 760px;
}

.placenta-page .placenta-figure-slot img,
.placenta-page .placenta-figure-img {
  width: 100%;
  height: auto;
  display: block;
  border: 2px solid var(--pl-border);
  border-radius: 16px;
  padding: 6px;
  background: var(--pl-figure-bg);
  box-sizing: border-box;
}

.placenta-page .placenta-figure-slot figcaption {
  display: block;
  width: 100%;
  text-align: center;
  margin-top: 0.45rem;
  font-size: 1rem;
  line-height: 1.4;
  color: var(--pl-text);
}

.placenta-page .question-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
  margin: 1.4rem 0 1.7rem 0;
}

.placenta-page .question-card {
  border: 2px solid var(--pl-border);
  border-radius: 18px;
  background: var(--pl-card-bg);
  color: var(--pl-text);
  padding: 1.1rem 1.2rem;
  box-sizing: border-box;
}

.placenta-page .question-card strong {
  display: block;
  color: var(--pl-theme);
  margin-bottom: 0.35rem;
}

.placenta-page .comparison-table-wrap {
  width: 100%;
  overflow-x: auto;
  margin: 1.4rem 0 1.8rem 0;
}

.placenta-page .comparison-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--pl-text);
}

.placenta-page .comparison-table th,
.placenta-page .comparison-table td {
  border: 1px solid rgba(242, 161, 195, 0.8);
  padding: 0.8rem;
  vertical-align: top;
}

.placenta-page .comparison-table th {
  background: var(--pl-soft-bg);
  color: var(--pl-theme);
  text-align: left;
}

.placenta-page .comparison-table td {
  background: rgba(242, 161, 195, 0.05);
}

.placenta-page .references {
  clear: both;
  margin-top: 2rem;
  padding-top: 0.5rem;
  color: var(--pl-theme) !important;
}

.placenta-page .references strong {
  display: block;
  font-size: 1.2rem;
  margin-bottom: 0.6rem;
  color: var(--pl-theme) !important;
}

.placenta-page .ref-list {
  padding-left: 1.4rem;
  margin-top: 0.75rem;
  color: var(--pl-theme) !important;
}

.placenta-page .ref-list li {
  margin-bottom: 0.8rem;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--pl-theme) !important;
}

.placenta-page .ref-list li::marker {
  color: var(--pl-theme) !important;
}

.placenta-page .references a,
.placenta-page .references a:visited,
.placenta-page .references em {
  color: var(--pl-theme) !important;
}

.placenta-page .references a {
  text-decoration: none;
}

.placenta-page .references a:hover {
  text-decoration: underline;
}

/* Dark/night mode protection */
html[data-theme="dark"] .placenta-page,
body[data-theme="dark"] .placenta-page,
[data-theme="dark"] .placenta-page {
  --pl-text: var(--global-text-color, #f4f4f4);
  --pl-soft-bg: rgba(242, 161, 195, 0.14);
  --pl-card-bg: rgba(242, 161, 195, 0.09);
  --pl-box-bg: rgba(255, 255, 255, 0.08);
  --pl-figure-bg: rgba(255, 255, 255, 0.06);
}

@media (prefers-color-scheme: dark) {
  .placenta-page {
    --pl-text: var(--global-text-color, #f4f4f4);
    --pl-soft-bg: rgba(242, 161, 195, 0.14);
    --pl-card-bg: rgba(242, 161, 195, 0.09);
    --pl-box-bg: rgba(255, 255, 255, 0.08);
    --pl-figure-bg: rgba(255, 255, 255, 0.06);
  }
}

@media (max-width: 900px) {
  .placenta-page {
    font-size: 1.15rem;
    line-height: 1.7;
  }

  .placenta-page .question-grid {
    grid-template-columns: 1fr;
  }

  .placenta-page .placenta-figure-slot {
    width: 100%;
    margin: 1.25rem auto 1.6rem auto;
  }

  .placenta-page .figure-placeholder {
    min-height: 220px;
  }

  .placenta-page .comparison-table {
    font-size: 0.95rem;
  }

  .placenta-page .ref-list li {
    font-size: 0.95rem;
  }
}
</style>

<div class="placenta-page">

  <p>The placenta is a temporary, fetal-derived organ that supports pregnancy by connecting maternal physiology with fetal development. It is not simply a barrier. It senses changes in the maternal environment and adjusts transport, vascular, endocrine, and immune functions that help regulate fetal growth.</p>

  <p>In the Cariaco Lab, we study the placenta as an active biological interface. We ask how maternal signals such as metabolism, inflammation, oxygenation, medications, and environmental exposures reshape placental structure and function.</p>

  <figure class="placenta-figure-slot" aria-labelledby="fig1-human-placenta-caption">
    <img
      src="{{ '/assets/img/human-placenta.svg' | relative_url }}"
      alt="Schematic of the human placenta showing the maternal–fetal interface, placental villi, trophoblast layers, fetal vessels, maternal blood, and umbilical cord."
      class="placenta-figure-img"
      loading="lazy"
    />

    <figcaption id="fig1-human-placenta-caption">
      <strong>Figure 1. The placenta as an active interface between maternal physiology and fetal development.</strong>
      The schematic highlights the maternal–fetal interface, including maternal blood, placental villi, trophoblast layers, fetal vessels, and the umbilical cord.
    </figcaption>
  </figure>

  <h2>A Temporary Organ with Many Jobs</h2>

  <p>During pregnancy, the placenta supports many functions that fetal organs cannot yet perform on their own. It transfers oxygen and nutrients, removes waste products, produces hormones, regulates immune communication, and helps coordinate maternal–fetal exchange.</p>

  <figure class="placenta-figure-slot" aria-labelledby="fig2-multitasker-caption">
    <img
      src="{{ '/assets/img/multitasker.png' | relative_url }}"
      alt="Schematic showing the placenta as a multitasking organ during pregnancy"
      class="placenta-figure-img"
      loading="lazy"
    />

    <figcaption id="fig2-multitasker-caption">
      <strong>Figure 2. The placenta functions as a multitasking organ during pregnancy.</strong>
      The placenta supports gas exchange, nutrient handling, waste transfer, endocrine signaling, immune communication, and vascular regulation.
    </figcaption>
  </figure>

  <h2>A Sensor of Resilience and Dysfunction</h2>

  <p>Maternal stressors such as poor nutrition, metabolic imbalance, inflammation, medication exposure, or toxicant exposure can alter placental tissue architecture, immune signaling, transport capacity, and protein expression. These changes may reveal how the placenta responds to stress before clinical symptoms are visible.</p>

  <p>In some pregnancies, the placenta compensates and continues to support fetal growth. In others, these adaptive responses are overwhelmed and shift toward dysfunction. Our research aims to identify the molecular and structural features that distinguish resilience from early failure.</p>


  <h2>The Vascular Tree: Building the Exchange Surface</h2>

  <p>The placenta contains a dense network of fetal blood vessels organized within tree-like chorionic villi. These villi are surrounded by maternal blood in the intervillous space, bringing maternal and fetal circulation into close proximity while keeping the two blood supplies physically separated.</p>

  <p>A successful pregnancy also requires remodeling of maternal spiral arteries. These arteries normally transform from narrow, high-resistance vessels into wider, low-resistance channels that deliver blood to the placenta. When vascular remodeling or villous vascular development is disrupted, oxygen and nutrient exchange can be compromised, contributing to fetal growth restriction and placental dysfunction.</p>

  <h2>Decoding Human Pregnancy Through Preclinical Models</h2>

  <p>Many key mechanisms of placental development cannot be tested directly during human pregnancy. Mouse models allow controlled studies of maternal exposures, gene function, placental development, and fetal outcomes. They are especially useful for testing cause-and-effect relationships.</p>

  <p>Translation, however, requires careful attention to species-specific anatomy. Mouse and human placentas share important biological principles, including hemochorial organization, trophoblast differentiation, and maternal–fetal exchange. They also differ in tissue architecture, trophoblast invasion, vascular organization, and developmental timing.</p>

  <figure class="placenta-figure-slot" aria-labelledby="fig4-placental-vascularization-caption">
    <img
      src="{{ '/assets/img/vascular.svg' | relative_url }}"
      alt="Comparative schematic of mouse and human placental vascularization, showing maternal and fetal circulation, placental vascular compartments, and the placental barrier."
      class="placenta-figure-img"
      loading="lazy"
    />

    <figcaption id="fig4-placental-vascularization-caption">
      <strong>Figure 3. Comparative placental vascularization and maternal–fetal barrier organization in mouse and human placenta.</strong>
      The schematic compares the organization of maternal and fetal blood flow in mouse and human placentas. In the mouse placenta, maternal blood enters through uterine, radial, and spiral arteries and passes through the decidua, junctional zone, blood sinusoids, and labyrinth, where exchange occurs near fetal capillaries. In the human placenta, maternal blood is supplied through uterine, radial, and spiral arteries into the intervillous space surrounding chorionic villi, while fetal circulation is connected through the umbilical cord and fetal capillaries. The lower panels highlight the placental barrier, including maternal red blood cells, fetal red blood cells, endothelial cells, trophoblast layers, and species-specific placental cell types. Adapted from Rusidzé et al. 2023 https://doi.org/10.3390/cells12040620.
      <br><br>
      <em>Abbreviations:</em> S-TGC, sinusoidal trophoblast giant cell; SynT-I and SynT-II, syncytiotrophoblast layers I and II; SynT, syncytiotrophoblast; CTB, cytotrophoblast; EC, endothelial cell; mRBC, maternal red blood cell; fRBC, fetal red blood cell.
    </figcaption>
  </figure>

  <div class="comparison-table-wrap">
    <table class="comparison-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th>Human Placenta</th>
          <th>Mouse Placenta</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Overall Shape</strong></td>
          <td>Discoid, with a villous exchange structure.</td>
          <td>Discoid, with a labyrinthine exchange structure.</td>
        </tr>
        <tr>
          <td><strong>Main Exchange Region</strong></td>
          <td>Tree-like chorionic villi containing fetal vessels surrounded by maternal blood in the intervillous space.</td>
          <td>A labyrinth zone where fetal capillaries and maternal blood spaces are closely interdigitated.</td>
        </tr>
        <tr>
          <td><strong>Trophoblast Invasion</strong></td>
          <td>Extravillous trophoblasts invade the decidua and inner myometrium and contribute to spiral artery remodeling.</td>
          <td>Trophoblast invasion is more limited and involves species-specific trophoblast populations, including trophoblast giant cells and glycogen trophoblasts.</td>
        </tr>
        <tr>
          <td><strong>Gestational Timeline</strong></td>
          <td>Approximately nine months, allowing prolonged placental growth, branching, and maturation.</td>
          <td>Approximately 19–21 days, with rapid placental development that supports a short pregnancy and larger litters.</td>
        </tr>
        <tr>
          <td><strong>Translational Value</strong></td>
          <td>Provides direct relevance to human placental biology and pregnancy complications.</td>
          <td>Enables controlled maternal environmental perturbations, genetic manipulation, and mechanistic testing.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <h2>What the Cariaco Lab Studies</h2>

  <p>The Cariaco Lab combines placental biology, experimental models, human tissue datasets, histology, molecular profiling, and computational image analysis to study how maternal exposures reshape placental structure and function.</p>

  <div class="question-grid">

    <div class="question-card">
      <strong>How does the placenta sense maternal exposures?</strong>
      We map how metabolic stress, inflammation, medications, and environmental contaminants alter placental tissue organization and signaling.
    </div>

    <div class="question-card">
      <strong>What drives placental resilience?</strong>
      We investigate the protective programs that allow some placentas to maintain vascular growth, immune balance, and nutrient transport under stress.
    </div>

    <div class="question-card">
      <strong>When does adaptation become dysfunction?</strong>
      We study the molecular and structural thresholds where compensatory changes fail, leading to restricted exchange capacity and altered fetal growth.
    </div>

    <div class="question-card">
      <strong>How can we measure placental structure more precisely?</strong>
      We develop quantitative image-analysis tools to make placental histology faster, more reproducible, and easier to compare across models and datasets.
    </div>

  </div>

  <p>To answer these questions, our lab bridges classic placental histology with computational pathology. We design automated digital pipelines alongside molecular profiling approaches to connect tissue architecture, cellular organization, and biological function.</p>

  <div class="references" id="references">
    <strong>References</strong>
    <ol class="ref-list">
      <li>
        <a href="https://doi.org/10.1016/j.rbmo.2015.10.005" target="_blank" rel="noopener">
          Costa MA. The endocrine function of human placenta: an overview. <em>Reproductive BioMedicine Online</em>. 2016;32(1):14–43.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1007/s00018-014-1794-x" target="_blank" rel="noopener">
          Soncin F, Natale D, Parast MM. Signaling pathways in mouse and human trophoblast differentiation: a comparative review. <em>Cellular and Molecular Life Sciences</em>. 2015;72(7):1291–1302.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1007/s43032-020-00212-8" target="_blank" rel="noopener">
          Albrecht ED, Pepe GJ. Regulation of Uterine Spiral Artery Remodeling: a Review. <em>Reproductive Sciences</em>. 2020;27:1932–1942.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1016/j.placenta.2020.05.003" target="_blank" rel="noopener">
          Burton GJ, Jauniaux E. The placenta in fetal growth restriction: What is going wrong? <em>Placenta</em>. 2020;96:10–18.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1016/j.placenta.2006.11.002" target="_blank" rel="noopener">
          Carter AM. Animal models of human placentation — a review. <em>Placenta</em>. 2007;28 Suppl A:S41–S47.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.3390/cells12040620" target="_blank" rel="noopener">
          Rusidzé et al. Comparative placental vascularization and maternal–fetal barrier organization. <em>Cells</em>. 2023;12(4):620.
        </a>
      </li>
    </ol>
  </div>

</div>
