"""Vérifications du carnet Python « Terminale spécialité · Chapitre 16 · Sommes de variables aléatoires et échantillons ».

Ce fichier accompagne le carnet ch16-sommes-variables-aleatoires.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch16 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_binomiale(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_binomiale', 'verifier_moyenne_variance', 'verifier_somme_deux_des', 'verifier_moyenne_echantillon']

# ─────────────────────────────────────────────────────────────────────────────
# Mécanique commune des vérifications (elle ne concerne pas l'élève).
# Tout ce qui commence par _ reste invisible après « from ... import * ».
# ─────────────────────────────────────────────────────────────────────────────
import sys as _sys
import io as _io
import re as _re
import contextlib as _contextlib

# Encouragements (Sigma) : une phrase variée après chaque vérification.
import random as _random

_BRAVO = [
    "Bien raisonné !", "Tu vois, tu en es capable.", "Ta méthode est la bonne.",
    "Ton programme fonctionne : c'est toi qui l'as écrit.", "Bravo, tu as pris le temps de réfléchir.",
    "C'est juste : ton travail paie.", "Belle rigueur !", "Tu progresses, continue comme ça.",
    "Bien joué : étape par étape, tu y arrives.", "Excellent : le code et les maths vont ensemble.",
    "Juste ! Garde cette méthode, elle fonctionne.", "Tu as trouvé : la programmation, c'est aussi pour toi.",
    "Solide ! Ton raisonnement est clair.", "Bravo : la persévérance, ça marche.",
    "Réussi ! Et ce n'est pas de la chance.",
]
_COURAGE = [
    "Une erreur, c'est une étape : relis le conseil ci-dessus.", "Pas encore, mais tu cherches : c'est comme ça qu'on apprend.",
    "Ce n'est pas grave : corrige une ligne à la fois, puis relance.", "Tout le monde fait des erreurs en programmant. Continue.",
    "Chaque message d'erreur te rapproche du bon programme.", "Respire, relis ton code : la solution est à ta portée.",
    "Une erreur repérée aujourd'hui, c'est une erreur évitée demain.", "Garde confiance : le conseil te donne la piste.",
    "Courage : comprendre une erreur, c'est apprendre deux fois.", "Essaie ta fonction sur un petit exemple : ça aide souvent.",
    "Tu as le droit de te tromper : c'est comme ça qu'on progresse.", "Ne lâche rien : relance la vérification après ta correction.",
]


def _bravo():
    print("  ★ " + _random.choice(_BRAVO))


def _courage():
    print("  ➜ " + _random.choice(_COURAGE))

_LIMITE = 300000      # nombre de lignes exécutées avant de conclure à une boucle sans fin
_RETURN = ("Le return doit être aligné avec le mot for (ou while) : s'il est décalé à l'intérieur de la boucle, "
           "la fonction s'arrête dès le premier tour.")
_RETURN_OU = ("ou bien ton return est décalé à l'intérieur de la boucle : il doit être aligné avec le mot for, "
              "sinon la fonction s'arrête dès le premier tour.")


class _PasEncore(Exception):
    """Réponse fausse : le message explique pourquoi."""


class _TropLong(Exception):
    """Le code de l'élève tourne trop longtemps (boucle qui ne s'arrête pas)."""


def _faux(message):
    raise _PasEncore(message)


def _montre(r):
    """Écrit pour un élève la valeur obtenue."""
    if r is Ellipsis:
        return "... (il reste des ... à remplacer)"
    if r is None:
        return "None, c'est-à-dire rien (as-tu oublié le return, ou l'as-tu placé à l'intérieur de la boucle ?)"
    if isinstance(r, str):
        return '"' + r + '"'
    if callable(r):
        return "une fonction, et non un nombre (as-tu oublié les parenthèses ?)"
    return repr(r)


def _nombre(x):
    """Écrit un nombre attendu sans décimales inutiles."""
    x = float(x)
    if x == int(x):
        return str(int(x))
    return repr(round(x, 10))


def _est_nombre(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _proche(x, y, tol=1e-9):
    if not _est_nombre(x):
        return False
    try:
        return abs(x - y) <= tol * max(1, abs(y))
    except Exception:
        return False


def _contient_points(code):
    """True si le code d'une fonction contient encore ... (Ellipsis)."""
    for c in code.co_consts:
        if c is Ellipsis:
            return True
        if hasattr(c, "co_consts") and _contient_points(c):
            return True
    return False


def _sortie(f, *valeurs):
    """Appelle f(*valeurs) et renvoie (ce que f renvoie, ce que f affiche)."""
    tampon = _io.StringIO()
    with _contextlib.redirect_stdout(tampon):
        r = f(*valeurs)
    return r, tampon.getvalue()


def _executer(test, objets, g):
    """Lance le test en comptant les lignes exécutées dans le code de l'élève."""
    compte = [0]

    def locale(frame, evenement, arg):
        if evenement == "line":
            compte[0] += 1
            if compte[0] > _LIMITE:
                raise _TropLong()
        return locale

    def globale(frame, evenement, arg):
        if frame.f_globals is g:
            return locale
        return None

    ancien = _sys.gettrace()
    _sys.settrace(globale)
    try:
        return test(*objets)
    finally:
        _sys.settrace(ancien)


def _nom_inconnu(e):
    nom = getattr(e, "name", None)
    if not nom:
        m = _re.search(r"'([^']+)'", str(e))
        nom = m.group(1) if m else "?"
    return nom


def _verifier(test, noms, aide=None):
    """Cherche les noms de l'élève dans le carnet, lance le test, affiche le bilan."""
    aide = aide or {}
    try:
        g = _sys._getframe(2).f_globals
    except Exception:
        import __main__
        g = vars(__main__)
    objets = []
    for nom in noms:
        if nom not in g:
            print("✘ Pas encore : Python ne connaît pas encore « " + nom + " ».")
            print("  → Exécute d'abord la cellule où tu as écrit " + nom
                  + " (Maj + Entrée), puis relance cette vérification.")
            _courage()
            return
        obj = g[nom]
        if obj is Ellipsis:
            print("✘ Pas encore : « " + nom + " » vaut encore ... .")
            print("  → Remplace les ... par ta réponse, exécute la cellule, puis relance cette vérification.")
            _courage()
            return
        code = getattr(obj, "__code__", None)
        if code is not None and _contient_points(code):
            print("✘ Pas encore : il reste des ... à remplacer dans ta fonction " + nom + ".")
            print("  → Remplace chaque ... par ton code, exécute la cellule de ta fonction,"
                  " puis relance cette vérification.")
            _courage()
            return
        objets.append(obj)
    try:
        bilan = _executer(test, objets, g)
    except _PasEncore as e:
        print("✘ Pas encore : " + str(e))
        _courage()
        return
    except _TropLong:
        print("✘ Pas encore : ta fonction ne s'arrête pas (sa boucle a fait des centaines de milliers de tours).")
        print("  → " + aide.get("boucle", "Vérifie ta boucle while : la variable testée doit changer à chaque "
                                          "tour, pour que la condition finisse par devenir fausse."))
        _courage()
        return
    except NameError as e:
        nom = _nom_inconnu(e)
        print("✘ Pas encore : ta fonction utilise le nom « " + nom + " », que Python ne connaît pas.")
        print("  → Vérifie son orthographe (Python distingue majuscules et minuscules). "
              "Si c'est une fonction écrite plus haut dans le carnet, exécute d'abord sa cellule.")
        _courage()
        return
    except ZeroDivisionError:
        print("✘ Pas encore : ta fonction divise par 0, ce qui est impossible.")
        print("  → " + aide.get("division", "Repère la division (/, // ou %) dont le diviseur vaut 0."))
        _courage()
        return
    except IndexError:
        print("✘ Pas encore : ta fonction demande un élément de la liste qui n'existe pas (indice trop grand).")
        print("  → " + aide.get("indice", "Les indices d'une liste de longueur n vont de 0 à n - 1."))
        _courage()
        return
    except RecursionError:
        print("✘ Pas encore : ta fonction s'appelle elle-même sans jamais s'arrêter.")
        _courage()
        return
    except TypeError as e:
        texte = str(e)
        if "ellipsis" in texte.lower():
            print("✘ Pas encore : il reste des ... à remplacer (Python ne sait pas calculer avec ...).")
        elif "NoneType" in texte:
            print("✘ Pas encore : un calcul utilise une valeur vide (None).")
            print("  → Une de tes fonctions ne renvoie rien : vérifie qu'elle se termine par un return.")
        else:
            print("✘ Pas encore : ta fonction fait un calcul impossible "
                  "(par exemple avec un texte au lieu d'un nombre).")
            print("  → " + aide.get("calcul", "Relis chaque ligne de ta fonction : chaque calcul doit porter sur des nombres."))
        _courage()
        return
    except Exception:
        print("✘ Pas encore : ta fonction s'arrête sur une erreur.")
        print("  → Appelle ta fonction toute seule dans une nouvelle cellule (par exemple avec un petit nombre)"
              " pour voir le message de Python, puis relis ton code ligne par ligne.")
        _courage()
        return
    print("✔ Juste : " + bilan)
    _bravo()


# ─────────────────────────────────────────────────────────────────────────────
# Outils communs des vérifications (cachés).
# ─────────────────────────────────────────────────────────────────────────────
import math as _math
import random as _hasard_mod


def _booleen(r, appel, conseil=""):
    if r is not True and r is not False:
        _faux(appel + " doit renvoyer True ou False. Ta fonction renvoie " + _montre(r) + ". " + conseil)


def _affichage(f, *valeurs):
    """Appelle f(*valeurs) et renvoie la liste des lignes affichées (sans les lignes vides)."""
    r, texte = _sortie(f, *valeurs)
    return [ligne.strip() for ligne in texte.split("\n") if ligne.strip() != ""]


def _nombre_attendu(r, appel):
    if r is Ellipsis or r is None or not _est_nombre(r):
        _faux(appel + " doit renvoyer un nombre. Ta fonction renvoie " + _montre(r) + ".")


def _est_liste(r, appel):
    if not isinstance(r, list):
        _faux(appel + " doit renvoyer une liste, écrite entre crochets [ ]. Ta fonction renvoie " + _montre(r) + ".")


def _listes_proches(r, attendu, tol=1e-9):
    if not isinstance(r, list) or len(r) != len(attendu):
        return False
    for i in range(len(r)):
        if not _proche(r[i], attendu[i], tol):
            return False
    return True


class _Graine:
    """Rend le hasard reproductible pendant un test, puis rend au module random son état."""
    def __init__(self, graine):
        self.graine = graine

    def __enter__(self):
        self.etat = _hasard_mod.getstate()
        _hasard_mod.seed(self.graine)

    def __exit__(self, *a):
        _hasard_mod.setstate(self.etat)
        return False


def _ecrire(x, chiffres=6):
    """Écrit un nombre arrondi pour un message."""
    if isinstance(x, int):
        return str(x)
    return repr(round(x, chiffres)).replace(".", ",")

# ─────────────────────────────────────────────────────────────────────────────
# Vérifications du carnet (une fonction par cellule « Vérification »).
# ─────────────────────────────────────────────────────────────────────────────
def _test_binomiale(bernoulli, binomiale):
    with _Graine(160):
        b = [bernoulli(0.21) for k in range(3000)]
    for x in b:
        if x != 0 and x != 1:
            _faux("bernoulli(0.21) doit renvoyer 0 ou 1. Ta fonction renvoie " + _montre(x) + ".")
    f = b.count(1) / 3000
    if abs(f - 0.79) < 0.04:
        _faux("bernoulli(0.21) renvoie 1 avec une fréquence proche de 0,79 : la condition du succès est random.random() < p.")
    if abs(f - 0.21) > 0.04:
        _faux("sur 3000 essais, bernoulli(0.21) renvoie 1 avec la fréquence " + _ecrire(f, 3) + ", trop loin de 0,21.")
    with _Graine(161):
        r = [binomiale(50, 0.21) for k in range(400)]
    for x in r:
        if not isinstance(x, int):
            _faux("binomiale(50, 0.21) doit renvoyer un entier (un nombre de succès). Ta fonction renvoie " + _montre(x)
                  + " : ajoute bernoulli(p), et non p.")
        if x < 0 or x > 50:
            _faux("binomiale(50, 0.21) doit renvoyer un entier de 0 à 50. Ta fonction renvoie " + _montre(x) + ".")
    m = sum(r) / 400
    v = sum([(x - m) ** 2 for x in r]) / 400
    if abs(m - 10.5) > 0.5 or abs(v - 8.295) > 2.5:
        _faux("sur 400 simulations, binomiale(50, 0.21) a pour moyenne " + _ecrire(m, 2) + " et pour variance " + _ecrire(v, 2)
              + " : on attend environ 10,5 et 8,3.")
    return "bernoulli(0.21) donne 1 dans " + _ecrire(100 * f, 1) + " % des cas ; binomiale(50, 0.21) : moyenne " + _ecrire(m, 2) + ", variance " + _ecrire(v, 2) + "."


def verifier_binomiale():
    """Vérifie les fonctions bernoulli et binomiale."""
    _verifier(_test_binomiale, ["bernoulli", "binomiale"])


def _test_moyenne_variance(moyenne, variance):
    r = moyenne([2, 4, 9])
    _nombre_attendu(r, "moyenne([2, 4, 9])")
    if _proche(r, 15):
        _faux("moyenne([2, 4, 9]) renvoie 15 : c'est la somme. Divise par le nombre de valeurs : s / len(L).")
    if not _proche(r, 5):
        _faux("(2 + 4 + 9) / 3 = 5. Ta fonction renvoie " + _montre(r) + ".")
    r = variance([2, 4, 9])
    _nombre_attendu(r, "variance([2, 4, 9])")
    if _proche(r, 0):
        _faux("variance([2, 4, 9]) renvoie 0 : la somme des écarts x - m est toujours nulle. Il faut les élever au carré : "
              "(x - m) ** 2.")
    if not _proche(r, 26 / 3):
        _faux("variance([2, 4, 9]) = ((2 - 5)² + (4 - 5)² + (9 - 5)²) / 3 = 26/3 ≈ 8,667. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(variance([7, 7, 7]), 0) or not _proche(variance([0, 10]), 25):
        _faux("variance([7, 7, 7]) doit renvoyer 0 et variance([0, 10]) doit renvoyer 25.")
    return "moyenne([2, 4, 9]) = 5, variance([2, 4, 9]) = 26/3 ≈ 8,667 et variance([0, 10]) = 25."


def verifier_moyenne_variance():
    """Vérifie les fonctions moyenne et variance."""
    _verifier(_test_moyenne_variance, ["moyenne", "variance"],
              aide={"division": "Une liste vide n'a pas de moyenne : teste avec une liste non vide."})


def _test_somme_deux_des(somme_deux_des):
    with _Graine(162):
        r = [somme_deux_des() for k in range(4000)]
    for x in r:
        if not isinstance(x, int) or x < 2 or x > 12:
            _faux("somme_deux_des() doit renvoyer un entier de 2 à 12. Ta fonction renvoie " + _montre(x) + ".")
    if r.count(3) == 0:
        _faux("sur 4000 lancers, ta fonction ne renvoie jamais 3 (ni aucun nombre impair) : avec 2 × randint(1, 6), un seul dé "
              "est lancé. Les deux dés doivent être indépendants : randint(1, 6) + randint(1, 6).")
    f7, f2 = r.count(7) / 4000, r.count(2) / 4000
    if abs(f7 - 1 / 11) < 0.02 and abs(f2 - 1 / 11) < 0.02:
        _faux("toutes les sommes de 2 à 12 sortent avec la même fréquence : randint(2, 12) n'est pas la somme de deux dés. "
              "Écris randint(1, 6) + randint(1, 6).")
    if abs(f7 - 1 / 6) > 0.03 or abs(f2 - 1 / 36) > 0.015:
        _faux("sur 4000 lancers, la somme 7 sort avec la fréquence " + _ecrire(f7, 3) + " (on attend 6/36 ≈ 0,167) et la somme 2 "
              "avec " + _ecrire(f2, 3) + " (on attend 1/36 ≈ 0,028).")
    return "sur 4000 lancers, la somme 7 sort dans " + _ecrire(100 * f7, 1) + " % des cas (6/36 ≈ 16,7 %), la somme 2 dans " + _ecrire(100 * f2, 1) + " % (1/36 ≈ 2,8 %)."


def verifier_somme_deux_des():
    """Vérifie la fonction somme_deux_des."""
    _verifier(_test_somme_deux_des, ["somme_deux_des"])


def _test_moyenne_echantillon(moyenne_echantillon):
    with _Graine(163):
        r = [moyenne_echantillon(10) for k in range(600)]
    for x in r:
        if not _est_nombre(x):
            _faux("moyenne_echantillon(10) doit renvoyer un nombre. Ta fonction renvoie " + _montre(x) + ".")
        if x > 6 or x < 1:
            _faux("moyenne_echantillon(10) renvoie " + _ecrire(x) + " : la moyenne de dix résultats de dé est entre 1 et 6. "
                  "Divise la somme par n : s / n.")
    m = sum(r) / 600
    v = sum([(x - m) ** 2 for x in r]) / 600
    if v > 1.5:
        _faux("sur 600 échantillons de taille 10, la variance de M_10 vaut " + _ecrire(v, 3) + " : c'est la variance d'un seul dé "
              "(35/12 ≈ 2,92). Les n dés doivent être indépendants : un nouveau randint(1, 6) à chaque tour de boucle.")
    if abs(m - 3.5) > 0.15 or abs(v - 35 / 120) > 0.08:
        _faux("sur 600 échantillons de taille 10, M_10 a pour moyenne " + _ecrire(m, 3) + " et pour variance " + _ecrire(v, 3)
              + " : on attend environ 3,5 et 35/120 ≈ 0,292.")
    return "sur 600 échantillons de taille 10 : moyenne de M_10 ≈ " + _ecrire(m, 3) + " (E = 3,5), variance ≈ " + _ecrire(v, 3) + " (V(X)/10 ≈ 0,292)."


def verifier_moyenne_echantillon():
    """Vérifie la fonction moyenne_echantillon."""
    _verifier(_test_moyenne_echantillon, ["moyenne_echantillon"])


print("Vérifications prêtes. Tu peux commencer.")
