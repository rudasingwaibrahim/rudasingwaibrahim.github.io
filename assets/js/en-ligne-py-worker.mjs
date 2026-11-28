/* Σ Sigma — exécution de Python dans le navigateur (Pyodide hébergé sur le site, /assets/pyodide/).
   Travailleur (Web Worker) : le programme de l'élève tourne à part, la page reste fluide et le bouton
   « Arrêter » peut interrompre une boucle sans fin (le travailleur est alors recréé).
   Messages reçus : {type:'run', code} (programme) · {type:'eval', code} (une ligne de la console) · {type:'reset'}.
   Messages envoyés : ready · out (texte) · err (texte) · done. Aucune donnée ne quitte l'appareil. */
import { loadPyodide } from '/assets/pyodide/pyodide.mjs';

let py = null;
const send = (type, text) => postMessage({ type, text });

/* Outils internes (invisibles pour l'élève) : espace de noms partagé entre le programme et la console,
   affichage des valeurs dans la console comme dans Python, messages d'erreur courts. */
const OUTILS = `
import sys, traceback, builtins
_sigma_ns = {"__name__": "__main__"}
def _sigma_reset():
    _sigma_ns.clear()
    _sigma_ns["__name__"] = "__main__"
def _sigma_input(message=""):
    raise RuntimeError("input() ne fonctionne pas sur cette page : écris directement la valeur dans le programme (par exemple n = 10), ou ouvre l'activité dans Basthon.")
builtins.input = _sigma_input
def _sigma_erreur(fichier):
    t, v, tb = sys.exc_info()
    pile = [f for f in traceback.extract_tb(tb) if f.filename == fichier]
    ligne = ""
    if pile and fichier == "<programme>":
        ligne = "Ligne " + str(pile[-1].lineno) + " : "
    if t is SyntaxError and fichier == "<programme>" and v.lineno:
        ligne = "Ligne " + str(v.lineno) + " : "
    sys.stderr.write(ligne + t.__name__ + " : " + str(v) + "\\n")
def _sigma_run(code):
    _sigma_reset()
    try:
        exec(compile(code, "<programme>", "exec"), _sigma_ns)
    except BaseException:
        _sigma_erreur("<programme>")
def _sigma_eval(code):
    try:
        exec(compile(code, "<console>", "single"), _sigma_ns)
    except BaseException:
        _sigma_erreur("<console>")
`;

async function init() {
  py = await loadPyodide({ indexURL: '/assets/pyodide/' });
  py.setStdout({ batched: (s) => send('out', s + '\n') });
  py.setStderr({ batched: (s) => send('err', s + '\n') });
  py.runPython(OUTILS);
  send('ready', 'Python ' + py.runPython('import sys; sys.version.split()[0]'));
}
const pret = init().catch((e) => send('fatal', String(e && e.message || e)));

onmessage = async (e) => {
  await pret;
  if (!py) return;
  const { type, code } = e.data || {};
  try {
    if (type === 'run') py.globals.get('_sigma_run')(code);
    else if (type === 'eval') py.globals.get('_sigma_eval')(code);
    else if (type === 'reset') py.globals.get('_sigma_reset')();
  } catch (err) {
    send('err', String(err && err.message || err) + '\n');
  }
  send('done', type);
};
