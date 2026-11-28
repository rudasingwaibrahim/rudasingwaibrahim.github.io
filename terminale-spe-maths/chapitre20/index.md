---
title: Chapitre 20 — Calcul intégral 2/2
permalink: /classes/terminale-spe-maths/chapitre20/
hero_title: Chapitre 20
hero_subtitle: Intégration par parties — Suites d'intégrales — Aires et valeurs moyennes
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch20-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch20-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch20-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch20-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Fonction aire · Intégration par parties · Suite d'intégrales
  duree: 2 h environ
  pdf: terminale-spe-ch20-dm-01.pdf
- num: 2
  contenu: Décomposition · IPP et récurrence · Aire
  duree: 2 h environ
  pdf: terminale-spe-ch20-dm-02.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Intégrales · IPP · Aire · Étude de fonction
  duree: 4 h
  pdf: terminale-spe-ch20-dsblanc-01.pdf
- num: 2
  contenu: Calculs d'intégrales · IPP · Aire · Valeur moyenne
  duree: 4 h
  pdf: terminale-spe-ch20-dsblanc-02.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch20-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch20-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch20-ds-01.pdf
- num: 2
  pdf: terminale-spe-ch20-ds-02.pdf
- num: 3
  pdf: terminale-spe-ch20-ds-03.pdf
python:
- titre: "Calculer ln 2 : l'algorithme de Brouncker"
  fichier: /assets/python/terminale-spe-maths/ch20-brouncker-ln2.ipynb
  module: /assets/python/terminale-spe-maths/verif_tspe_ch20.py
  duree: "30 min"
  contenu: "Somme de Brouncker · Rectangles sous l'hyperbole · Encadrement de ln 2 · Rang pour une précision"
erreurs:
- 'Se tromper de signe dans l''intégration par parties : $\displaystyle\int_a^b u v'' = [uv]_a^b - \int_a^b u'' v$'
- 'Mal choisir $u$ : dans $\displaystyle\int x\mathrm{e}^x$, on pose $u = x$ (qui se simplifie en dérivant) et $v'' = \mathrm{e}^x$'
- Oublier d'évaluer le crochet $[uv]_a^b$ aux deux bornes
- 'Écrire $\displaystyle\int_a^b f(x)g(x)\,\mathrm{d}x = \int_a^b f(x)\,\mathrm{d}x \times \int_a^b g(x)\,\mathrm{d}x$ : c''est faux en général'
- Ne pas justifier le signe de l'intégrande avant d'interpréter une intégrale comme une aire
- Dans une suite d'intégrales, comparer $I_{n+1}$ et $I_n$ en étudiant le signe de l'intégrande de $I_{n+1} - I_n$
---
{% include cours-cards.html %}
