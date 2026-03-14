---
title: Accueil
layout: default
hero_title: "Sigma"
hero_subtitle: "Cours • Exercices • Devoirs • Ressources"
---

## Mathématicien de la semaine

<div class="math-spotlight">

<img id="math-image" class="math-image">

<h3 id="math-name"></h3>

<p id="math-dates"></p>

<p id="math-resume"></p>

<p><strong>Apport essentiel</strong></p>

<p id="math-apport"></p>

<p id="math-citation"></p>

<div class="math-controls">
<button id="math-prev">◀</button>
<button id="math-next">▶</button>
</div>

</div>

---

## Accès rapide

<div class="cards">

<div class="card">
<h3>Seconde</h3>
<a href="/classes/seconde205/">Accéder</a>
</div>

<div class="card">
<h3>Voie générale</h3>
<a href="/classes/premiere-tronc-commun/">Accéder</a>
</div>

<div class="card">
<h3>Voie technologique</h3>
<a href="/classes/premiere-techno-tronc-commun/">Accéder</a>
</div>

<div class="card">
<h3>Post-bac</h3>
<a href="/classes/bts-mec1/">Accéder</a>
</div>

</div>

<script>

window.mathData=[

{% for m in site.data.mathematiciens %}

{
nom:{{ m.nom | jsonify }},
dates:{{ m.dates | jsonify }},
image:{{ m.image | jsonify }},
resume:{{ m.resume | jsonify }},
apport:{{ m.apport | jsonify }},
citation:{{ m.citation | jsonify }}
},

{% endfor %}

];

</script>
