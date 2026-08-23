---
layout: page
title: News
permalink: /news/
nav: true
nav_order: 6
---

<br>

<div class="news-container">

  <div class="news-item">
    <div class="news-date">September 2026</div>
    <div class="news-content">
      <h3>Elisabeth Starts Her Master's</h3>
      <p>
        Elisabeth Mouge begins her Master's in Biology at UQAM with the support of FRQ and NSERC scholarships. Congratulations, Elisabeth!
      </p>
    </div>
  </div>

  <div class="news-item">
    <div class="news-date">July 2026</div>
    <div class="news-content">
      <h3>Cariaco Lab Opens at UQAM</h3>
      <p>
        The Cariaco Lab officially launched in the Department of Biological Sciences at Université du Québec à Montréal (UQAM).
      </p>
    </div>
  </div>

</div>

<style>
.news-container {
  max-width: 1000px;
  margin: 0 auto;
}

.news-item {
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 25px;
  padding: 20px 0;
  border-bottom: 1px solid #e5e5e5;
}

.news-date {
  font-weight: 600;
  color: #e91e63;
}

.news-content h3 {
  margin: 0 0 8px 0;
  font-size: 1.2rem;
}

.news-content p {
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 700px) {
  .news-item {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
</style>
