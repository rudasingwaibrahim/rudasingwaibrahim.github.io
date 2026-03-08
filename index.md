---
title: Accueil
layout: default
hero_title: "Sigma"
hero_subtitle: "Cours • Exercices • Devoirs • Ressources"
---

## Bienvenue

Choisis ta classe pour accéder aux cours, exercices, devoirs et corrigés.

<div class="cards">
  <div class="card">
    <div class="card__title">Seconde 205</div>
    <a href="/classes/seconde205/">Accéder</a>
  </div>

  <div class="card">
    <div class="card__title">Seconde 219</div>
    <a href="/classes/seconde219/">Accéder</a>
  </div>

  <div class="card">
    <div class="card__title">TSTMG RH T19</div>
    <a href="/classes/tstmg-t19/">Accéder</a>
  </div>

  <div class="card">
    <div class="card__title">Tale Techno Spé</div>
    <a href="/classes/tale-techno-spe/">Accéder</a>
  </div>

  <div class="card">
    <div class="card__title">BTS MEC1</div>
    <a href="/classes/bts-mec1/">Accéder</a>
  </div>
</div>

## Mathématicien de la semaine

<div class="math-spotlight" id="math-spotlight">
  <div class="math-spotlight-card">
    <img id="math-image" class="math-image" src="" alt="">
    <h3 id="math-name"></h3>
    <p id="math-dates" class="math-dates"></p>
    <p id="math-resume"></p>

    <div class="math-box">
      <strong>Apport essentiel</strong><br>
      <span id="math-apport"></span>
    </div>

    <p id="math-citation" class="math-citation"></p>

    <div class="math-controls">
      <button type="button" id="math-prev">◀ Précédent</button>
      <button type="button" id="math-next">Suivant ▶</button>
    </div>
  </div>
</div>

<script>
  window.mathData = [
    {% for m in site.data.mathematiciens %}
    {
      nom: {{ m.nom | jsonify }},
      dates: {{ m.dates | jsonify }},
      image: {{ m.image | jsonify }},
      resume: {{ m.resume | jsonify }},
      apport: {{ m.apport | jsonify }},
      citation: {{ m.citation | jsonify }}
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ];
</script>
