---
title: Accueil
layout: default
hero_title: "Sigma"
hero_subtitle: "Cours • Exercices • Devoirs • Ressources"
---

## Mathématicien de la semaine

<img id="math-image" class="math-image">

### <span id="math-name"></span>

<p id="math-dates"></p>

<p id="math-resume"></p>

**Apport essentiel**

<p id="math-apport"></p>

<p id="math-citation"></p>

<button id="math-prev">◀</button>
<button id="math-next">▶</button>

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
