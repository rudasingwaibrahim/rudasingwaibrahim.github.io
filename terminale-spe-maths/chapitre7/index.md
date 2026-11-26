---
title: Chapitre 7 — Variables aléatoires 1/2
permalink: /classes/terminale-spe-maths/chapitre7/
hero_title: Chapitre 7
hero_subtitle: Succession d'épreuves indépendantes — Schéma de Bernoulli et loi binomiale
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch7-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch7-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch7-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch7-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Loi de Bernoulli · Loi binomiale
  duree: 1 semaine
  pdf: terminale-spe-ch7-dm-01-sujet.pdf
- num: 2
  contenu: Sommes de variables aléatoires · Espérance
  duree: 1 semaine
  pdf: terminale-spe-ch7-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Loi binomiale · Probabilités conditionnelles
  duree: 4 h
  pdf: terminale-spe-ch7-dsblanc-01-sujet.pdf
- num: 2
  contenu: Loi binomiale · Indépendance
  duree: 4 h
  pdf: terminale-spe-ch7-dsblanc-02-sujet.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch7-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch7-ds-02-sujet.pdf
- num: 3
  pdf: terminale-spe-ch7-ds-03-sujet.pdf
erreurs:
- 'Utiliser la loi binomiale pour des tirages sans remise : les épreuves ne sont alors pas indépendantes'
- 'Oublier le coefficient binomial : $P(X=k)=\binom{n}{k}p^k(1-p)^{n-k}$'
- 'Calculer $P(X\geqslant k)$ par $1-P(X\leqslant k)$ : pour $X$ à valeurs entières, $P(X\geqslant k)=1-P(X\leqslant k-1)$'
- 'Confondre $P(X<k)$ et $P(X\leqslant k)$ : pour $X$ à valeurs entières, $P(X<k)=P(X\leqslant k-1)$'
- 'Écrire $V(X)=np$ pour $X\sim\mathcal{B}(n,p)$ : $E(X)=np$ et $V(X)=np(1-p)$'
- 'Confondre événements indépendants et incompatibles : deux événements incompatibles de probabilités non nulles ne sont jamais indépendants'
---
{% include cours-cards.html %}
