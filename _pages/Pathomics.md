---
layout: page
title: Pathomics
permalink: /research/pathomics/
nav: false
---

<style>
.pathomics-page {
  font-size: 1.3rem;
  line-height: 1.8;
  width: 100%;
  display: flow-root; /* keeps floats inside the container */
}

.pathomics-page p {
  margin: 0 0 1.25rem 0;
}

.pathomics-page .content-figure {
  width: clamp(280px, 30vw, 420px);
  margin: 0.25rem 0 1rem 0;
  box-sizing: border-box;
}

.pathomics-page .figure-right {
  float: right;
  margin-left: 1.25rem;
  clear: right;
}

.pathomics-page .figure-left {
  float: left;
  margin-right: 1.25rem;
  clear: left;
}

.pathomics-page .figure-large {
  width: clamp(440px, 52vw, 680px);
}

.pathomics-page .content-figure img,
.pathomics-page .content-figure video {
  width: 100%;
  height: auto;
  display: block;
}

.pathomics-page .content-figure figcaption {
  display: block;
  width: 100%;
  text-align: left;
  margin-top: 0.4rem;
  font-size: 1rem;
  line-height: 1.4;
}

.pathomics-page .figure-pink img,
.pathomics-page .figure-pink video {
  border: 2px solid #f2a1c3;
  border-radius: 16px;
  padding: 6px;
  background: #ffe9f2;
  box-sizing: border-box;
}

.pathomics-page .figure-nudge-up {
  margin-top: -1rem;
}

/* Figure 1: centered and full page width */
.pathomics-page .figure-full-width {
  float: none;
  clear: both;
  width: 100%;
  max-width: 100%;
  margin: 1.5rem auto 1.75rem auto;
}

.pathomics-page .figure-full-width img,
.pathomics-page .figure-full-width video {
  width: 100%;
  max-width: 100%;
  height: auto;
}

.pathomics-page .figure-full-width figcaption {
  text-align: center;
}

.pathomics-page .ref-list {
  padding-left: 1.4rem;
  margin-top: 0.75rem;
}

.pathomics-page .ref-list li {
  margin-bottom: 0.8rem;
  font-size: 1rem;
  line-height: 1.5;
}

.pathomics-page .ref-list a {
  color: inherit;
  text-decoration: none;
}

.pathomics-page .ref-list a:hover {
  text-decoration: underline;
}

@media (max-width: 900px) {
  .pathomics-page {
    font-size: 1.15rem;
    line-height: 1.7;
  }

  .pathomics-page .content-figure {
    float: none;
    width: 100%;
    max-width: 100%;
    margin: 1rem 0;
  }

  .pathomics-page .figure-full-width {
    width: 100%;
    margin: 1.25rem auto 1.5rem auto;
  }

  .pathomics-page .ref-list li {
    font-size: 0.95rem;
  }
}
</style>

<div class="pathomics-page">

  <p>Pathomics refers to the high-throughput quantitative analysis of digital histopathology images, typically whole-slide images, to extract measurable information about tissue architecture, cell morphology, texture, and spatial organization. By transforming placental histology into structured quantitative data, pathomics complements conventional microscopy and enables more reproducible and scalable assessment of placental structure and disease. This is particularly valuable for the placenta, an organ characterized by marked spatial heterogeneity and dynamic changes across gestation.</p>

  <!-- FIGURE 1: Overview schematic -->
  <figure class="content-figure figure-full-width figure-pink">
    <img
      src="{{ '/assets/img/placental_pathomics_workflow.svg' | relative_url }}"
      alt="Pathomics overview schematic">
    <figcaption>Figure 1. Overview of the pathomics workflow in placental histology.</figcaption>
  </figure>

  <p>Recent placental applications illustrate this potential: deep learning models such as GestAltNet have estimated gestational age from placental whole-slide images; hierarchical convolutional approaches have identified decidual vasculopathy; whole-slide learning models have classified villous infarction and other parenchymal lesions; and computational pathology models have distinguished preeclamptic placentas from controls.</p>

  <!-- FIGURE 2: Example model results -->
  <figure class="content-figure figure-left figure-pink">
    <img
      src="{{ '/assets/img/HAPPY.gif' | relative_url }}"
      alt="Example model results">
    <figcaption>Figure 2. HAPPY-based cell classification in our human placental samples.</figcaption>
  </figure>

  <p>Notably, the HAPPY pipeline (Histology Analysis Pipeline.PY) provides a biologically interpretable framework for quantifying nuclei, cell types, and tissue microstructures across placenta whole-slide images, and subsequent work has shown that lesion-associated changes can extend beyond visibly abnormal regions. We are now applying this framework in our laboratory to generate quantitative whole-slide human placental phenotypes in our own cohorts (Figure 2), while also developing AI-powered image analysis and deep learning workflows to segment tissue regions, classify cell types, and quantify their spatial organization in mouse placentas (Figure 3).</p>

  <!-- FIGURE 3: Tissue microstructure quantification -->
  <figure class="content-figure figure-right figure-large figure-pink">
    <img
      src="{{ '/assets/img/Mouse_placenta_AI.png' | relative_url }}"
      alt="Tissue microstructure quantification">
    <figcaption>Figure 3. AI-based whole-slide tissue segmentation of mouse placenta generated by our own in-house pipeline.</figcaption>
  </figure>

  <p>Together, these studies suggest that placental pathomics can improve diagnostic reproducibility, reveal subtle disease-associated morphology, and support biomarker discovery, although broader validation and standardization are still needed for routine clinical implementation.</p>

  <strong>References</strong>
  <ol class="ref-list">
    <li>
      <a href="https://www.nature.com/articles/s41540-023-00301-9" target="_blank" rel="noopener">
        Bülow RD, Jäger PF, Isensee F, et al. Extending the landscape of omics technologies by pathomics. 2023.
      </a>
    </li>

    <li>
      <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC10900832/" target="_blank" rel="noopener">
        Hosseini MS, Bera K, Wang S, et al. Computational pathology: A survey review and the way forward. 2024.
      </a>
    </li>

    <li>
      <a href="https://www.nature.com/articles/s41374-021-00579-5" target="_blank" rel="noopener">
        Mobadersany P, Cooper LAD, Goldstein JA. GestAltNet: aggregation and attention to improve deep learning of gestational age from placental whole-slide images. 2021.
      </a>
    </li>

    <li>
      <a href="https://pubmed.ncbi.nlm.nih.gov/32679230/" target="_blank" rel="noopener">
        Clymer D, Jimenez JA, Mamoon A, et al. Decidual vasculopathy identification in whole slide images using multiresolution hierarchical convolutional neural networks. 2020.
      </a>
    </li>

    <li>
      <a href="https://www.nature.com/articles/s41467-024-46986-2" target="_blank" rel="noopener">
        Vanea C, Campbell J, Dodi O, et al. Mapping cell-to-tissue graphs across human placenta histology whole slide images using deep learning with HAPPY. 2024.
      </a>
    </li>

    <li>
      <a href="https://www.biorxiv.org/content/10.64898/2025.12.22.693945v1" target="_blank" rel="noopener">
        Walker EC, Vanea C, Ernst LM, et al. Biologically Inspired Digital Histology for Deep Phenotyping of Placental Composition Changes Across Major Lesion Types. 2025.
      </a>
    </li>

    <li>
      <a href="https://www.mdpi.com/2313-433X/11/4/110" target="_blank" rel="noopener">
        d’Amati A, Baldini GM, Difonzo T, et al. Artificial Intelligence in Placental Pathology: New Diagnostic Imaging Tools in Evolution and in Perspective. 2025.
      </a>
    </li>
  </ol>

</div>
