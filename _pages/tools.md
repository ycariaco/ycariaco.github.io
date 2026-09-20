---
layout: page
permalink: /tools/
title: Tools
nav: false
nav_order: x8
calendar: false
---

<style>
  .data-launch-card {
    display: grid;
    grid-template-columns: 150px minmax(0, 1fr);
    gap: clamp(28px, 5vw, 52px);
    align-items: center;
    max-width: 900px;
    margin: 42px auto 20px;
    padding: clamp(30px, 5vw, 56px);
    background: var(--global-card-bg-color, #ffffff);
    border: 1px solid var(--global-divider-color, #dedede);
    border-radius: 24px;
    box-shadow: 0 18px 50px rgba(30, 34, 40, 0.09);
  }

  .data-launch-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 150px;
    height: 150px;
  }

  .data-launch-icon svg {
    width: 100%;
    height: 100%;
  }

  .data-launch-kicker {
    margin: 0 0 8px;
    color: #ff1f78;
    font-size: 0.78rem;
    font-weight: 750;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .data-launch-title {
    margin: 0 0 14px;
    color: var(--global-text-color);
    font-size: clamp(1.8rem, 4vw, 2.6rem);
    font-weight: 720;
    line-height: 1.1;
  }

  .data-launch-description {
    max-width: 620px;
    margin: 0 0 22px;
    color: var(--global-text-color-light, #5b6475);
    font-size: 1.05rem;
    line-height: 1.65;
  }

  .data-launch-features {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 26px;
  }

  .data-launch-feature {
    padding: 7px 12px;
    color: var(--global-text-color);
    font-size: 0.82rem;
    font-weight: 600;
    background: rgba(255, 31, 120, 0.08);
    border: 1px solid rgba(255, 31, 120, 0.18);
    border-radius: 999px;
  }

  .data-launch-button {
    display: inline-flex;
    gap: 10px;
    align-items: center;
    padding: 13px 21px;
    color: #ffffff !important;
    font-weight: 700;
    text-decoration: none !important;
    background: #ff1f78;
    border-radius: 11px;
    box-shadow: 0 8px 20px rgba(255, 31, 120, 0.23);
    transition:
      transform 160ms ease,
      box-shadow 160ms ease,
      background 160ms ease;
  }

  .data-launch-button:hover {
    color: #ffffff !important;
    background: #e8186a;
    box-shadow: 0 11px 26px rgba(255, 31, 120, 0.3);
    transform: translateY(-2px);
  }

  .data-launch-button svg {
    width: 18px;
    height: 18px;
  }

  .data-launch-note {
    max-width: 780px;
    margin: 20px auto;
    color: var(--global-text-color-light, #667085);
    font-size: 0.82rem;
    line-height: 1.55;
    text-align: center;
  }

  @media (max-width: 700px) {
    .data-launch-card {
      grid-template-columns: 1fr;
      margin-top: 28px;
      text-align: center;
    }

    .data-launch-icon {
      width: 125px;
      height: 125px;
      margin: 0 auto;
    }

    .data-launch-description {
      margin-right: auto;
      margin-left: auto;
    }

    .data-launch-features {
      justify-content: center;
    }
  }
</style>

<div class="data-launch-card">
  <div class="data-launch-icon" aria-hidden="true">
    <svg viewBox="0 0 144 144" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="6" width="132" height="132" rx="32" fill="#FFF2F7"/>
      <rect x="6" y="6" width="132" height="132" rx="32" stroke="#FFB7D2" stroke-width="2"/>
      
      <path d="M35 104V39M35 104H112" stroke="#333333" stroke-width="5" stroke-linecap="round"/>
      
      <rect x="47" y="77" width="15" height="27" rx="4" fill="#FF1F78"/>
      <rect x="69" y="60" width="15" height="44" rx="4" fill="#F45B5B"/>
      <rect x="91" y="47" width="15" height="57" rx="4" fill="#6695FF"/>
      
      <path d="M53 62L76 49L98 32L113 40" stroke="#333333" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
      
      <circle cx="53" cy="62" r="5" fill="#FF1F78"/>
      <circle cx="76" cy="49" r="5" fill="#F45B5B"/>
      <circle cx="98" cy="32" r="5" fill="#6695FF"/>
      <circle cx="113" cy="40" r="5" fill="#333333"/>
    </svg>
  </div>

  <div>
    <p class="data-launch-kicker">Lab Research Tool</p>
    <h2 class="data-launch-title">Data Explorer</h2>

    <p class="data-launch-description">
      Create customizable figures and perform exploratory analyses directly
      in your browser. Your data remain on your device.
    </p>

    <div class="data-launch-features">
      <span class="data-launch-feature">Publication-ready figures</span>
      <span class="data-launch-feature">Exploratory statistics</span>
      <span class="data-launch-feature">No data uploads</span>
    </div>

    <a
      class="data-launch-button"
      href="https://cariaco-lab-data-explorer.pages.dev/"
      target="_blank"
      rel="noopener noreferrer"
    >
      Launch Data Explorer
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
        <path d="M14 5H19V10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M19 5L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M19 13V18C19 18.55 18.55 19 18 19H6C5.45 19 5 18.55 5 18V6C5 5.45 5.45 5 6 5H11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </a>
  </div>
</div>

<p class="data-launch-note">
  Intended for data exploration and visualization. Confirm critical statistical
  analyses using validated statistical software.
</p>
