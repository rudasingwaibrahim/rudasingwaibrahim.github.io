---
title: Chapitre 12 — Produit scalaire (Partie 2)
permalink: /classes/premiere-spe-maths/chapitre12/
dossier_pdf: premiere-spe-maths
hero_title: Chapitre 12
hero_subtitle: Produit scalaire — Applications géométriques
cours:
- titre: Cours — Version élève
  pdf: premiere-spe-ch12-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: premiere-spe-ch12-cours-prof.pdf
planches:
- num: 1
  pdf: premiere-spe-ch12-planche-01.pdf
- num: 2
  pdf: premiere-spe-ch12-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Orthogonalité avec et sans coordonnées
  duree: "1 semaine"
  pdf: premiere-spe-ch12-dm-01-sujet.pdf
- num: 2
  contenu: Projeté orthogonal · Perpendicularité
  duree: "1 semaine"
  pdf: premiere-spe-ch12-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Démontrer une orthogonalité
  duree: "55 min"
  pdf: premiere-spe-ch12-dsblanc-01-sujet.pdf
- num: 2
  contenu: Orthogonalité · Lignes de niveau
  duree: "55 min"
  pdf: premiere-spe-ch12-dsblanc-02-sujet.pdf
ds_published: false
ds:
- num: 1
  pdf: premiere-spe-ch12-ds-01-sujet.pdf
- num: 2
  pdf: premiere-spe-ch12-ds-02-sujet.pdf
- num: 3
  pdf: premiere-spe-ch12-ds-03-sujet.pdf
erreurs:
- "Se tromper de formule en repère orthonormé : $\\vec u\\cdot\\vec v = xx' + yy'$, et non $xy' + yx'$"
- "Croire que deux droites sont perpendiculaires quand leurs vecteurs normaux sont colinéaires : c'est le produit scalaire de ces vecteurs normaux qui doit être nul"
- "Écrire $\\vec u\\cdot\\vec v = \\lVert\\vec u\\rVert\\,\\lVert\\vec v\\rVert$ : il manque le facteur $\\cos\\theta$, où $\\theta$ est la mesure de l'angle entre $\\vec u$ et $\\vec v$"
- "Utiliser $\\vec u\\cdot\\vec v = xx' + yy'$ dans un repère qui n'est pas orthonormé"
- "Croire que $\\vec u\\cdot\\vec v = 0$ impose $\\vec u = \\vec 0$ ou $\\vec v = \\vec 0$ : les vecteurs peuvent être orthogonaux"
- "Oublier le signe avec le projeté orthogonal $H$ de $C$ sur $(AB)$ : $\\overrightarrow{AB}\\cdot\\overrightarrow{AC} = AB \\times AH$ si $H$ appartient à la demi-droite $[AB)$, et $-AB \\times AH$ sinon"
liens:
- nom: "Jaicompris — Théorème d'Al-Kashi"
  desc: Méthode complète avec exercices corrigés
  url: "https://www.jaicompris.com/lycee/math/produit-scalaire/al-kashi.php"
  ico: 🎯
  cat: methode
- nom: "Lumni — Théorème d'Al-Kashi"
  desc: Démonstration et applications dans le triangle quelconque
  url: "https://www.lumni.fr/video/le-theoreme-d-al-kashi"
  ico: 🎬
  cat: cours
- nom: GeoGebra — Triangle quelconque
  desc: "Faites varier les côtés et angles, vérifiez Al-Kashi en direct"
  url: "https://www.geogebra.org/m/n7aSn7gZ"
  ico: 📐
  cat: calcul
- nom: Khan Academy — Loi des cosinus
  desc: Cours et exercices sur Al-Kashi (en français)
  url: "https://fr.khanacademy.org/math/trigonometry/trig-with-general-triangles/law-of-cosines/v/law-of-cosines-example"
  ico: 🎬
  cat: cours
- nom: Maths-Cours — Formules trigonométriques
  desc: "Toutes les formules d'addition et de duplication avec exercices"
  url: "https://www.maths-cours.fr/exercices/produit-scalaire-2"
  ico: 📝
  cat: entrainement
---
{% include cours-cards.html %}
