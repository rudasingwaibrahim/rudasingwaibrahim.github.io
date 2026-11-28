---
title: "Chapitre 2 — Éléments d'algorithmique et de programmation"
permalink: /classes/bts-mec1/chapitre2/
hero_title: Chapitre 2
hero_subtitle: "Éléments d'algorithmique et de programmation"
activites:
- titre: Activités — Version élève
  pdf: bts-mec1-ch2-activites.pdf
- titre: Activités — Version professeur
  pdf: bts-mec1-ch2-activites-prof.pdf
cours:
- titre: Cours — Version élève
  pdf: bts-mec1-ch2-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: bts-mec1-ch2-cours-prof.pdf
planches:
- num: 1
  themes: "Types · Conditions · Fonctions · Boucles"
  pdf: bts-mec1-ch2-planche-01.pdf
- num: 2
  themes: "Listes · Bibliothèques · Bases de données SQL"
  pdf: bts-mec1-ch2-planche-02.pdf
dm:
- num: 1
  contenu: "Boucles · Fonctions · Programmes à corriger"
  duree: "1 semaine"
  pdf: bts-mec1-ch2-dm-01-sujet.pdf
- num: 2
  contenu: "Fonctions · Listes · Requêtes SQL"
  duree: "1 semaine"
  pdf: bts-mec1-ch2-dm-02-sujet.pdf
ds_blancs:
- num: 1
  contenu: "CCF situation n° 1 · Types, fonctions, conditions, boucles"
  duree: "55 min · /10"
  pdf: bts-mec1-ch2-dsblanc-01-sujet.pdf
  correction: bts-mec1-ch2-dsblanc-01-corrige.pdf
- num: 2
  contenu: "CCF situation n° 1 · Bases de données, listes"
  duree: "55 min · /10"
  pdf: bts-mec1-ch2-dsblanc-02-sujet.pdf
  correction: bts-mec1-ch2-dsblanc-02-corrige.pdf
ds_published: false
ds:
- num: 1
  pdf: bts-mec1-ch2-ds-01-sujet.pdf
- num: 2
  pdf: bts-mec1-ch2-ds-02-sujet.pdf
- num: 3
  pdf: bts-mec1-ch2-ds-03-sujet.pdf
erreurs:
- "Oublier l'indentation : le bloc d'un if, d'un for ou d'une fonction doit être décalé"
- "Confondre = (affectation) et == (test d'égalité)"
- "Croire que range(1, 5) va jusqu'à 5 : il s'arrête à 4"
- "Oublier que les indices d'une liste commencent à 0 : le premier élément est L[0]"
- "Additionner une chaîne et un nombre : \"12\" + 3 provoque une erreur, int(\"12\") + 3 vaut 15"
- "Oublier de convertir input() avec int() ou float()"
- "En SQL, oublier la condition de jointure ON clé étrangère = clé primaire"
---
{% include cours-cards.html %}

<section class="mec-data" aria-labelledby="t-chantiers">
<h2 id="t-chantiers">Base de données « chantiers »</h2>
<p>La base du cours (§ 6.1), à ouvrir avec un utilitaire de base de données (par exemple DB Browser for SQLite), et les mêmes tables au format CSV pour s'entraîner à l'import depuis un tableur.</p>
<ul>
  <li><a href="/assets/data/bts-mec1-ch2/chantiers.db" download>chantiers.db</a> — base SQLite : tables <code>fournisseur</code>, <code>materiau</code>, <code>commande</code></li>
  <li><a href="/assets/data/bts-mec1-ch2/fournisseur.csv" download>fournisseur.csv</a> · <a href="/assets/data/bts-mec1-ch2/materiau.csv" download>materiau.csv</a> · <a href="/assets/data/bts-mec1-ch2/commande.csv" download>commande.csv</a> — les trois tables, une ligne d'en-têtes</li>
  <li><a href="/assets/data/bts-mec1-ch2/engin.csv" download>engin.csv</a> — liste des engins à importer (planche 2, exercice « Import CSV »)</li>
</ul>
</section>
