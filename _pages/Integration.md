---
layout: page
title: Multi-omics Integration
permalink: /research/integration/
nav: false
---

<style>
.multiomics-page {
  font-size: 1.3rem;
  line-height: 1.8;
  width: 100%;
  display: flow-root;

  --mo-theme: var(--global-theme-color, #e83e8c);
  --mo-text: var(--global-text-color, #2b2b2b);
  --mo-border: #f2a1c3;
  --mo-soft-bg: rgba(242, 161, 195, 0.16);
  --mo-card-bg: rgba(242, 161, 195, 0.10);
  --mo-mini-bg: rgba(255, 255, 255, 0.72);
  --mo-box-bg: #fff7fb;
  --mo-figure-bg: #ffe9f2;
}

.multiomics-page p {
  margin: 0 0 1.25rem 0;
  color: var(--mo-text);
}

.multiomics-page h2 {
  margin-top: 1.8rem;
  margin-bottom: 0.8rem;
  font-size: 1.65rem;
  line-height: 1.35;
  color: var(--mo-theme);
}

.multiomics-page .omics-figure-center {
  clear: both;
  width: min(94%, 1050px);
  margin: 1.5rem auto 1.9rem auto;
  padding: 0;
  box-sizing: border-box;
}

.multiomics-page .omics-figure-center img {
  width: 100%;
  height: auto;
  display: block;
  border: 2px solid var(--mo-border);
  border-radius: 16px;
  padding: 6px;
  background: var(--mo-figure-bg);
  box-sizing: border-box;
}

.multiomics-page .omics-figure-center figcaption {
  display: block;
  width: 100%;
  text-align: center;
  margin-top: 0.4rem;
  font-size: 1rem;
  line-height: 1.4;
  color: var(--mo-text);
}

.multiomics-page .integration-callout {
  border-left: 5px solid var(--mo-border);
  background: var(--mo-soft-bg);
  color: var(--mo-text);
  padding: 1rem 1.25rem;
  margin: 1.25rem 0;
  border-radius: 0 14px 14px 0;
}

.multiomics-page .integration-callout p {
  margin-bottom: 0;
  color: inherit;
}

.multiomics-page .integration-callout strong {
  color: inherit;
}

.multiomics-page .integration-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1.25rem;
  margin: 1.5rem 0 1.75rem 0;
}

.multiomics-page .integration-card {
  border: 2px solid var(--mo-border);
  border-radius: 18px;
  background: var(--mo-card-bg);
  color: var(--mo-text);
  padding: 1.1rem 1.2rem;
  box-sizing: border-box;
}

.multiomics-page .integration-card h2 {
  margin-top: 0;
  color: var(--mo-theme);
}

.multiomics-page .mini-visual {
  margin: 1rem 0;
  padding: 1rem;
  border-radius: 16px;
  background: var(--mo-mini-bg);
  border: 1px solid rgba(242, 161, 195, 0.55);
}

.multiomics-page .horizontal-visual {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  gap: 0.65rem;
}

.multiomics-page .cohort-box {
  border: 2px solid var(--mo-border);
  border-radius: 14px;
  padding: 0.8rem 0.55rem;
  text-align: center;
  background: var(--mo-box-bg);
  color: var(--mo-text);
  font-size: 1rem;
  line-height: 1.35;
}

.multiomics-page .cohort-box strong {
  color: var(--mo-theme);
}

.multiomics-page .visual-arrow {
  color: var(--mo-theme);
  font-weight: bold;
  font-size: 1.4rem;
  text-align: center;
}

.multiomics-page .vertical-visual {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  align-items: stretch;
}

.multiomics-page .omics-layer {
  border-radius: 999px;
  padding: 0.45rem 0.8rem;
  text-align: center;
  font-size: 1rem;
  line-height: 1.3;
  font-weight: 600;
  border: 2px solid rgba(242, 161, 195, 0.75);
  background: var(--mo-box-bg);
}

.multiomics-page .omics-layer.layer-genomics {
  color: #8b4cf6;
}

.multiomics-page .omics-layer.layer-epigenomics {
  color: #10b981;
}

.multiomics-page .omics-layer.layer-transcriptomics {
  color: #f472b6;
}

.multiomics-page .omics-layer.layer-proteomics {
  color: #ef4444;
}

.multiomics-page .omics-layer.layer-metabolomics {
  color: #d99a00;
}

.multiomics-page .omics-layer.layer-spatial {
  color: #a16207;
}

.multiomics-page .vertical-result {
  margin-top: 0.55rem;
  border-radius: 14px;
  padding: 0.7rem;
  text-align: center;
  font-weight: 600;
  background: var(--mo-soft-bg);
  color: var(--mo-text);
}

.multiomics-page .workflow-strip {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.8rem;
  margin: 1.5rem 0 1.75rem 0;
}

.multiomics-page .workflow-step {
  border: 2px solid var(--mo-border);
  border-radius: 16px;
  padding: 0.85rem 0.7rem;
  background: var(--mo-card-bg);
  color: var(--mo-text);
  text-align: center;
  font-size: 1rem;
  line-height: 1.35;
}

.multiomics-page .workflow-step strong {
  display: block;
  color: var(--mo-theme);
  margin-bottom: 0.25rem;
}

.multiomics-page .references {
  clear: both;
  margin-top: 2rem;
  padding-top: 0.5rem;
  color: var(--mo-theme) !important;
}

.multiomics-page .references strong {
  display: block;
  font-size: 1.2rem;
  margin-bottom: 0.6rem;
  color: var(--mo-theme) !important;
}

.multiomics-page .ref-list {
  padding-left: 1.4rem;
  margin-top: 0.75rem;
  color: var(--mo-theme) !important;
}

.multiomics-page .ref-list li {
  margin-bottom: 0.8rem;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--mo-theme) !important;
}

.multiomics-page .ref-list li::marker {
  color: var(--mo-theme) !important;
}

.multiomics-page .references a,
.multiomics-page .references a:visited,
.multiomics-page .references em {
  color: var(--mo-theme) !important;
}

.multiomics-page .references a {
  text-decoration: none;
}

.multiomics-page .references a:hover {
  text-decoration: underline;
}

/* Dark/night mode protection */
html[data-theme="dark"] .multiomics-page,
body[data-theme="dark"] .multiomics-page,
[data-theme="dark"] .multiomics-page {
  --mo-text: var(--global-text-color, #f4f4f4);
  --mo-soft-bg: rgba(242, 161, 195, 0.14);
  --mo-card-bg: rgba(242, 161, 195, 0.09);
  --mo-mini-bg: rgba(255, 255, 255, 0.06);
  --mo-box-bg: rgba(255, 255, 255, 0.08);
  --mo-figure-bg: #ffffff;
}

html[data-theme="dark"] .multiomics-page .omics-figure-center img,
body[data-theme="dark"] .multiomics-page .omics-figure-center img,
[data-theme="dark"] .multiomics-page .omics-figure-center img {
  background: #ffffff;
}

html[data-theme="dark"] .multiomics-page .cohort-box,
html[data-theme="dark"] .multiomics-page .omics-layer,
body[data-theme="dark"] .multiomics-page .cohort-box,
body[data-theme="dark"] .multiomics-page .omics-layer,
[data-theme="dark"] .multiomics-page .cohort-box,
[data-theme="dark"] .multiomics-page .omics-layer {
  color: var(--mo-text);
}

html[data-theme="dark"] .multiomics-page .omics-layer.layer-genomics,
body[data-theme="dark"] .multiomics-page .omics-layer.layer-genomics,
[data-theme="dark"] .multiomics-page .omics-layer.layer-genomics {
  color: #c4a5ff;
}

html[data-theme="dark"] .multiomics-page .omics-layer.layer-epigenomics,
body[data-theme="dark"] .multiomics-page .omics-layer.layer-epigenomics,
[data-theme="dark"] .multiomics-page .omics-layer.layer-epigenomics {
  color: #7ee7b8;
}

html[data-theme="dark"] .multiomics-page .omics-layer.layer-transcriptomics,
body[data-theme="dark"] .multiomics-page .omics-layer.layer-transcriptomics,
[data-theme="dark"] .multiomics-page .omics-layer.layer-transcriptomics {
  color: #ff9de0;
}

html[data-theme="dark"] .multiomics-page .omics-layer.layer-proteomics,
body[data-theme="dark"] .multiomics-page .omics-layer.layer-proteomics,
[data-theme="dark"] .multiomics-page .omics-layer.layer-proteomics {
  color: #ff8b8b;
}

html[data-theme="dark"] .multiomics-page .omics-layer.layer-metabolomics,
body[data-theme="dark"] .multiomics-page .omics-layer.layer-metabolomics,
[data-theme="dark"] .multiomics-page .omics-layer.layer-metabolomics {
  color: #ffd166;
}

html[data-theme="dark"] .multiomics-page .omics-layer.layer-spatial,
body[data-theme="dark"] .multiomics-page .omics-layer.layer-spatial,
[data-theme="dark"] .multiomics-page .omics-layer.layer-spatial {
  color: #f5c16c;
}

@media (prefers-color-scheme: dark) {
  .multiomics-page {
    --mo-text: var(--global-text-color, #f4f4f4);
    --mo-soft-bg: rgba(242, 161, 195, 0.14);
    --mo-card-bg: rgba(242, 161, 195, 0.09);
    --mo-mini-bg: rgba(255, 255, 255, 0.06);
    --mo-box-bg: rgba(255, 255, 255, 0.08);
    --mo-figure-bg: #ffffff;
  }

  .multiomics-page .omics-figure-center img {
    background: #ffffff;
  }

  .multiomics-page .omics-layer.layer-genomics {
    color: #c4a5ff;
  }

  .multiomics-page .omics-layer.layer-epigenomics {
    color: #7ee7b8;
  }

  .multiomics-page .omics-layer.layer-transcriptomics {
    color: #ff9de0;
  }

  .multiomics-page .omics-layer.layer-proteomics {
    color: #ff8b8b;
  }

  .multiomics-page .omics-layer.layer-metabolomics {
    color: #ffd166;
  }

  .multiomics-page .omics-layer.layer-spatial {
    color: #f5c16c;
  }
}

@media (max-width: 900px) {
  .multiomics-page {
    font-size: 1.15rem;
    line-height: 1.7;
  }

  .multiomics-page .omics-figure-center {
    width: 100%;
    margin: 1.25rem auto 1.6rem auto;
  }

  .multiomics-page .integration-grid {
    grid-template-columns: 1fr;
  }

  .multiomics-page .horizontal-visual {
    grid-template-columns: 1fr;
  }

  .multiomics-page .visual-arrow {
    transform: rotate(90deg);
  }

  .multiomics-page .workflow-strip {
    grid-template-columns: 1fr;
  }

  .multiomics-page .ref-list li {
    font-size: 0.95rem;
  }
}
</style>

<div class="multiomics-page">

  <p>Multi-omics integration brings together different layers of biological information to understand how a system works as a whole. In placental biology, no single dataset can fully explain function. Gene expression may show that a pathway is activated, proteomics can reveal whether this signal is translated into protein changes, metabolomics can capture the biochemical state of the tissue, and spatial histology can show where these changes occur within placental architecture.</p>

  <figure class="omics-figure-center" aria-label="Multi-omics integration schematic">
    <img
      src="{{ '/assets/img/integration.png' | relative_url }}"
      alt="Schematic showing integration of genomics, methylomics, transcriptomics, proteomics, metabolomics, and tissue-level image analysis to generate biological insights"
      loading="lazy"
      decoding="async">
    <figcaption>Figure 1. Multi-omics integration connects molecular and tissue-level datasets to identify pathways and biological insights.</figcaption>
  </figure>

  <p>One way to think about multi-omics is as a layered biological system. Genomics represents the inherited biological instructions. Methylomics and other epigenomic marks act as regulatory switches that influence which instructions are accessible. Transcriptomics captures which genes are being actively read. Proteomics measures the proteins that carry out many cellular functions. Metabolomics reflects biochemical products and energetic state. Tissue-level image analysis adds spatial and structural context by measuring architecture, cell organization, vascular patterning, and regional heterogeneity.</p>

  <div class="integration-callout">
    <p><strong>In our research, multi-omics integration helps move from lists of altered molecules toward biological mechanisms.</strong> We use it to ask how maternal exposures reshape placental regulation across molecular, cellular, metabolic, vascular, and structural scales.</p>
  </div>

  <div class="integration-grid">

    <div class="integration-card">
      <h2>Horizontal integration</h2>

      <p>Horizontal integration combines datasets from the same biological layer across different samples, cohorts, time points, species, or experimental conditions. The goal is to identify patterns that are reproducible across contexts.</p>

      <div class="mini-visual">
        <div class="horizontal-visual">
          <div class="cohort-box">Mouse exposure model<br><strong>transcriptomics</strong></div>
          <div class="visual-arrow">→</div>
          <div class="cohort-box">Human placenta cohort<br><strong>transcriptomics</strong></div>
          <div class="visual-arrow">→</div>
          <div class="cohort-box">Public dataset<br><strong>transcriptomics</strong></div>
        </div>
      </div>

      <p>For example, we can compare placental transcriptomic signatures from mouse models of maternal exposure with human placental datasets to identify shared inflammatory, metabolic, mitochondrial, or vascular programs. Similarly, image-derived tissue features from different cohorts can be integrated horizontally to test whether structural phenotypes are robust across datasets.</p>
    </div>

    <div class="integration-card">
      <h2>Vertical integration</h2>

      <p>Vertical integration combines different biological layers measured from the same samples or matched experimental groups. The goal is to connect regulation across scales, from molecular signals to tissue organization and phenotype.</p>

      <div class="mini-visual">
        <div class="vertical-visual">
          <div class="omics-layer layer-genomics">Genomics</div>
          <div class="omics-layer layer-epigenomics">Methylomics / Epigenomics</div>
          <div class="omics-layer layer-transcriptomics">Transcriptomics</div>
          <div class="omics-layer layer-proteomics">Proteomics</div>
          <div class="omics-layer layer-metabolomics">Metabolomics</div>
          <div class="omics-layer layer-spatial">Spatial histology</div>
          <div class="vertical-result">Integrated mechanism</div>
        </div>
      </div>

      <p>For example, a maternal exposure may alter genes involved in nutrient transport, reduce the abundance of transport-related proteins, shift metabolite availability, and produce measurable changes in villous vascularization. Vertical integration connects these signals into one mechanistic model of placental adaptation or dysfunction.</p>
    </div>

  </div>

  <h2>Why both types of integration matter</h2>

  <p>Horizontal and vertical integration answer different questions. Horizontal integration asks whether a biological signature is consistent across datasets or contexts. Vertical integration asks how different molecular and tissue layers interact within the same biological system. Together, they help distinguish robust placental programs from dataset-specific effects and connect molecular regulation to structural and functional outcomes.</p>

  <div class="workflow-strip">
    <div class="workflow-step">
      <strong>1. Measure</strong>
      Omics and histology data from placenta samples
    </div>

    <div class="workflow-step">
      <strong>2. Harmonize</strong>
      Quality control, normalization, and annotation
    </div>

    <div class="workflow-step">
      <strong>3. Integrate</strong>
      Horizontal and vertical data integration
    </div>

    <div class="workflow-step">
      <strong>4. Interpret</strong>
      Pathways, networks, cell states, and tissue patterns
    </div>

    <div class="workflow-step">
      <strong>5. Validate</strong>
      Targeted assays and biological follow-up
    </div>
  </div>

  <p>In our laboratory, this approach allows us to link maternal exposures with placental biology at multiple scales. We first analyze each data layer separately to identify exposure-associated changes. We then use pathway analysis, correlation networks, latent-factor models, multivariate integration, and machine-learning approaches to identify molecular and structural features that move together. This helps us prioritize pathways that are not only statistically altered, but also biologically connected across layers.</p>

  <p>The final goal is to build interpretable models of placental function. Instead of treating transcriptomics, proteomics, metabolomics, and histology as separate datasets, we use them as complementary views of the same biological process. This allows us to identify candidate mechanisms, generate testable hypotheses, and better understand how the placenta adapts, compensates, or fails in response to maternal exposures.</p>

  <div class="references" id="references">
    <strong>References</strong>
    <ol class="ref-list">
      <li>
        <a href="https://doi.org/10.1186/s13059-017-1215-1" target="_blank" rel="noopener">
          Hasin Y, Seldin M, Lusis A. Multi-omics approaches to disease. <em>Genome Biology</em>. 2017;18:83.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1177/1177932219899051" target="_blank" rel="noopener">
          Subramanian I, Verma S, Kumar S, Jere A, Anamika K. Multi-omics Data Integration, Interpretation, and Its Application. <em>Bioinformatics and Biology Insights</em>. 2020;14:1177932219899051.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1371/journal.pcbi.1005752" target="_blank" rel="noopener">
          Rohart F, Gautier B, Singh A, Lê Cao KA. mixOmics: An R package for ‘omics feature selection and multiple data integration. <em>PLOS Computational Biology</em>. 2017;13(11):e1005752.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1093/bioinformatics/bty1054" target="_blank" rel="noopener">
          Singh A, Shannon CP, Gautier B, et al. DIABLO: an integrative approach for identifying key molecular drivers from multi-omics assays. <em>Bioinformatics</em>. 2019;35(17):3055–3062.
        </a>
      </li>

      <li>
        <a href="https://doi.org/10.1186/s13059-020-02015-1" target="_blank" rel="noopener">
          Argelaguet R, Arnol D, Bredikhin D, et al. MOFA+: a statistical framework for comprehensive integration of multi-modal single-cell data. <em>Genome Biology</em>. 2020;21:111.
        </a>
      </li>

      <li>
        <a href="https://www.nature.com/articles/s41540-023-00301-9" target="_blank" rel="noopener">
          Bülow RD, Jäger PF, Isensee F, et al. Extending the landscape of omics technologies by pathomics. 2023.
        </a>
      </li>
    </ol>
  </div>

</div>
