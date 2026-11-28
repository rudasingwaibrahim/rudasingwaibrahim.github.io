/* Produit en JSON N sujets complets (corrigé compris) pour l'audit Python, et vérifie dans le moteur :
   réponses parfaites → 20/20, réponses fausses → 0/20, formules KaTeX valides. Usage : node dump.js 300 */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');
const N = +process.argv[2] || 300, DEV = 'seconde-ch4-dm1';
const ctx = {}; vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'moteur.js'), 'utf8') + ';this.M = SigmaMoteur;', ctx);
const M = ctx.M;
const katex = require(path.join(__dirname, '..', '..', '..', 'assets', 'lib', 'katex', 'katex.min.js'));
const prenoms = ['Sophie', 'Paul', 'Anaïs', 'Louis', 'Louise', 'Hugo', 'Margaux', 'Jules', 'Élise', 'Romain', 'Chloé', 'Nathan'];
const noms = ['Lefèvre', 'Martin', "D'Almeida", 'Bernard', 'Durand', 'Moreau', 'Petit', 'Roux', 'Fontaine', 'Garnier'];
const out = [], katexErr = [];
function formules(s) { const p = String(s || '').split('$'); return p.filter((_, i) => i % 2); }
for (let i = 0; i < N; i++) {
  const ident = { nom: noms[i % noms.length], prenom: prenoms[Math.floor(i / noms.length) % prenoms.length] + (i >= 120 ? '-' + 'abcdefghij'[i % 10] + 'abcdefghij'[Math.floor(i / 10) % 10] : ''), classe: i % 2 ? 'Seconde 219' : 'Seconde 220' };
  const essai = 1 + (i % 3 === 0 ? 1 : 0), sel = 'audit';
  const qs = M.genererComplet(DEV, M.graine(DEV, ident.nom, ident.prenom, ident.classe, essai, sel));
  const bon = {}, faux = {};
  qs.forEach(q => {
    if (q.type === 'qcm') { bon[q.id] = q.bonne; faux[q.id] = (q.bonne + 1) % q.choix.length; }
    else if (q.type === 'trous') { bon[q.id] = q.trous.map(t => t.rep[0]); faux[q.id] = q.trous.map(() => '0'); }
    else if (q.mode === 'decomp') { bon[q.id] = M.facteurs(q.n).map(f => f[0] + (f[1] > 1 ? '^' + f[1] : '')).join('*'); faux[q.id] = String(q.n); }
    else { bon[q.id] = q.rep[0]; faux[q.id] = String(Number(q.rep[0].split('/')[0]) + 1); }
    [q.enonce, q.expl, q.aff, q.aide, q.texte].concat(q.choix || [], (q.trous || []).map(t => t.aff)).forEach(t => formules(t).forEach(f => {
      try { katex.renderToString(f, { throwOnError: true }); } catch (e) { katexErr.push(q.id + ' : ' + f + ' → ' + e.message); }
    }));
  });
  const cb = M.corriger(DEV, ident, essai, sel, bon), cf = M.corriger(DEV, ident, essai, sel, faux);
  out.push({ ident, essai, note_parfaite: cb.note, note_fausse: cf.note, questions: qs });
}
fs.writeFileSync(process.argv[3] || '/tmp/devoirs-audit.json', JSON.stringify({ katexErr, sujets: out }));
console.log(N + ' sujets écrits ; erreurs KaTeX : ' + katexErr.length);
