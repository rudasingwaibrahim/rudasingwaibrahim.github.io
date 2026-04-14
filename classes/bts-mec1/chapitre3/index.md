---
title: "Chapitre 3 - Calcul intégral"
permalink: /classes/bts-mec1/chapitre3/
hero_title: "Chapitre 3"
hero_subtitle: "Calcul intégral"
---

<style>
.ch-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; margin: 1.2rem 0 2rem; }
.ch-card { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border-radius: 10px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); text-decoration: none; color: inherit; transition: background 0.15s, border-color 0.15s; }
.ch-card:hover { background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.3); text-decoration: none; }
.ch-icon { font-size: 28px; flex-shrink: 0; }
.ch-info { display: flex; flex-direction: column; gap: 2px; }
.ch-title { font-weight: 600; font-size: 0.95rem; }
.ch-sub { font-size: 0.78rem; opacity: 0.65; }
.ch-badge { display: inline-block; margin-top: 5px; padding: 2px 9px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; background: rgba(99,179,255,0.18); color: #63b3ff; border: 1px solid rgba(99,179,255,0.3); width: fit-content; }
.ch-badge.dm   { background: rgba(154,230,180,0.15); color: #68d391; border-color: rgba(154,230,180,0.3); }
.ch-badge.dsb  { background: rgba(246,173,85,0.15);  color: #f6ad55; border-color: rgba(246,173,85,0.3); }
.ch-badge.soon { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.4); border-color: rgba(255,255,255,0.15); cursor: default; pointer-events: none; }
.ch-sep { border: none; border-top: 1px solid rgba(255,255,255,0.1); margin: 2rem 0; }
.ch-section-title { font-size: 1.05rem; font-weight: 700; margin: 0 0 0.8rem; opacity: 0.9; letter-spacing: 0.02em; }
.ch-link-row { display: flex; align-items: flex-start; gap: 14px; padding: 13px 18px; border-radius: 10px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); margin-bottom: 10px; }
.ch-link-row .ch-icon { font-size: 22px; margin-top: 2px; }
.ch-link-body { display: flex; flex-direction: column; gap: 3px; }
.ch-link-name { font-weight: 600; font-size: 0.9rem; }
.ch-link-desc { font-size: 0.78rem; opacity: 0.6; }
.ch-link-btn { display: inline-block; margin-top: 6px; padding: 4px 14px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; background: rgba(99,179,255,0.15); color: #63b3ff; border: 1px solid rgba(99,179,255,0.3); text-decoration: none; width: fit-content; transition: background 0.15s; }
.ch-link-btn:hover { background: rgba(99,179,255,0.28); text-decoration: none; }
.ch-errors { background: rgba(229,62,62,0.08); border: 1px solid rgba(229,62,62,0.25); border-radius: 10px; padding: 16px 20px; }
.ch-errors li { font-size: 0.85rem; opacity: 0.85; margin-bottom: 5px; }
</style>

## 📘 Cours

<div class="ch-grid">
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-cours-eleve.pdf">
    <span class="ch-icon">📄</span>
    <div class="ch-info">
      <span class="ch-title">Cours — Version élève</span>
      <span class="ch-sub">Espaces de réponse, tableaux à compléter</span>
      <span class="ch-badge">PDF</span>
    </div>
  </a>
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-cours-prof.pdf">
    <span class="ch-icon">📘</span>
    <div class="ch-info">
      <span class="ch-title">Cours — Version professeur</span>
      <span class="ch-sub">Corrections complètes incluses</span>
      <span class="ch-badge">PDF</span>
    </div>
  </a>
</div>

<hr class="ch-sep">

## 📝 Planches d'exercices

<div class="ch-grid">
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-planche-01.pdf">
    <span class="ch-icon">🗒️</span>
    <div class="ch-info">
      <span class="ch-title">Planche 1</span>
      <span class="ch-sub">Primitives · IPP · Changement de variable</span>
      <span class="ch-badge">PDF</span>
    </div>
  </a>
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-planche-02.pdf">
    <span class="ch-icon">🗒️</span>
    <div class="ch-info">
      <span class="ch-title">Planche 2</span>
      <span class="ch-sub">Aires · Valeur moyenne · Applications BTP</span>
      <span class="ch-badge">PDF</span>
    </div>
  </a>
</div>

<hr class="ch-sep">

## 🏠 Devoirs maison

<div class="ch-grid">
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-dm-01-sujet.pdf">
    <span class="ch-icon">🏠</span>
    <div class="ch-info">
      <span class="ch-title">DM 1</span>
      <span class="ch-sub">Primitives · Déblai · Énergie solaire</span>
      <span class="ch-badge dm">1 semaine · PDF</span>
    </div>
  </a>
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-dm-02-sujet.pdf">
    <span class="ch-icon">🏠</span>
    <div class="ch-info">
      <span class="ch-title">DM 2</span>
      <span class="ch-sub">Valeur moyenne · IPP double · Réservoir · Thermique</span>
      <span class="ch-badge dm">1 semaine · PDF</span>
    </div>
  </a>
</div>

<hr class="ch-sep">

## ✍️ Devoirs surveillés blancs

<div class="ch-grid">
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-dsblanc-01-sujet.pdf">
    <span class="ch-icon">✍️</span>
    <div class="ch-info">
      <span class="ch-title">DS Blanc 1</span>
      <span class="ch-sub">Vérifications · Intégrales · IPP · Flux thermique</span>
      <span class="ch-badge dsb">55 min · PDF</span>
    </div>
  </a>
  <a class="ch-card" href="/assets/pdf/bts-mec1/bts-calcul-integral-dsblanc-02-sujet.pdf">
    <span class="ch-icon">✍️</span>
    <div class="ch-info">
      <span class="ch-title">DS Blanc 2</span>
      <span class="ch-sub">Primitives · Intégrales · Toiture parabolique</span>
      <span class="ch-badge dsb">55 min · PDF</span>
    </div>
  </a>
</div>

<hr class="ch-sep">

## 🧪 Devoirs surveillés

<div class="ch-grid">
  <div class="ch-card">
    <span class="ch-icon">🔒</span>
    <div class="ch-info">
      <span class="ch-title">DS 1 · DS 2 · DS 3</span>
      <span class="ch-sub">Publiés après le passage du contrôle</span>
      <span class="ch-badge soon">À venir</span>
    </div>
  </div>
</div>

<hr class="ch-sep">

## 📁 Divers

### ⚠️ Erreurs fréquentes

<div class="ch-errors">
<ul>
<li>Oublier la constante <code>+ C</code> dans les primitives indéfinies</li>
<li>Confondre dérivée et primitive d'une fonction</li>
<li>Mal appliquer la linéarité de l'intégrale</li>
<li>Inverser les bornes sans changer le signe</li>
<li>Oublier la valeur absolue pour l'aire entre deux courbes</li>
<li>Confondre aire algébrique et aire géométrique</li>
<li>Erreurs dans les primitives usuelles : sin, cos, exp, puissances</li>
</ul>
</div>

<hr class="ch-sep">

### 🔗 Liens utiles

<p class="ch-section-title">🧮 Calculer et vérifier</p>

<div class="ch-link-row">
  <span class="ch-icon">🔢</span>
  <div class="ch-link-body">
    <span class="ch-link-name">Wolfram Alpha</span>
    <span class="ch-link-desc">Calcule primitives et intégrales définies avec toutes les étapes détaillées</span>
    <a class="ch-link-btn" href="https://www.wolframalpha.com/calculators/integral-calculator/" target="_blank" rel="noopener">→ Ouvrir Wolfram Alpha</a>
  </div>
</div>

<div class="ch-link-row">
  <span class="ch-icon">📐</span>
  <div class="ch-link-body">
    <span class="ch-link-name">GeoGebra — Visualiser l'intégrale</span>
    <span class="ch-link-desc">Applet interactif : modifier les bornes et voir l'aire colorée se mettre à jour en temps réel</span>
    <a class="ch-link-btn" href="https://www.geogebra.org/m/ACVXrSjF" target="_blank" rel="noopener">→ Ouvrir l'applet</a>
  </div>
</div>

<div class="ch-link-row">
  <span class="ch-icon">📊</span>
  <div class="ch-link-body">
    <span class="ch-link-name">GeoGebra — Méthode des rectangles</span>
    <span class="ch-link-desc">Comprendre d'où vient la définition de l'intégrale par approximation rectangulaire</span>
    <a class="ch-link-btn" href="https://www.geogebra.org/m/hwdV4TyX" target="_blank" rel="noopener">→ Ouvrir l'applet</a>
  </div>
</div>

<div class="ch-link-row">
  <span class="ch-icon">⚙️</span>
  <div class="ch-link-body">
    <span class="ch-link-name">GeoGebra Calculatrice</span>
    <span class="ch-link-desc">Taper <code>Integrale(f(x), a, b)</code> pour calculer directement n'importe quelle intégrale</span>
    <a class="ch-link-btn" href="https://www.geogebra.org/calculator" target="_blank" rel="noopener">→ Ouvrir la calculatrice</a>
  </div>
</div>

<div class="ch-link-row">
  <span class="ch-icon">⚙️</span>
  <div class="ch-link-body">
    <span class="ch-link-name">Symbolab</span>
    <span class="ch-link-desc">Primitives et intégrales avec étapes détaillées en français, idéal pour vérifier ses calculs</span>
    <a class="ch-link-btn" href="https://www.symbolab.com/solver/integral-calculator" target="_blank" rel="noopener">→ Ouvrir Symbolab</a>
  </div>
</div>

<p class="ch-section-title" style="margin-top:1.5rem">📖 Cours et exercices</p>

<div class="ch-link-row">
  <span class="ch-icon">📚</span>
  <div class="ch-link-body">
    <span class="ch-link-name">Bibm@th</span>
    <span class="ch-link-desc">Cours complet et exercices corrigés BTS Analyse — intégration</span>
    <a class="ch-link-btn" href="https://www.bibmath.net/ressources/index.php?action=affiche&quoi=bts/analyse/integration.html" target="_blank" rel="noopener">→ Ouvrir Bibm@th</a>
  </div>
</div>

<div class="ch-link-row">
  <span class="ch-icon">📝</span>
  <div class="ch-link-body">
    <span class="ch-link-name">Math'O karé</span>
    <span class="ch-link-desc">Cours illustré avec applets GeoGebra intégrés directement dans la page</span>
    <a class="ch-link-btn" href="https://mathokare.re/2021/06/07/tc-calcul-integral/" target="_blank" rel="noopener">→ Ouvrir Math'O karé</a>
  </div>
</div>

<div class="ch-link-row">
  <span class="ch-icon">🎓</span>
  <div class="ch-link-body">
    <span class="ch-link-name">Mon lycée numérique</span>
    <span class="ch-link-desc">Cours avec outils Xcas et Python en ligne pour calculer des intégrales</span>
    <a class="ch-link-btn" href="http://www.monlyceenumerique.fr/maths_en1/integrale/integrale.html" target="_blank" rel="noopener">→ Ouvrir le cours</a>
  </div>
</div>
