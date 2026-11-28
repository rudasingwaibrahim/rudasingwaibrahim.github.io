"""Vérifications du carnet Python « Terminale spécialité · Chapitre 9 · Seuils et valeurs approchées de √2, du nombre d'or et de e ».

Ce fichier accompagne le carnet ch9-seuils-valeurs-approchees.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch9 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_seuil_aquarium(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_seuil_aquarium', 'verifier_racine2', 'verifier_nombre_or', 'verifier_approx_e']

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
def _aq(s):
    n, u = 0, 200
    while u <= s:
        n, u = n + 1, 0.85 * u + 45
    return n


def _test_seuil_aquarium(seuil_aquarium):
    r = seuil_aquarium(299)
    if _est_nombre(r) and r > 290 and r < 300:
        _faux("seuil_aquarium(299) renvoie " + _ecrire(r) + " : c'est le terme u_n. La fonction doit renvoyer le rang : return n.")
    if r != 29:
        _faux("seuil_aquarium(299) doit renvoyer 29 (u_28 ≈ 298,9 et u_29 ≈ 299,1). Ta fonction renvoie " + _montre(r)
              + ". La relation est u = 0.85 * u + 45.")
    for s in [250, 299.9, 200]:
        if seuil_aquarium(s) != _aq(s):
            _faux("seuil_aquarium(" + str(s) + ") doit renvoyer " + str(_aq(s)) + ". Ta fonction renvoie " + _montre(seuil_aquarium(s)) + ".")
    return "seuil_aquarium(299) = 29, seuil_aquarium(250) = " + str(_aq(250)) + " et seuil_aquarium(299.9) = " + str(_aq(299.9)) + "."


def verifier_seuil_aquarium():
    """Vérifie la fonction seuil_aquarium."""
    _verifier(_test_seuil_aquarium, ["seuil_aquarium"],
              aide={"boucle": "Ta boucle ne s'arrête pas : vérifie la relation u = 0.85 * u + 45 ; les termes se rapprochent "
                              "de 300 sans l'atteindre, donc s doit être inférieur à 300."})


def _test_racine2(racine2):
    r = racine2(0.001)
    _est_liste(r, "racine2(0.001)")
    if len(r) != 2:
        _faux("racine2 doit renvoyer une liste [a, b]. Ta fonction renvoie " + _montre(r) + ".")
    a, b = r[0], r[1]
    if b - a > 0.001:
        _faux("l'amplitude b - a de racine2(0.001) vaut " + _ecrire(b - a) + " > 0,001.")
    if not (a * a <= 2 <= b * b):
        _faux("racine2(0.001) renvoie " + _montre(r) + ", qui n'encadre pas √2 ≈ 1,4142. On compare le carré : si c * c < 2, "
              "alors c < √2, donc √2 est dans [c ; b] et on remplace a par c (a = c) ; sinon b = c.")
    r = racine2(1e-10)
    if not (r[1] - r[0] <= 1e-10 and r[0] <= _math.sqrt(2) <= r[1]):
        _faux("racine2(1e-10) doit encadrer √2 avec une amplitude ≤ 10⁻¹⁰.")
    return "racine2(0.001) = " + _montre(racine2(0.001)) + " ; racine2(1e-10) encadre √2 ≈ 1,4142135623."


def verifier_racine2():
    """Vérifie la fonction racine2."""
    _verifier(_test_racine2, ["racine2"])


def _test_nombre_or(nombre_or):
    r = nombre_or(1)
    _nombre_attendu(r, "nombre_or(1)")
    if _proche(r, 0.5) and _proche(nombre_or(2), 2 / 3):
        _faux("nombre_or(1) renvoie 0,5 : la relation est u = 1 + 1 / u (et non 1 / (1 + u)).")
    if not _proche(r, 2) or not _proche(nombre_or(2), 1.5):
        _faux("u_1 = 1 + 1/1 = 2 et u_2 = 1 + 1/2 = 1,5. Ta fonction renvoie " + _montre(r) + " et " + _montre(nombre_or(2))
              + ". La relation est u = 1 + 1 / u.")
    if not _proche(nombre_or(30), (1 + _math.sqrt(5)) / 2, 1e-11):
        _faux("nombre_or(30) doit être très proche de (1 + √5) / 2 ≈ 1,6180340.")
    return "u_1 = 2, u_2 = 1,5, u_3 ≈ 1,667 et u_30 ≈ 1,6180340 ≈ (1 + √5)/2."


def verifier_nombre_or():
    """Vérifie la fonction nombre_or."""
    _verifier(_test_nombre_or, ["nombre_or"])


def _test_approx_e(approx_e):
    r = approx_e(1)
    _nombre_attendu(r, "approx_e(1)")
    if _proche(r, 1):
        _faux("approx_e(1) renvoie 1 au lieu de 1 + 1/1! = 2 : S doit commencer à 1 = 1/0!.")
    if not _proche(r, 2):
        _faux("S_1 = 1 + 1/1! = 2. Ta fonction renvoie " + _montre(r) + ".")
    r = approx_e(3)
    if _proche(r, 1 + 1 + 2 + 6):
        _faux("approx_e(3) renvoie 10 = 1 + 1 + 2 + 6 : tu multiplies t par k, ce qui donne k!. Pour 1/k!, on divise : t = t / k.")
    if _proche(r, 1 + 1 + 1 / 2 + 1 / 3):
        _faux("approx_e(3) ajoute 1/3 au lieu de 1/3! = 1/6 : t doit être mis à jour à partir de sa valeur précédente : "
              "t = t / k.")
    if _proche(r, 1 + 1 / 2 + 1 / 6):
        _faux("approx_e(3) renvoie 1/1! + 1/2! + 1/3! : il manque 1/0! = 1, S doit commencer à 1.")
    if not _proche(r, 1 + 1 + 1 / 2 + 1 / 6):
        _faux("S_3 = 1 + 1 + 1/2 + 1/6 ≈ 2,6667. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(approx_e(15), _math.exp(1), 1e-12):
        _faux("approx_e(15) doit valoir e ≈ 2,718281828459 à 10⁻¹¹ près.")
    return "S_1 = 2, S_3 ≈ 2,6667, S_10 ≈ 2,7182818 et S_15 ≈ 2,718281828458995."


def verifier_approx_e():
    """Vérifie la fonction approx_e."""
    _verifier(_test_approx_e, ["approx_e"])


print("Vérifications prêtes. Tu peux commencer.")
