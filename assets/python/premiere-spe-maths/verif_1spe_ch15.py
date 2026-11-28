"""Vérifications du carnet Python « Première spécialité · Chapitre 15 · Espérance, variance, écart type et simulation ».

Ce fichier accompagne le carnet ch15-esperance-variance.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_1spe_ch15 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_esperance(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_esperance', 'verifier_variance', 'verifier_ecart_type', 'verifier_gain', 'verifier_moyenne', 'verifier_frequence_lettre']

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
_X = [-4, 0, 4, 20]
_P = [0.5, 0.2, 0.2, 0.1]


def _test_esperance(esperance):
    r = esperance(_X, _P)
    _nombre_attendu(r, "esperance(X, P)")
    if _proche(r, 20):
        _faux("avec X = [-4, 0, 4, 20] et P = [0.5, 0.2, 0.2, 0.1], ta fonction renvoie 20 : elle additionne les valeurs sans "
              "les multiplier par leurs probabilités. Écris E = E + X[i] * P[i].")
    if _proche(r, 2):
        _faux("ta fonction renvoie 2 = 20 × 0,1 : seul le dernier produit est gardé. Il faut ajouter chaque produit : "
              "E = E + X[i] * P[i].")
    if _proche(r, 0.2):
        _faux("ta fonction renvoie 0,2 : on ne divise pas par le nombre de valeurs. L'espérance est la somme des p_i × x_i.")
    if not _proche(r, 0.8):
        _faux("E(X) = 0,5 × (-4) + 0,2 × 0 + 0,2 × 4 + 0,1 × 20 = 0,8. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(esperance([95, 0, -10], [0.5, 0.22, 0.28]), 44.7) or not _proche(esperance([1, 2, 3, 4, 5, 6], [1 / 6] * 6), 3.5):
        _faux("esperance([95, 0, -10], [0.5, 0.22, 0.28]) doit renvoyer 44,7 et l'espérance d'un dé équilibré vaut 3,5.")
    return "E(X) = 0,8 pour la loi du cours ; 44,7 pour le gain G ; 3,5 pour un dé équilibré."


def verifier_esperance():
    """Vérifie la fonction esperance."""
    _verifier(_test_esperance, ["esperance"],
              aide={"indice": "Les deux listes ont la même longueur : parcours les indices avec range(len(X))."})


def _test_variance(variance):
    r = variance(_X, _P)
    _nombre_attendu(r, "variance(X, P)")
    if _proche(r, 0, 1e-9):
        _faux("ta fonction renvoie 0 : la somme des p_i × (x_i - E(X)) vaut toujours 0. Il faut élever l'écart au carré : "
              "P[i] * (X[i] - m) ** 2.")
    if _proche(r, 51.2):
        _faux("ta fonction renvoie 51,2 = E(X²) : il faut l'écart à l'espérance au carré, (X[i] - m) ** 2.")
    if _proche(r, 0.25 * 23.04 + 0.04 * 0.64 + 0.04 * 10.24 + 0.01 * 368.64):
        _faux("ta fonction élève aussi la probabilité au carré. Seul l'écart est au carré : P[i] * (X[i] - m) ** 2.")
    if not _proche(r, 50.56, 1e-9):
        _faux("V(X) = 0,5 × 4,8² + 0,2 × 0,8² + 0,2 × 3,2² + 0,1 × 19,2² = 50,56. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(variance([95, 0, -10], [0.5, 0.22, 0.28]), 2542.41, 1e-9):
        _faux("variance([95, 0, -10], [0.5, 0.22, 0.28]) doit renvoyer 2542,41.")
    return "V(X) = 50,56 pour la loi du cours et V(G) = 2542,41 pour le gain."


def verifier_variance():
    """Vérifie la fonction variance."""
    _verifier(_test_variance, ["variance"])


def _test_ecart_type(ecart_type):
    r = ecart_type(_X, _P)
    _nombre_attendu(r, "ecart_type(X, P)")
    if not _proche(r, _math.sqrt(50.56), 1e-9):
        _faux("σ(X) = √50,56 ≈ 7,11 : l'écart type est la racine carrée de la variance, sqrt(variance(X, P)). Ta fonction renvoie "
              + _montre(r) + ".")
    return "σ(X) = √50,56 ≈ 7,11."


def verifier_ecart_type():
    """Vérifie la fonction ecart_type."""
    _verifier(_test_ecart_type, ["ecart_type"])


def _test_gain(gain):
    with _Graine(447):
        r = [gain() for k in range(3000)]
    for x in r:
        if x not in [95, 0, -10]:
            _faux("gain() doit renvoyer 95, 0 ou -10. Ta fonction renvoie " + _montre(x) + ".")
    f95, f0, fm = r.count(95) / 3000, r.count(0) / 3000, r.count(-10) / 3000
    if f0 < 0.02:
        _faux("sur 3000 parties, ta fonction ne renvoie presque jamais 0 : les seuils sont cumulés. Le match nul correspond à "
              "0,5 ≤ a < 0,5 + 0,22 = 0,72 : elif a < 0.72.")
    if abs(f0 - 0.28) < 0.04 and abs(fm - 0.22) < 0.04:
        _faux("tu as échangé le match nul et la défaite : le match nul (G = 0) a la probabilité 0,22, donc elif a < 0.72: return 0.")
    if abs(f95 - 0.5) > 0.04 or abs(f0 - 0.22) > 0.04 or abs(fm - 0.28) > 0.04:
        _faux("sur 3000 parties, les fréquences de 95, 0 et -10 sont " + _ecrire(f95, 3) + ", " + _ecrire(f0, 3) + " et "
              + _ecrire(fm, 3) + " : elles devraient être proches de 0,5, 0,22 et 0,28.")
    return ("sur 3000 parties, les fréquences de 95, 0 et -10 sont " + _ecrire(f95, 3) + ", " + _ecrire(f0, 3) + " et "
            + _ecrire(fm, 3) + " (probabilités 0,5 ; 0,22 ; 0,28).")


def verifier_gain():
    """Vérifie la fonction gain."""
    _verifier(_test_gain, ["gain"])


def _test_moyenne(moyenne):
    r = moyenne([2, 4, 9])
    _nombre_attendu(r, "moyenne([2, 4, 9])")
    if _proche(r, 15):
        _faux("moyenne([2, 4, 9]) renvoie 15 : c'est la somme. Divise par le nombre d'éléments : S / len(L).")
    if _proche(r, 1):
        _faux("moyenne([2, 4, 9]) renvoie 1 : tu ajoutes 1 au lieu de la valeur. Écris S = S + x.")
    if not _proche(r, 5):
        _faux("(2 + 4 + 9) / 3 = 5. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(moyenne([95, 0, -10, -10]), 18.75) or not _proche(moyenne([7]), 7):
        _faux("moyenne([95, 0, -10, -10]) doit renvoyer 18,75 et moyenne([7]) doit renvoyer 7.")
    return "moyenne([2, 4, 9]) = 5 et moyenne([95, 0, -10, -10]) = 18,75."


def verifier_moyenne():
    """Vérifie la fonction moyenne."""
    _verifier(_test_moyenne, ["moyenne"],
              aide={"division": "Une liste vide n'a pas de moyenne : teste ta fonction avec une liste non vide."})


def _test_frequence_lettre(frequence_lettre):
    r = frequence_lettre("abracadabra", "a")
    _nombre_attendu(r, "frequence_lettre(\"abracadabra\", \"a\")")
    if r == 5:
        _faux("ta fonction renvoie 5 : c'est le nombre de « a ». La fréquence est ce nombre divisé par le nombre de lettres.")
    if not _proche(r, 5 / 11):
        _faux("« abracadabra » contient 11 lettres dont 5 « a » : la fréquence est 5/11 ≈ 0,4545. Ta fonction renvoie "
              + _montre(r) + ".")
    r = frequence_lettre("le petit chat dort", "t")
    if _proche(r, 4 / 18):
        _faux("pour « le petit chat dort », ta fonction renvoie 4/18 : elle divise par la longueur du texte, espaces compris. "
              "Divise par le nombre de lettres : nb / nb_lettres.")
    if not _proche(r, 4 / 15):
        _faux("« le petit chat dort » contient 15 lettres dont 4 « t » : la fréquence est 4/15 ≈ 0,267. Ta fonction renvoie "
              + _montre(r) + ".")
    if not _proche(frequence_lettre("bonjour, monde !", "z"), 0):
        _faux("la lettre « z » n'apparaît pas dans « bonjour, monde ! » : la fréquence doit être 0.")
    return "fréquence de « a » dans « abracadabra » : 5/11 ; de « t » dans « le petit chat dort » : 4/15 (15 lettres)."


def verifier_frequence_lettre():
    """Vérifie la fonction frequence_lettre."""
    _verifier(_test_frequence_lettre, ["frequence_lettre"],
              aide={"division": "Le texte doit contenir au moins une lettre."})


print("Vérifications prêtes. Tu peux commencer.")
