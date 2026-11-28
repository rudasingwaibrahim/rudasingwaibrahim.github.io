"""Vérifications du carnet Python « Seconde · Chapitre 2 · Puissances : la première qui dépasse une valeur ».

Ce fichier accompagne le carnet ch2-premiere-puissance.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch2 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_puissance(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_puissance', 'verifier_premiere_puissance_sup', 'verifier_premiere_puissance_inf', 'verifier_annees']

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
def _test_puissance(puissance):
    r = puissance(2, 0)
    if r == 0:
        _faux("puissance(2, 0) renvoie 0 : p doit commencer à 1, car a⁰ = 1 (avec p = 0, tous les produits restent nuls).")
    if r == 2:
        _faux("puissance(2, 0) renvoie 2, alors que 2⁰ = 1 : ta boucle tourne une fois de trop. Pour aⁿ, elle tourne n fois : range(n).")
    if r != 1:
        _faux("2⁰ = 1 : puissance(2, 0) doit renvoyer 1. Ta fonction renvoie " + _montre(r) + ".")
    r = puissance(2, 5)
    if r == 64:
        _faux("puissance(2, 5) renvoie 64 = 2⁶ : ta boucle tourne une fois de trop. Pour aⁿ, elle tourne n fois : range(n).")
    if r == 2:
        _faux("puissance(2, 5) renvoie 2 : la boucle s'arrête après un seul tour. " + _RETURN)
    if r == 11:
        _faux("puissance(2, 5) renvoie 11 = 1 + 5 × 2 : tu ajoutes a au lieu de multiplier. Dans la boucle : p = p * a.")
    if r != 32:
        _faux("2⁵ = 32 : puissance(2, 5) doit renvoyer 32. Ta fonction renvoie " + _montre(r) + ".")
    for a, n in [(3, 4), (10, 6), (0.5, 3), (-2, 3), (1.5, 2)]:
        if not _proche(puissance(a, n), a ** n):
            _faux("puissance(" + str(a) + ", " + str(n) + ") doit renvoyer " + _ecrire(a ** n) + ". Ta fonction renvoie "
                  + _montre(puissance(a, n)) + ".")
    return "puissance(2, 0) = 1, puissance(2, 5) = 32, et les cas 3⁴, 10⁶, 0,5³, (-2)³ et 1,5² sont justes."


def verifier_puissance():
    """Vérifie la fonction puissance."""
    _verifier(_test_puissance, ["puissance"])


def _sup(a, b):
    n, p = 0, 1
    while p <= b:
        n, p = n + 1, p * a
    return n


def _test_premiere_puissance_sup(premiere_puissance_sup):
    r = premiere_puissance_sup(2, 8)
    if r == 3:
        _faux("premiere_puissance_sup(2, 8) renvoie 3, mais 2³ = 8 n'est pas strictement supérieur à 8. "
              "On continue tant que p <= b (et non p < b) : la réponse est 4, car 2⁴ = 16 > 8.")
    if r == 16:
        _faux("premiere_puissance_sup(2, 8) renvoie 16 : c'est la puissance 2⁴. La fonction doit renvoyer l'exposant n = 4 : "
              "écris return n (ta fonction renvoie la puissance p).")
    if r == 0:
        _faux("premiere_puissance_sup(2, 8) renvoie 0 : n ne change jamais. Dans la boucle, ajoute n = n + 1.")
    if r != 4:
        _faux("2³ = 8 ≤ 8 et 2⁴ = 16 > 8 : premiere_puissance_sup(2, 8) doit renvoyer 4. Ta fonction renvoie " + _montre(r) + ".")
    r = premiere_puissance_sup(3, 100)
    if r != 5:
        _faux("3⁴ = 81 ≤ 100 et 3⁵ = 243 > 100 : premiere_puissance_sup(3, 100) doit renvoyer 5. Ta fonction renvoie " + _montre(r)
              + ". Vérifie la multiplication dans la boucle : p = p * a.")
    if premiere_puissance_sup(3, 0.5) != 0:
        _faux("3⁰ = 1 > 0,5 : premiere_puissance_sup(3, 0.5) doit renvoyer 0 (la boucle ne tourne pas).")
    if premiere_puissance_sup(1.5, 1000) != _sup(1.5, 1000):
        _faux("premiere_puissance_sup(1.5, 1000) doit renvoyer " + str(_sup(1.5, 1000)) + ". Ta fonction renvoie "
              + _montre(premiere_puissance_sup(1.5, 1000)) + ".")
    return "premiere_puissance_sup(2, 8) = 4, premiere_puissance_sup(3, 100) = 5, et les cas (3 ; 0,5) et (1,5 ; 1000) sont justes."


def verifier_premiere_puissance_sup():
    """Vérifie la fonction premiere_puissance_sup."""
    _verifier(_test_premiere_puissance_sup, ["premiere_puissance_sup"],
              aide={"boucle": "Dans la boucle, p doit être multiplié par a (p = p * a) et n doit augmenter de 1 "
                              "(n = n + 1) ; la condition du while compare p à b : p <= b."})


def _inf(a, b):
    n, p = 0, 1
    while p >= b:
        n, p = n + 1, p * a
    return n


def _test_premiere_puissance_inf(premiere_puissance_inf):
    r = premiere_puissance_inf(0.5, 0.25)
    if r == 0:
        _faux("premiere_puissance_inf(0.5, 0.25) renvoie 0 : la boucle ne tourne jamais, car ta condition est fausse dès le départ "
              "(p = 1). On continue tant que p n'est pas strictement inférieur à b, c'est-à-dire tant que p >= b.")
    if r == 2:
        _faux("premiere_puissance_inf(0.5, 0.25) renvoie 2, mais 0,5² = 0,25 n'est pas strictement inférieur à 0,25. "
              "La condition est p >= b (et non p > b) : la réponse est 3.")
    if r != 3:
        _faux("0,5² = 0,25 et 0,5³ = 0,125 < 0,25 : premiere_puissance_inf(0.5, 0.25) doit renvoyer 3. Ta fonction renvoie "
              + _montre(r) + ".")
    for a, b in [(0.5, 0.01), (0.9, 0.5), (0.1, 0.000001), (0.8, 2)]:
        r = premiere_puissance_inf(a, b)
        if r != _inf(a, b):
            _faux("premiere_puissance_inf(" + str(a) + ", " + str(b) + ") doit renvoyer " + str(_inf(a, b))
                  + ". Ta fonction renvoie " + _montre(r) + ".")
    return ("premiere_puissance_inf(0.5, 0.25) = 3, premiere_puissance_inf(0.5, 0.01) = 7 (0,5⁷ = 0,0078125), "
            "et les autres cas testés sont justes.")


def verifier_premiere_puissance_inf():
    """Vérifie la fonction premiere_puissance_inf."""
    _verifier(_test_premiere_puissance_inf, ["premiere_puissance_inf"],
              aide={"boucle": "Ta boucle ne s'arrête pas : avec 0 < a < 1, les puissances diminuent. "
                              "La condition doit être p >= b, pour s'arrêter au premier p < b."})


def _ans(objectif):
    c, n = 1000, 0
    while c < objectif:
        c, n = c * 1.01, n + 1
    return n


def _test_annees(annees):
    r = annees(1100)
    if r == 100 or r == 99:
        _faux("annees(1100) renvoie " + str(r) + " : tu ajoutes 1,01 € par an. Chaque année, le capital est multiplié par 1,01 : "
              "capital = capital * 1.01.")
    if r == 1:
        _faux("annees(1100) renvoie 1 : avec capital * 1.1, le taux est de 10 %. Pour 1 %, on multiplie par 1,01 : "
              "capital = capital * 1.01.")
    if r == 0:
        _faux("annees(1100) renvoie 0 : n ne change pas. Dans la boucle, écris n = n + 1.")
    if r != 10:
        _faux("1000 × 1,01⁹ ≈ 1093,69 < 1100 et 1000 × 1,01¹⁰ ≈ 1104,62 : annees(1100) doit renvoyer 10. Ta fonction renvoie "
              + _montre(r) + ".")
    if annees(1000) != 0:
        _faux("le capital vaut déjà 1000 € au départ : annees(1000) doit renvoyer 0.")
    r = annees(2000)
    if r != _ans(2000):
        _faux("annees(2000) doit renvoyer " + str(_ans(2000)) + ". Ta fonction renvoie " + _montre(r) + ".")
    return "annees(1100) = 10, annees(2000) = 70 (le capital double en 70 ans) et annees(1000) = 0."


def verifier_annees():
    """Vérifie la fonction annees."""
    _verifier(_test_annees, ["annees"],
              aide={"boucle": "Vérifie que le capital augmente à chaque tour (capital = capital * 1.01) "
                              "et que n augmente de 1 (n = n + 1)."})


print("Vérifications prêtes. Tu peux commencer.")
