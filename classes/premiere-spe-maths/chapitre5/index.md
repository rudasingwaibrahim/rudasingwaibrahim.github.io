---
title: Chapitre 5 — Probabilités conditionnelles et indépendance
permalink: /classes/premiere-spe-maths/chapitre5/
dossier_pdf: premiere-spe-maths
hero_title: Chapitre 5
hero_subtitle: Probabilités conditionnelles — Arbre pondéré et indépendance
cours:
- titre: Cours — Version élève
  pdf: premiere-spe-ch5-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: premiere-spe-ch5-cours-prof.pdf
planches:
- num: 1
  pdf: premiere-spe-ch5-planche-01.pdf
- num: 2
  pdf: premiere-spe-ch5-planche-02.pdf
dm_published: true
dm:
- num: 1
  contenu: Arbre à trois branches · Probabilités totales · Test de dépistage
  duree: "1 semaine"
  pdf: premiere-spe-ch5-dm-01-sujet.pdf
- num: 2
  contenu: Probabilités totales · Indépendance · Tirages avec remise
  duree: "1 semaine"
  pdf: premiere-spe-ch5-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: QCM · Tableau croisé et indépendance · Bracelets (sujet type bac)
  duree: "55 min"
  pdf: premiere-spe-ch5-dsblanc-01-sujet.pdf
- num: 2
  contenu: Vrai-faux · V.O.D. (sujet type bac) · Vaccin et inconnue
  duree: "55 min"
  pdf: premiere-spe-ch5-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: premiere-spe-ch5-activites.pdf
- titre: Activités — Version professeur
  pdf: premiere-spe-ch5-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: premiere-spe-ch5-ds-01-sujet.pdf
- num: 2
  pdf: premiere-spe-ch5-ds-02-sujet.pdf
- num: 3
  pdf: premiere-spe-ch5-ds-03-sujet.pdf
python:
- titre: "La méthode de Monte-Carlo"
  fichier: /assets/python/premiere-spe-maths/ch5-monte-carlo.ipynb
  module: /assets/python/premiere-spe-maths/verif_1spe_ch5.py
  duree: "35 min"
  contenu: "Point au hasard dans le carré unité · Aire sous la parabole · Estimation de π · Fluctuation des estimations"
erreurs:
- "Confondre $P(A \\cap B)$ et $P_A(B)$ : sur un arbre, on multiplie le long d'un chemin pour obtenir $P(A \\cap B)$"
- "Oublier la définition $P_B(A) = \\dfrac{P(A \\cap B)}{P(B)}$, avec $P(B) \\neq 0$"
- "Croire que deux événements sans issue commune sont indépendants : si $A \\cap B = \\varnothing$, avec $P(A) \\neq 0$ et $P(B) \\neq 0$, alors $P(A \\cap B) = 0 \\neq P(A) \\times P(B)$"
- "Mal utiliser la formule des probabilités totales : oublier une branche de la partition"
- "Sur un arbre, la somme des poids partant d'un même nœud doit valoir 1"
- "Confondre $P_B(A)$ et $P_A(B)$ : en général, ils sont différents"
liens:
- nom: Jaicompris — Probabilités conditionnelles
  desc: "Méthode complète : arbre, formule des probas totales"
  url: "https://www.jaicompris.com/lycee/math/probabilite/probabilite-conditionnelle.php"
  ico: 🎯
  cat: methode
- nom: Khan Academy — Probabilités conditionnelles
  desc: "Définition, formule et indépendance"
  url: "https://fr.khanacademy.org/math/statistics-probability/probability-library/conditional-probability-independence"
  ico: 🎬
  cat: cours
- nom: GeoGebra — Arbre de probabilités
  desc: Construire un arbre pondéré interactif
  url: "https://www.geogebra.org/m/CCgfTBsT"
  ico: 📐
  cat: calcul
- nom: Lumni — Probabilités conditionnelles
  desc: "Vidéo : raisonner avec un arbre pondéré"
  url: "https://www.lumni.fr/programme/probabilites-conditionnelles"
  ico: 🎬
  cat: cours
- nom: Maths-Cours — Probabilités conditionnelles
  desc: Exercices progressifs avec corrigés détaillés
  url: "https://www.maths-cours.fr/exercices/probabilite-conditionnelle"
  ico: 📝
  cat: entrainement
---
{% include cours-cards.html %}
