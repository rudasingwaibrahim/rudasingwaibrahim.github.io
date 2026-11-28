"""Vérifications du carnet Python « Terminale spécialité · Chapitre 19 · Inégalité de Bienaymé-Tchebychev et loi des grands nombres ».

Ce fichier accompagne le carnet ch19-concentration-grands-nombres.ipynb. Basthon le charge automatiquement
quand on ouvre le carnet depuis le site (paramètre d'adresse module=) ; la
première cellule du carnet l'importe avec : from verif_tspe_ch19 import *

L'élève n'a pas besoin de le lire. Chaque cellule « Vérification » du carnet
appelle une seule fonction, par exemple verifier_proba_ecart(), qui affiche
« ✔ Juste : ... » ou un conseil précis pour corriger.
"""

__all__ = ['verifier_proba_ecart', 'verifier_marche', 'verifier_moyennes', 'verifier_proportion_ecarts', 'verifier_taille_echantillon']

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
def _pe(n, p, strict=True):
    S = 0
    for k in range(n + 1):
        e = abs(k - n * p)
        if (e > _math.sqrt(n)) if strict else (e >= _math.sqrt(n)):
            S = S + _math.comb(n, k) * p ** k * (1 - p) ** (n - k)
    return S


def _test_proba_ecart(proba_ecart):
    r = proba_ecart(100, 0.5)
    _nombre_attendu(r, "proba_ecart(100, 0.5)")
    if _proche(r, _pe(100, 0.5, False), 1e-9):
        _faux("proba_ecart(100, 0.5) renvoie environ 0,0569 : tu comptes aussi les k tels que |k - 50| = 10. L'écart doit être "
              "strictement supérieur à √n : > (et non >=).")
    if _proche(r, _pe(100, 0.5) / 2, 1e-9):
        _faux("proba_ecart(100, 0.5) renvoie environ 0,0176 : tu ne comptes que les écarts au-dessus de np. Utilise la valeur "
              "absolue : abs(k - n * p) > sqrt(n).")
    if r < 1e-20:
        _faux("proba_ecart(100, 0.5) est presque nul : il manque le coefficient binomial comb(n, k) dans P(S_n = k).")
    if not _proche(r, _pe(100, 0.5), 1e-9):
        _faux("proba_ecart(100, 0.5) doit renvoyer environ 0,0352. Ta fonction renvoie " + _montre(r) + ".")
    if not _proche(proba_ecart(400, 0.3), _pe(400, 0.3), 1e-9):
        _faux("proba_ecart(400, 0.3) doit renvoyer environ " + _ecrire(_pe(400, 0.3), 4) + ".")
    return "P(|S_100 - 50| > 10) ≈ 0,0352 pour p = 0,5, très inférieure à la majoration 0,25."


def verifier_proba_ecart():
    """Vérifie la fonction proba_ecart."""
    _verifier(_test_proba_ecart, ["proba_ecart"])


def _test_marche(marche):
    with _Graine(190):
        r = [marche(20) for k in range(1500)]
    for x in r:
        if not isinstance(x, int):
            _faux("marche(20) doit renvoyer un entier. Ta fonction renvoie " + _montre(x) + ".")
    if max(r) <= 1 and min(r) >= -1:
        _faux("marche(20) ne renvoie que -1 ou 1 : la position doit changer à chaque pas, position = position + 1 ou position - 1.")
    if min(r) >= 0:
        _faux("marche(20) ne renvoie jamais de position négative : dans le else, le pion recule, position = position - 1.")
    for x in r:
        if x % 2 != 0 or x < -20 or x > 20:
            _faux("après 20 pas de ±1, la position est un entier pair entre -20 et 20. Ta fonction renvoie " + _montre(x) + ".")
    m = sum(r) / 1500
    v = sum([(x - m) ** 2 for x in r]) / 1500
    if abs(m) > 0.5 or abs(v - 20) > 3:
        _faux("sur 1500 marches de 20 pas, la moyenne vaut " + _ecrire(m, 3) + " et la variance " + _ecrire(v, 3)
              + " : on attend environ 0 et 20.")
    return "sur 1500 marches de 20 pas : moyenne de S_20 ≈ " + _ecrire(m, 2) + " (E = 0), variance ≈ " + _ecrire(v, 2) + " (V = 20)."


def verifier_marche():
    """Vérifie la fonction marche."""
    _verifier(_test_marche, ["marche"])


def _test_moyennes(moyennes, ecart_type_liste):
    r = ecart_type_liste([2, 4, 9])
    _nombre_attendu(r, "ecart_type_liste([2, 4, 9])")
    if not _proche(r, _math.sqrt(26 / 3), 1e-9):
        _faux("ecart_type_liste([2, 4, 9]) doit renvoyer √(26/3) ≈ 2,944 : on additionne les carrés des écarts, (x - m) ** 2. "
              "Ta fonction renvoie " + _montre(r) + ".")
    with _Graine(191):
        L = moyennes(300, 25)
    _est_liste(L, "moyennes(300, 25)")
    if len(L) != 300:
        _faux("moyennes(300, 25) doit renvoyer 300 moyennes. Ta liste en contient " + str(len(L))
              + " : écris [moyenne_des(n) for j in range(N)].")
    s = ecart_type_liste(L)
    att = _math.sqrt(35 / 12) / 5
    if abs(s - att) > 0.06:
        _faux("pour 300 échantillons de taille 25, l'écart type des moyennes vaut " + _ecrire(s, 3) + " ; on attend environ "
              "σ/√25 ≈ 0,342. Chaque moyenne doit porter sur n dés : moyenne_des(n).")
    return "ecart_type_liste([2, 4, 9]) ≈ 2,944 ; pour 300 échantillons de 25 dés, s ≈ " + _ecrire(s, 3) + " (σ/√25 ≈ 0,342)."


def verifier_moyennes():
    """Vérifie les fonctions moyennes et ecart_type_liste."""
    _verifier(_test_moyennes, ["moyennes", "ecart_type_liste"])


def _test_proportion_ecarts(proportion_ecarts):
    sigma = _math.sqrt(35 / 12)
    L = [3.5, 4.2, 3.4, 4.5, 2.5, 3.4, 5.0]
    r = proportion_ecarts(L, 25)
    _nombre_attendu(r, "proportion_ecarts")
    if _proche(r, 3 / 7):
        _faux("pour la liste testée, ta fonction compte les petits écarts : la condition est |m - 3,5| >= 2σ/√n.")
    if _proche(r, 0):
        _faux("ta fonction ne compte aucun écart : le seuil est 2σ/√n, n'oublie pas de diviser par sqrt(n).")
    if not _proche(r, 4 / 7):
        _faux("pour L = " + _montre(L) + " et n = 25 (2σ/√25 ≈ 0,683), 4 moyennes sur 7 sont à distance "
              ">= 0,683 de 3,5. Ta fonction renvoie " + _montre(r) + ".")
    return "la proportion est juste sur un exemple (4 moyennes sur 7 à distance ≥ 2σ/√25 ≈ 0,683 de 3,5)."


def verifier_proportion_ecarts():
    """Vérifie la fonction proportion_ecarts."""
    _verifier(_test_proportion_ecarts, ["proportion_ecarts"])


def _taille(d, a):
    n = 1
    while 35 / 12 / (n * d ** 2) > a:
        n = n + 1
    return n


def _test_taille_echantillon(taille_echantillon):
    r = taille_echantillon(0.1, 0.05)
    if r == 584:
        _faux("taille_echantillon(0.1, 0.05) renvoie 584 : dans l'inégalité de concentration, δ est au carré, delta ** 2.")
    if r == 1:
        _faux("taille_echantillon(0.1, 0.05) renvoie 1 : ta condition est fausse dès le départ. Mets des parenthèses : "
              "V / (n * delta ** 2).")
    if r != 5834:
        _faux("V / (n δ²) ≤ 0,05 avec δ = 0,1 donne n ≥ 5833,3… : taille_echantillon(0.1, 0.05) doit renvoyer 5834. Ta fonction "
              "renvoie " + _montre(r) + ".")
    if taille_echantillon(0.5, 0.05) != _taille(0.5, 0.05):
        _faux("taille_echantillon(0.5, 0.05) doit renvoyer " + str(_taille(0.5, 0.05)) + ".")
    return "taille_echantillon(0.1, 0.05) = 5834 et taille_echantillon(0.5, 0.05) = " + str(_taille(0.5, 0.05)) + "."


def verifier_taille_echantillon():
    """Vérifie la fonction taille_echantillon."""
    _verifier(_test_taille_echantillon, ["taille_echantillon"])


print("Vérifications prêtes. Tu peux commencer.")
