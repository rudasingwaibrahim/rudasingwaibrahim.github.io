---
title: Chapitre 10 — Suites arithmétiques et géométriques
permalink: /classes/premiere-spe-maths/chapitre10/
dossier_pdf: premiere-spe-maths
hero_title: Chapitre 10
hero_subtitle: Suites arithmétiques et géométriques
cours:
- titre: Cours — Version élève
  pdf: premiere-spe-ch10-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: premiere-spe-ch10-cours-prof.pdf
planches:
- num: 1
  pdf: premiere-spe-ch10-planche-01.pdf
- num: 2
  pdf: premiere-spe-ch10-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: "Suites arithmétiques · Somme de Gauss · Modélisation"
  duree: "1 semaine"
  pdf: premiere-spe-ch10-dm-01-sujet.pdf
- num: 2
  contenu: "Suites géométriques · Évolutions · Somme"
  duree: "1 semaine"
  pdf: premiere-spe-ch10-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: "Suites arithmétiques · Reconnaissance · Calcul"
  duree: "55 min"
  pdf: premiere-spe-ch10-dsblanc-01-sujet.pdf
- num: 2
  contenu: "Suites géométriques · Application financière"
  duree: "55 min"
  pdf: premiere-spe-ch10-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: premiere-spe-ch10-activites.pdf
- titre: Activités — Version professeur
  pdf: premiere-spe-ch10-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: premiere-spe-ch10-ds-01-sujet.pdf
- num: 2
  pdf: premiere-spe-ch10-ds-02-sujet.pdf
- num: 3
  pdf: premiere-spe-ch10-ds-03-sujet.pdf
python:
- titre: "Sommes de termes et seuils"
  fichier: /assets/python/premiere-spe-maths/ch10-suites-arithmetiques-geometriques.ipynb
  module: /assets/python/premiere-spe-maths/verif_1spe_ch10.py
  duree: "35 min"
  contenu: "Somme 1 + 2 + … + n · Somme 1 + q + … + qⁿ · Somme de termes géométriques · Seuil · Liste en compréhension"
erreurs:
- "Confondre suite arithmétique ($u_{n+1} = u_n + r$) et suite géométrique ($u_{n+1} = q\\,u_n$)"
- "Se tromper de formule explicite : $u_n = u_0 + nr$ (arithmétique), $u_n = u_0\\,q^n$ (géométrique)"
- "Oublier la condition $q \\neq 1$ dans $1 + q + \\dots + q^n = \\dfrac{1 - q^{n+1}}{1 - q}$"
- "Confondre la raison $r$ d'une suite arithmétique et la raison $q$ d'une suite géométrique"
- "Mal compter les termes d'une somme : de $u_0$ à $u_n$, il y a $n + 1$ termes"
- "Confondre évolution en pourcentage et raison : une hausse de 5 % par an correspond à $q = 1{,}05$"
liens:
- nom: Jaicompris — Suites arithmétiques et géométriques
  desc: Méthode complète avec exercices corrigés
  url: "https://www.jaicompris.com/lycee/math/suites/suite-arithmetique-geometrique.php"
  ico: 🎯
  cat: methode
- nom: Khan Academy — Suites arithmétiques et géométriques
  desc: "Définitions, formules et applications"
  url: "https://fr.khanacademy.org/math/algebra-home/alg-series-and-induction/alg-arithmetic-and-geometric-sequences"
  ico: 🎬
  cat: cours
- nom: GeoGebra — Suites arith./géom.
  desc: Comparez visuellement les deux types de suites
  url: "https://www.geogebra.org/m/AGFZsSeR"
  ico: 📐
  cat: calcul
- nom: Lumni — Suites particulières
  desc: "Vidéo : reconnaître et manipuler les suites usuelles"
  url: "https://www.lumni.fr/programme/suites-numeriques"
  ico: 🎬
  cat: cours
- nom: Maths-Cours — Suites arith. et géom.
  desc: Exercices progressifs avec corrigés
  url: "https://www.maths-cours.fr/exercices/suite-2"
  ico: 📝
  cat: entrainement
---
{% include cours-cards.html %}
