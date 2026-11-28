"""Vérifications du carnet Python « Terminale technologique · Chapitre 6 · Triangle de Pascal, loi binomiale et espérance ».

Ce fichier accompagne le carnet ch6-pascal-loi-binomiale.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tle_techno_ch6 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_pascal(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_pascal', 'verifier_esperance', 'verifier_loi_binomiale', 'verifier_frequences']

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
def _pascal(n):
    T = [[1]]
    for i in range(1, n + 1):
        prec, ligne = T[i - 1], [1]
        for k in range(1, i):
            ligne.append(prec[k - 1] + prec[k])
        ligne.append(1)
        T.append(ligne)
    return T


def _test_pascal(pascal):
    r = pascal(4)
    _est_liste(r, "pascal(4)")
    if len(r) > 2 and r[2] == [1, 1, 1]:
        _faux("la ligne 2 de ton triangle est [1, 1, 1] : chaque nombre intérieur est la somme des deux nombres au-dessus, "
              "prec[k - 1] + prec[k].")
    if r != _pascal(4):
        _faux("pascal(4) doit renvoyer " + _montre(_pascal(4)) + ". Ta fonction renvoie " + _montre(r) + ".")
    if pascal(10) != _pascal(10):
        _faux("la ligne 10 doit être " + _montre(_pascal(10)[10]) + ".")
    return "pascal(4) se termine par [1, 4, 6, 4, 1] et la ligne 10 est " + _montre(_pascal(10)[10]) + "."


def verifier_pascal():
    """Vérifie la fonction pascal."""
    _verifier(_test_pascal, ["pascal"],
              aide={"indice": "La ligne précédente a i éléments, d'indices 0 à i - 1 : utilise prec[k - 1] + prec[k], pour k de 1 à i - 1."})


def _test_esperance(esperance):
    r = esperance([-4, 0, 4, 20], [0.5, 0.2, 0.2, 0.1])
    _nombre_attendu(r, "esperance([-4, 0, 4, 20], [0.5, 0.2, 0.2, 0.1])")
    if _proche(r, 20):
        _faux("ta fonction renvoie 20 : elle additionne les valeurs sans les multiplier par leurs probabilités : E = E + x[i] * p[i].")
    if _proche(r, 2):
        _faux("ta fonction renvoie 2 = 20 × 0,1 : seul le dernier produit est gardé. Il faut ajouter chaque produit : E = E + x[i] * p[i].")
    if not _proche(r, 0.8):
        _faux("E = 0,5 × (-4) + 0,2 × 0 + 0,2 × 4 + 0,1 × 20 = 0,8. Ta fonction renvoie " + _montre(r) + ".")
    return "esperance([-4, 0, 4, 20], [0.5, 0.2, 0.2, 0.1]) = 0,8."


def verifier_esperance():
    """Vérifie la fonction esperance."""
    _verifier(_test_esperance, ["esperance"])


def _loi(n, p):
    c = _pascal(n)[n]
    return [c[k] * p ** k * (1 - p) ** (n - k) for k in range(n + 1)]


def _test_loi_binomiale(loi_binomiale):
    r = loi_binomiale(4, 0.5)
    _est_liste(r, "loi_binomiale(4, 0.5)")
    if _listes_proches(r, [1 / 16] * 5):
        _faux("toutes tes probabilités valent 1/16 : il manque le nombre de chemins c[k] (coefficient du triangle de Pascal).")
    if not _listes_proches(r, [1 / 16, 4 / 16, 6 / 16, 4 / 16, 1 / 16]):
        _faux("pour B(4 ; 0,5), on attend [1/16, 4/16, 6/16, 4/16, 1/16]. Ta fonction renvoie " + _montre(r)
              + ". L'exposant de 1 - p est n - k.")
    r = loi_binomiale(5, 0.4)
    if not _listes_proches(r, _loi(5, 0.4)):
        _faux("loi_binomiale(5, 0.4) doit renvoyer environ " + _montre([round(x, 4) for x in _loi(5, 0.4)]) + ". Ta fonction renvoie "
              + _montre(r) + ". L'exposant de 1 - p est le nombre d'échecs, n - k.")
    return "loi_binomiale(4, 0.5) = [1/16, 4/16, 6/16, 4/16, 1/16] et loi_binomiale(5, 0.4) ≈ " + _montre([round(x, 4) for x in _loi(5, 0.4)]) + "."


def verifier_loi_binomiale():
    """Vérifie la fonction loi_binomiale."""
    _verifier(_test_loi_binomiale, ["loi_binomiale"])


def _test_frequences(frequences):
    with _Graine(60):
        r = frequences(3000, 5, 0.4)
    _est_liste(r, "frequences(3000, 5, 0.4)")
    if len(r) != 6:
        _faux("frequences(3000, 5, 0.4) doit renvoyer 6 fréquences (0 à 5 succès). Ta liste en contient " + str(len(r)) + ".")
    t = 0
    for x in r:
        t = t + x
    if t > 1.5:
        _faux("tes « fréquences » valent jusqu'à " + _ecrire(t, 0) + " au total : ce sont des effectifs. Divise par N : [e / N for e in eff].")
    if t < 0.5:
        _faux("la somme de tes fréquences vaut " + _ecrire(t, 4) + " au lieu de 1 : chaque échantillon doit augmenter de 1 l'effectif "
              "de son nombre de succès, eff[s] = eff[s] + 1.")
    att = _loi(5, 0.4)
    for k in range(6):
        if abs(r[k] - att[k]) > 0.04:
            _faux("sur 3000 échantillons, la fréquence de " + str(k) + " succès vaut " + _ecrire(r[k], 3) + ", trop loin de P(X = "
                  + str(k) + ") ≈ " + _ecrire(att[k], 3) + ".")
    return "sur 3000 échantillons, les fréquences " + _montre([round(x, 3) for x in r]) + " sont proches de la loi B(5 ; 0,4)."


def verifier_frequences():
    """Vérifie les fonctions nb_succes et frequences."""
    _verifier(_test_frequences, ["frequences"])


print("Vérifications prêtes. Tu peux commencer.")
