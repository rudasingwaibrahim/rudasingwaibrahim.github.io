---
title: Chapitre 8 — Continuité des fonctions
permalink: /classes/terminale-spe-maths/chapitre8/
hero_title: Chapitre 8
hero_subtitle: Continuité — Théorème des valeurs intermédiaires et dichotomie
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch8-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch8-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch8-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch8-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Continuité en un point · TVI et dénombrement
  duree: 1 semaine
  pdf: terminale-spe-ch8-dm-01-sujet.pdf
- num: 2
  contenu: Problèmes complets · Limites et TVI
  duree: 1 semaine
  pdf: terminale-spe-ch8-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Continuité · TVI · Corollaire du TVI
  duree: 4 h
  pdf: terminale-spe-ch8-dsblanc-01-sujet.pdf
- num: 2
  contenu: Limites et asymptotes · Vrai/Faux
  duree: 4 h
  pdf: terminale-spe-ch8-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch8-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch8-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch8-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch8-ds-02-sujet.pdf
- num: 3
  pdf: terminale-spe-ch8-ds-03-sujet.pdf
python:
- titre: "Dichotomie, méthode de Newton, méthode de la sécante"
  fichier: /assets/python/terminale-spe-maths/ch8-dichotomie-newton-secante.ipynb
  module: /assets/python/terminale-spe-maths/verif_tspe_ch8.py
  duree: "45 min"
  contenu: "Suite récurrente uₙ₊₁ = f(uₙ) · Dichotomie · Méthode de Newton · Méthode de la sécante · Comparaison"
erreurs:
- 'Croire que le TVI donne l''unicité : sans stricte monotonie, l''équation $f(x)=k$ peut avoir plusieurs solutions'
- Oublier de citer la continuité de $f$ sur $[a;b]$ avant d'appliquer le théorème des valeurs intermédiaires
- Appliquer le TVI alors que $k$ n'est pas compris entre $f(a)$ et $f(b)$ (ou entre les limites aux bornes)
- 'Confondre « $f$ croissante » et « $f$ strictement croissante » : l''unicité exige la stricte monotonie'
- 'Justifier une égalité par des valeurs approchées : $\sqrt{9+4\sqrt{5}}\approx 4{,}236$ ne prouve pas $\sqrt{9+4\sqrt{5}}=2+\sqrt{5}$'
- 'Arrêter la dichotomie trop tôt : l''encadrement final doit avoir l''amplitude demandée ($b-a<10^{-2}$ par exemple)'
---
{% include cours-cards.html %}
