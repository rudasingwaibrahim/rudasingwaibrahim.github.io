/* Faux serveur imitant l'application Web Apps Script (même contrat JSON) : exécute le vrai Code.gs
   avec les bouchons de gas-stubs.js. Usage : node fake-server.js [port=8851]
   - GET/POST /exec : doGet / doPost (CORS ouvert, comme script.googleusercontent.com)
   - GET /__control?perdre=1 : la prochaine réponse à « rendre » est perdue (rendu enregistré, connexion coupée)
   - GET /__control?lent=ms : délai artificiel ; /__control?etat=1 : feuilles et courriels (JSON) ; /__control?recap=1 */
'use strict';
const http = require('http'), { chargerCodeGs } = require('./gas-stubs.js');
const port = +process.argv[2] || 8851;
const G = chargerCodeGs(); G.ctx.installer();
let perdre = 0, lent = 0;
function cors(res) { res.setHeader('Access-Control-Allow-Origin', '*'); }
http.createServer((req, res) => {
  const u = new URL(req.url, 'http://x');
  if (u.pathname === '/__control') {
    if (u.searchParams.has('perdre')) perdre = +u.searchParams.get('perdre');
    if (u.searchParams.has('lent')) lent = +u.searchParams.get('lent');
    if (u.searchParams.has('recap')) G.ctx.envoyerRecapitulatif('seconde-ch4-dm1', 'Récapitulatif demandé');
    cors(res);
    if (u.searchParams.has('corrige')) { /* réponses parfaites d'un élève (outil de test uniquement) */
      const [nom, prenom, classe, essai] = u.searchParams.get('corrige').split('|'), M = G.ctx.SigmaMoteur, r = {};
      M.genererComplet('seconde-ch4-dm1', M.graine('seconde-ch4-dm1', nom, prenom, classe, +essai, G.props.SIGMA_SEL)).forEach(q => {
        r[q.id] = q.type === 'qcm' ? q.bonne : q.type === 'trous' ? q.trous.map(t => t.rep[0]) : q.mode === 'decomp' ? M.facteurs(q.n).map(f => f[0] + (f[1] > 1 ? '^' + f[1] : '')).join('×') : q.rep[0];
      });
      res.setHeader('Content-Type', 'application/json'); return res.end(JSON.stringify(r));
    } res.setHeader('Content-Type', 'application/json');
    return res.end(JSON.stringify({ rendus: G.ss.sheets['Rendus']._s.data, reglages: G.ss.sheets['Réglages']._s.data, mails: G.mails }));
  }
  if (u.pathname !== '/exec') { res.statusCode = 404; return res.end('introuvable'); }
  if (req.method === 'OPTIONS') { res.statusCode = 405; return res.end(); } /* Apps Script ne répond pas aux requêtes préalables */
  let body = '';
  req.on('data', c => { body += c; });
  req.on('end', () => setTimeout(() => {
    const out = req.method === 'POST' ? G.ctx.doPost({ postData: { contents: body, type: req.headers['content-type'] } })
      : G.ctx.doGet({ parameter: Object.fromEntries(u.searchParams) });
    if (req.method === 'POST' && perdre > 0 && /"action":"rendre"/.test(body)) { perdre--; return req.socket.destroy(); }
    cors(res); res.setHeader('Content-Type', out.getMimeType()); res.end(out.getContent());
  }, lent));
}).listen(port, () => console.log('faux serveur Apps Script sur http://localhost:' + port + '/exec'));
