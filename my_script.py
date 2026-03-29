from pathlib import Path

seconde_chapitres = [
    "Calcul algébrique",
    "Puissances et racines carrées",
    "Les vecteurs (Partie 1)",
    "Notion de multiple, diviseur et nombre premier",
    "Les vecteurs (Partie 2)",
    "Nombres réels (Partie 1)",
    "Notion de fonction",
    "Nombres réels (Partie 2)",
    "Vecteurs et repérage",
    "Équations et inéquations",
    "Information chiffrée",
    "Les fonctions de référence",
    "Statistiques descriptives",
    "Variations d’une fonction",
    "Droites du plan",
    "Probabilités",
    "Systèmes d’équations et droites",
    "Échantillonnage"
]

classes = {
    "seconde205": {
        "shared_pdf_root": "seconde/commun",
        "chapitres": seconde_chapitres,
    },
    "seconde219": {
        "shared_pdf_root": "seconde/commun",
        "chapitres": seconde_chapitres,
    },
    "premiere-spe-maths": {
        "shared_pdf_root": "premiere-spe-maths/commun",
        "chapitres": [
            "Second degré (Partie 1)",
            "Dérivation (Partie 1)",
            "Second degré (Partie 2)",
            "Dérivation (Partie 2)",
            "Probabilités conditionnelles et indépendance",
            "Dérivation (Partie 3)",
            "Généralités sur les suites",
            "Trigonométrie (Partie 1)",
            "Produit scalaire (Partie 1)",
            "Suites arithmétiques et géométriques",
            "Trigonométrie (Partie 2)",
            "Produit scalaire (Partie 2)",
            "Fonction exponentielle",
            "Géométrie repérée",
            "Variables aléatoires",
        ],
    },
    "premiere-techno-tronc-commun": {
        "shared_pdf_root": "premiere-techno-tronc-commun/commun",
        "chapitres": [
            "Généralités sur les fonctions",
            "Evolutions (Rappels)",
            "Fonctions polynômes de degré 2 (1/2)",
            "Les suites 1/2",
            "Statistiques",
            "Fonctions polynômes de degré 2 (2/2)",
            "Les suites 2/2",
            "Probabilités conditionnelles",
            "Fonctions polynômes de degré 3",
            "Variables aléatoires",
            "Dérivation 1/2",
            "Loi de Bernoulli 1/2",
            "Dérivation 2/2",
            "Loi de Bernoulli 2/2",
        ],
    },
    "premiere-techno-spe": {
        "shared_pdf_root": "premiere-techno-spe/commun",
        "chapitres": [
            "Trigonométrie",
            "Produit scalaire",
            "Nombres complexes",
            "Dérivation",
            "Primitives",
        ],
    },
    "terminale-spe-maths": {
        "shared_pdf_root": "terminale-spe-maths/commun",
        "chapitres": [
            "Suites 1/2",
            "Limites des fonctions 1/2",
            "Combinatoire et dénombrement",
            "Limites des fonctions 2/2",
            "Vecteurs, droites et plans dans l'espace",
            "Dérivation",
            "Variables aléatoires 1/2",
            "Continuité des fonctions",
            "Suites 2/2",
            "Convexité",
            "Produit scalaire dans l'espace",
            "Fonction logarithme 1/2",
            "Fonction logarithme 2/2",
            "Représentations paramétriques et équations cartésiennes",
            "Primitives et équations différentielles",
            "Variables aléatoires 2/2",
            "Fonctions trigonométriques",
            "Calcul intégral 1/2",
            "Concentration, loi des grands nombres",
            "Calcul intégral 2/2",
        ],
    },
    "terminale-maths-complementaires": {
        "shared_pdf_root": "terminale-maths-complementaires/commun",
        "chapitres": [
            "Suites 1/2",
            "Limites des fonctions",
            "Lois discrètes 1/2",
            "Dérivation",
            "Lois discrètes 2/2",
            "Continuité des fonctions",
            "Suites 2/2",
            "Convexité",
            "Fonction logarithme",
            "Statistiques",
            "Primitives et équations différentielles",
            "Calcul intégral 1/2",
            "Lois à densité",
            "Calcul intégral 2/2",
        ],
    },
    "terminale-maths-expertes": {
        "shared_pdf_root": "terminale-maths-expertes/commun",
        "chapitres": [
            "Nombres complexes 1/4",
            "Matrices 1/2",
            "Divisibilité et congruences",
            "Nombres complexes 2/4",
            "Matrices 2/2",
            "Nombres complexes 3/4",
            "PGCD et nombres premiers",
            "Nombres complexes 4/4",
            "Graphes 1/2",
            "Equations polynomiales",
            "Graphes 2/2",
        ],
    },
    "terminale-techno-commun": {
        "shared_pdf_root": "terminale-techno-commun/commun",
        "chapitres": [
            "Les suites 1/2",
            "Probabilités conditionnelles",
            "Les suites 2/2",
            "Fonctions exponentielles",
            "Variables aléatoires 1/2",
            "Fonction logarithme décimal",
            "Variables aléatoires 2/2",
            "Fonction inverse",
            "Statistique",
        ],
    },
    "terminale-techno-spe": {
        "shared_pdf_root": "terminale-techno-spe/commun",
        "chapitres": [
            "Intégration",
            "Fonctions exponentielles",
            "Fonction logarithme népérien",
            "Fonctions composées",
            "Équations différentielles",
            "Nombres complexes",
        ],
    },
    "bts-mec1": {
        "shared_pdf_root": "bts-mec1/commun",
        "chapitres": [
            "Rappels – Suites numériques",
            "Fonctions d’une variable réelle",
            "Calcul intégral",
            "Équations différentielles",
            "Statistique descriptive",
            "Probabilités – Variables aléatoires discrètes",
        ],
    },
    "bts-mec2": {
        "shared_pdf_root": "bts-mec2/commun",
        "chapitres": [
            "Rappels probabilités",
            "Probabilités – lois usuelles",
            "Statistique inférentielle",
            "Configurations géométriques",
            "Calcul vectoriel",
            "Révisions et préparation BTS",
        ],
    },
}


def make_pdf_dirs(shared_root: str, classe: str, chap: str) -> None:
    for sub in ["cours", "planches", "dm", "dsblanc", "fiche-methode"]:
        Path(f"assets/pdf/{shared_root}/{chap}/{sub}").mkdir(parents=True, exist_ok=True)
    Path(f"assets/pdf/{classe}/{chap}/ds").mkdir(parents=True, exist_ok=True)


def build_planches(shared_root: str, chap: str) -> str:
    return "\n".join(
        f"- Planche {j} — [Sujet](/assets/pdf/{shared_root}/{chap}/planches/planche{j}-sujet.pdf) • [Correction](/assets/pdf/{shared_root}/{chap}/planches/planche{j}-correction.pdf)"
        for j in range(1, 7)
    )


def build_dm(shared_root: str, chap: str) -> str:
    return "\n".join(
        f"- DM{j} — [Sujet](/assets/pdf/{shared_root}/{chap}/dm/dm{j}-sujet.pdf) • [Correction](/assets/pdf/{shared_root}/{chap}/dm/dm{j}-correction.pdf)"
        for j in range(1, 7)
    )


def build_dsblanc(shared_root: str, chap: str) -> str:
    return "\n".join(
        f"- DS Blanc {j} — [Sujet](/assets/pdf/{shared_root}/{chap}/dsblanc/ds{j}-sujet.pdf) • [Correction](/assets/pdf/{shared_root}/{chap}/dsblanc/ds{j}-correction.pdf)"
        for j in range(1, 4)
    )


def build_ds(classe: str, chap: str) -> str:
    return "\n".join(
        f"- DS {j} — [Sujet](/assets/pdf/{classe}/{chap}/ds/ds{j}-sujet.pdf) • [Correction](/assets/pdf/{classe}/{chap}/ds/ds{j}-correction.pdf)"
        for j in range(1, 4)
    )


for classe, config in classes.items():
    shared_root = config["shared_pdf_root"]

    for i, titre in enumerate(config["chapitres"], start=1):
        chap = f"chapitre{i}"

        make_pdf_dirs(shared_root, classe, chap)

        md_path = Path(f"classes/{classe}/{chap}/index.md")
        md_path.parent.mkdir(parents=True, exist_ok=True)

        if md_path.exists():
            print(f"SKIP index existant : {md_path}")
            continue

        cours_filename = f"{classe}-ch{i}-cours.pdf"
        if classe in ("seconde205", "seconde219"):
            cours_filename = f"seconde-ch{i}-cours.pdf"

        contenu = f"""---
layout: default
title: "Chapitre {i} - {titre}"
permalink: /classes/{classe}/{chap}/
hero_title: "Chapitre {i}"
hero_subtitle: "{titre}"
---

## 📘 Cours
- 📄 [Cours complet — PDF](/assets/pdf/{shared_root}/{chap}/cours/{cours_filename})

---

## 📝 Planches
{build_planches(shared_root, chap)}

---

## 🏠 Devoirs maison
{build_dm(shared_root, chap)}

---

## ✍️ Devoirs blancs
{build_dsblanc(shared_root, chap)}

---

## 🧪 Devoirs surveillés
{build_ds(classe, chap)}

---

## 📁 Divers
- 📄 Fiche méthode — [PDF](/assets/pdf/{shared_root}/{chap}/fiche-methode/fiche-methode.pdf)

---

## 🔗 Liens utiles
- https://www.jeuxmaths.fr/
- https://www.geogebra.org/
"""

        md_path.write_text(contenu, encoding="utf-8")
        print(f"CREATE index : {md_path}")

print("✅ Génération safe terminée.")