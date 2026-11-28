---
title: Chapitre 8 — Trigonométrie (Partie 1)
permalink: /classes/premiere-spe-maths/chapitre8/
dossier_pdf: premiere-spe-maths
hero_title: Chapitre 8
hero_subtitle: "Trigonométrie — Cercle trigonométrique, radian et enroulement"
cours:
- titre: Cours — Version élève
  pdf: premiere-spe-ch8-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: premiere-spe-ch8-cours-prof.pdf
planches:
- num: 1
  pdf: premiere-spe-ch8-planche-01.pdf
- num: 2
  pdf: premiere-spe-ch8-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Radian · Enroulement · Longueurs d'arc
  duree: "1 semaine"
  pdf: premiere-spe-ch8-dm-01-sujet.pdf
- num: 2
  contenu: Approximation de π (Archimède) · Python
  duree: "1 semaine"
  pdf: premiere-spe-ch8-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Placer et lire sur le cercle
  duree: "55 min"
  pdf: premiere-spe-ch8-dsblanc-01-sujet.pdf
- num: 2
  contenu: Radian et enroulement
  duree: "55 min"
  pdf: premiere-spe-ch8-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: premiere-spe-ch8-activites.pdf
- titre: Activités — Version professeur
  pdf: premiere-spe-ch8-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: premiere-spe-ch8-ds-01-sujet.pdf
- num: 2
  pdf: premiere-spe-ch8-ds-02-sujet.pdf
- num: 3
  pdf: premiere-spe-ch8-ds-03-sujet.pdf
python:
- titre: "Approcher π par la méthode d'Archimède"
  fichier: /assets/python/premiere-spe-maths/ch8-archimede-pi.ipynb
  module: /assets/python/premiere-spe-maths/verif_1spe_ch8.py
  duree: "30 min"
  contenu: "Périmètre du polygone inscrit · Polygone exinscrit · Encadrement de π · Nombre de côtés pour une précision"
erreurs:
- "Confondre radians et degrés : $\\pi$ rad correspond à $180^\\circ$, mais $\\pi \\neq 180$"
- "Se tromper de signe : $\\sin x < 0$ quand le point associé est sous l'axe des abscisses"
- "Croire que deux réels associés au même point du cercle sont égaux : ils diffèrent d'un multiple de $2\\pi$, par exemple $\\dfrac{\\pi}{3}$ et $\\dfrac{7\\pi}{3}$"
- "Confondre $\\cos(\\pi - x) = -\\cos x$ et $\\sin(\\pi - x) = \\sin x$ : s'aider du cercle trigonométrique"
- "Croire que $\\cos^2 x$ signifie $\\cos(\\cos x)$ : c'est $(\\cos x)^2$"
- "Oublier l'orientation : le sens direct (trigonométrique) est le sens contraire des aiguilles d'une montre"
liens:
- nom: Jaicompris — Trigonométrie
  desc: Méthode pas à pas avec exercices corrigés en vidéo
  url: "https://www.jaicompris.com/lycee/math/trigonometrie/trigonometrie.php"
  ico: 🎯
  cat: cours
- nom: Khan Academy — Cercle unité
  desc: Définition de sin et cos sur le cercle trigonométrique
  url: "https://fr.khanacademy.org/math/trigonometry/trig-with-general-triangles"
  ico: 🎬
  cat: cours
- nom: GeoGebra — Cercle trigonométrique interactif
  desc: "Faites varier l'angle et observez sin, cos, tan en direct"
  url: "https://www.geogebra.org/m/Au7gYUEM"
  ico: 📐
  cat: calcul
- nom: Lumni — Trigonométrie au lycée
  desc: "Vidéos courtes : du collège au cercle trigonométrique"
  url: "https://www.lumni.fr/programme/trigonometrie"
  ico: 🎬
  cat: cours
- nom: "Exo7 — Fiches d'exercices trigonométrie"
  desc: Exercices classiques (universitaires) avec corrections détaillées
  url: "http://exo7.emath.fr/ficpdf/fic00003.pdf"
  ico: 📝
  cat: entrainement
---
{% include cours-cards.html %}
