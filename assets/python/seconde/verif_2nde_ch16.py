"""Vérifications du carnet Python « Seconde · Chapitre 16 · Filtrer des données et dresser un tableau croisé ».

Ce fichier accompagne le carnet ch16-filtres-tableau-croise.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_2nde_ch16 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_effectif_et(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_effectif_et', 'verifier_effectif_ou', 'verifier_effectif_non', 'verifier_effectif_sexe', 'verifier_frequence_sachant', 'sexe', 'sport']

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
_SEXE = "GGGFGGGGGFFGGGFGFFFFFGFGFFFGGFGFFFGFGGFF"
_SPORT = "ffdddffffddddffffdddffdfdddfddfdfdffffdf"


def _numero(i):
    if not (isinstance(i, int) and 0 <= i <= 39):
        raise IndexError("le numéro d'élève va de 0 à 39")


def sexe(i):
    """Renvoie "F" ou "G", le sexe de l'élève numéro i (i de 0 à 39)."""
    _numero(i)
    return _SEXE[i]


def sport(i):
    """Renvoie "foot" ou "danse", l'activité de l'élève numéro i (i de 0 à 39)."""
    _numero(i)
    if _SPORT[i] == "f":
        return "foot"
    return "danse"


def _et(s, a):
    return len([i for i in range(40) if sexe(i) == s and sport(i) == a])


_AIDE_INDICE = {"indice": "Les élèves sont numérotés de 0 à 39 : range(40)."}


def _test_effectif_et(effectif_et):
    r = effectif_et("F", "foot")
    if r == 5:
        _faux("effectif_et(\"F\", \"foot\") renvoie 5 au lieu de 6 : le dernier élève (numéro 39) n'est pas compté. "
              "Pour i de 0 à 39, écris range(40).")
    if r == 6 + 14 + 15:
        _faux("effectif_et(\"F\", \"foot\") renvoie 35 : tu comptes les filles OU les footballeurs. Pour « et », utilise and.")
    if r != 6:
        _faux("6 élèves sont des filles qui font du football. Ta fonction renvoie " + _montre(r) + ".")
    for s, a in [("F", "danse"), ("G", "foot"), ("G", "danse")]:
        if effectif_et(s, a) != _et(s, a):
            _faux("effectif_et(\"" + s + "\", \"" + a + "\") doit renvoyer " + str(_et(s, a)) + ". Ta fonction renvoie "
                  + _montre(effectif_et(s, a)) + ".")
    return "6 filles font du football, 14 de la danse ; 15 garçons font du football, 5 de la danse."


def verifier_effectif_et():
    """Vérifie la fonction effectif_et."""
    _verifier(_test_effectif_et, ["effectif_et"], aide=_AIDE_INDICE)


def _test_effectif_ou(effectif_ou):
    r = effectif_ou("F", "foot")
    if r == 6:
        _faux("effectif_ou(\"F\", \"foot\") renvoie 6 : tu comptes les élèves qui sont des filles ET qui font du football. "
              "Pour « ou », utilise or.")
    if r != 35:
        _faux("20 filles + 21 footballeurs - 6 filles footballeuses (comptées deux fois) = 35. Ta fonction renvoie "
              + _montre(r) + ".")
    if effectif_ou("G", "danse") != 20 + 19 - 5:
        _faux("effectif_ou(\"G\", \"danse\") doit renvoyer 20 + 19 - 5 = 34. Ta fonction renvoie " + _montre(effectif_ou("G", "danse")) + ".")
    return "35 élèves sont des filles ou font du football (20 + 21 - 6), et 34 sont des garçons ou font de la danse."


def verifier_effectif_ou():
    """Vérifie la fonction effectif_ou."""
    _verifier(_test_effectif_ou, ["effectif_ou"], aide=_AIDE_INDICE)


def _test_effectif_non(effectif_non):
    r = effectif_non("foot")
    if r == 21:
        _faux("effectif_non(\"foot\") renvoie 21 : ce sont les élèves qui font du football. Il faut ceux qui n'en font PAS : "
              "not sport(i) == a (ou sport(i) != a).")
    if r != 19:
        _faux("21 élèves font du football, donc 40 - 21 = 19 n'en font pas. Ta fonction renvoie " + _montre(r) + ".")
    if effectif_non("danse") != 21:
        _faux("effectif_non(\"danse\") doit renvoyer 21.")
    return "19 élèves ne font pas de football et 21 ne font pas de danse."


def verifier_effectif_non():
    """Vérifie la fonction effectif_non."""
    _verifier(_test_effectif_non, ["effectif_non"], aide=_AIDE_INDICE)


def _test_effectif_sexe(effectif_sexe):
    r = effectif_sexe("F")
    if r == 1:
        _faux("effectif_sexe(\"F\") renvoie 1 : le compteur doit augmenter de 1 à chaque fille : compteur = compteur + 1.")
    if r != 20 or effectif_sexe("G") != 20:
        _faux("il y a 20 filles et 20 garçons. Ta fonction renvoie " + _montre(r) + " pour \"F\" et "
              + _montre(effectif_sexe("G")) + " pour \"G\".")
    return "20 filles et 20 garçons."


def verifier_effectif_sexe():
    """Vérifie la fonction effectif_sexe."""
    _verifier(_test_effectif_sexe, ["effectif_sexe"], aide=_AIDE_INDICE)


def _test_frequence_sachant(frequence_sachant):
    r = frequence_sachant("F", "foot")
    _nombre_attendu(r, "frequence_sachant(\"F\", \"foot\")")
    if _proche(r, 6 / 40):
        _faux("frequence_sachant(\"F\", \"foot\") renvoie 0,15 = 6 / 40 : c'est la fréquence des filles footballeuses dans toute "
              "la classe. Parmi les filles, on divise par l'effectif de la sous-population : effectif_sexe(s).")
    if _proche(r, 20 / 6):
        _faux("frequence_sachant(\"F\", \"foot\") renvoie environ 3,33 : tu as inversé le quotient. Une fréquence est comprise "
              "entre 0 et 1 : effectif_et(s, a) / effectif_sexe(s).")
    if not _proche(r, 0.3):
        _faux("6 des 20 filles font du football : la fréquence est 6 / 20 = 0,3. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(frequence_sachant("G", "foot"), 0.75) or not _proche(frequence_sachant("F", "danse"), 0.7):
        _faux("frequence_sachant(\"G\", \"foot\") doit renvoyer 15 / 20 = 0,75 et frequence_sachant(\"F\", \"danse\") 14 / 20 = 0,7.")
    return "parmi les filles, 6 / 20 = 30 % font du football ; parmi les garçons, 15 / 20 = 75 %."


def verifier_frequence_sachant():
    """Vérifie la fonction frequence_sachant."""
    _verifier(_test_frequence_sachant, ["frequence_sachant"],
              aide={"division": "Vérifie que effectif_sexe renvoie bien le nombre d'élèves de sexe s (et non 0)."})


print("Vérifications prêtes. Tu peux commencer.")
