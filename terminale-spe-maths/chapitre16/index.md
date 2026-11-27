---
title: Chapitre 16 — Variables aléatoires 2/2
permalink: /classes/terminale-spe-maths/chapitre16/
hero_title: Chapitre 16
hero_subtitle: Somme de variables aléatoires — Linéarité de l'espérance, variance, échantillon
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch16-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch16-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch16-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch16-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Espérance, variance · Combinaisons linéaires
  duree: 1 semaine
  pdf: terminale-spe-ch16-dm-01-sujet.pdf
- num: 2
  contenu: Somme de Bernoulli · Loi binomiale
  duree: 1 semaine
  pdf: terminale-spe-ch16-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Somme de variables aléatoires · Échantillon
  duree: 1 h
  pdf: terminale-spe-ch16-dsblanc-01-sujet.pdf
- num: 2
  contenu: Loi binomiale · Combinaisons linéaires
  duree: 1 h
  pdf: terminale-spe-ch16-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch16-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch16-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch16-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch16-ds-02-sujet.pdf
- num: 3
  pdf: terminale-spe-ch16-ds-03-sujet.pdf
erreurs:
- 'Utiliser $V(X+Y) = V(X) + V(Y)$ sans indépendance : cette relation est donnée pour des variables indépendantes'
- 'Écrire $V(aX) = aV(X)$ : on a $V(aX) = a^2V(X)$ et $\sigma(aX) = |a|\sigma(X)$'
- 'Croire que $V(X-Y) = V(X) - V(Y)$ : pour $X$, $Y$ indépendantes, $V(X-Y) = V(X) + V(Y)$'
- 'Oublier qu''ajouter une constante ne change pas la variance : $V(X+b) = V(X)$, mais $E(X+b) = E(X) + b$'
- 'Affirmer qu''une somme de variables de Bernoulli de paramètres différents suit une loi binomiale : il faut le même paramètre $p$ et l''indépendance'
- 'Pour la moyenne $M_n$ d''un échantillon : $E(M_n) = E(X)$ et $V(M_n) = \dfrac{V(X)}{n}$ (et non $nV(X)$)'
---
{% include cours-cards.html %}
