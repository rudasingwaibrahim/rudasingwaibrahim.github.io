---
title: Chapitre 7 — Généralités sur les suites
permalink: /classes/premiere-spe-maths/chapitre7/
dossier_pdf: premiere-spe-maths
hero_title: Chapitre 7
hero_subtitle: Suites — Modes de définition et sens de variation
cours:
- titre: Cours — Version élève
  pdf: premiere-spe-ch7-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: premiere-spe-ch7-cours-prof.pdf
planches:
- num: 1
  pdf: premiere-spe-ch7-planche-01.pdf
- num: 2
  pdf: premiere-spe-ch7-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: "Suites explicites et récurrentes · Fibonacci · Seuil"
  duree: "1 semaine"
  pdf: premiere-spe-ch7-dm-01-sujet.pdf
- num: 2
  contenu: "Sens de variation · Seuil · Somme des carrés"
  duree: "1 semaine"
  pdf: premiere-spe-ch7-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: "Premiers termes · Conjecture · Syracuse"
  duree: "55 min"
  pdf: premiere-spe-ch7-dsblanc-01-sujet.pdf
- num: 2
  contenu: "Sens de variation · Seuils · Modélisation"
  duree: "55 min"
  pdf: premiere-spe-ch7-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: premiere-spe-ch7-activites.pdf
- titre: Activités — Version professeur
  pdf: premiere-spe-ch7-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: premiere-spe-ch7-ds-01-sujet.pdf
- num: 2
  pdf: premiere-spe-ch7-ds-02-sujet.pdf
- num: 3
  pdf: premiere-spe-ch7-ds-03-sujet.pdf
python:
- titre: "Calculer les termes d'une suite"
  fichier: /assets/python/premiere-spe-maths/ch7-generalites-suites.ipynb
  module: /assets/python/premiere-spe-maths/verif_1spe_ch7.py
  duree: "40 min"
  contenu: "Termes explicites et par récurrence · Liste et somme de termes · Seuil et limite · Fibonacci, Syracuse"
erreurs:
- "Confondre une suite et une fonction : une suite n'est définie que pour les entiers $n$"
- "Mal compter les termes : si la suite commence à $u_0$, alors $u_{10}$ est le 11ᵉ terme"
- "Confondre définition explicite ($u_n = f(n)$) et définition par récurrence ($u_{n+1} = f(u_n)$)"
- "Étudier les variations de $(u_n)$ définie par $u_{n+1} = f(u_n)$ avec les variations de $f$ : on étudie le signe de $u_{n+1} - u_n$"
- "Croire qu'une suite croissante a une limite finie : elle peut tendre vers $+\\infty$"
- Oublier de donner le premier terme ($u_0$ ou $u_1$) dans une définition par récurrence
liens:
- nom: Jaicompris — Généralités sur les suites
  desc: "Méthode complète : définition, sens de variation"
  url: "https://www.jaicompris.com/lycee/math/suites/suites-numeriques.php"
  ico: 🎯
  cat: methode
- nom: Khan Academy — Suites numériques
  desc: "Notation, modes de définition, premiers termes"
  url: "https://fr.khanacademy.org/math/algebra-home/alg-series-and-induction"
  ico: 🎬
  cat: cours
- nom: GeoGebra — Suites récurrentes
  desc: Visualisez la suite (uₙ) et son comportement
  url: "https://www.geogebra.org/m/AGFZsSeR"
  ico: 📐
  cat: calcul
- nom: Lumni — Les suites numériques
  desc: "Vidéo : introduction aux suites"
  url: "https://www.lumni.fr/programme/suites-numeriques"
  ico: 🎬
  cat: cours
- nom: Maths-Cours — Suites (généralités)
  desc: Exercices progressifs avec corrigés
  url: "https://www.maths-cours.fr/exercices/suite-1"
  ico: 📝
  cat: entrainement
---
{% include cours-cards.html %}
