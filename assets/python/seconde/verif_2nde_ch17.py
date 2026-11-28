"""Vérifications du carnet Python « Seconde · Chapitre 17 · Alignement, parallélisme et point d'intersection ».

Ce fichier accompagne le carnet ch17-alignement-parallelisme.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch17 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_determinant(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_determinant', 'verifier_alignes', 'verifier_parallele', 'verifier_intersection', 'verifier_pieces']

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
def _test_determinant(determinant):
    r = determinant(2, 1, 4, 2)
    _nombre_attendu(r, "determinant(2, 1, 4, 2)")
    if r == 6 and determinant(1, 2, 3, 4) == -5:
        _faux("determinant(2, 1, 4, 2) renvoie 6 : la formule est x × y' - y × x', soit x * y2 - y * x2.")
    if r == 8:
        _faux("determinant(2, 1, 4, 2) renvoie 8 : le déterminant est une différence, x * y2 - y * x2.")
    if r != 0:
        _faux("det = 2 × 2 - 1 × 4 = 0 (les vecteurs sont colinéaires). Ta fonction renvoie " + _montre(r)
              + ". La formule est x * y2 - y * x2.")
    if determinant(1, 2, 3, 4) != -2 or determinant(3, -1, 2, 5) != 17:
        _faux("determinant(1, 2, 3, 4) = 1 × 4 - 2 × 3 = -2 et determinant(3, -1, 2, 5) = 15 + 2 = 17. Ta fonction renvoie "
              + _montre(determinant(1, 2, 3, 4)) + " et " + _montre(determinant(3, -1, 2, 5)) + ".")
    return "det((2 ; 1), (4 ; 2)) = 0, det((1 ; 2), (3 ; 4)) = -2 et det((3 ; -1), (2 ; 5)) = 17."


def verifier_determinant():
    """Vérifie la fonction determinant."""
    _verifier(_test_determinant, ["determinant"])


def _test_alignes(alignes):
    r = alignes(1, 1, 3, 2, 7, 4)
    _booleen(r, "alignes(1, 1, 3, 2, 7, 4)", "Compare le déterminant à 0 avec ==.")
    if r is False and alignes(1, 1, 3, 2, 7, 5) is True:
        _faux("ta fonction répond l'inverse : des points sont alignés quand le déterminant est nul, == 0.")
    if r is not True:
        _faux("AB(2 ; 1) et AC(6 ; 3) : det = 2 × 3 - 1 × 6 = 0, donc A(1 ; 1), B(3 ; 2), C(7 ; 4) sont alignés. Ta fonction renvoie "
              + _montre(r) + ". Utilise les vecteurs : determinant(xB - xA, yB - yA, xC - xA, yC - yA).")
    if alignes(1, 1, 3, 2, 7, 5) is not False:
        _faux("A(1 ; 1), B(3 ; 2) et C(7 ; 5) ne sont pas alignés (det = 2 × 4 - 1 × 6 = 2). Ta fonction répond True. "
              "Utilise les vecteurs AB et AC, et non les coordonnées des points.")
    if alignes(2, 3, 2, 7, 2, -1) is not True or alignes(-1, 4, 1, 0, 2, -3) is not False:
        _faux("(2 ; 3), (2 ; 7), (2 ; -1) sont alignés (sur la droite x = 2) ; (-1 ; 4), (1 ; 0), (2 ; -3) ne le sont pas. "
              "Vérifie les coordonnées de AB (xB - xA ; yB - yA) et de AC (xC - xA ; yC - yA), dans cet ordre.")
    return "A(1 ; 1), B(3 ; 2), C(7 ; 4) sont alignés, pas A(1 ; 1), B(3 ; 2), C(7 ; 5) ; les autres cas sont justes."


def verifier_alignes():
    """Vérifie la fonction alignes."""
    _verifier(_test_alignes, ["alignes"])


def _test_parallele(parallele):
    r = parallele(0, 0, 2, 1, 1, 3, 5, 5)
    _booleen(r, "parallele(0, 0, 2, 1, 1, 3, 5, 5)", "Compare le déterminant à 0 avec ==.")
    if r is not True:
        _faux("AB(2 ; 1) et CD(4 ; 2) : det = 2 × 2 - 1 × 4 = 0, les droites sont parallèles. Ta fonction renvoie " + _montre(r)
              + ". Utilise les vecteurs AB et CD : determinant(xB - xA, yB - yA, xD - xC, yD - yC).")
    if parallele(0, 0, 2, 1, 1, 3, 5, 6) is not False:
        _faux("AB(2 ; 1) et CD(4 ; 3) ne sont pas colinéaires (det = 6 - 4 = 2) : les droites sont sécantes.")
    if parallele(0, 0, 1, 1, 3, 0, 4, 1) is not True:
        _faux("AB(1 ; 1) et CD(1 ; 1) : (AB) et (CD) sont parallèles. Ta fonction répond False : le deuxième vecteur est CD "
              "(xD - xC ; yD - yC).")
    return "(AB) ∥ (CD) pour A(0 ; 0), B(2 ; 1), C(1 ; 3), D(5 ; 5), et les autres cas sont justes."


def verifier_parallele():
    """Vérifie la fonction parallele."""
    _verifier(_test_parallele, ["parallele"])


def _test_intersection(abscisse_intersection, ordonnee_intersection):
    x = abscisse_intersection(-1, 20, -2, 36)
    _nombre_attendu(x, "abscisse_intersection(-1, 20, -2, 36)")
    if _proche(x, -16):
        _faux("abscisse_intersection(-1, 20, -2, 36) renvoie -16 au lieu de 16 : de m1 x + p1 = m2 x + p2, on tire "
              "(m1 - m2) x = p2 - p1, donc x = (p2 - p1) / (m1 - m2).")
    if not _proche(x, 16):
        _faux("-x + 20 = -2x + 36 donne x = 16. Ta fonction renvoie " + _montre(x) + ".")
    y = ordonnee_intersection(-1, 20, -2, 36)
    if _proche(y, 20):
        _faux("ordonnee_intersection(-1, 20, -2, 36) renvoie 20 : on remplace x dans l'équation de la première droite, "
              "y = m1 * x + p1.")
    if not _proche(y, 4):
        _faux("pour x = 16, y = -16 + 20 = 4. Ta fonction renvoie " + _montre(y) + ". Écris y = m1 * x + p1.")
    if not _proche(abscisse_intersection(2, 1, -1, 7), 2) or not _proche(ordonnee_intersection(2, 1, -1, 7), 5):
        _faux("les droites y = 2x + 1 et y = -x + 7 se coupent en (2 ; 5).")
    return "les droites y = -x + 20 et y = -2x + 36 se coupent en (16 ; 4), les droites y = 2x + 1 et y = -x + 7 en (2 ; 5)."


def verifier_intersection():
    """Vérifie les fonctions abscisse_intersection et ordonnee_intersection."""
    _verifier(_test_intersection, ["abscisse_intersection", "ordonnee_intersection"],
              aide={"division": "Les droites doivent être sécantes : m1 doit être différent de m2."})


def _test_pieces(pieces_2, pieces_1):
    if not _est_nombre(pieces_2) or not _est_nombre(pieces_1):
        _faux("pieces_2 et pieces_1 doivent être des nombres, obtenus avec tes fonctions.")
    if _proche(pieces_2, 16) and _proche(pieces_1, 16):
        _faux("pieces_1 vaut 16 : c'est l'abscisse. Le nombre de pièces de 1 € est l'ordonnée du point d'intersection : "
              "ordonnee_intersection(-1, 20, -2, 36).")
    if not _proche(pieces_2, 16) or not _proche(pieces_1, 4):
        _faux("les deux droites ont pour équations y = -x + 20 (m1 = -1, p1 = 20) et y = -2x + 36 (m2 = -2, p2 = 36). "
              "Tu obtiens " + _montre(pieces_2) + " et " + _montre(pieces_1) + ".")
    return "16 pièces de 2 € et 4 pièces de 1 € (16 + 4 = 20 pièces, 32 + 4 = 36 €)."


def verifier_pieces():
    """Vérifie les deux réponses du problème du porte-monnaie."""
    _verifier(_test_pieces, ["pieces_2", "pieces_1"])


print("Vérifications prêtes. Tu peux commencer.")
