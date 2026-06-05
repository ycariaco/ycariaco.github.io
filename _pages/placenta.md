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

  <p>When people think about pregnancy, attention naturally goes to the developing baby. Yet fetal development depends on another remarkable organ working at the maternal–fetal interface: the placenta. The placenta is temporary, fetal-derived, and highly specialized. It supports pregnancy for only a short period, but during that time it performs functions essential for growth, protection, communication, and adaptation.</p>

  <p>In our laboratory, we study the placenta as an active biological interface. It does not simply pass nutrients from mother to fetus. It senses the maternal environment, interprets signals such as metabolism, inflammation, oxygenation, xenobiotic exposure, and nutrient availability, and adjusts cellular, vascular, endocrine, immune, and transport programs that influence fetal development.</p>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: placenta overview">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: simple schematic of the maternal–fetal interface showing maternal blood, placental villi, fetal vessels, trophoblast layers, and umbilical cord.</span>
    </div>
    <figcaption>Figure 1. The placenta as an active interface between maternal physiology and fetal development.</figcaption>
  </figure>

  <h2>A temporary organ with many jobs</h2>

  <p>For a developing fetus, many organs are still forming. The placenta helps support functions that, after birth, will be carried out by specialized organs. It manages gas exchange, nutrient transfer, waste removal, endocrine signaling, immune communication, and vascular regulation. This makes the placenta one of the most biologically complex organs in pregnancy.</p>

  <figure class="placenta-figure-slot" aria-label="Figure: placenta as a multitasking organ">
    <img
      src="{{ '/assets/multitasker.png' | relative_url }}"
      alt="Schematic showing the placenta as a multitasking organ during pregnancy"
    >
    <figcaption>
      Figure 2. The placenta functions as a multitasking organ during pregnancy, supporting gas exchange, nutrient handling, waste transfer, endocrine signaling, immune communication, and vascular regulation.
    </figcaption>
  </figure>

  <div class="placenta-callout">
    <p><strong>Our central question is simple:</strong> how does the placenta decide whether to adapt, compensate, or fail when the maternal environment changes?</p>
  </div>

  <h2>A sensor of resilience and dysfunction</h2>

  <p>The placenta is a sensitive recorder of pregnancy conditions. Maternal stressors such as metabolic imbalance, inflammation, altered oxygenation, medication exposure, environmental contaminants, or poor nutrient availability can leave measurable traces in placental structure and molecular activity. These traces may appear as changes in trophoblast behavior, vascular development, nutrient transport, immune signaling, hormone production, or tissue architecture.</p>

  <p>One of the most interesting features of the placenta is its capacity for resilience. In some pregnancies, the placenta adapts to maternal stress and continues to support fetal growth. In others, similar stressors push the organ toward dysfunction. Understanding this difference is a major goal of our research. We want to identify which placental responses are protective, which ones mark early vulnerability, and which mechanisms determine the transition from compensation to failure.</p>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: resilience versus dysfunction">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: two-panel schematic showing placental resilience versus dysfunction after maternal exposure, with examples such as immune tone, vascular remodeling, nutrient transport, and trophoblast function.</span>
    </div>
    <figcaption>Figure 3. Maternal exposures can produce compensatory or maladaptive placental responses.</figcaption>
  </figure>

  <h2>The vascular tree of the placenta</h2>

  <p>The placenta is highly vascularized. In the human placenta, tree-like chorionic villi contain fetal blood vessels and are surrounded by maternal blood. This arrangement allows maternal and fetal blood to come into close contact while remaining physically separated by placental tissue. Efficient exchange depends on proper vascular development, trophoblast function, and blood flow on both sides of the maternal–fetal interface.</p>

  <p>Early in pregnancy, maternal spiral arteries must remodel from narrow, high-resistance vessels into wider, low-resistance channels that can deliver blood to the placenta. At the same time, the placenta develops a dense fetal vascular network within the villous tree. When these vascular programs are disrupted, oxygen and nutrient delivery can be compromised, increasing the risk of poor fetal growth and placental dysfunction.</p>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: placental vascularization">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: placental vascular tree showing maternal spiral artery remodeling, intervillous space, chorionic villi, and fetal capillaries.</span>
    </div>
    <figcaption>Figure 4. Placental vascularization supports oxygen and nutrient exchange across the maternal–fetal interface.</figcaption>
  </figure>

  <h2>The placenta–brain axis</h2>

  <p>The consequences of placental adaptation may extend beyond fetal growth. The developing brain is sensitive to oxygen delivery, nutrient availability, inflammatory signals, endocrine cues, and metabolic balance. Since the placenta helps regulate each of these signals, changes in placental function may influence fetal brain development.</p>

  <p>This idea is known as the placenta–brain axis. In our work, we use this concept to ask how placental responses to maternal exposures may shape fetal neurodevelopmental programs. Rather than viewing the placenta and brain as separate systems, we study how altered placental signaling may change the environment in which the fetal brain develops.</p>

  <div class="placenta-callout">
    <p><strong>The placenta–brain axis asks what the placenta sends, modifies, or fails to send to the developing brain.</strong> These signals may include oxygen, nutrients, hormones, inflammatory mediators, metabolic cues, extracellular vesicles, and growth-related factors.</p>
  </div>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: placenta-brain axis">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: placenta–brain axis schematic showing maternal exposures, placental response, fetal circulation, and fetal brain development.</span>
    </div>
    <figcaption>Figure 5. Placental signals may influence fetal brain development through oxygen, nutrient, endocrine, immune, and metabolic pathways.</figcaption>
  </figure>

  <h2>Why mouse models still matter</h2>

  <p>Many important questions in placental biology cannot be tested directly during human pregnancy. Mouse models allow researchers to study placental development, gene function, maternal exposures, and fetal outcomes in controlled experimental systems. They are especially useful for identifying mechanisms and testing cause-and-effect relationships.</p>

  <p>Mouse models are powerful, but they are not miniature humans. Translation requires careful attention to both conserved and species-specific features of placentation. Mouse and human placentas share important biological principles, including trophoblast differentiation, maternal–fetal exchange, and hemochorial organization. They also differ in structure, depth of trophoblast invasion, endocrine programs, and developmental timing.</p>

  <div class="comparison-table-wrap">
    <table class="comparison-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th>Human placenta</th>
          <th>Mouse placenta</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Overall shape</td>
          <td>Discoid, with a villous exchange structure.</td>
          <td>Discoid, with a labyrinthine exchange structure.</td>
        </tr>
        <tr>
          <td>Main exchange region</td>
          <td>Chorionic villi containing fetal vessels surrounded by maternal blood.</td>
          <td>Labyrinth zone where fetal vessels and maternal blood spaces are closely interdigitated.</td>
        </tr>
        <tr>
          <td>Trophoblast invasion</td>
          <td>Extravillous trophoblasts invade deeply into the decidua and inner myometrium and contribute to spiral artery remodeling.</td>
          <td>Invasion is more limited and involves species-specific trophoblast populations such as trophoblast giant cells and glycogen trophoblasts.</td>
        </tr>
        <tr>
          <td>Gestational timing</td>
          <td>Approximately nine months, allowing prolonged placental growth and maturation.</td>
          <td>Approximately 19–21 days, with rapid placental development supporting a short pregnancy and larger litters.</td>
        </tr>
        <tr>
          <td>Best use in research</td>
          <td>Human tissues provide direct relevance to human pregnancy and placental pathology.</td>
          <td>Mouse models allow controlled perturbation, genetic manipulation, and mechanistic testing.</td>
        </tr>
      </tbody>
    </table>
  </div>

  <figure class="placenta-figure-slot" aria-label="Figure placeholder: mouse and human placentation">
    <div class="figure-placeholder">
      <strong>Figure space</strong>
      <span>Suggested figure: side-by-side comparison of human chorionic villi and mouse labyrinth, emphasizing conserved functions and species-specific anatomy.</span>
    </div>
    <figcaption>Figure 6. Mouse and human placentas share key functions but differ in tissue organization and developmental timing.</figcaption>
  </figure>

  <h2>What our lab is trying to understand</h2>

  <p>The Cariaco Lab studies how the placenta senses maternal exposures and converts them into biological responses that influence fetal development. We are especially interested in the mechanisms that separate resilience from dysfunction.</p>

  <div class="question-grid">

    <div class="question-card">
      <strong>How does the placenta sense maternal exposures?</strong>
      We study how metabolic stress, inflammation, drugs, xenobiotics, and environmental contaminants alter placental signaling and tissue organization.
    </div>

    <div class="question-card">
      <strong>What makes a placenta resilient?</strong>
      We investigate how some placentas preserve vascular development, nutrient transport, immune balance, and growth support under stress.
    </div>

    <div class="question-card">
      <strong>When does adaptation become dysfunction?</strong>
      We examine how compensatory responses may become maladaptive, leading to altered exchange capacity, trophoblast function, and fetal development.
    </div>

    <div class="question-card">
      <strong>How does placental state relate to fetal brain development?</strong>
      We study the placenta–brain axis to understand how altered placental signals may shape fetal neurodevelopmental programs.
    </div>

  </div>

  <p>To answer these questions, we combine experimental models, human placental datasets, histology, immunofluorescence, molecular profiling, and computational image analysis. This integrated approach allows us to study the placenta across scales, from molecular pathways to tissue architecture to fetal developmental outcomes.</p>

  <div class="references" id="references">
    <strong>References</strong>
    <ol class="ref-list">
      <li>
        <a href="https://doi.org/10.1016/j.rbmo.2015.10.005" target="_blank" rel="noopener">
          Costa MA. The endocrine function of human placenta: an overview. <em>Reproductive BioMedicine Online</em>. 2016;32(1):14–43.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1002/jnr.24603" target="_blank" rel="noopener">
          Rosenfeld CS. The Placenta-Brain-Axis. <em>Journal of Neuroscience Research</em>. 2021;99(1):271–283.
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
