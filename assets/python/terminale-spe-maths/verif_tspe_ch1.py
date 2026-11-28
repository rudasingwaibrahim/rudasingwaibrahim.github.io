"""Vérifications du carnet Python « Terminale spécialité · Chapitre 1 · Récurrence, conjecture et recherche de seuils ».

Ce fichier accompagne le carnet ch1-recurrence-seuils.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch1 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_u(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_u', 'verifier_seuil', 'verifier_seuil_convergente', 'verifier_seuil_geo']

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
def _u(n):
    t = 1
    for i in range(n):
        t = 2 * t + 1
    return t


def _test_u(u):
    r = u(0)
    if r == 3:
        _faux("u(0) renvoie 3 = u_1 : ta boucle tourne une fois de trop. Pour u_n, elle tourne n fois : range(n).")
    if r != 1:
        _faux("u(0) doit renvoyer u_0 = 1. Ta fonction renvoie " + _montre(r) + ".")
    r = u(1)
    if r == 4:
        _faux("u(1) renvoie 4 = 2 × (1 + 1) : la relation est u_(n+1) = 2 u_n + 1, soit terme = 2 * terme + 1.")
    if r != 3:
        _faux("u_1 = 2 × 1 + 1 = 3. Ta fonction renvoie " + _montre(r) + ".")
    for n in [2, 5, 10, 30]:
        if u(n) != _u(n):
            _faux("u(" + str(n) + ") doit renvoyer " + str(_u(n)) + ". Ta fonction renvoie " + _montre(u(n)) + ".")
    return "u(0) = 1, u(1) = 3, u(5) = 63 et u(30) = " + str(_u(30)) + "."


def verifier_u():
    """Vérifie la fonction u."""
    _verifier(_test_u, ["u"])


def _seuil(A):
    n, t = 0, 1
    while t <= A:
        n, t = n + 1, 2 * t + 1
    return n


def _test_seuil(seuil):
    r = seuil(1000)
    if r == 1023:
        _faux("seuil(1000) renvoie 1023 : c'est le terme u_9. La fonction doit renvoyer le rang : return n.")
    if r != 9:
        _faux("u_8 = 511 ≤ 1000 et u_9 = 1023 > 1000 : seuil(1000) doit renvoyer 9. Ta fonction renvoie " + _montre(r) + ".")
    r = seuil(1023)
    if r == 9:
        _faux("seuil(1023) renvoie 9, mais u_9 = 1023 n'est pas strictement supérieur à 1023. On continue tant que terme <= A : "
              "la réponse est 10.")
    if r != 10:
        _faux("seuil(1023) doit renvoyer 10. Ta fonction renvoie " + _montre(r) + ".")
    if seuil(0) != 0 or seuil(10 ** 6) != _seuil(10 ** 6):
        _faux("seuil(0) doit renvoyer 0 et seuil(10 ** 6) doit renvoyer " + str(_seuil(10 ** 6)) + ".")
    return "seuil(1000) = 9, seuil(1023) = 10 et seuil(10 ** 6) = " + str(_seuil(10 ** 6)) + "."


def verifier_seuil():
    """Vérifie la fonction seuil."""
    _verifier(_test_seuil, ["seuil"],
              aide={"boucle": "Vérifie que terme change à chaque tour (terme = 2 * terme + 1) et que n augmente."})


def _sc(e):
    n = 1
    while (1 + 1 / n ** 2) - 1 >= e:
        n = n + 1
    return n


def _test_seuil_convergente(seuil_convergente):
    try:
        r = seuil_convergente(0.001)
    except ZeroDivisionError:
        _faux("ta fonction divise par 0 : v_n n'est défini que pour n ≥ 1. Commence avec n = 1.")
    if r != 32:
        _faux("1/31² ≈ 0,00104 ≥ 0,001 et 1/32² ≈ 0,00098 < 0,001 : seuil_convergente(0.001) doit renvoyer 32. Ta fonction renvoie "
              + _montre(r) + ". La condition porte sur l'écart à la limite : v(n) - 1 >= e.")
    for e in [0.0002, 0.5]:
        if seuil_convergente(e) != _sc(e):
            _faux("seuil_convergente(" + str(e) + ") doit renvoyer " + str(_sc(e)) + ". Ta fonction renvoie "
                  + _montre(seuil_convergente(e)) + ".")
    return "seuil_convergente(0.001) = 32, seuil_convergente(0.0002) = 71 et seuil_convergente(0.5) = 2."


def verifier_seuil_convergente():
    """Vérifie la fonction seuil_convergente."""
    _verifier(_test_seuil_convergente, ["seuil_convergente"],
              aide={"boucle": "Ta boucle ne s'arrête pas : v(n) tend vers 1, donc v(n) >= e reste vrai. Compare l'écart "
                              "v(n) - 1 à e.",
                    "division": "v_n n'est défini que pour n ≥ 1 : commence avec n = 1."})


def _sg(q, e):
    n, t = 0, 1
    while t >= e:
        n, t = n + 1, t * q
    return n


def _test_seuil_geo(seuil_geo):
    r = seuil_geo(0.5, 0.001)
    if r == 0:
        _faux("seuil_geo(0.5, 0.001) renvoie 0 : n doit augmenter de 1 à chaque tour, n = n + 1.")
    if r != 10:
        _faux("0,5⁹ ≈ 0,00195 ≥ 0,001 et 0,5¹⁰ ≈ 0,00098 < 0,001 : seuil_geo(0.5, 0.001) doit renvoyer 10. Ta fonction renvoie "
              + _montre(r) + ". Dans la boucle : t = t * q puis n = n + 1.")
    for q, e in [(0.9, 0.001), (0.99, 0.01)]:
        if seuil_geo(q, e) != _sg(q, e):
            _faux("seuil_geo(" + str(q) + ", " + str(e) + ") doit renvoyer " + str(_sg(q, e)) + ". Ta fonction renvoie "
                  + _montre(seuil_geo(q, e)) + ".")
    return "seuil_geo(0.5, 0.001) = 10, seuil_geo(0.9, 0.001) = 66 et seuil_geo(0.99, 0.01) = 459."


def verifier_seuil_geo():
    """Vérifie la fonction seuil_geo."""
    _verifier(_test_seuil_geo, ["seuil_geo"],
              aide={"boucle": "Ta boucle ne s'arrête pas : t doit être multiplié par q à chaque tour (t = t * q)."})


print("Vérifications prêtes. Tu peux commencer.")
