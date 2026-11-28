"""Vérifications du carnet Python « Première spécialité · Chapitre 5 · La méthode de Monte-Carlo ».

Ce fichier accompagne le carnet ch5-monte-carlo.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_1spe_ch5 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_sous_parabole(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_sous_parabole', 'verifier_estimation_aire', 'verifier_dans_quart_disque', 'verifier_estimation_pi']

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
def _frequence_bool(fonction, nom, n, graine):
    with _Graine(graine):
        r = [fonction() for k in range(n)]
    for x in r:
        if x is not True and x is not False:
            _faux(nom + "() doit renvoyer True ou False. Ta fonction renvoie " + _montre(x) + ".")
    return r.count(True) / n


def _test_sous_parabole(sous_parabole):
    f = _frequence_bool(sous_parabole, "sous_parabole", 4000, 51)
    if abs(f - 2 / 3) < 0.04:
        _faux("sur 4000 points, ta fonction répond True dans environ 2 cas sur 3 : elle teste « au-dessus » de la parabole. "
              "Sous la parabole, la condition est y <= x ** 2.")
    if abs(f - 0.75) < 0.04:
        _faux("sur 4000 points, ta fonction répond True dans environ 75 % des cas : tu as écrit x * 2 (le double) au lieu du "
              "carré x ** 2.")
    if f > 0.95 or f < 0.01:
        _faux("ta fonction répond presque toujours la même chose : y doit être tiré au hasard, indépendamment de x, "
              "avec y = random.random().")
    if abs(f - 1 / 3) > 0.04:
        _faux("sur 4000 points, ta fonction répond True avec la fréquence " + _ecrire(f, 3) + ", trop loin de 1/3. "
              "La condition est y <= x ** 2, avec x et y tirés au hasard.")
    return "sur 4000 points, " + _ecrire(100 * f, 1) + " % sont sous la parabole (l'aire exacte est 1/3)."


def verifier_sous_parabole():
    """Vérifie la fonction sous_parabole."""
    _verifier(_test_sous_parabole, ["sous_parabole"])


def _test_estimation_aire(estimation_aire):
    with _Graine(52):
        r = estimation_aire(4000)
    _nombre_attendu(r, "estimation_aire(4000)")
    if r > 1:
        _faux("estimation_aire(4000) renvoie " + _ecrire(r) + " : c'est un effectif. Une fréquence est un effectif divisé par n : "
              "compteur / n.")
    if abs(r - 2 / 3) < 0.04:
        _faux("estimation_aire(4000) renvoie environ 2/3 : tu comptes les points au-dessus de la parabole. "
              "Le test est if sous_parabole():.")
    if abs(r - 1 / 3) > 0.04:
        _faux("estimation_aire(4000) renvoie " + _ecrire(r, 3) + ", trop loin de 1/3.")
    return "estimation_aire(4000) ≈ " + _ecrire(r, 3) + ", proche de 1/3."


def verifier_estimation_aire():
    """Vérifie la fonction estimation_aire."""
    _verifier(_test_estimation_aire, ["estimation_aire"])


def _test_dans_quart_disque(dans_quart_disque):
    f = _frequence_bool(dans_quart_disque, "dans_quart_disque", 4000, 53)
    if abs(f - 0.5) < 0.04:
        _faux("sur 4000 points, ta fonction répond True dans environ la moitié des cas : x + y <= 1 décrit un triangle. "
              "Le quart de disque est x ** 2 + y ** 2 <= 1.")
    if abs(f - _math.pi / 4) > 0.04:
        _faux("sur 4000 points, ta fonction répond True avec la fréquence " + _ecrire(f, 3) + ", trop loin de π/4 ≈ 0,785. "
              "La condition est x ** 2 + y ** 2 <= 1.")
    return "sur 4000 points, " + _ecrire(100 * f, 1) + " % sont dans le quart de disque (π/4 ≈ 78,5 %)."


def verifier_dans_quart_disque():
    """Vérifie la fonction dans_quart_disque."""
    _verifier(_test_dans_quart_disque, ["dans_quart_disque"])


def _test_estimation_pi(estimation_pi):
    with _Graine(54):
        r = estimation_pi(4000)
    _nombre_attendu(r, "estimation_pi(4000)")
    if abs(r - _math.pi / 4) < 0.06:
        _faux("estimation_pi(4000) renvoie environ 0,785 : c'est une estimation de π/4. Pour estimer π, on multiplie par 4 "
              "la fréquence : 4 * compteur / n.")
    if abs(r - _math.pi / 16) < 0.03:
        _faux("estimation_pi(4000) renvoie environ 0,196 : tu divises par 4. On multiplie par 4 la fréquence : 4 * compteur / n.")
    if abs(r - _math.pi) > 0.12:
        _faux("estimation_pi(4000) renvoie " + _ecrire(r, 4) + ", trop loin de π.")
    return "estimation_pi(4000) ≈ " + _ecrire(r, 4) + " (π ≈ 3,1416)."


def verifier_estimation_pi():
    """Vérifie la fonction estimation_pi."""
    _verifier(_test_estimation_pi, ["estimation_pi"])


print("Vérifications prêtes. Tu peux commencer.")
