---
layout: page
title: Transcriptomics
permalink: /research/transcriptomics/
nav: false
---

<style>
.transcriptomics-page {
  font-size: 1.3rem;
  line-height: 1.8;
  width: 100%;
  display: flow-root;
}

.transcriptomics-page p {
  margin: 0 0 1.25rem 0;
}

.transcriptomics-page h2 {
  clear: both;
  margin: 2.25rem 0 1rem;
}

.transcriptomics-page h3 {
  margin: 1.65rem 0 0.65rem;
  color: var(--global-theme-color, #e83e8c);
}

.transcriptomics-page .content-figure {
  box-sizing: border-box;
}

.transcriptomics-page .content-figure img {
  width: 100%;
  height: auto;
  display: block;
}

.transcriptomics-page .content-figure figcaption {
  display: block;
  width: 100%;
  margin-top: 0.55rem;
  font-size: 1rem;
  line-height: 1.45;
  text-align: center;
}

.transcriptomics-page .figure-full-width {
  float: none;
  clear: both;
  width: min(100%, 1100px);
  margin: 1.6rem auto 2rem;
}

.transcriptomics-page .figure-pink img {
  border: 2px solid #f2a1c3;
  border-radius: 16px;
  padding: 8px;
  background: #fff7fa;
  box-sizing: border-box;
}

.transcriptomics-page .method-intro,
.transcriptomics-page .workflow-intro {
  margin-bottom: 0.75rem;
}

@media (max-width: 900px) {
  .transcriptomics-page {
    font-size: 1.15rem;
    line-height: 1.7;
  }

  .transcriptomics-page h2 {
    margin-top: 1.9rem;
  }

  .transcriptomics-page .figure-full-width {
    width: 100%;
    max-width: 100%;
    margin: 1.25rem auto 1.6rem;
  }

  .transcriptomics-page .content-figure figcaption {
    font-size: 0.95rem;
    text-align: left;
  }
}
</style>

<div class="transcriptomics-page">

  <p>Transcriptomics is the study of RNA molecules produced by cells and tissues. Together, these molecules form the <strong>transcriptome</strong>. The transcriptome shows which genes are being used when a sample is collected and how strongly they are expressed.</p>

  <p>Nearly every cell contains the same DNA, but cells use different parts of it. A trophoblast, an endothelial cell, and an immune cell have distinct functions because they express different sets of genes. Measuring RNA allows researchers to study these differences and to see how cells change during development, normal physiology, and disease.</p>

  <p>In placental research, transcriptomics reveals molecular changes in development, immune regulation, vascular function, metabolism, and nutrient transport. These measurements can identify early or subtle changes in placental cell activity.</p>

  <!-- FIGURE 1: DNA, RNA processing, and protein production -->
  <figure class="content-figure figure-full-width figure-pink">
    <img
      src="{{ '/assets/img/transcriptomics/trans1.png' | relative_url }}"
      alt="DNA is transcribed into pre-mRNA, processed and regulated to form mature mRNA, and translated into protein"
      loading="lazy"
      decoding="async">
    <figcaption>Figure 1. DNA is transcribed into pre-mRNA. Splicing, capping, polyadenylation, microRNAs, and RNA-binding proteins influence the formation, stability, and use of mature mRNA before it is translated into protein.</figcaption>
  </figure>

  <h2>From DNA to Gene Expression</h2>

  <p>DNA contains genes, which serve as biological instructions. When a cell uses a protein-coding gene, it first copies the relevant DNA sequence into a precursor RNA, or pre-mRNA, through transcription. The pre-mRNA is then processed by removing introns, joining exons, and adding a protective 5′ cap and poly(A) tail. The resulting mature mRNA can be translated by ribosomes to produce a protein.</p>

  <p>RNA abundance is also shaped after transcription. MicroRNAs and RNA-binding proteins can influence RNA processing, stability, localization, and translation. Other RNA molecules perform regulatory or structural functions without being translated into proteins. Transcriptomics captures these RNA-level patterns, but it does not directly measure protein abundance or activity.</p>

  <p>One way to picture this process is to think of DNA as a reference library. RNA represents the pages that have been selected for current use. Different cell types consult different pages, and the selection changes as cells develop or respond to their surroundings.</p>

  <p>The amount of RNA detected from a gene is commonly described as its <strong>expression level</strong>. Measuring many transcripts at once reveals patterns that describe cell identity and tissue state.</p>

  <h2>A Snapshot of Cellular Activity</h2>

  <p>The transcriptome changes over time. It varies across cell types, tissue regions, stages of pregnancy, and health conditions. A transcriptomic dataset should therefore be understood as a snapshot taken under defined biological and experimental conditions.</p>

  <p>This snapshot can show whether cells are activating inflammatory pathways, changing energy use, reorganizing the extracellular matrix, adjusting nutrient transport, or modifying blood-vessel development. Genes that change together can point to a coordinated biological program rather than an isolated event.</p>

  <p>A change in RNA may not lead to an equivalent functional change. Findings should therefore be interpreted in their anatomical context and validated experimentally.</p>

  <h2>Four Ways to Measure the Transcriptome</h2>

  <p class="method-intro">The most appropriate approach depends on whether the study requires a tissue-level average, information from individual cells or nuclei, or the location of expression within the placenta.</p>

  <h3>Bulk RNA Sequencing</h3>

  <p>Bulk RNA sequencing measures RNA collected from a piece of tissue containing many cells. The result is an average expression profile for the sample. It is similar to hearing a choir as a whole without separating each singer.</p>

  <p>This approach is useful for comparing groups, developmental stages, or clinical conditions. It can identify genes with higher or lower expression and show which biological pathways are most affected. Because many samples can be studied together, bulk RNA sequencing is well suited to identifying consistent tissue-level patterns.</p>

  <p>Signals from different cell populations are mixed. A stronger inflammatory signature could reflect more active immune cells, a greater number of immune cells, or both. Deconvolution can estimate which populations contribute, but it does not replace cell-level measurements.</p>

  <h3>Single-Cell RNA Sequencing</h3>

  <p>Single-cell RNA sequencing measures gene expression in individual cells. Cells with similar expression patterns are grouped together, allowing researchers to identify cell populations and examine their distinct states.</p>

  <p>In the placenta, this approach can distinguish trophoblast subtypes, endothelial cells, stromal cells, and maternal and fetal immune populations. It can show whether a biological change occurs broadly or is concentrated in one cell type. It can also identify uncommon cell states that may be difficult to detect in bulk tissue.</p>

  <p>Standard single-cell sequencing requires intact cells. Preparing these cells can be difficult in complex tissues and may underrepresent cells that are large, fragile, or tightly connected to surrounding structures.</p>

  <h3>Single-Nucleus RNA Sequencing</h3>

  <p>Single-nucleus RNA sequencing measures RNA contained within isolated nuclei rather than intact cells. Nuclei can often be recovered from frozen or archived tissue, making this approach useful when fresh samples are unavailable. Nuclear isolation is also gentler than whole-cell dissociation and may reduce the loss of fragile cell populations.</p>

  <p>This is particularly relevant to placental research. The syncytiotrophoblast forms a large, continuous, multinucleated layer and cannot be isolated as conventional individual cells. A nuclei-based approach can capture nuclei from this structure and improve representation of trophoblast biology. It can also be applied to placental tissues that are fibrous, difficult to dissociate, or collected through clinical studies and stored frozen.</p>

  <p>Single-nucleus data contain fewer cytoplasmic RNA molecules than whole-cell data and may provide less information for some genes. A nucleus also does not always correspond to a complete cell, especially in multinucleated tissues. These differences must be considered when annotating cell populations and comparing single-cell with single-nucleus results.</p>

  <h3>Spatial Transcriptomics</h3>

  <p>Spatial transcriptomics measures RNA while preserving information about where it was detected in a tissue section. It links gene expression with placental anatomy.</p>

  <p>This spatial information is important because the placenta is not uniform. Trophoblast layers, stromal regions, immune niches, and vascular structures occupy specific locations and perform different functions. A gene-expression change near a vessel may have a different meaning from the same change in a trophoblast-rich region.</p>

  <p>Spatial methods vary in resolution, and some capture areas contain several cells. Annotation and deconvolution help interpret these mixed signals.</p>

  <!-- FIGURE 2: Transcriptomic methods -->
  <figure class="content-figure figure-full-width figure-pink">
    <img
      src="{{ '/assets/img/transcriptomics/trans2.png' | relative_url }}"
      alt="Comparison of bulk, single-cell, single-nucleus, and spatial transcriptomics"
      loading="lazy"
      decoding="async">
    <figcaption>Figure 2. Bulk RNA sequencing measures an average tissue profile, single-cell sequencing separates intact cells, single-nucleus sequencing profiles isolated nuclei—including nuclei from frozen tissue and multinucleated trophoblast—and spatial transcriptomics maps expression within placental anatomy.</figcaption>
  </figure>

  <h2>A Typical Transcriptomics Workflow</h2>

  <p class="workflow-intro">Although the details vary among platforms, transcriptomics studies move through the same broad stages: careful experimental design, consistent sample handling, sequencing, data analysis, biological interpretation, and validation.</p>

  <h3>1. Study Design and Tissue Selection</h3>

  <p>The study begins with a defined question. Gestational age, fetal sex, tissue region, biological replication, and collection procedures are considered before sequencing.</p>

  <h3>2. Tissue and RNA</h3>

  <p>Tissue is collected consistently and preserved rapidly because RNA degrades easily. Depending on the method, RNA is obtained from bulk tissue, intact cells, isolated nuclei, or a tissue section. Sample quality is assessed before library preparation.</p>

  <h3>3. Sequencing</h3>

  <p>RNA molecules are converted into sequencing libraries and read by a sequencing instrument. The resulting short sequences provide a measurable record of the transcripts present in each sample, cell, nucleus, or spatial location.</p>

  <h3>4. Analysis</h3>

  <p>Reads are checked for quality, assigned to genes, and quantified. Statistical analysis identifies expression differences, while cell-level and spatial analyses identify the populations or regions involved. Groups of related genes can then be organized into biological pathways and processes.</p>

  <h3>5. Interpretation and Validation</h3>

  <p>Expression plots, heatmaps, cell maps, and spatial maps help researchers interpret the results in their biological context. Selected findings are then tested using targeted experiments or independent samples.</p>

  <!-- FIGURE 3: Transcriptomics workflow -->
  <figure class="content-figure figure-full-width figure-pink">
    <img
      src="{{ '/assets/img/transcriptomics/trans3.png' | relative_url }}"
      alt="Five-step transcriptomics workflow from study design to interpretation and validation"
      loading="lazy"
      decoding="async">
    <figcaption>Figure 3. A transcriptomics study moves from experimental design and tissue collection through RNA preparation, sequencing, analysis, biological interpretation, and validation.</figcaption>
  </figure>

  <h2>Interpreting the Results Carefully</h2>

  <p>Gene-expression differences show altered regulation, but they do not automatically establish altered function or causality. Results may also reflect differences in cell composition, gestational timing, tissue sampling, fetal sex, RNA quality, or technical batch.</p>

  <p>Strong conclusions rely on adequate replication, appropriate statistical models, consistent pathway-level patterns, clear anatomical context, and independent validation. This is particularly important when interpreting predicted cell communication or linking placental RNA patterns with fetal outcomes.</p>

  <h2>Why Transcriptomics Matters for Placental Health</h2>

  <p>The placenta changes throughout pregnancy as it supports fetal growth, regulates exchange, produces hormones, and maintains the maternal–fetal interface. Problems can begin at the molecular level before they produce an obvious lesion or clinical sign.</p>

  <p>Transcriptomics provides access to this hidden layer of placental biology. Bulk sequencing describes the overall tissue response, single-cell sequencing separates intact cell populations, single-nucleus sequencing improves access to frozen tissue and multinucleated trophoblast, and spatial transcriptomics shows where those responses occur.</p>

  <p>Together with experimental validation, these approaches help explain how placental cells develop, communicate, and maintain essential functions. They also provide a clearer basis for studying how placental dysfunction contributes to pregnancy complications and developmental health.</p>

</div>
