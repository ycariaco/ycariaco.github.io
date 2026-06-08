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

.placenta-page .placenta-figure-slot img {
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

  <p>The placenta is a temporary powerhouse created by the embryo to nurture, protect, and support life. Far from a passive sieve, it acts as a dynamic biological interface between mother and baby, continuously reading environmental cues to dictate the course of pregnancy.</p>

  <p>In our laboratory, we study the placenta as an active biosensor. It continuously decodes complex maternal signals—including metabolic shifts, inflammation, oxygenation fluctuations, and environmental exposures. By interpreting these inputs, the placenta dynamically adjusts its cellular, vascular, and transport programs to optimize fetal development.</p>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: placenta overview">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: simple schematic of the maternal–fetal interface showing maternal blood, placental villi, fetal vessels, trophoblast layers, and umbilical cord.</span>
    </div>
    <figcaption>Figure 1. The placenta as an active interface between maternal physiology and fetal development.</figcaption>
  </figure>

  <h2>A One-Organ Symphony: Master of All Trades</h2>

  <p>While an adult relies on a complex network of organ systems to survive, a developing fetus relies entirely on the placenta. Because fetal organs are still under construction, this temporary tissue steps in to mimic their vital workloads simultaneously. It acts as the lungs for gas exchange, the gut and liver for nutrient transfer and detoxification, the kidneys for waste clearing, and an endocrine control center for immune and vascular regulation.</p>

  <figure class="placenta-figure-slot" aria-label="Figure: placenta as a multitasking organ">
    <img
      src="{{ '/assets/img/multitasker.png' | relative_url }}"
      alt="Schematic showing the placenta as a multitasking organ during pregnancy"
    >
    <figcaption>
      Figure 2. The placenta functions as a multitasking organ during pregnancy, supporting gas exchange, nutrient handling, waste transfer, endocrine signaling, immune communication, and vascular regulation.
    </figcaption>
  </figure>


  <h2>A Sensor of Resilience and Dysfunction</h2>

  <p>When a pregnancy faces challenges, the placenta records the struggle. Maternal stressors like poor nutrition, metabolic imbalances, or toxicant exposures alter tissue architecture and protein expression long before clinical symptoms manifest. Yet, what makes this organ truly remarkable is its capacity for resilience; it can alter its own structure and accelerate nutrient transport to protect the fetus from harm.</p>

  <p>However, this resilience has limits. When stress overwhelms these compensatory mechanisms, the placenta shifts toward maladaptive dysfunction, rewriting the trajectory of fetal growth. Our research focuses on identifying the early structural and molecular biomarkers that define this transition, allowing us to spot vulnerabilities before they compromise pregnancy outcomes.</p>

  <h2>The Vascular Tree: Engineering the Exchange</h2>

  <p>The placenta operates like a tree of life. Its dense canopy of fetal capillaries, organized into tree-like chorionic villi, sits directly within pools of maternal blood. This intricate vascularization allows maternal and fetal blood to come into incredibly close contact to swap oxygen and nutrients without ever truly mixing.</p>

  <p>A successful pregnancy requires an extraordinary vascular remodeling process: maternal spiral arteries must transform from narrow, high-resistance vessels into wide, low-resistance channels to flood the tissue canopy with blood. When these vascular blueprints are disrupted, the resulting flow resistance starves the fetus, sparking severe clinical complications like Intrauterine Growth Restriction (IUGR) or maternal preeclampsia.</p>

  <figure class="placenta-figure-slot" aria-labelledby="fig3-placental-vascularization-caption">

  <img

    src="{{ '/assets/img/vascular.svg' | relative_url }}"

    alt="Comparative schematic of mouse and human placental vascularization, showing maternal and fetal circulation, placental vascular compartments, and the placental barrier."

    class="placenta-figure-img"

    loading="lazy"

  />

  <figcaption id="fig3-placental-vascularization-caption">

    <strong>Figure 3. Comparative placental vascularization and maternal–fetal barrier organization in mouse and human placenta.</strong>

    The schematic compares the organization of maternal and fetal blood flow in mouse and human placentas. In the mouse placenta, maternal blood enters through uterine, radial, and spiral arteries and passes through the decidua, junctional zone, blood sinusoids, and labyrinth, where exchange occurs near fetal capillaries. In the human placenta, maternal blood is supplied through uterine, radial, and spiral arteries into the intervillous space surrounding chorionic villi, while fetal circulation is connected through the umbilical cord and fetal capillaries. The lower panels highlight the placental barrier, including maternal red blood cells, fetal red blood cells, endothelial cells, trophoblast layers, and species-specific placental cell types. Adapted from Rusidzé et al. 2023 https://doi.org/10.3390/cells12040620.

    <em>Abbreviations:</em> S-TGC, sinusoidal trophoblast giant cell; SynT-I and SynT-II, syncytiotrophoblast layers I and II; SynT, syncytiotrophoblast; CTB, cytotrophoblast; EC, endothelial cell; mRBC, maternal red blood cell; fRBC, fetal red blood cell.

  </figcaption>

</figure>

  <h2>Decoding Human Pregnancy Through Preclinical Models</h2>

  <p>Ethical boundaries mean we cannot experiment on a developing human placenta in real-time. To unlock these mechanisms, we look to mouse models. While a mouse placenta differs structurally from a human's, they share core cellular, genetic, and physiological pathways that make them invaluable tools for evaluating pregnancy complications and decoding cause-and-effect relationships.</p>

  <p>Translation, however, requires precise attention to species-specific anatomy. Both systems share a hemochorial organization and overlapping trophoblast differentiation pathways, but their underlying architectures are shaped by wildly different evolutionary timelines. Understanding these structural contrasts is what allows us to translate preclinical breakthroughs into actionable human health insights.</p>

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
          <td>Tree-like chorionic villi containing fetal vessels bathed in pools of maternal blood.</td>
          <td>A dense labyrinth zone where fetal capillaries and maternal blood spaces tightly interdigitate.</td>
        </tr>
        <tr>
          <td><strong>Trophoblast Invasion</strong></td>
          <td>Deep, aggressive invasion: extravillous trophoblasts penetrate the decidua and inner myometrium to aggressively remodel spiral arteries.</td>
          <td>Shallow, restricted invasion: limited to the decidua, mediated by species-specific trophoblast giant cells and glycogen trophoblasts.</td>
        </tr>
        <tr>
          <td><strong>Gestational Timeline</strong></td>
          <td>~9 months: allows for slow, highly complex structural development, branching, and prolonged maturation.</td>
          <td>~19–21 days: characterized by rapid, hyper-accelerated development optimized to support large litters over a brief period.</td>
        </tr>
        <tr>
          <td><strong>Translational Value</strong></td>
          <td>Provides direct human pathological relevance, validation datasets, and clinical endpoints.</td>
          <td>Enables controlled maternal environmental perturbations, genetic manipulation, and real-time mechanistic tracking.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: mouse and human placentation">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: side-by-side comparison of human chorionic villi and mouse labyrinth, emphasizing conserved functions and species-specific anatomy.</span>
    </div>
    <figcaption>Figure 4. Mouse and human placentas share key functions but differ in tissue organization and developmental timing.</figcaption>
  </figure>

  <h2>What the Cariaco Lab is Unlocking</h2>

  <p>We blend computational innovation with tissue biology to decipher the placenta's molecular playbook. By combining advanced mouse models and human datasets with high-throughput imaging, we explore how the maternal environment alters tissue architecture across multiple scales.</p>

  <div class="question-grid">

    <div class="question-card">
      <strong>How does the placenta sense maternal exposures?</strong>
      We map how metabolic stress, inflammation, and environmental contaminants alter early tissue organization and baseline signaling.
    </div>

    <div class="question-card">
      <strong>What drives placental resilience?</strong>
      We investigate the protective programs that allow some placentas to maintain vascular growth and stable nutrient transport under stress.
    </div>

    <div class="question-card">
      <strong>When does adaptation cross into dysfunction?</strong>
      We target the molecular thresholds where compensatory changes fail, leading to restricted exchange capacity and poor fetal growth.
    </div>

  </div>

  <p>To answer these questions, our lab bridges the gap between classic histology and computational pathology. By designing automated, AI-driven digital pipelines alongside standard molecular profiling, we are making advanced quantitative tissue analysis faster, highly reproducible, and universally accessible.</p>

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
    </ol>
  </div>

</div>
