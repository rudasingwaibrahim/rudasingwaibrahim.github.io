---
title: Chapitre 3 — Combinatoire et dénombrement
permalink: /classes/terminale-spe-maths/chapitre3/
hero_title: Chapitre 3
hero_subtitle: Principes additif et multiplicatif — Combinaisons et triangle de Pascal
cours:
- titre: Cours — Version élève
  pdf: terminale-spe-ch3-cours-eleve.pdf
- titre: Cours — Version professeur
  pdf: terminale-spe-ch3-cours-prof.pdf
planches:
- num: 1
  pdf: terminale-spe-ch3-planche-01.pdf
- num: 2
  pdf: terminale-spe-ch3-planche-02.pdf
dm_published: false
dm:
- num: 1
  contenu: Permutations · Listes d'éléments distincts
  duree: 1 semaine
  pdf: terminale-spe-ch3-dm-01-sujet.pdf
- num: 2
  contenu: Combinaisons · Relation de Pascal
  duree: 1 semaine
  pdf: terminale-spe-ch3-dm-02-sujet.pdf
dsblancs_published: true
ds_blancs:
- num: 1
  contenu: Cartes, urnes, anagrammes
  duree: 2 h
  pdf: terminale-spe-ch3-dsblanc-01-sujet.pdf
- num: 2
  contenu: Combinatoire et probabilités
  duree: 2 h
  pdf: terminale-spe-ch3-dsblanc-02-sujet.pdf
activites:
- titre: Activités — Version élève
  pdf: terminale-spe-ch3-activites.pdf
- titre: Activités — Version professeur
  pdf: terminale-spe-ch3-activites-prof.pdf
ds_published: false
ds:
- num: 1
  pdf: terminale-spe-ch3-ds-01-sujet.pdf
- num: 2
  pdf: terminale-spe-ch3-ds-02-sujet.pdf
- num: 3
  pdf: terminale-spe-ch3-ds-03-sujet.pdf
python:
- titre: "Triangle de Pascal, parties et permutations"
  fichier: /assets/python/terminale-spe-maths/ch3-pascal-parties-permutations.ipynb
  module: /assets/python/terminale-spe-maths/verif_tspe_ch3.py
  duree: "45 min"
  contenu: "Factorielle · Triangle de Pascal · Parties à 2 éléments · 3-uplets d'éléments distincts · Permutation aléatoire"
erreurs:
- 'Confondre $k$-uplets (ordre et répétitions : $n^k$), $k$-uplets d''éléments distincts ($\dfrac{n!}{(n-k)!}$) et combinaisons (sans ordre : $\binom{n}{k}$)'
- 'Appliquer le principe additif à des ensembles non disjoints : $\#(A\cup B)=\#A+\#B-\#(A\cap B)$'
- Oublier que $0!=1$, d'où $\binom{n}{0}=\binom{n}{n}=1$
- 'Mal écrire la relation de Pascal : $\binom{n}{k}=\binom{n-1}{k-1}+\binom{n-1}{k}$ pour $1\leqslant k\leqslant n-1$'
- 'Mettre $n$ facteurs au numérateur de $\binom{n}{k}$ : il en faut $k$, $\binom{n}{k}=\dfrac{n(n-1)\cdots(n-k+1)}{k!}$'
- 'Oublier l''ensemble vide et l''ensemble lui-même : un ensemble à $n$ éléments possède $2^n$ parties'
---
{% include cours-cards.html %}
