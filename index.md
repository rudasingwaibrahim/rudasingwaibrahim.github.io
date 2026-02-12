---
layout: default
title: Accueil
---

<h1>Mes classes</h1>

<ul>
  {% for classe in site.data.classes %}
    <li>
      <a href="{{ classe.url }}">{{ classe.name }}</a>
      <p>{{ classe.description }}</p>
    </li>
  {% endfor %}
</ul>
