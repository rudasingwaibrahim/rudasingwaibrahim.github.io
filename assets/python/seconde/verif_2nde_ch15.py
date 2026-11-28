"""Vérifications du carnet Python « Seconde · Chapitre 15 · Équation d'une droite passant par deux points ».

Ce fichier accompagne le carnet ch15-equation-droite.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch15 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_coefficient_directeur(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_coefficient_directeur', 'verifier_ordonnee_origine', 'verifier_equation', 'verifier_sur_la_droite']

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
def _test_coefficient_directeur(coefficient_directeur):
    r = coefficient_directeur(-1, -1, 1, 3)
    _nombre_attendu(r, "coefficient_directeur(-1, -1, 1, 3)")
    if _proche(r, 0.5):
        _faux("coefficient_directeur(-1, -1, 1, 3) renvoie 0,5 : tu as inversé le quotient. On divise la variation des ordonnées "
              "par la variation des abscisses : (yB - yA) / (xB - xA).")
    if _proche(r, -2):
        _faux("coefficient_directeur(-1, -1, 1, 3) renvoie -2 au lieu de 2 : écris les deux différences dans le même ordre, "
              "B moins A : (yB - yA) / (xB - xA).")
    if not _proche(r, 2):
        _faux("pour A(-1 ; -1) et B(1 ; 3) : m = (3 - (-1)) / (1 - (-1)) = 4 / 2 = 2. Ta fonction renvoie " + _montre(r)
              + ". Mets des parenthèses : (yB - yA) / (xB - xA).")
    for pts, v in [((0, 3, 4, 1), -0.5), ((2, 5, 7, 5), 0), ((1, 1, 4, 10), 3)]:
        if not _proche(coefficient_directeur(*pts), v):
            _faux("coefficient_directeur" + str(pts) + " doit renvoyer " + str(v) + ". Ta fonction renvoie "
                  + _montre(coefficient_directeur(*pts)) + ".")
    return "pour A(-1 ; -1) et B(1 ; 3), m = 2 ; les cas m = -0,5, m = 0 et m = 3 sont justes aussi."


def verifier_coefficient_directeur():
    """Vérifie la fonction coefficient_directeur."""
    _verifier(_test_coefficient_directeur, ["coefficient_directeur"],
              aide={"division": "xA et xB doivent être différents ; et on divise par xB - xA, pas par yB - yA."})


def _test_ordonnee_origine(ordonnee_origine):
    r = ordonnee_origine(-1, -1, 1, 3)
    _nombre_attendu(r, "ordonnee_origine(-1, -1, 1, 3)")
    if not _proche(r, 1):
        _faux("pour A(-1 ; -1) et B(1 ; 3), m = 2 et p = yA - m × xA = -1 - 2 × (-1) = 1. Ta fonction renvoie " + _montre(r)
              + ". Écris p = yA - m * xA.")
    for pts, v in [((0, 3, 4, 1), 3), ((2, 5, 7, 5), 5), ((1, 1, 4, 10), -2)]:
        if not _proche(ordonnee_origine(*pts), v):
            _faux("ordonnee_origine" + str(pts) + " doit renvoyer " + str(v) + ". Ta fonction renvoie "
                  + _montre(ordonnee_origine(*pts)) + ". Écris p = yA - m * xA.")
    return "pour A(-1 ; -1) et B(1 ; 3), p = 1 ; les autres cas sont justes."


def verifier_ordonnee_origine():
    """Vérifie la fonction ordonnee_origine."""
    _verifier(_test_ordonnee_origine, ["ordonnee_origine"])


def _sans_espace(t):
    return t.replace(" ", "")


def _test_equation(equation):
    try:
        r = equation(2, 5, 2, -4)
    except ZeroDivisionError:
        _faux("equation(2, 5, 2, -4) divise par 0 : quand xA == xB, la droite est parallèle à l'axe des ordonnées. "
              "Traite ce cas en premier : if xA == xB: return \"x = \" + str(xA).")
    if not isinstance(r, str):
        _faux("equation doit renvoyer un texte. Ta fonction renvoie " + _montre(r) + ".")
    if _sans_espace(r) != "x=2":
        _faux("A(2 ; 5) et B(2 ; -4) ont la même abscisse : equation(2, 5, 2, -4) doit renvoyer \"x = 2\". Ta fonction renvoie "
              + _montre(r) + ". Le test est xA == xB.")
    r = equation(-1, -1, 1, 3)
    if not isinstance(r, str) or _sans_espace(r) != "y=2.0x+1.0":
        _faux("equation(-1, -1, 1, 3) doit renvoyer \"y = 2.0 x + 1.0\". Ta fonction renvoie " + _montre(r)
              + ". As-tu écrit p = ordonnee_origine(xA, yA, xB, yB) ?")
    try:
        r = equation(0, 3, 4, 3)
    except ZeroDivisionError:
        _faux("equation(0, 3, 4, 3) divise par 0 : le test du cas particulier porte sur les abscisses, xA == xB.")
    if not isinstance(r, str) or _sans_espace(r) != "y=0.0x+3.0":
        _faux("A(0 ; 3) et B(4 ; 3) ont la même ordonnée, mais pas la même abscisse : la droite a pour équation y = 3, "
              "et equation(0, 3, 4, 3) doit renvoyer \"y = 0.0 x + 3.0\". Ta fonction renvoie " + _montre(r)
              + ". Le cas particulier est xA == xB.")
    return "equation(2, 5, 2, -4) renvoie \"x = 2\", equation(-1, -1, 1, 3) renvoie \"y = 2.0 x + 1.0\" et equation(0, 3, 4, 3) renvoie \"y = 0.0 x + 3.0\"."


def verifier_equation():
    """Vérifie la fonction equation."""
    _verifier(_test_equation, ["equation"],
              aide={"division": "Quand xA == xB, la droite est parallèle à l'axe des ordonnées : traite ce cas avant de calculer m."})


def _test_sur_la_droite(sur_la_droite):
    r = sur_la_droite(-1, -1, 1, 3, 2, 5)
    _booleen(r, "sur_la_droite(-1, -1, 1, 3, 2, 5)", "Compare yC à m * xC + p avec ==.")
    if r is not True:
        _faux("(AB) a pour équation y = 2x + 1 et 2 × 2 + 1 = 5 : C(2 ; 5) est sur la droite. Ta fonction renvoie "
              + _montre(r) + ". Le test est yC == m * xC + p.")
    if sur_la_droite(-1, -1, 1, 3, 5, 2) is not False:
        _faux("2 × 5 + 1 = 11 ≠ 2 : C(5 ; 2) n'est pas sur la droite y = 2x + 1. As-tu échangé xC et yC ? Le test est yC == m * xC + p.")
    if sur_la_droite(2, 5, 2, -4, 2, 100) is not True:
        _faux("(AB) a pour équation x = 2 : le point C(2 ; 100) est sur la droite. Dans ce cas, le test est xC == xA.")
    if sur_la_droite(2, 5, 2, -4, 3, 5) is not False:
        _faux("(AB) a pour équation x = 2 : le point C(3 ; 5) n'est pas sur la droite (3 ≠ 2). Le test est xC == xA.")
    if sur_la_droite(0, 3, 4, 1, 6, 0) is not True or sur_la_droite(0, 3, 4, 1, 6, 1) is not False:
        _faux("la droite passant par (0 ; 3) et (4 ; 1) a pour équation y = -0,5x + 3 : elle passe par (6 ; 0) mais pas par (6 ; 1).")
    return "C(2 ; 5) est sur y = 2x + 1, C(5 ; 2) non ; C(2 ; 100) est sur x = 2, C(3 ; 5) non."


def verifier_sur_la_droite():
    """Vérifie la fonction sur_la_droite."""
    _verifier(_test_sur_la_droite, ["sur_la_droite"])


print("Vérifications prêtes. Tu peux commencer.")
