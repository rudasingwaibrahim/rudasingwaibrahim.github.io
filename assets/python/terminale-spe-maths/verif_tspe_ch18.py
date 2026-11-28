"""Vérifications du carnet Python « Terminale spécialité · Chapitre 18 · Valeurs approchées d'une intégrale ».

Ce fichier accompagne le carnet ch18-rectangles-trapezes-monte-carlo.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch18 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_rectangles(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_rectangles', 'verifier_milieux', 'verifier_trapezes', 'verifier_monte_carlo']

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
def _R(f, a, b, n):
    h = (b - a) / n
    return h * sum([f(a + k * h) for k in range(n)])


def _M(f, a, b, n):
    h = (b - a) / n
    return h * sum([f(a + k * h + h / 2) for k in range(n)])


def _T(f, a, b, n):
    h = (b - a) / n
    return h * sum([(f(a + k * h) + f(a + (k + 1) * h)) / 2 for k in range(n)])


def _test_rectangles(rectangles, f):
    r = rectangles(0, 1, 10)
    _nombre_attendu(r, "rectangles(0, 1, 10)")
    if _proche(r, 10 * _R(f, 0, 1, 10), 1e-9):
        _faux("rectangles(0, 1, 10) renvoie la somme des hauteurs : il faut la multiplier par la largeur h, return S * h.")
    if not _proche(r, _R(f, 0, 1, 10), 1e-9):
        _faux("rectangles(0, 1, 10) doit renvoyer environ " + _ecrire(_R(f, 0, 1, 10)) + ". Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(rectangles(1, 3, 20), _R(f, 1, 3, 20), 1e-9):
        _faux("rectangles(1, 3, 20) doit renvoyer environ " + _ecrire(_R(f, 1, 3, 20)) + ". Ta fonction renvoie "
              + _montre(rectangles(1, 3, 20)) + ". Les points sont x_k = a + k * h.")
    return "rectangles(0, 1, 10) ≈ " + _ecrire(_R(f, 0, 1, 10), 5) + " et rectangles(1, 3, 20) ≈ " + _ecrire(_R(f, 1, 3, 20), 5) + "."


def verifier_rectangles():
    """Vérifie la fonction rectangles."""
    _verifier(_test_rectangles, ["rectangles", "f"])


def _test_milieux(milieux, f):
    r = milieux(0, 1, 10)
    _nombre_attendu(r, "milieux(0, 1, 10)")
    if not _proche(r, _M(f, 0, 1, 10), 1e-9):
        _faux("milieux(0, 1, 10) doit renvoyer environ " + _ecrire(_M(f, 0, 1, 10)) + ". Ta fonction renvoie " + _montre(r)
              + ". Le milieu de [x_k ; x_(k+1)] est x_k + h / 2 : f(a + k * h + h / 2).")
    if not _proche(milieux(1, 3, 20), _M(f, 1, 3, 20), 1e-9):
        _faux("milieux(1, 3, 20) doit renvoyer environ " + _ecrire(_M(f, 1, 3, 20)) + ".")
    return "milieux(0, 1, 10) ≈ " + _ecrire(_M(f, 0, 1, 10), 6) + "."


def verifier_milieux():
    """Vérifie la fonction milieux."""
    _verifier(_test_milieux, ["milieux", "f"])


def _test_trapezes(trapezes, f):
    r = trapezes(0, 1, 10)
    _nombre_attendu(r, "trapezes(0, 1, 10)")
    if _proche(r, 2 * _T(f, 0, 1, 10), 1e-9):
        _faux("trapezes(0, 1, 10) renvoie le double du résultat : l'aire d'un trapèze est h × (f(x_k) + f(x_(k+1))) / 2, "
              "n'oublie pas / 2.")
    if not _proche(r, _T(f, 0, 1, 10), 1e-9):
        _faux("trapezes(0, 1, 10) doit renvoyer environ " + _ecrire(_T(f, 0, 1, 10)) + ". Ta fonction renvoie " + _montre(r)
              + ". Le point suivant est x_(k+1) = a + (k + 1) * h.")
    if not _proche(trapezes(1, 3, 20), _T(f, 1, 3, 20), 1e-9):
        _faux("trapezes(1, 3, 20) doit renvoyer environ " + _ecrire(_T(f, 1, 3, 20)) + ".")
    return "trapezes(0, 1, 10) ≈ " + _ecrire(_T(f, 0, 1, 10), 6) + "."


def verifier_trapezes():
    """Vérifie la fonction trapezes."""
    _verifier(_test_trapezes, ["trapezes", "f"])


def _test_monte_carlo(monte_carlo):
    I = 3 - 3 / _math.e
    with _Graine(180):
        r = monte_carlo(4000)
    _nombre_attendu(r, "monte_carlo(4000)")
    if abs(r - I / 2) < 0.03:
        _faux("monte_carlo(4000) renvoie environ " + _ecrire(r, 3) + " = I/2 : la fréquence estime I / 2, car le rectangle a "
              "l'aire 2. Renvoie 2 * C / n.")
    if abs(r - 2) < 1e-9:
        _faux("monte_carlo(4000) renvoie 2 : tous les points sont sous la courbe, car y est tiré dans [0 ; 1] et f(x) ≥ 1. "
              "Tire y dans [0 ; 2] : y = 2 * random.random().")
    if abs(r - I) > 0.04:
        _faux("monte_carlo(4000) renvoie " + _ecrire(r, 4) + ", trop loin de I ≈ 1,8964.")
    return "monte_carlo(4000) ≈ " + _ecrire(r, 4) + " (I ≈ 1,8964)."


def verifier_monte_carlo():
    """Vérifie la fonction monte_carlo."""
    _verifier(_test_monte_carlo, ["monte_carlo"])


print("Vérifications prêtes. Tu peux commencer.")
