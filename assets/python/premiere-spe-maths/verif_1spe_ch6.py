"""Vérifications du carnet Python « Première spécialité · Chapitre 6 · La méthode de Newton ».

Ce fichier accompagne le carnet ch6-methode-newton.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_1spe_ch6 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_fp(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_fp', 'verifier_newton', 'verifier_etapes', 'verifier_heron']

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
def _f(x):
    return 2 * x ** 3 - x - 5


def _fp(x):
    return 6 * x ** 2 - 1


def _test_fp(fp):
    r = fp(1)
    _nombre_attendu(r, "fp(1)")
    if _proche(fp(2), 22) and _proche(fp(0), 0):
        _faux("fp(0) renvoie 0 : la dérivée de -x est -1 (et non -x). f'(x) = 6x² - 1.")
    if _proche(fp(2), 11) and _proche(fp(1), 5) and _proche(fp(0), -1):
        _faux("fp(2) renvoie 11 : la dérivée de x³ est 3x², donc celle de 2x³ est 6x² (et non 6x). Écris 6 * x ** 2 - 1.")
    if _proche(fp(2), 3 * 4 - 1):
        _faux("fp(2) renvoie 11 : la dérivée de 2x³ est 2 × 3x² = 6x² (et non 3x²). Écris 6 * x ** 2 - 1.")
    if not _proche(r, 5) or not _proche(fp(2), 23) or not _proche(fp(-1.5), 12.5):
        _faux("f'(x) = 2 × 3x² - 1 = 6x² - 1 : fp(1) = 5 et fp(2) = 23. Ta fonction renvoie " + _montre(r) + " et "
              + _montre(fp(2)) + ".")
    return "f'(x) = 6x² - 1 : fp(1) = 5, fp(2) = 23, fp(-1,5) = 12,5."


def verifier_fp():
    """Vérifie la fonction fp."""
    _verifier(_test_fp, ["fp"])


def _newton(x, p):
    for n in range(p):
        x = x - _f(x) / _fp(x)
    return x


def _test_newton(newton):
    r = newton(1, 1)
    _nombre_attendu(r, "newton(1, 1)")
    if _proche(r, 1 + 4 / 5 * -1):
        _faux("newton(1, 1) renvoie 0,2 : le signe est faux. La relation est x = x - f(x) / fp(x).")
    if _proche(r, 1 - 5 / -4):
        _faux("newton(1, 1) renvoie 2,25 : tu as inversé le quotient. La relation est x = x - f(x) / fp(x).")
    if _proche(r, _newton(1, 2)):
        _faux("newton(1, 1) renvoie " + _ecrire(r) + " = x₂ : ta boucle tourne une fois de trop. Pour p étapes : range(p).")
    if not _proche(r, 1.8):
        _faux("x₁ = 1 - f(1) / f'(1) = 1 - (-4) / 5 = 1,8. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(newton(1, 0), 1):
        _faux("newton(1, 0) doit renvoyer 1 : aucune étape.")
    if not _proche(newton(1, 3), _newton(1, 3), 1e-12):
        _faux("newton(1, 3) doit renvoyer environ 1,4819. Ta fonction renvoie " + _montre(newton(1, 3)) + ".")
    if abs(_f(newton(1, 8))) > 1e-9:
        _faux("après 8 étapes, f(x) devrait être presque nul.")
    return "newton(1, 1) = 1,8, newton(1, 3) ≈ 1,4819 et newton(1, 8) ≈ 1,4797 (f(x) presque nul)."


def verifier_newton():
    """Vérifie la fonction newton."""
    _verifier(_test_newton, ["newton"],
              aide={"division": "La dérivée fp(x) s'annule : vérifie ta fonction fp et la relation x = x - f(x) / fp(x)."})


def _etapes(x, e):
    n = 0
    while abs(_f(x)) >= e:
        x, n = x - _f(x) / _fp(x), n + 1
    return n


def _test_etapes(etapes):
    r = etapes(1, 0.001)
    if r == 0:
        _faux("etapes(1, 0.001) renvoie 0 : la boucle ne tourne pas, ou n ne change pas. On continue tant que |f(x)| >= e : "
              "while abs(f(x)) >= e, et n augmente de 1 à chaque étape : n = n + 1.")
    if r == 1 and _etapes(1, 0.001) != 1:
        _faux("etapes(1, 0.001) renvoie 1 : au départ, f(1) = -4 est négatif, donc f(x) >= e est faux. Compare la valeur absolue : "
              "abs(f(x)) >= e.")
    if r != _etapes(1, 0.001):
        _faux("etapes(1, 0.001) doit renvoyer " + str(_etapes(1, 0.001)) + ". Ta fonction renvoie " + _montre(r) + ".")
    for x, e in [(1, 1e-10), (2, 1e-6), (1.5, 0.1)]:
        if etapes(x, e) != _etapes(x, e):
            _faux("etapes(" + str(x) + ", " + str(e) + ") doit renvoyer " + str(_etapes(x, e)) + ". Ta fonction renvoie "
                  + _montre(etapes(x, e)) + ".")
    return ("etapes(1, 0.001) = " + str(_etapes(1, 0.001)) + ", etapes(1, 1e-10) = " + str(_etapes(1, 1e-10))
            + " : la précision augmente très vite.")


def verifier_etapes():
    """Vérifie la fonction etapes."""
    _verifier(_test_etapes, ["etapes"],
              aide={"boucle": "Vérifie que x change à chaque tour (x = x - f(x) / fp(x)) et que la condition est abs(f(x)) >= e."})


def _test_heron(heron):
    r = heron(1, 1)
    _nombre_attendu(r, "heron(1, 1)")
    if not _proche(r, 1.5):
        _faux("x₁ = 1 - (1² - 2) / (2 × 1) = 1,5. Ta fonction renvoie " + _montre(r) + ". Mets des parenthèses : "
              "x - (x ** 2 - 2) / (2 * x).")
    r = heron(1, 2)
    if not _proche(r, 17 / 12, 1e-12):
        _faux("x₂ = 1,5 - (1,5² - 2) / 3 = 17/12 ≈ 1,41667. Ta fonction renvoie " + _montre(r)
              + ". On divise par g'(x) = 2x, qui change à chaque étape : (2 * x). Vérifie aussi les parenthèses.")
    if not _proche(heron(1, 5), _math.sqrt(2), 1e-12):
        _faux("heron(1, 5) doit renvoyer √2 ≈ 1,41421356 avec au moins 12 décimales exactes.")
    return "heron(1, 1) = 1,5, heron(1, 2) = 17/12 ≈ 1,41667 et heron(1, 5) ≈ 1,414213562373095 = √2."


def verifier_heron():
    """Vérifie la fonction heron."""
    _verifier(_test_heron, ["heron"])


print("Vérifications prêtes. Tu peux commencer.")
