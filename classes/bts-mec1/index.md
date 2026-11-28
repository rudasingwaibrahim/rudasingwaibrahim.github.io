---
title: BTS MEC — Management économique de la construction — 1re année
permalink: /classes/bts-mec1/
classe: bts-mec1
hero_title: BTS MEC — Management économique de la construction — 1re année
hero_subtitle: "Management économique de la construction · Mathématiques"
description: "BTS Management économique de la construction (MEC), 1re année : cours, exercices, devoirs et corrigés de mathématiques et séances de co-enseignement."
programme: "Programme de 1re année = modules de la 1re situation d'évaluation du CCF : calcul et numération, éléments d'algorithmique et de programmation, configurations géométriques, calcul vectoriel, fonctions d'une variable réelle."
chapitres:
- num: 1
  titre: "Calcul et numération"
  url: /classes/bts-mec1/chapitre1/
- num: 2
  titre: "Éléments d'algorithmique et de programmation"
  url: /classes/bts-mec1/chapitre2/
- num: 3
  titre: "Configurations géométriques"
  url: /classes/bts-mec1/chapitre3/
- num: 4
  titre: "Calcul vectoriel"
  url: /classes/bts-mec1/chapitre4/
- num: 5
  titre: "Fonctions d'une variable réelle"
  url: /classes/bts-mec1/chapitre5/
---

<div class="mec-tabs">
<div class="mec-tablist" role="tablist" aria-label="Enseignements du BTS MEC 1re année">
  <button type="button" role="tab" id="tab-maths" aria-controls="panel-maths" aria-selected="true" tabindex="0" data-hash="maths">Mathématiques</button>
  <button type="button" role="tab" id="tab-co" aria-controls="panel-co" aria-selected="false" tabindex="-1" data-hash="co-enseignement">Co-enseignement</button>
</div>

<section class="mec-panel" role="tabpanel" id="panel-maths" aria-labelledby="tab-maths" tabindex="0">
{% include chapter-list.html %}
</section>

<section class="mec-panel" role="tabpanel" id="panel-co" aria-labelledby="tab-co" tabindex="0" hidden>
<p class="lead">Une heure par semaine en 1re année : mathématiques et enseignement professionnel ensemble, sur des situations de chantier et d'économie de la construction (référentiel, note 7 de la grille horaire). Les séances s'appuient sur les chapitres 1, 2 et 3.</p>
<ol class="mec-seances">
  <li><b>Numération et informatique de chantier</b> — bases 2 et 16, octets, durées en base 60 (relevés horaires, planning). <a href="/classes/bts-mec1/chapitre1/">Chapitre 1</a></li>
  <li><b>Pourcentages et devis</b> — TVA, remises successives, acomptes, indices simples en base 100 (prix d'un matériau), évolutions des coûts. <a href="/classes/bts-mec1/chapitre1/">Chapitre 1</a></li>
  <li><b>Premiers programmes Python</b> — types, saisie, conditions : tarif de livraison selon la surface, volume d'une dalle. <a href="/classes/bts-mec1/chapitre2/">Chapitre 2</a></li>
  <li><b>Boucles, fonctions et listes</b> — métré cumulé de murs, nombre d'années pour qu'un coût double, graphiques de coûts. <a href="/classes/bts-mec1/chapitre2/">Chapitre 2</a></li>
  <li><b>Bases de données de chantier</b> — matériaux, fournisseurs, commandes : requêtes SQL, montant d'une commande. <a href="/classes/bts-mec1/chapitre2/">Chapitre 2</a></li>
  <li><b>Métrés et quantitatifs</b> — périmètres, surfaces de plancher, aires de carrelage, volumes de béton et de terrassement. <a href="/classes/bts-mec1/chapitre3/">Chapitre 3</a></li>
  <li><b>Pentes, toitures et escaliers</b> — pente en pourcentage, longueur de chevrons, giron et hauteur de marche. <a href="/classes/bts-mec1/chapitre3/">Chapitre 3</a></li>
</ol>
<p class="mec-note">Les évaluations de co-enseignement (devoirs sur table) sont disponibles sur demande auprès du professeur.</p>
</section>
</div>

<style>
.mec-tablist{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 1.5rem;border-bottom:1px solid var(--line)}
.mec-tablist [role=tab]{font:inherit;font-weight:700;padding:12px 18px;min-height:48px;border:1px solid var(--line);border-bottom:0;border-radius:var(--radius-sm) var(--radius-sm) 0 0;background:transparent;color:inherit;cursor:pointer}
.mec-tablist [role=tab][aria-selected=true]{background:var(--gold-bright);color:#1a1405;border-color:var(--gold-bright)}
.mec-tablist [role=tab]:focus-visible{outline:3px solid var(--gold-bright);outline-offset:2px}
.mec-panel:focus-visible{outline:2px dashed var(--gold);outline-offset:6px}
.mec-seances{padding-left:1.4rem;line-height:1.6}
.mec-seances li{margin:.6rem 0}
.mec-note{opacity:.85;font-size:.95em}
@media (max-width:560px){.mec-tablist [role=tab]{flex:1 1 0;padding:12px 8px}}
</style>
<script>
(function(){
  var tabs=[].slice.call(document.querySelectorAll('.mec-tablist [role=tab]'));
  if(!tabs.length)return;
  function sel(t,focus,push){
    tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on?'true':'false');x.tabIndex=on?0:-1;
      document.getElementById(x.getAttribute('aria-controls')).hidden=!on;});
    if(focus)t.focus();
    if(push&&history.replaceState)history.replaceState(null,'','#'+t.dataset.hash);
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){sel(t,false,true);});
    t.addEventListener('keydown',function(e){var k=e.key,j=null;
      if(k==='ArrowRight')j=(i+1)%tabs.length;else if(k==='ArrowLeft')j=(i-1+tabs.length)%tabs.length;else if(k==='Home')j=0;else if(k==='End')j=tabs.length-1;
      if(j!==null){e.preventDefault();sel(tabs[j],true,true);}});
  });
  function fromHash(){var h=location.hash.slice(1);tabs.forEach(function(t){if(t.dataset.hash===h)sel(t,false,false);});}
  fromHash();window.addEventListener('hashchange',fromHash);
})();
</script>

