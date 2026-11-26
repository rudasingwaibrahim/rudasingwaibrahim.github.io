/* Tests du serveur des devoirs (Code.gs) avec des bouchons Apps Script.
   Usage : node tools/devoirs/tests/harness.js */
'use strict';
const assert = require('assert'), fs = require('fs'), path = require('path'), { execFileSync } = require('child_process');
const { chargerCodeGs } = require('./gas-stubs.js');
const DEV = 'seconde-ch4-dm1', JETON = 's4dm1-Kq7e2Vb';
let n = 0, echecs = 0;
function test(nom, fn) { n++; try { fn(); console.log('  ok  ' + nom); } catch (e) { echecs++; console.log('  ÉCHEC  ' + nom + '\n        ' + (e && e.stack || e).split('\n').slice(0, 3).join('\n        ')); } }
function post(G, o) { return JSON.parse(G.ctx.doPost({ postData: { contents: typeof o === 'string' ? o : JSON.stringify(o) } }).getContent()); }
function get(G, a) { return JSON.parse(G.ctx.doGet({ parameter: { action: a } }).getContent()); }
function installe(opt) { const G = chargerCodeGs(opt); G.ctx.installer(); return G; }
function reglage(G, col, v) { G.ss.sheets['Réglages']._s.data[7][col] = v; }
function rendus(G) { return G.ss.sheets['Rendus']._s.data.slice(1).filter(r => r.some(x => x !== '')); }
const E1 = { nom: 'Abdallah', prenom: 'Zaïnaba', classe: 'Seconde 219' };
function idem(o, x) { return Object.assign({}, o, x); }
/* Réponses parfaites à partir du corrigé complet (régénéré côté test, comme le fait le serveur). */
function parfaites(G, ident, essai) {
  const M = G.ctx.SigmaMoteur, sel = G.props.SIGMA_SEL;
  const qs = M.genererComplet(DEV, M.graine(DEV, ident.nom, ident.prenom, ident.classe, essai, sel)), r = {};
  qs.forEach(q => {
    if (q.type === 'qcm') r[q.id] = q.bonne;
    else if (q.type === 'trous') r[q.id] = q.trous.map(t => t.rep[0]);
    else if (q.mode === 'decomp') r[q.id] = M.facteurs(q.n).map(f => f[0] + (f[1] > 1 ? '^' + f[1] : '')).reverse().join('×');
    else r[q.id] = q.rep[0];
  });
  return r;
}
function fausses(G, ident, essai) {
  const r = parfaites(G, ident, essai), o = {};
  Object.keys(r).forEach(k => { o[k] = typeof r[k] === 'number' ? (r[k] + 1) % 3 : Array.isArray(r[k]) ? r[k].map(() => 'zzz') : '=1+1'; });
  return o;
}
function rendre(G, ident, essai, reponses, extra) { return post(G, Object.assign({ action: 'rendre', devoir: DEV, jeton: JETON, essai, idRendu: 'r-' + Math.random().toString(36).slice(2), duree: 1234, reponses }, ident, extra || {})); }
function sujet(G, ident) { return post(G, Object.assign({ action: 'sujet', devoir: DEV, jeton: JETON }, ident)); }

console.log('Installation et réglages');
test('installer crée Réglages, Rendus, le déclencheur horaire et le sel ; relançable sans doublon', () => {
  const G = installe();
  assert.ok(G.ss.sheets['Réglages'] && G.ss.sheets['Rendus']);
  assert.strictEqual(G.triggers.length, 1); assert.strictEqual(G.triggers[0].f, 'verifierEcheances'); assert.strictEqual(G.triggers[0].h, 1);
  const sel = G.props.SIGMA_SEL; G.ctx.installer();
  assert.strictEqual(G.triggers.length, 1); assert.strictEqual(G.props.SIGMA_SEL, sel);
  assert.deepStrictEqual(G.ss.sheets['Rendus']._s.data[0].slice(0, 6), ['Horodatage', 'Devoir', 'Classe', 'Nom', 'Prénom', 'Note /20']);
  const r = G.ctx.lireReglages();
  assert.strictEqual(r.prof, 'prof@example.org'); assert.strictEqual(r.devoirs[DEV].essaisMax, 2); assert.deepStrictEqual(Array.from(r.devoirs[DEV].classes), ['Seconde 219', 'Seconde 220']);
});
test('GET liste et ping : pas de jeton divulgué', () => {
  const G = installe(), l = get(G, 'liste');
  assert.ok(l.ok); assert.strictEqual(l.devoirs.length, 1); assert.strictEqual(l.devoirs[0].ouvert, true);
  assert.ok(!JSON.stringify(l).includes(JETON));
  assert.strictEqual(get(G, 'ping').version, '1.0');
});
test('classeur retrouvé par son identifiant si getActiveSpreadsheet() est vide (application Web)', () => {
  const G = installe(); G.ctx.SpreadsheetApp.getActiveSpreadsheet = () => null;
  assert.ok(sujet(G, E1).ok);
});

console.log('Sujets personnalisés');
test('sujet : 9 questions, 20 points, aucun élément du corrigé envoyé', () => {
  const G = installe(), r = sujet(G, E1);
  assert.ok(r.ok, JSON.stringify(r)); assert.strictEqual(r.essai, 1); assert.strictEqual(r.essaisMax, 2);
  assert.strictEqual(r.sujet.questions.length, 9); assert.strictEqual(r.sujet.total, 20);
  const s = JSON.stringify(r);
  ['"bonne"', '"rep"', '"expl"', '"aff"', '"params"', '"mode"', '"n":'].forEach(k => assert.ok(!s.includes(k), 'fuite : ' + k));
  assert.deepStrictEqual(r.sujet.questions.map(q => q.type), ['qcm', 'saisie', 'saisie', 'qcm', 'saisie', 'saisie', 'qcm', 'saisie', 'trous']);
});
test('sujet déterministe : même élève (casse, accents, espaces) → même sujet', () => {
  const G = installe(), a = sujet(G, E1), b = sujet(G, { nom: '  ABDALLAH ', prenom: 'zainaba', classe: 'Seconde 219' });
  assert.deepStrictEqual(a.sujet, b.sujet);
});
test('sujets différents d\'un élève à l\'autre (voisins de table)', () => {
  const G = installe(); const vus = new Set(); let memeQ1 = 0, total = 60;
  const base = sujet(G, E1).sujet.questions.map(q => q.enonce + (q.choix || []).join());
  for (let i = 0; i < total; i++) {
    const s = sujet(G, { nom: 'Eleve', prenom: 'Numero' + 'abcdefghijklmnopqrstuvwxyz'[i % 26] + 'abcdefghijklmnopqrstuvwxyz'[Math.floor(i / 26)], classe: i % 2 ? 'Seconde 219' : 'Seconde 220' }).sujet;
    const sig = s.questions.map(q => q.enonce + (q.choix || []).join()).join('#'); vus.add(sig);
    const qs = s.questions.map(q => q.enonce + (q.choix || []).join());
    memeQ1 += qs.filter((x, k) => x === base[k]).length;
  }
  assert.strictEqual(vus.size, total);
  assert.ok(memeQ1 / (total * 9) < 0.12, 'trop de questions identiques : ' + memeQ1);
});
test('le sel secret change les nombres (le dépôt public ne suffit pas à prévoir un sujet)', () => {
  const G = installe(), a = sujet(G, E1).sujet; G.props.SIGMA_SEL = 'autre-sel'; const b = sujet(G, E1).sujet;
  assert.notDeepStrictEqual(a.questions, b.questions);
});

console.log('Correction et enregistrement');
test('réponses parfaites → 20/20, ligne écrite dans Rendus', () => {
  const G = installe(); sujet(G, E1);
  const r = rendre(G, E1, 1, parfaites(G, E1, 1));
  assert.ok(r.ok, JSON.stringify(r)); assert.strictEqual(r.note, 20); assert.strictEqual(r.points, 20); assert.strictEqual(r.restants, 1); assert.strictEqual(r.peutRefaire, true);
  assert.ok(r.detail.every(d => d.statut === 'juste'));
  const L = rendus(G); assert.strictEqual(L.length, 1);
  const row = L[0];
  assert.ok(row[0] instanceof G.ctx.Date || row[0] instanceof Date); assert.strictEqual(row[1], DEV); assert.strictEqual(row[2], 'Seconde 219');
  assert.strictEqual(row[3], 'Abdallah'); assert.strictEqual(row[4], 'Zaïnaba'); assert.strictEqual(row[5], 20); assert.strictEqual(row[7], 20);
  assert.ok(/^Q1 2\/2 · Q2 2\/2 .* Q9 4\/4$/.test(row[8]), row[8]); assert.strictEqual(row[9], 20.6); assert.strictEqual(row[10], 1);
});
test('réponses fausses → 0/20, statuts « faux » ; réponses vides → « vide »', () => {
  const G = installe();
  const r = rendre(G, E1, 1, fausses(G, E1, 1)); assert.strictEqual(r.note, 0); assert.ok(r.detail.every(d => d.statut === 'faux'), JSON.stringify(r.detail.map(d => d.statut)));
  const E2 = idem(E1, { prenom: 'Autre' }), v = rendre(G, E2, 1, {}); assert.strictEqual(v.note, 0); assert.ok(v.detail.every(d => d.statut === 'vide'));
});
test('correction partielle de la démonstration à trous (1 point par trou) et note arrondie', () => {
  const G = installe(), rep = parfaites(G, E1, 1); rep.q9 = [rep.q9[0], 'zzz', rep.q9[2], '']; rep.q1 = 99;
  const r = rendre(G, E1, 1, rep); const q9 = r.detail.find(d => d.id === 'q9');
  assert.strictEqual(q9.points, 2); assert.strictEqual(q9.statut, 'partiel'); assert.deepStrictEqual(q9.trous.map(t => t.ok), [true, false, true, false]);
  assert.strictEqual(r.note, 16);
});
test('saisie tolérante côté serveur : espaces, ×, ², ordre des facteurs, \\frac, parenthèses autour de k+m', () => {
  const G = installe(), M = G.ctx.SigmaMoteur, rep = parfaites(G, E1, 1);
  const qs = M.genererComplet(DEV, M.graine(DEV, E1.nom, E1.prenom, E1.classe, 1, G.props.SIGMA_SEL));
  const q5 = qs[4], q6 = qs[5], q9 = qs[8];
  const f = M.facteurs(q5.n);
  rep.q5 = f.map(x => Array(x[1]).fill(x[0]).join(' x ')).join(' × ');
  rep.q6 = '\\frac{' + q6.params.p + '}{' + q6.params.q + '}';
  rep.q9 = ['m × ' + q9.params.a, '(m + k)', ' Multiple ', ' ' + (q9.params.p + q9.params.q) + ' '];
  rep.q2 = ' ' + qs[1].params.k + ' ';
  const r = rendre(G, E1, 1, rep); assert.strictEqual(r.note, 20, JSON.stringify(r.detail.filter(d => d.statut !== 'juste')));
});
test('saisie refusée : fraction non simplifiée, décomposition avec un facteur non premier, calcul recopié', () => {
  const G = installe(), M = G.ctx.SigmaMoteur, rep = parfaites(G, E1, 1);
  const qs = M.genererComplet(DEV, M.graine(DEV, E1.nom, E1.prenom, E1.classe, 1, G.props.SIGMA_SEL));
  rep.q6 = qs[5].params.A + '/' + qs[5].params.B;
  rep.q5 = '4×' + (qs[4].n / 4); if (qs[4].n % 4) rep.q5 = '1×' + qs[4].n;
  rep.q2 = '(' + qs[1].params.n + '-1)/2';
  const r = rendre(G, E1, 1, rep), st = id => r.detail.find(d => d.id === id).statut;
  assert.strictEqual(st('q6'), 'faux'); assert.strictEqual(st('q5'), 'faux'); assert.strictEqual(st('q2'), 'faux'); assert.strictEqual(r.note, 14);
});
test('anti-injection : aucune cellule écrite ne commence par = + - @ sans apostrophe', () => {
  const G = installe();
  rendre(G, E1, 1, { q2: '=IMPORTXML("http://x")', q3: '+1', q5: '-2', q6: '@x', q9: ['=A1', '', '', ''] });
  assert.strictEqual(G.ss.sheets['Rendus']._s.formulaInjection || 0, 0);
  ['=a', '+a', '-a', '@a', '\ta'].forEach(x => assert.strictEqual(G.ctx.cellule(x)[0], "'"));
  assert.strictEqual(G.ctx.cellule('Abdou'), 'Abdou'); assert.strictEqual(G.ctx.cellule(12), 12);
});

console.log('Règles');
test('jeton, devoir, identité, classe, taille, JSON invalide', () => {
  const G = installe();
  assert.strictEqual(post(G, Object.assign({ action: 'sujet', devoir: DEV, jeton: 'faux' }, E1)).code, 'JETON');
  assert.strictEqual(post(G, Object.assign({ action: 'sujet', devoir: 'inconnu', jeton: JETON }, E1)).code, 'DEVOIR');
  assert.strictEqual(sujet(G, idem(E1, { nom: '=HYPERLINK("x")' })).code, 'IDENTITE');
  assert.strictEqual(sujet(G, idem(E1, { prenom: '' })).code, 'IDENTITE');
  assert.strictEqual(sujet(G, idem(E1, { nom: 'A'.repeat(41) })).code, 'IDENTITE');
  assert.strictEqual(sujet(G, idem(E1, { nom: "M'Tsanga-Ali" })).ok, true);
  assert.strictEqual(sujet(G, idem(E1, { classe: 'Seconde 221' })).code, 'CLASSE');
  assert.strictEqual(post(G, 'x'.repeat(20001)).code, 'TAILLE');
  assert.strictEqual(post(G, '{pas du json').code, 'REQUETE');
  assert.strictEqual(post(G, { action: 'pirater' }).code, 'REQUETE');
  assert.strictEqual(rendre(G, E1, 1, 'chaine').code, 'REQUETE');
  assert.strictEqual(rendus(G).length, 0);
});
test('devoir fermé (Ouvert = non) et date limite dépassée', () => {
  const G = installe();
  reglage(G, 3, 'non'); assert.strictEqual(sujet(G, E1).code, 'FERME'); assert.strictEqual(get(G, 'liste').devoirs[0].ouvert, false);
  reglage(G, 3, true); assert.ok(sujet(G, E1).ok);
  reglage(G, 4, new G.ctx.Date(Date.now() - 3600e3)); assert.strictEqual(sujet(G, E1).code, 'ECHEANCE'); assert.strictEqual(rendre(G, E1, 1, {}).code, 'ECHEANCE');
});
test('date sans heure = jusqu\'à 23:59:59 ce jour-là (fuseau de la feuille) ; date saisie en texte', () => {
  const G = installe(), tz = 'Indian/Mayotte';
  const auj = G.ctx.Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd');
  reglage(G, 4, new G.ctx.Date(auj + 'T00:00:00+03:00'));
  const D = G.ctx.lireReglages().devoirs[DEV];
  assert.strictEqual(G.ctx.Utilities.formatDate(D.dateLimite, tz, 'HH:mm:ss'), '23:59:59'); assert.ok(sujet(G, E1).ok);
  reglage(G, 4, '05/12/2026 18:30');
  assert.strictEqual(G.ctx.lireReglages().devoirs[DEV].dateLimite.toISOString(), '2026-12-05T15:30:00.000Z');
  reglage(G, 4, '7/1/2027');
  assert.strictEqual(G.ctx.lireReglages().devoirs[DEV].dateLimite.toISOString(), '2027-01-07T20:59:59.000Z');
});
test('essais : nouveau sujet à l\'essai 2, puis ESSAIS avec la meilleure note', () => {
  const G = installe();
  const s1 = sujet(G, E1); rendre(G, E1, 1, fausses(G, E1, 1));
  const s2 = sujet(G, E1); assert.strictEqual(s2.essai, 2); assert.notDeepStrictEqual(s1.sujet.questions, s2.sujet.questions);
  const r2 = rendre(G, E1, 2, parfaites(G, E1, 2)); assert.strictEqual(r2.note, 20); assert.strictEqual(r2.restants, 0); assert.strictEqual(r2.peutRefaire, false);
  const s3 = sujet(G, E1); assert.strictEqual(s3.code, 'ESSAIS'); assert.strictEqual(s3.meilleureNote, 20);
  assert.strictEqual(rendre(G, E1, 3, {}).code, 'ESSAIS'); assert.strictEqual(rendus(G).length, 2);
});
test('sujet périmé (rendu entre-temps depuis un autre appareil) → SUJET_PERIME, rien d\'écrit', () => {
  const G = installe(); rendre(G, E1, 1, {});
  const r = rendre(G, E1, 1, {}); assert.strictEqual(r.code, 'SUJET_PERIME'); assert.strictEqual(r.essaiAttendu, 2); assert.strictEqual(rendus(G).length, 1);
});
test('renvoi du même rendu (réponse perdue par le réseau) → même résultat, pas de doublon', () => {
  const G = installe(), rep = parfaites(G, E1, 1); rep.q3 = '0';
  const a = rendre(G, E1, 1, rep, { idRendu: 'abc-123' }), b = rendre(G, E1, 1, rep, { idRendu: 'abc-123' });
  assert.strictEqual(a.note, 18); assert.strictEqual(b.note, 18); assert.strictEqual(b.dejaRecu, true); assert.strictEqual(b.essai, 1);
  assert.strictEqual(rendus(G).length, 1);
});
test('verrou occupé → OCCUPE, rien d\'écrit', () => {
  const G = installe({ verrouOccupe: true }); assert.strictEqual(rendre(G, E1, 1, {}).code, 'OCCUPE'); assert.strictEqual(rendus(G).length, 0);
});
test('réponses trop longues tronquées, clés inconnues ignorées', () => {
  const G = installe(), r = rendre(G, E1, 1, { q2: '9'.repeat(5000), hack: 'x', q9: Array(50).fill('a') });
  assert.ok(r.ok); const rep = JSON.parse(rendus(G)[0][11]); assert.strictEqual(rep.q2.length, 200); assert.ok(!('hack' in rep)); assert.strictEqual(rep.q9.length, 12);
});

console.log('Courriel récapitulatif');
function classeRemplie() {
  const G = installe();
  const el = [['Saïd', 'Nadia', 'Seconde 220'], ['abdou', 'Ali', 'Seconde 220'], ['Madi', 'Ben', 'Seconde 219'], ['Ahmed', 'Zoé', 'Seconde 219'], ['Ahmed', 'Anli', 'Seconde 219']];
  el.forEach(([nom, prenom, classe], i) => {
    const id = { nom, prenom, classe }, rep = parfaites(G, id, 1); rep.q7 = (rep.q7 + 1) % 3; if (i % 2) rep.q3 = '0';
    rendre(G, id, 1, rep);
  });
  const id0 = { nom: 'Madi', prenom: 'Ben', classe: 'Seconde 219' };
  rendre(G, id0, 2, fausses(G, id0, 2));
  return G;
}
test('tableau trié par classe puis nom, moyennes, question la plus échouée, note retenue = meilleure', () => {
  const G = classeRemplie(), n = G.ctx.envoyerRecapitulatif(DEV, 'Récapitulatif demandé');
  assert.strictEqual(n, 5); assert.strictEqual(G.mails.length, 1);
  const m = G.mails[0], h = m.htmlBody;
  assert.strictEqual(m.to, 'prof@example.org'); assert.ok(m.subject.includes('5 rendus'));
  const ordre = [...h.matchAll(/<td [^>]*><b>([A-ZÀ-Ý' -]+)<\/b><\/td><td [^>]*>([^<]+)<\/td>/g)].map(x => x[1] + ' ' + x[2]);
  assert.deepStrictEqual(ordre, ['AHMED Anli', 'AHMED Zoé', 'MADI Ben', 'ABDOU Ali', 'SAÏD Nadia']);
  assert.ok(h.includes('Question la plus échouée : <b>Q7 — Parité d\'une expression</b> (0 % des points obtenus)'), h);
  assert.ok(/moyenne générale : <b>17,2\/20<\/b>/.test(h), h.match(/moyenne[^<]*<b>[^<]*/));
  assert.ok(h.includes('Seconde 219 : 17,3/20 (3)') && h.includes('Seconde 220 : 17/20 (2)'), h);
  assert.ok(m.body.includes('MADI ; Ben ; 18/20 ; 2 essai(s)'), m.body);
});
test('note retenue = dernière', () => {
  const G = classeRemplie(); G.ss.sheets['Réglages']._s.data[3][1] = 'dernière';
  G.ctx.envoyerRecapitulatif(DEV, 'x'); assert.ok(G.mails[0].body.includes('MADI ; Ben ; 0/20 ; 2 essai(s)'), G.mails[0].body);
});
test('noms échappés dans le courriel HTML', () => {
  const G = installe(); rendre(G, { nom: "O'Neil", prenom: 'Anna', classe: 'Seconde 219' }, 1, {});
  G.ctx.envoyerRecapitulatif(DEV, 'x'); assert.ok(!/<script/i.test(G.mails[0].htmlBody)); assert.ok(G.mails[0].htmlBody.includes("O'NEIL"));
});
test('aucun rendu : courriel quand même (« Aucun rendu »)', () => {
  const G = installe(); G.ctx.envoyerRecapitulatif(DEV, 'x'); assert.ok(G.mails[0].htmlBody.includes('Aucun rendu'));
});
test('déclencheur horaire : un seul envoi à l\'échéance, date notée dans Réglages', () => {
  const G = classeRemplie();
  G.ctx.verifierEcheances(); assert.strictEqual(G.mails.length, 0, 'pas avant l\'échéance');
  G.horloge.decalage = 20 * 86400e3;
  G.ctx.verifierEcheances(); assert.strictEqual(G.mails.length, 1); assert.ok(G.mails[0].htmlBody.includes('Date limite atteinte'));
  assert.ok(G.ss.sheets['Réglages']._s.data[7][7] instanceof Date || G.ss.sheets['Réglages']._s.data[7][7]);
  G.ctx.verifierEcheances(); assert.strictEqual(G.mails.length, 1, 'pas de second envoi');
});
test('récapitulatif automatique désactivé (« non ») : aucun envoi', () => {
  const G = classeRemplie(); G.ss.sheets['Réglages']._s.data[4][1] = 'non'; G.horloge.decalage = 20 * 86400e3;
  G.ctx.verifierEcheances(); assert.strictEqual(G.mails.length, 0);
});
test('menu Sigma : récapitulatif à la demande et courriel de test', () => {
  const G = classeRemplie(); G.ctx.menuRecapitulatif(); G.ctx.menuTestCourriel();
  assert.strictEqual(G.mails.length, 2); assert.ok(G.logs.some(l => l.includes('Récapitulatif envoyé à prof@example.org')));
  const G2 = chargerCodeGs({ ui: true }); G2.ctx.onOpen();
});

console.log('Cohérence');
test('saisie tolérante du moteur identique à assets/js/quiz.js', () => {
  global.window = {}; global.document = { body: {}, querySelector: () => null, createElement: () => ({}) };
  require(path.join(__dirname, '..', '..', '..', 'assets', 'js', 'quiz.js'));
  const Q = global.window.SigmaQuiz, M = chargerCodeGs().ctx.SigmaMoteur;
  const cas = ['2^3×3^2×5', ' 7 m ', '\\frac{3}{4}', '\\dfrac{12}{35}', '−4', '3,5', 'k+m', '(k+m)', '2²×3', '√2', 'π', 'x²−1', "a'", 'MULTIPLE', '1 573', '2**3', '3·4'];
  const specs = [{ rep: ['7m'], mode: 'dev' }, { rep: ['k+m'], mode: 'dev' }, { rep: ['3/4'], mode: 'txt' }, { rep: ['12/35'], mode: 'num' }, { rep: ['1573'], mode: 'num' }, { rep: ['multiple'] }, { rep: ['2^3*3^2*5'], mode: 'prod' }];
  cas.forEach(c => { assert.strictEqual(M.norm(c), Q.norm(c), c); specs.forEach(s => assert.strictEqual(M.accept(c, s), Q.accept(c, s), c + ' ' + JSON.stringify(s))); });
});
test('copies du moteur à jour (Code.gs et _includes/devoirs/moteur-demo.js)', () => {
  execFileSync('python3', [path.join(__dirname, '..', 'sync.py'), '--check'], { stdio: 'pipe' });
});
test('jeton identique dans Code.gs et _data/devoirs.yml', () => {
  const y = fs.readFileSync(path.join(__dirname, '..', '..', '..', '_data', 'devoirs.yml'), 'utf8');
  assert.ok(y.includes('jeton: "' + JETON + '"'));
  assert.ok(fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8').includes("jeton: '" + JETON + "'"));
});

console.log('\n' + (n - echecs) + '/' + n + ' tests réussis');
process.exit(echecs ? 1 : 0);
