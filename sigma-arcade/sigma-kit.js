/* =====================================================================
   SIGMA ARCADE — kit commun (à inclure tel quel, en ligne, en fin de <body>)
   ---------------------------------------------------------------------
   Fournit à tous les jeux une identité commune :
   - Maki, la mascotte (lémurien original de Sigma Arcade) ;
   - l'écran de fin de niveau (étoiles, fanfare, boutons standard) ;
   - le Passeport Sigma Arcade (progression enregistrée sur l'appareil) ;
   - l'Épreuve finale : QCM + textes à trous, verdict « acquis » ;
   - la musique de fond (module sigma-music, inclus plus bas).

   API (window.SigmaKit) :
   SigmaKit.init({game:'sacs-surprise', title:'Les Sacs à Surprise', levels:7,
                  levelNames:['Inventaire',…], music:'aventure'|'epique',
                  buildFinal: () => [questions…] })
   SigmaKit.levelComplete({level:3, score:4, total:5}) -> Promise<'next'|'replay'|'final'|'close'>
   SigmaKit.openFinal()        ouvre l'Épreuve finale (bouton aussi ajouté automatiquement)
   SigmaKit.fanfare('ok'|'level'|'trophy')
   SigmaKit.maki(mood)         renvoie le SVG de Maki : 'joie' | 'neutre' | 'pense' | 'bravo'
   SigmaKit.stars(n, total=3)  renvoie le HTML d'une rangée d'étoiles
   SigmaKit.passport()         renvoie l'objet Passeport (lecture)
   SigmaKit.encourage(ok, {after|into, hint}) phrase d'encouragement (module
                               /assets/js/encouragements.js, chargé par le kit ;
                               #win/#fb suivis automatiquement, init({encourage:false}) pour couper)

   Format d'une question d'Épreuve finale :
   { type:'qcm',   level:3, prompt:'html', choices:['html',…], answer:indexBonneRéponse, explain:'html' }
   { type:'trous', level:2, prompt:'Le résultat est {0} et le signe est {1}.',
     blanks:[{answers:['−3','-3'], size:4}, {answers:['moins']}], explain:'html' }
   Les réponses des trous sont comparées après normalisation (espaces, − et -,
   virgule décimale, ×/x/*, casse) ; donner toutes les écritures acceptées.
   Accolades littérales (ensembles) : ajouter braces:true à la question ; alors
   « {{ » affiche « { », « }} » affiche « } » et seul « {n} » reste un trou.
     { type:'trous', braces:true, prompt:'Sur ℝ∖{{0}}, A = {{{0} ; {1}}}.', … }
     -> « Sur ℝ∖{0}, A = { [trou 0] ; [trou 1] }. »
   Sans braces (comportement historique, inchangé) : tout « {n} » est un trou et
   « { », « } » isolés restent tels quels ; ℝ∖{0} s'écrit alors ℝ∖&#123;0&#125;.

   Épreuve Platine (facultative, après Or, ouverte à tous, sans verrou) :
   SigmaKit.addFinal('platine', () => [questions…], {n:12})   (ou finals.platine dans init)
   Un jeu sans épreuve Platine s'affiche exactement comme avant. Accès direct : ?epreuve=platine.
   Champs facultatifs (Platine) : tag, title, consigne. Types supplémentaires :
   { type:'qcm', fixed:true, … }            choix affichés dans l'ordre donné (Toujours / Parfois / Jamais)
   { type:'demo', prompt:'html … {0} …', blanks:[{ok:'distributivité', bad:['…','…']}], explain }
                                            démonstration à compléter (listes déroulantes, texte brut)
   { type:'ordre', prompt:'html', steps:['étape 1', 'étape 2', …] (dans le bon ordre), explain }
   { type:'faute', prompt:'html', lines:['énoncé', 'ligne 1', …], wrong:k (k ≥ 1),
     reasons:['raison juste', 'leurre', …] (la première est la bonne), explain }
   ===================================================================== */
(function () {
  'use strict';
  if (window.SigmaKit) return;

  /* ---------------- stockage ---------------- */
  var KEY = 'sigma-passeport-v1';
  function load() { try { return JSON.parse(localStorage.getItem(KEY)) || { games: {} }; } catch (e) { return { games: {} }; } }
  function save(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {} }
  function gameRec(p, g) { p.games[g] = p.games[g] || { levels: {}, final: null, title: '' }; return p.games[g]; }

  var cfg = null;

  /* ---------------- encouragements (module commun du site) ----------------
     /assets/js/encouragements.js : phrases après chaque réponse, applaudissements,
     bilan de progression. Les panneaux #win / #fb des jeux sont suivis automatiquement,
     sauf pour les jeux de ENC_SKIP (en cours de modification : à retirer ensuite). */
  var ENC_SKIP = ['sans-faux-pas', 'le-sonar', 'aire-libre'];
  var encWait = [];
  function enc(cb) {
    if (window.SigmaEncourage) { cb(window.SigmaEncourage); return; }
    encWait.push(cb);
    if (encWait.length > 1) return;
    var s = document.createElement('script'); s.src = '/assets/js/encouragements.js?v=1'; s.async = true;
    s.onload = function () { var E = window.SigmaEncourage, w = encWait; encWait = []; if (E) w.forEach(function (f) { try { f(E); } catch (e) {} }); };
    s.onerror = function () { encWait = []; };
    (document.head || document.documentElement).appendChild(s);
  }
  function E() { return window.SigmaEncourage || null; }
  enc(function () {});

  /* ---------------- styles communs ---------------- */
  var CSS = [
    ':root{--sk-or:var(--sg-accent,#6c8eff);--sk-on:var(--sg-on-accent,#071022);--sk-ink:var(--sg-text,#f0f4ff);--sk-bg:var(--sg-panel-solid,#0c1a30);',
    '--sk-mut:var(--sg-muted,rgba(200,215,255,.72));--sk-panel:rgba(255,255,255,.04);--sk-line:var(--sg-border-strong,rgba(120,160,255,.32));',
    '--sk-ok:var(--sg-ok,#5fd27c);--sk-ko:var(--sg-coral,#ff6b6b);--sk-gold:var(--sg-gold,#c8a84b)}',
    '.sk-ov{position:fixed;inset:0;z-index:20000;background:rgba(3,7,16,.72);display:flex;align-items:center;justify-content:center;padding:16px;',
    '-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);animation:skfade .2s ease-out}',
    '@keyframes skfade{from{opacity:0}to{opacity:1}}',
    '.sk-card{background:linear-gradient(160deg,#10213d,#0a1628 70%);border:1px solid var(--sk-line);color:var(--sk-ink);border-radius:22px;width:min(720px,100%);max-height:calc(100dvh - 32px);overflow:auto;',
    'box-shadow:0 30px 80px -30px rgba(0,0,0,.6);font:17px/1.55 var(--sg-font,Outfit,system-ui,sans-serif);animation:skpop .35s cubic-bezier(.2,1.4,.4,1)}',
    '@keyframes skpop{from{transform:scale(.9) translateY(12px);opacity:0}to{transform:none;opacity:1}}',
    '.sk-head{display:flex;gap:16px;align-items:center;padding:22px 24px 8px}',
    '.sk-head svg{flex:none;width:96px;height:96px}',
    '.sk-head h2{margin:0;font-size:clamp(24px,4vw,32px);line-height:1.1}',
    '.sk-head p{margin:4px 0 0;color:var(--sk-mut)}',
    '.sk-body{padding:8px 24px 22px}',
    '.sk-stars{display:inline-flex;gap:6px;vertical-align:middle}',
    '.sk-stars svg{width:1.4em;height:1.4em}',
    '.sk-big .sk-stars svg{width:52px;height:52px}',
    '.sk-big .sk-stars svg{animation:skstar .5s cubic-bezier(.2,1.6,.4,1) backwards}',
    '.sk-big .sk-stars svg:nth-child(2){animation-delay:.15s}.sk-big .sk-stars svg:nth-child(3){animation-delay:.3s}',
    '@keyframes skstar{from{transform:scale(0) rotate(-40deg)}to{transform:none}}',
    '.sk-row{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}',
    '.sk-btn{min-height:48px;padding:0 20px;border-radius:12px;border:0;background:var(--sk-ink);color:#0a1628;font:600 16px var(--sg-font,Outfit,system-ui,sans-serif);cursor:pointer}',
    '.sk-btn.or{background:var(--sk-or);color:var(--sk-on);box-shadow:0 6px 20px -8px var(--sg-glow,rgba(108,142,255,.5))}.sk-btn.gh{background:transparent;color:var(--sk-ink);border:1.5px solid var(--sk-line)}',
    '.sk-btn:disabled{opacity:.35;cursor:not-allowed}',
    '.sk-btn:focus-visible,.sk-ch:focus-visible,.sk-in:focus-visible{outline:3px solid var(--sk-or);outline-offset:2px}',
    '.sk-prog{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}',
    '.sk-prog span{width:14px;height:14px;border-radius:50%;background:var(--sk-line)}',
    '.sk-prog span.c{background:var(--sk-or);box-shadow:0 0 0 3px rgba(108,142,255,.2)}.sk-prog span.g{background:var(--sk-ok)}.sk-prog span.r{background:var(--sk-ko)}',
    '.sk-q{font-size:clamp(19px,2.6vw,23px);font-weight:600;line-height:1.45;margin:4px 0 14px}',
    '.sk-tag{display:inline-block;font-size:13px;font-weight:600;color:var(--sk-mut);margin-bottom:4px}',
    '.sk-chs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px}',
    '.sk-ch{min-height:56px;padding:10px 16px;border-radius:14px;border:1.5px solid var(--sk-line);background:var(--sk-bg);color:var(--sk-ink);',
    'font:600 19px var(--sg-font,Outfit,system-ui,sans-serif);text-align:left;cursor:pointer}',
    '.sk-ch:hover:not(:disabled){border-color:var(--sk-or);background:rgba(108,142,255,.1)}',
    '.sk-ch.ok{border-color:var(--sk-ok);background:rgba(95,210,124,.14)}.sk-ch.ko{border-color:var(--sk-ko);background:rgba(255,107,107,.14)}',
    '.sk-ch:disabled{cursor:default}',
    '.sk-in{width:5.5em;height:46px;margin:2px 4px;padding:0 8px;font:700 20px var(--sg-font,Outfit,system-ui,sans-serif);text-align:center;border:1.5px solid var(--sk-line);',
    'border-bottom:3px solid var(--sk-or);border-radius:10px;background:var(--sk-bg);color:var(--sk-ink);vertical-align:middle}',
    '.sk-in.ok{border-color:var(--sk-ok);color:var(--sk-ok)}.sk-in.ko{border-color:var(--sk-ko);color:var(--sk-ko)}',
    '.sk-fb{margin-top:14px;padding:12px 14px;border-radius:12px;line-height:1.5}',
    '.sk-fb.ok{background:rgba(95,210,124,.14)}.sk-fb.ko{background:rgba(200,168,75,.14)}',
    '.sk-fb>b:first-child{display:block;font-size:18px;margin-bottom:2px}',
    '.sk-res{font:700 clamp(48px,9vw,72px)/1 var(--sg-font,Outfit,system-ui,sans-serif)}.sk-res small{font-size:.4em;color:var(--sk-mut)}',
    '.sk-verdict{display:inline-block;margin-top:8px;padding:6px 14px;border-radius:999px;font-weight:700}',
    '.sk-verdict.a{background:rgba(95,210,124,.14);color:var(--sk-ok)}.sk-verdict.b{background:rgba(108,142,255,.15);color:var(--sg-gold-bright,#e8c766)}',
    '.sk-verdict.c{background:rgba(255,107,107,.14);color:var(--sk-ko)}',
    '.sk-list{margin:12px 0 0;padding-left:1.2em}.sk-list li{margin:4px 0}',
    '.sk-trophy{display:flex;align-items:center;gap:10px;margin-top:12px;font-weight:700}',
    '.sk-trophy svg{width:44px;height:44px;flex:none}',
    '.sk-tis{display:grid;gap:12px}',
    '.sk-ti{display:grid;grid-template-columns:64px minmax(0,1fr) auto;gap:14px;align-items:center;padding:14px;border-radius:16px;border:1px solid var(--sk-line);background:rgba(255,255,255,.035)}',
    '.sk-ti svg{width:64px;height:64px}.sk-ti.got{border-color:rgba(200,168,75,.55);background:rgba(200,168,75,.08)}.sk-ti.locked{opacity:.6}',
    '.sk-ti-t b{display:block;font-size:18px}.sk-ti-t span{display:block;color:var(--sk-mut);font-size:15px;line-height:1.4}',
    '.sk-ti-st{margin-top:4px;font-weight:600;color:var(--sk-ink)!important}.sk-ti-st.ok{color:var(--sk-gold)!important}.sk-ti-st.lock{color:var(--sk-mut)!important}',
    '.sk-prof{margin-top:16px;color:var(--sk-mut);font-size:14px}.sk-prof summary{cursor:pointer;min-height:32px}.sk-prof-f{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-top:8px}',
    '.sk-trophy .sk-maki{width:64px;height:64px;flex:none}',
    '@media (max-width:520px){.sk-ti{grid-template-columns:52px minmax(0,1fr)}.sk-ti svg{width:52px;height:52px}.sk-ti .sk-btn{grid-column:1/-1;min-height:48px;height:auto}}',
    '.sk-launch{position:absolute;left:max(12px,env(safe-area-inset-left));top:12px;z-index:9000}',
    '.sk-final-btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 6px;border-radius:999px;border:1.5px solid var(--sk-gold);',
    'background:rgba(200,168,75,.12);color:var(--sk-ink);font:600 15px var(--sg-font,Outfit,system-ui,sans-serif);cursor:pointer;box-shadow:0 6px 18px -10px rgba(0,0,0,.4)}',
    '.sk-final-btn svg{width:34px;height:34px}',
    '.sk-final-btn:hover{background:rgba(200,168,75,.22)}',
    '.sk-maki .arm-r{transform-box:fill-box;transform-origin:10% 90%}',
    '.sk-maki.joie .arm-r,.sk-maki.bravo .arm-r{animation:skwave 1.2s ease-in-out infinite}',
    '@keyframes skwave{0%,100%{transform:rotate(0)}50%{transform:rotate(-22deg)}}',
    '.sk-maki .tail{transform-box:fill-box;transform-origin:0% 0%;animation:sktail 3s ease-in-out infinite}',
    '@keyframes sktail{50%{transform:rotate(6deg)}}',
    '@media (prefers-reduced-motion:reduce){.sk-ov,.sk-card,.sk-big .sk-stars svg,.sk-maki .arm-r,.sk-maki .tail{animation:none!important}}',
    '.sk-final-btn .s{display:none}',
    '@media (max-width:520px){.sk-head{padding:18px 16px 6px}.sk-head svg{width:72px;height:72px}.sk-body{padding:6px 16px 18px}.sk-final-btn .l{display:none}.sk-final-btn .s{display:inline}}',
    /* épreuve Platine : raisonnement et démonstration */
    '.sk-ti.pt{border-color:rgba(214,224,240,.45);background:linear-gradient(150deg,rgba(214,224,240,.10),rgba(255,255,255,.02) 65%)}.sk-ti.pt.got{border-color:rgba(232,238,248,.75)}',
    '.sk-pt{font-size:clamp(19px,2.4vw,22px);font-weight:700;line-height:1.3;margin:2px 0 4px}',
    '.sk-cons{margin:0 0 8px;color:var(--sk-mut)}',
    '.sk-pq{font-size:18px;line-height:1.6;margin:4px 0 6px}.sk-pq p{margin:6px 0}.sk-pq ol:not(.sk-ord){padding-left:1.5em;margin:8px 0}.sk-pq ol:not(.sk-ord) li{margin:10px 0}',
    '.sk-pq .sk-q{font-size:18px;font-weight:600;margin:4px 0 10px}',
    '.sk-sel{min-height:44px;max-width:100%;margin:2px 0;padding:0 8px;font:600 17px var(--sg-font,Outfit,system-ui,sans-serif);border:1.5px solid var(--sk-line);border-bottom:3px solid var(--sk-or);',
    'border-radius:10px;background:var(--sk-bg);color:var(--sk-ink);vertical-align:middle;cursor:pointer}',
    '.sk-sel.ok{border-color:var(--sk-ok)}.sk-sel.ko{border-color:var(--sk-ko)}.sk-sel:disabled{opacity:1;cursor:default}',
    '.sk-good{color:var(--sk-ok);font-weight:700;margin-left:6px}',
    '.sk-bg{display:grid;gap:6px;margin:6px 0 8px}.sk-bg .sk-bo{min-height:44px;padding:8px 14px;font:500 16px/1.4 var(--sg-font,Outfit,system-ui,sans-serif)}',
    '.sk-bo[aria-pressed=true]{border-color:var(--sk-or);background:rgba(108,142,255,.16);box-shadow:inset 0 0 0 1.5px var(--sk-or)}.sk-bo.ok,.sk-bo.ko{box-shadow:none}',
    '.sk-ord{list-style:none;padding:0;margin:10px 0;display:grid;gap:8px;counter-reset:skst}',
    '.sk-it{display:grid;grid-template-columns:30px minmax(0,1fr) auto;gap:10px;align-items:center;padding:8px 8px 8px 10px;border:1.5px solid var(--sk-line);border-radius:12px;background:var(--sk-bg);margin:0}',
    '.sk-it::before{counter-increment:skst;content:counter(skst);width:28px;height:28px;border-radius:50%;background:rgba(255,255,255,.08);display:grid;place-items:center;font-weight:700;font-size:14px}',
    '.sk-mvs{display:flex;gap:6px}',
    '.sk-mv{width:44px;height:44px;border-radius:10px;border:1.5px solid var(--sk-line);background:rgba(255,255,255,.06);color:var(--sk-ink);font-size:16px;cursor:pointer}',
    '.sk-mv:hover:not(:disabled){border-color:var(--sk-or)}.sk-mv:disabled{opacity:.35;cursor:default}',
    '.sk-it.ok{border-color:var(--sk-ok)}.sk-it.ko{border-color:var(--sk-ko)}',
    '.sk-it.moved{animation:skmv .35s ease-out}@keyframes skmv{from{background:rgba(108,142,255,.22)}to{background:var(--sk-bg)}}',
    '.sk-lines,.sk-chs.pl{display:grid;gap:8px;margin:6px 0 10px}.sk-chs.pl.row{grid-template-columns:repeat(3,minmax(0,1fr))}',
    '.sk-l0,.sk-ln{display:flex;gap:4px 14px;align-items:baseline;flex-wrap:wrap;width:100%;padding:10px 14px;border-radius:12px;border:1.5px solid var(--sk-line);background:var(--sk-bg);color:var(--sk-ink);',
    'font:600 18px/1.4 var(--sg-font,Outfit,system-ui,sans-serif);text-align:left;min-height:48px}',
    '.sk-l0{border-style:dashed}.sk-ln{cursor:pointer}.sk-num{font-size:13px;color:var(--sk-mut);font-weight:600;min-width:4.4em}',
    '.sk-chs.pl .sk-ch{min-height:48px;font:500 17px/1.45 var(--sg-font,Outfit,system-ui,sans-serif)}.sk-chs.pl.row .sk-ch{text-align:center;font-weight:700}',
    '.sk-ln:hover:not(:disabled),.sk-rs:hover:not(:disabled){border-color:var(--sk-or)}',
    '.sk-ln[aria-pressed=true],.sk-rs[aria-pressed=true]{border-color:var(--sk-or);background:rgba(108,142,255,.16);box-shadow:inset 0 0 0 1.5px var(--sk-or)}',
    '.sk-ln:disabled,.sk-rs:disabled{cursor:default}',
    '.sk-ln.ok,.sk-rs.ok{border-color:var(--sk-ok);background:rgba(95,210,124,.12);box-shadow:none}.sk-ln.ko,.sk-rs.ko{border-color:var(--sk-ko);background:rgba(255,107,107,.1);box-shadow:none}',
    '.sk-sub{font-weight:700;margin:12px 0 4px!important}.sk-sol{margin:4px 0 8px;padding-left:1.4em}.sk-sol li{margin:4px 0}',
    '.sk-eq{font:700 clamp(20px,2.4vw,26px)/1.4 var(--sg-font,Outfit,system-ui,sans-serif);margin:10px 0}',
    '.sk-ln:focus-visible,.sk-mv:focus-visible,.sk-sel:focus-visible{outline:3px solid var(--sk-or);outline-offset:2px}',
    '@media (max-width:560px){.sk-it{grid-template-columns:28px minmax(0,1fr)}.sk-mvs{grid-column:2;justify-self:end}.sk-chs.pl.row{grid-template-columns:minmax(0,1fr)}.sk-pq{font-size:17px}.sk-l0,.sk-ln{font-size:17px}}'
  ].join('');
  var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);

  /* ---------------- Maki (mascotte originale) ---------------- */
  function maki(mood) {
    mood = mood || 'neutre';
    var up = mood === 'joie' || mood === 'bravo';
    var mouth = mood === 'pense' ? '<path d="M52 63 h8" stroke="#2a1d12" stroke-width="2" stroke-linecap="round"/>'
      : '<path d="M50 61 Q56 67 62 61" stroke="#2a1d12" stroke-width="2" fill="none" stroke-linecap="round"/>';
    var armR = up ? '<path class="arm-r" d="M70 78 Q84 66 88 50" stroke="#8d7b6a" stroke-width="7" stroke-linecap="round" fill="none"/>'
      : '<path class="arm-r" d="M70 80 Q80 88 82 96" stroke="#8d7b6a" stroke-width="7" stroke-linecap="round" fill="none"/>';
    var armL = mood === 'bravo' ? '<path d="M42 78 Q28 66 24 50" stroke="#8d7b6a" stroke-width="7" stroke-linecap="round" fill="none"/>'
      : mood === 'pense' ? '<path d="M42 80 Q40 70 50 66" stroke="#8d7b6a" stroke-width="7" stroke-linecap="round" fill="none"/>'
      : '<path d="M42 80 Q32 88 30 96" stroke="#8d7b6a" stroke-width="7" stroke-linecap="round" fill="none"/>';
    return '<svg class="sk-maki ' + mood + '" viewBox="0 0 112 112" aria-hidden="true">' +
      '<g class="tail"><path d="M66 100 Q100 104 102 76 Q104 52 90 40" stroke="#2a1d12" stroke-width="9" fill="none" stroke-linecap="round"/>' +
      '<path d="M66 100 Q100 104 102 76 Q104 52 90 40" stroke="#f3efe8" stroke-width="9" fill="none" stroke-linecap="round" stroke-dasharray="7 7"/></g>' +
      '<ellipse cx="56" cy="88" rx="20" ry="18" fill="#9a8775"/><ellipse cx="56" cy="92" rx="11" ry="11" fill="#e9dfd2"/>' +
      armL + armR +
      '<path d="M30 30 L38 44 L28 44 Z M82 30 L74 44 L84 44 Z" fill="#2a1d12"/>' +
      '<ellipse cx="56" cy="50" rx="27" ry="22" fill="#9a8775"/>' +
      '<path d="M40 54 Q56 76 72 54 Q64 60 56 60 Q48 60 40 54Z" fill="#f3efe8"/>' +
      '<ellipse cx="45" cy="47" rx="9" ry="9.5" fill="#2a1d12"/><ellipse cx="67" cy="47" rx="9" ry="9.5" fill="#2a1d12"/>' +
      '<circle cx="45" cy="47" r="6.5" fill="#ff9a1a"/><circle cx="67" cy="47" r="6.5" fill="#ff9a1a"/>' +
      '<circle cx="45" cy="47" r="3" fill="#1a1008"/><circle cx="67" cy="47" r="3" fill="#1a1008"/>' +
      '<circle cx="46.5" cy="45.5" r="1.2" fill="#fff"/><circle cx="68.5" cy="45.5" r="1.2" fill="#fff"/>' +
      '<ellipse cx="56" cy="57" rx="3.4" ry="2.4" fill="#2a1d12"/>' + mouth +
      '</svg>';
  }

  /* ---------------- étoiles et trophée ---------------- */
  function star(on) {
    return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3 6.1 20.6l1.3-6.6L2.5 9.4l6.6-.8z" ' +
      'fill="' + (on ? '#f5b301' : 'none') + '" stroke="' + (on ? '#c98a00' : '#b8c0c8') + '" stroke-width="1.5" stroke-linejoin="round"/></svg>';
  }
  function stars(n, total) {
    total = total || 3; var h = '<span class="sk-stars" role="img" aria-label="' + n + ' étoile' + (n > 1 ? 's' : '') + ' sur ' + total + '">';
    for (var i = 0; i < total; i++) h += star(i < n);
    return h + '</span>';
  }
  function trophy() {
    return '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M14 6h20v8a10 10 0 0 1-20 0z" fill="#f5b301" stroke="#c98a00" stroke-width="1.5"/>' +
      '<path d="M14 9H7a6 6 0 0 0 7 8M34 9h7a6 6 0 0 1-7 8" fill="none" stroke="#c98a00" stroke-width="2.5"/>' +
      '<rect x="21" y="23" width="6" height="9" fill="#e0a200"/><rect x="14" y="32" width="20" height="6" rx="2" fill="#8a5c0a"/>' +
      '<path d="M20 11l2 3 3-5" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  }
  function starsFor(score, total) { var r = score / total; return r >= 1 ? 3 : r >= 0.8 ? 2 : 1; }

  /* ---------------- fanfares (originales, synthétisées) ---------------- */
  var actx = null;
  function ac() { if (!actx) { try { actx = new (window.AudioContext || window.webkitAudioContext)(); } catch (e) { return null; } } if (actx.state === 'suspended') actx.resume(); return actx; }
  function blip(f, w, d, v, type) {
    var a = ac(); if (!a) return; var t = a.currentTime + w, o = a.createOscillator(), g = a.createGain(), lp = a.createBiquadFilter();
    o.type = type || 'sawtooth'; o.frequency.value = f; lp.type = 'lowpass'; lp.frequency.value = 2400;
    g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + 0.02); g.gain.exponentialRampToValueAtTime(0.0001, t + d);
    o.connect(lp); lp.connect(g); g.connect(a.destination); o.start(t); o.stop(t + d + 0.05);
  }
  function soundOn() { try { return localStorage.getItem('sigma-fanfare') !== '0'; } catch (e) { return true; } }
  function fanfare(kind) {
    if (!soundOn() || kind === 'none') return;
    var N = { G4: 392, C5: 523.25, E5: 659.25, G5: 783.99, A5: 880, C6: 1046.5 };
    if (kind === 'ok') { blip(N.E5, 0, .18, .06, 'triangle'); blip(N.A5, .09, .3, .06, 'triangle'); return; }
    var seqs = { level: [['G4', 0, .14], ['C5', .14, .14], ['E5', .28, .14], ['G5', .42, .5]],
      trophy: [['C5', 0, .12], ['E5', .12, .12], ['G5', .24, .12], ['E5', .36, .12], ['A5', .5, .2], ['G5', .74, .14], ['C6', .9, .7]] };
    (seqs[kind] || seqs.level).forEach(function (s) { blip(N[s[0]], s[1], s[2] + .15, .07); blip(N[s[0]] / 2, s[1], s[2] + .15, .04, 'triangle'); });
  }

  /* ---------------- fenêtre modale ---------------- */
  var lastFocus = null;
  function modal(html, onClose) {
    lastFocus = document.activeElement;
    var ov = document.createElement('div'); ov.className = 'sk-ov';
    ov.innerHTML = '<div class="sk-card" role="dialog" aria-modal="true">' + html + '</div>';
    document.body.appendChild(ov);
    var card = ov.firstChild;
    function close(v) { if (!ov.parentNode) return; ov.remove(); document.removeEventListener('keydown', key); if (lastFocus && lastFocus.focus) try { lastFocus.focus(); } catch (e) {} if (onClose) onClose(v); }
    function key(e) { if (e.key === 'Escape') close('close'); }
    document.addEventListener('keydown', key);
    setTimeout(function () { var f = card.querySelector('[data-auto],button,input'); if (f) f.focus(); }, 50);
    return { el: card, close: close };
  }

  /* ---------------- fin de niveau ---------------- */
  function levelComplete(o) {
    var p = load(), g = gameRec(p, cfg.game), n = starsFor(o.score, o.total), prev = g.levels[o.level] || 0;
    g.title = cfg.title; if (n > prev) g.levels[o.level] = n; save(p);
    fanfare('level');
    var name = cfg.levelNames && cfg.levelNames[o.level - 1] ? ' · ' + cfg.levelNames[o.level - 1] : '';
    var last = o.level >= cfg.levels;
    var msg = n === 3 ? 'Sans faute&nbsp;: bravo\u00a0!' : n === 2 ? 'Très bien joué\u00a0!' : 'Niveau terminé\u00a0: rejoue-le pour gagner plus d\'étoiles.';
    return new Promise(function (res) {
      var m = modal('<div class="sk-head">' + maki(n === 3 ? 'bravo' : 'joie') + '<div><h2>Niveau ' + o.level + ' réussi&nbsp;!</h2><p>' + cfg.title + name + '</p></div></div>' +
        '<div class="sk-body sk-big"><div>' + stars(n) + '</div><p style="margin:10px 0 0;font-size:18px"><b>' + o.score + ' / ' + o.total + '</b> du premier coup. ' + msg + '</p>' +
        (n < prev ? '<p style="margin:4px 0 0;color:var(--sk-mut)">Ton record reste ' + prev + ' étoile' + (prev > 1 ? 's' : '') + '.</p>' : '') +
        '<div class="sk-row">' +
        (last ? '<button class="sk-btn or" data-v="final" data-auto>Passer les épreuves finales</button>' : '<button class="sk-btn or" data-v="next" data-auto>Niveau suivant →</button>') +
        '<button class="sk-btn gh" data-v="replay">Rejouer ce niveau</button>' +
        (last ? '' : '<button class="sk-btn gh" data-v="final">Épreuves finales</button>') + '</div></div>', function (v) { if (v === 'final') setTimeout(function () { openFinal(); }, 60); res(v || 'close'); });
      m.el.addEventListener('click', function (e) { var b = e.target.closest('[data-v]'); if (b) m.close(b.dataset.v); });
      if (E()) E().bilan({ key: 'arcade/' + cfg.game + '/niveau' + o.level, score: o.score, total: o.total, after: m.el.querySelector('.sk-body > p'), sound: false, noHead: true });
    });
  }

  /* ---------------- Épreuve finale ---------------- */
  function norm(s) {
    return String(s).toLowerCase().replace(/\s+/g, '').replace(/[−–—]/g, '-').replace(/,/g, '.').replace(/[×*·]/g, 'x').replace(/^\+/, '');
  }
  function esc(x) { return String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  /* ---------------- trois épreuves : Bronze, Argent, Or ---------------- */
  var TIERS = [
    { id: 'bronze', name: 'Bronze', sub: 'Les bases', desc: 'Les automatismes indispensables\u00a0: une étape, des nombres simples.', col: '#cd7f32', col2: '#8a4f1c' },
    { id: 'argent', name: 'Argent', sub: 'La maîtrise', desc: 'Toute la notion, avec les pièges classiques.', col: '#c9d2de', col2: '#7d8896' },
    { id: 'or', name: 'Or', sub: 'L’expert', desc: 'Plusieurs étapes, des notions mélangées, des situations concrètes.', col: '#e8c766', col2: '#a8862c' },
    { id: 'platine', name: 'Platine', sub: 'Le raisonnement', desc: 'On corse un peu les choses\u00a0: démontrer, remettre des étapes dans l’ordre, débusquer l’étape fausse, justifier.', col: '#eef2f8', col2: '#5f6f86' }
  ];
  function tierOf(id) { for (var k = 0; k < TIERS.length; k++) if (TIERS[k].id === id) return TIERS[k]; return TIERS[1]; }
  function medal(id, earned) {
    var t = tierOf(id), c = earned ? t.col : 'rgba(200,215,255,.22)', c2 = earned ? t.col2 : 'rgba(200,215,255,.35)', u = 'skm' + id + (earned ? 1 : 0), pt = id === 'platine';
    return '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M15 3h7l4 12h-7zM33 3h-7l-4 12h7z" fill="' + (earned ? (pt ? '#9d8cff' : '#6c8eff') : 'rgba(108,142,255,.25)') + '"/>' +
      '<defs><radialGradient id="' + u + '" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity="' + (earned ? '.75' : '.1') + '"/><stop offset=".45" stop-color="' + c + '"/><stop offset="1" stop-color="' + c2 + '"/></radialGradient></defs>' +
      '<circle cx="24" cy="30" r="14" fill="url(#' + u + ')" stroke="' + c2 + '" stroke-width="1.5"/><circle cx="24" cy="30" r="9.5" fill="none" stroke="' + c2 + '" stroke-width="1" opacity=".7"/>' +
      '<text x="24" y="34.5" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="800" font-size="12" fill="' + c2 + '">Σ</text>' +
      (pt ? '<path d="M35.5 16.5l1.1 2.6 2.6 1.1-2.6 1.1-1.1 2.6-1.1-2.6-2.6-1.1 2.6-1.1z" fill="' + (earned ? '#fff' : 'rgba(200,215,255,.35)') + '" stroke="' + c2 + '" stroke-width=".6"/>' : '') + '</svg>';
  }
  var extra = {}, extraMeta = {};                    // épreuves ajoutées par addFinal (Platine)
  function finalsOf() {
    if (!cfg) return {};
    var F = cfg.finals ? cfg.finals : cfg.buildFinal ? { argent: cfg.buildFinal } : {};
    if (!Object.keys(extra).length) return F;
    var o = {}; Object.keys(F).forEach(function (k) { o[k] = F[k]; }); Object.keys(extra).forEach(function (k) { o[k] = extra[k]; });
    return o;
  }
  function addFinal(id, fn, meta) { extra[id] = fn; extraMeta[id] = meta || {}; if (cfg && !document.querySelector('.sk-final-btn')) { if (document.body) mountFinalButton(); else document.addEventListener('DOMContentLoaded', mountFinalButton); } refreshButton(); }
  function rec(g) {                                   // migration : ancienne épreuve unique → Argent
    if (!g.finals) { g.finals = {}; if (g.final) g.finals.argent = g.final; }
    return g.finals;
  }
  var PROF_KEY = 'sigma-prof';
  function prof() { try { return sessionStorage.getItem(PROF_KEY) === '1'; } catch (e) { return false; } }
  function unlocked(id) {
    var F = finalsOf(); if (!F[id]) return false; if (prof()) return true;
    var p = load(), f = rec(gameRec(p, cfg.game));
    if (id === 'bronze' || id === 'platine') return true;
    if (id === 'argent') return !F.bronze || !!(f.bronze && f.bronze.acquis) || !!(f.argent);
    if (id === 'or') return !!(f.argent && f.argent.acquis) || !!(f.or);
    return false;
  }
  function nextTier(id) { var F = finalsOf(), k = TIERS.map(function (t) { return t.id; }).indexOf(id); for (var j = k + 1; j < TIERS.length; j++) if (F[TIERS[j].id]) return TIERS[j].id; return null; }

  function openFinal(tier) {
    if (!cfg) return; var F = finalsOf(); if (!Object.keys(F).length) return;
    if (!tier || !F[tier]) return chooser();
    if (!unlocked(tier)) return chooser();
    runFinal(tier);
  }
  function chooser() {
    var F = finalsOf(), p = load(), f = rec(gameRec(p, cfg.game));
    var cards = TIERS.filter(function (t) { return F[t.id]; }).map(function (t) {
      var r = f[t.id], open = unlocked(t.id), got = !!(r && r.acquis), nq = t.id === 'platine' && extraMeta.platine && extraMeta.platine.n;
      var st = got ? '<span class="sk-ti-st ok">Médaille obtenue · record ' + r.best + ' / ' + r.total + '</span>'
        : r ? '<span class="sk-ti-st">Record\u00a0: ' + r.best + ' / ' + r.total + ' · il faut ' + Math.ceil(.8 * r.total) + '</span>'
        : open ? '<span class="sk-ti-st">À tenter' + (nq ? ' · ' + nq + ' questions, ' + Math.ceil(.8 * nq) + ' bonnes réponses pour la médaille' : '') + '</span>'
        : '<span class="sk-ti-st lock">🔒 Obtiens d’abord la médaille ' + (t.id === 'or' ? 'd’Argent' : 'de Bronze') + '</span>';
      return '<div class="sk-ti' + (open ? '' : ' locked') + (got ? ' got' : '') + (t.id === 'platine' ? ' pt' : '') + '">' + medal(t.id, got) +
        '<div class="sk-ti-t"><b>' + t.name + ' · ' + t.sub + '</b><span>' + t.desc + '</span>' + st + '</div>' +
        '<button class="sk-btn ' + (open ? 'or' : 'gh') + '" data-t="' + t.id + '"' + (open ? '' : ' disabled') + '>' + (r ? 'Rejouer' : 'Commencer') + '</button></div>';
    }).join('');
    var m = modal('<div class="sk-head">' + maki('pense') + '<div><h2>Épreuves finales</h2><p>' + cfg.title + (F.platine ? ' · Bronze, Argent, Or\u00a0: 10 questions sans aide, 8 bonnes réponses pour la médaille. Platine\u00a0: un défi de raisonnement, ouvert à tous.' : ' · 10 questions sans aide, 8 bonnes réponses pour la médaille.') + '</p></div></div>' +
      '<div class="sk-body"><div class="sk-tis">' + cards + '</div>' +
      '<details class="sk-prof"><summary>Professeur\u00a0: débloquer les trois épreuves</summary>' +
      '<form class="sk-prof-f"><input class="sk-in" style="width:9em" placeholder="code" aria-label="Code professeur" autocomplete="off"><button class="sk-btn gh" type="submit">Débloquer</button><span class="sk-prof-m"></span></form></details>' +
      '<div class="sk-row"><button class="sk-btn gh" data-x="1">Fermer</button></div></div>');
    m.el.addEventListener('click', function (e) {
      var b = e.target.closest('[data-t]'); if (b && !b.disabled) { m.close(); setTimeout(function () { runFinal(b.dataset.t); }, 60); }
      if (e.target.closest('[data-x]')) m.close();
    });
    var pf = m.el.querySelector('.sk-prof-f');
    pf.onsubmit = function (e) {
      e.preventDefault(); var v = norm(pf.querySelector('input').value);
      if (v === 'sigmaprof') { try { sessionStorage.setItem(PROF_KEY, '1'); } catch (_) {} m.close(); setTimeout(chooser, 60); }
      else pf.querySelector('.sk-prof-m').textContent = 'Code incorrect.';
    };
  }
  function runFinal(tier) {
    var PTAG = { demo: ' · Démonstration à compléter', ordre: ' · Étapes à remettre dans l’ordre', faute: ' · Trouver l’étape fausse' };
    var T = tierOf(tier), Q = finalsOf()[tier](), i = 0, score = 0, res = [], PT = tier === 'platine';
    var m = modal('<div class="sk-head">' + medal(tier, true) + '<div><h2>Épreuve ' + T.name + '</h2><p>' + cfg.title + ' · ' + T.sub + ' · ' + Q.length + ' questions, sans aide.</p></div></div><div class="sk-body" id="sk-fin"></div>');
    var box = m.el.querySelector('#sk-fin');
    function prog() { return '<div class="sk-prog">' + Q.map(function (_, k) { return '<span class="' + (k < res.length ? (res[k] ? 'g' : 'r') : k === i ? 'c' : '') + '"></span>'; }).join('') + '</div>'; }
    function show() {
      var q = Q[i], h = prog() + '<span class="sk-tag">Question ' + (i + 1) + ' sur ' + Q.length + (PT && q.tag ? ' · ' + q.tag : PTAG[q.type] || (q.type === 'qcm' ? ' · QCM' : ' · Texte à trous')) + '</span>';
      if (PT && q.title) h += '<div class="sk-pt">' + q.title + '</div>';
      if (PT && q.consigne) h += '<p class="sk-cons">' + q.consigne + '</p>';
      if (q.type === 'qcm' && PT) {
        var ord2 = q.fixed ? q.choices.map(function (_, k) { return k; }) : shuffle(q.choices.map(function (_, k) { return k; }));
        h += '<div class="sk-pq"><div class="sk-q">' + q.prompt + '</div><div class="sk-chs pl' + (q.fixed ? ' row' : '') + '">' + ord2.map(function (k) { return '<button class="sk-ch" data-k="' + k + '">' + q.choices[k] + '</button>'; }).join('') + '</div></div>';
      } else if (q.type === 'qcm') {
        var order = shuffle(q.choices.map(function (_, k) { return k; }));
        h += '<div class="sk-q">' + q.prompt + '</div><div class="sk-chs">' + order.map(function (k) { return '<button class="sk-ch" data-k="' + k + '">' + q.choices[k] + '</button>'; }).join('') + '</div>';
      } else if (q.type === 'demo') {
        var d = q.prompt.replace(/\{(\d+)\}/g, function (m, n) { var b = q.blanks[+n], os = shuffle([b.ok].concat(b.bad));
          if (os.some(function (o) { return String(o).length > 22; }))      // réponses longues : boutons (le texte passe à la ligne)
            return '<span class="sk-bg" data-b="' + n + '" role="group" aria-label="Case ' + (+n + 1) + '">' + os.map(function (o) {
              return '<button type="button" class="sk-ch sk-bo" data-v="' + esc(o) + '" aria-pressed="false">' + esc(o) + '</button>'; }).join('') + '</span>';
          return '<select class="sk-sel" data-b="' + n + '" aria-label="Case ' + (+n + 1) + '"><option value="">…</option>' +
            os.map(function (o) { return '<option value="' + esc(o) + '">' + esc(o) + '</option>'; }).join('') + '</select>'; });
        h += '<form class="sk-pq" id="sk-tf"><div class="sk-demo">' + d + '</div><div class="sk-row"><button class="sk-btn or" type="submit">Valider</button></div></form>';
      } else if (q.type === 'ordre') {
        var o, idn = q.steps.map(function (_, k) { return k; });
        do { o = shuffle(idn.slice()); } while (q.steps.length > 1 && o.every(function (k, j) { return k === j; }));
        h += '<form class="sk-pq" id="sk-tf">' + (q.prompt ? '<div class="sk-q">' + q.prompt + '</div>' : '') + '<ol class="sk-ord">' + o.map(function (k) {
          return '<li class="sk-it" data-k="' + k + '"><span>' + q.steps[k] + '</span><span class="sk-mvs"><button type="button" class="sk-mv" data-mv="-1" aria-label="Monter cette étape">▲</button>' +
            '<button type="button" class="sk-mv" data-mv="1" aria-label="Descendre cette étape">▼</button></span></li>'; }).join('') + '</ol>' +
          '<div class="sk-row"><button class="sk-btn or" type="submit">Valider</button></div></form>';
      } else if (q.type === 'faute') {
        var rs = shuffle(q.reasons.map(function (_, k) { return k; }));
        h += '<form class="sk-pq" id="sk-tf">' + (q.prompt ? '<div class="sk-q">' + q.prompt + '</div>' : '') +
          '<p class="sk-sub">1. Quelle ligne est fausse\u00a0?</p><div class="sk-lines" role="group" aria-label="Lignes du calcul">' + q.lines.map(function (l, k) {
            return k === 0 ? '<div class="sk-l0"><span class="sk-num">Énoncé</span><span>' + l + '</span></div>'
              : '<button type="button" class="sk-ln" data-i="' + k + '" aria-pressed="false"><span class="sk-num">Ligne ' + k + '</span><span>' + l + '</span></button>'; }).join('') + '</div>' +
          '<p class="sk-sub">2. Pourquoi est-elle fausse\u00a0?</p><div class="sk-chs pl" role="group" aria-label="Raisons">' + rs.map(function (k) {
            return '<button type="button" class="sk-ch sk-rs" data-r="' + k + '" aria-pressed="false">' + q.reasons[k] + '</button>'; }).join('') + '</div>' +
          '<div class="sk-row"><button class="sk-btn or" type="submit">Valider</button></div></form>';
      } else {
        var t = q.prompt.replace(q.braces ? /\{\{|\}\}|\{(\d+)\}/g : /\{(\d+)\}/g, function (m, n) { if (n === undefined) return m.charAt(0); var b = q.blanks[+n]; return '<input class="sk-in" data-b="' + n + '" autocomplete="off" autocapitalize="off" spellcheck="false" style="width:' + ((b.size || 4) + 1.5) + 'em" aria-label="Trou ' + (+n + 1) + '">'; });
        h += '<form class="sk-q" id="sk-tf">' + t + '<div class="sk-row"><button class="sk-btn or" type="submit">Valider</button></div></form>';
      }
      h += '<div id="sk-fb"></div>';
      box.innerHTML = h; box.parentNode.scrollTop = 0;
      var f = box.querySelector(q.type === 'faute' ? '.sk-ln' : '.sk-ch,.sk-in,.sk-sel,.sk-mv'); if (f) f.focus();
      function bval(x) { if (x.tagName === 'SELECT') return x.value; var o = x.querySelector('[aria-pressed=true]'); return o ? o.getAttribute('data-v') : ''; }
      if (q.type === 'qcm') box.querySelectorAll('.sk-ch').forEach(function (b) { b.onclick = function () { answer(+b.dataset.k === q.answer, b); }; });
      else if (q.type === 'demo' || q.type === 'ordre' || q.type === 'faute') {
        var fm = box.querySelector('#sk-tf'), wait = function (t) { box.querySelector('#sk-fb').innerHTML = '<div class="sk-fb ko">' + t + '</div>'; };
        fm.addEventListener('click', function (e) {
          var b = e.target.closest('button'); if (!b || b.type === 'submit' || b.disabled) return;
          if (b.classList.contains('sk-mv')) {
            var li = b.closest('.sk-it'), dd = +b.dataset.mv, sib = dd < 0 ? li.previousElementSibling : li.nextElementSibling; if (!sib) return;
            if (dd < 0) li.parentNode.insertBefore(li, sib); else li.parentNode.insertBefore(sib, li);
            li.classList.remove('moved'); void li.offsetWidth; li.classList.add('moved'); b.focus(); return;
          }
          if (b.classList.contains('sk-ln') || b.classList.contains('sk-rs') || b.classList.contains('sk-bo')) {
            b.parentNode.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
            box.querySelector('#sk-fb').innerHTML = '';
          }
        });
        fm.onsubmit = function (e) {
          e.preventDefault();
          if (q.type === 'demo') {
            var ss = [].slice.call(box.querySelectorAll('.sk-sel,.sk-bg'));
            if (ss.some(function (x) { return !bval(x); })) return wait('Choisis une réponse dans chaque case avant de valider.');
            answer(ss.every(function (x) { return bval(x) === q.blanks[+x.dataset.b].ok; }));
          } else if (q.type === 'ordre') {
            answer([].slice.call(box.querySelectorAll('.sk-it')).every(function (li, j) { return +li.dataset.k === j; }));
          } else {
            var l = box.querySelector('.sk-ln[aria-pressed=true]'), r = box.querySelector('.sk-rs[aria-pressed=true]');
            if (!l) return wait('Choisis d’abord la ligne fausse.');
            if (!r) return wait('Choisis maintenant la raison de l’erreur.');
            answer(+l.dataset.i === q.wrong && r.dataset.r === '0');
          }
        };
      }
      else box.querySelector('#sk-tf').onsubmit = function (e) {
        e.preventDefault(); var ok = true, empty = false;
        box.querySelectorAll('.sk-in').forEach(function (inp) {
          if (!inp.value.trim()) empty = true;
          var b = q.blanks[+inp.dataset.b], good = b.answers.some(function (a) { return norm(a) === norm(inp.value); });
          inp.dataset.good = good ? '1' : '0'; if (!good) ok = false;
        });
        if (empty) { box.querySelector('#sk-fb').innerHTML = '<div class="sk-fb ko">Remplis tous les trous avant de valider.</div>'; return; }
        answer(ok);
      };
    }
    function answer(ok, btn) {
      var q = Q[i]; res.push(ok); if (ok) score++;
      var det = '';
      if (q.type === 'qcm') box.querySelectorAll('.sk-ch').forEach(function (b) { b.disabled = true; if (+b.dataset.k === q.answer) b.classList.add('ok'); else if (b === btn) b.classList.add('ko'); });
      else if (q.type === 'demo' || q.type === 'ordre' || q.type === 'faute') {
        var sb2 = box.querySelector('#sk-tf button[type=submit]'); if (sb2) sb2.parentNode.remove();
        if (q.type === 'demo') {
          box.querySelectorAll('.sk-sel').forEach(function (x) { var ok1 = x.value === q.blanks[+x.dataset.b].ok; x.classList.add(ok1 ? 'ok' : 'ko'); x.disabled = true;
            if (!ok1) x.insertAdjacentHTML('afterend', '<span class="sk-good">→\u00a0' + esc(q.blanks[+x.dataset.b].ok) + '</span>'); });
          box.querySelectorAll('.sk-bg').forEach(function (g) { var good = q.blanks[+g.dataset.b].ok;
            g.querySelectorAll('.sk-bo').forEach(function (o) { o.disabled = true; var v1 = o.getAttribute('data-v');
              if (v1 === good) o.classList.add('ok'); else if (o.getAttribute('aria-pressed') === 'true') o.classList.add('ko'); }); });
        }
        else if (q.type === 'ordre') {
          box.querySelectorAll('.sk-it').forEach(function (li, j) { li.classList.add(+li.dataset.k === j ? 'ok' : 'ko'); });
          box.querySelectorAll('.sk-mv').forEach(function (b) { b.disabled = true; });
          if (!ok) det = '<p><b>Le bon ordre\u00a0:</b></p><ol class="sk-sol">' + q.steps.map(function (x) { return '<li>' + x + '</li>'; }).join('') + '</ol>';
        } else {
          box.querySelectorAll('.sk-ln,.sk-rs').forEach(function (b) { b.disabled = true;
            var good = b.classList.contains('sk-ln') ? +b.dataset.i === q.wrong : b.dataset.r === '0';
            if (good) b.classList.add('ok'); else if (b.getAttribute('aria-pressed') === 'true') b.classList.add('ko'); });
          if (!ok) det = '<p>La ligne fausse est la ligne ' + q.wrong + '. ' + q.reasons[0] + '</p>';
        }
      }
      else {
        box.querySelectorAll('.sk-in').forEach(function (inp) { inp.disabled = true; inp.classList.add(inp.dataset.good === '1' ? 'ok' : 'ko'); });
        var sb = box.querySelector('#sk-tf button'); if (sb) sb.remove();
      }
      var sol = q.type === 'trous' && !ok ? '<br>Réponse attendue&nbsp;: ' + q.blanks.map(function (b) { return '<b style="display:inline">' + b.answers[0] + '</b>'; }).join(', ') + '.' : '';
      fanfare(ok ? 'ok' : 'none');
      box.querySelector('#sk-fb').innerHTML = '<div class="sk-fb ' + (ok ? 'ok' : 'ko') + '"><b>' + (ok ? 'Exact\u00a0!' : PT ? 'Pas tout à fait. Regardons ensemble pourquoi.' : 'Pas tout à fait.') + '</b>' + det + (q.explain || '') + sol + '</div>' +
        '<div class="sk-row"><button class="sk-btn" id="sk-nx">' + (i < Q.length - 1 ? 'Question suivante →' : 'Voir mon résultat') + '</button></div>';
      box.querySelector('.sk-prog').outerHTML = prog();
      if (E()) { var efb = box.querySelector('#sk-fb .sk-fb'); if (ok) E().ok({ into: efb, sound: false }); else E().ko({ into: efb, hint: 'correction' }); }
      var nx = box.querySelector('#sk-nx'); nx.focus(); nx.onclick = function () { i++; if (i < Q.length) show(); else end(); };
    }
    function end() {
      var tot = Q.length, need = Math.ceil(0.8 * tot), v = score >= need ? 'a' : score / tot >= 0.5 ? 'b' : 'c';
      var p = load(), g = gameRec(p, cfg.game), f = rec(g); g.title = cfg.title;
      var old = f[tier], first = v === 'a' && !(old && old.acquis);
      f[tier] = { best: old ? Math.max(old.best, score) : score, last: score, total: tot, acquis: !!(old && old.acquis) || v === 'a', date: new Date().toISOString().slice(0, 10) };
      if (f.argent) g.final = f.argent;                 // compatibilité avec l'ancien Passeport
      save(p); fanfare(v === 'a' ? 'trophy' : 'level');
      var weak = {}; Q.forEach(function (q, k) { if (!res[k] && q.level) weak[q.level] = true; });
      var wl = Object.keys(weak).sort(function (a, b) { return a - b; });
      var advice = wl.length ? '<p style="margin:14px 0 4px"><b>À revoir&nbsp;:</b></p><ul class="sk-list">' + wl.map(function (l) {
        return '<li>Niveau ' + l + (cfg.levelNames && cfg.levelNames[l - 1] ? ' · ' + cfg.levelNames[l - 1] : '') + '</li>'; }).join('') + '</ul>' : '';
      var nx = v === 'a' ? nextTier(tier) : null;
      var head = v === 'a' ? (first ? 'Médaille ' + (tier === 'platine' ? 'de Platine' : tier === 'or' ? 'd’Or' : tier === 'argent' ? 'd’Argent' : 'de Bronze') + '\u00a0!' : 'Encore réussi\u00a0!') : v === 'b' ? 'Presque\u00a0!' : PT ? 'Un beau défi' : 'À retravailler';
      box.parentNode.querySelector('.sk-head').innerHTML = (v === 'a' ? medal(tier, true) : maki(v === 'b' ? 'joie' : 'pense')) +
        '<div><h2>' + head + '</h2><p>' + cfg.title + ' · Épreuve ' + T.name + '</p></div>';
      box.innerHTML = '<div class="sk-res">' + score + '<small> / ' + tot + '</small></div>' +
        '<span class="sk-verdict ' + v + '">' + (v === 'a' ? (tier === 'bronze' ? 'Les bases sont en place' : tier === 'argent' ? 'Notion acquise' : PT ? 'Raisonnement solide' : 'Notion maîtrisée') : v === 'b' ? (PT ? 'Raisonnement en construction' : 'En cours d’acquisition') : PT ? 'Le raisonnement se travaille' : 'Pas encore acquis') + '</span>' +
        (v === 'a' ? '<div class="sk-trophy">' + maki('bravo') + '<span>' + (first ? 'Médaille ajoutée à ton Passeport Sigma Arcade\u00a0!' : 'Ta médaille est déjà dans ton Passeport.') + (nx ? (nx === 'platine' ? ' Envie d’un défi\u00a0? L’épreuve Platine t’attend.' : ' L’épreuve ' + tierOf(nx).name + ' est débloquée.') : '') + '</span></div>'
          : '<p style="margin:12px 0 0">Il faut ' + need + ' bonnes réponses sur ' + tot + ' pour la médaille. ' + (PT ? 'Relis les corrections\u00a0: les questions changent à chaque essai.' : 'Les questions changent à chaque essai.') + '</p>') +
        advice +
        '<div class="sk-row">' + (nx ? '<button class="sk-btn or" id="sk-next">Tenter l’épreuve ' + tierOf(nx).name + ' →</button>' : '') +
        '<button class="sk-btn ' + (nx ? 'gh' : 'or') + '" id="sk-again">Recommencer cette épreuve</button><button class="sk-btn gh" id="sk-close">Fermer</button>' +
        '<a class="sk-btn gh" href="/sigma-arcade/#passeport" style="display:inline-flex;align-items:center;text-decoration:none">Mon Passeport</a></div>';
      if (nx) box.querySelector('#sk-next').onclick = function () { m.close(); setTimeout(function () { runFinal(nx); }, 60); };
      box.querySelector('#sk-again').onclick = function () { m.close(); setTimeout(function () { runFinal(tier); }, 60); };
      box.querySelector('#sk-close').onclick = function () { m.close(); };
      if (E()) E().bilan({ key: 'arcade/' + cfg.game + '/' + tier, score: score, total: tot, after: box.querySelector('.sk-verdict'), sound: false, noHead: true });
    }
    show();
  }

  /* ---------------- bouton « Épreuves » ---------------- */
  function mountFinalButton() {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'sk-final-btn sk-launch';
    b.innerHTML = medal('or', true) + '<span class="l">Épreuves finales</span><span class="s">Épreuves</span>'; b.title = 'Épreuves finales\u00a0: Bronze, Argent, Or' + (finalsOf().platine ? ', Platine' : '');
    b.onclick = function () { openFinal(); };
    var hdr = document.querySelector('header');
    if (hdr) { b.classList.remove('sk-launch'); b.style.margin = '8px 0 0'; hdr.appendChild(b); }
    else document.body.appendChild(b);
  }

  function refreshButton() { var b = document.querySelector('.sk-final-btn'); if (b && cfg) b.title = 'Épreuves finales\u00a0: Bronze, Argent, Or' + (finalsOf().platine ? ', Platine' : ''); }
  function direct() {                                 // accès direct : ?epreuve=bronze|argent|or|platine
    var t = ''; try { t = (new URLSearchParams(location.search).get('epreuve') || '').toLowerCase().trim(); } catch (e) {}
    if (!t) return; var go = function () { setTimeout(function () { if (finalsOf()[t] && !document.querySelector('.sk-ov')) openFinal(t); }, 80); };
    if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
  }
  function init(c) {
    cfg = c; var p = load(), g = gameRec(p, c.game); g.title = c.title; rec(g); save(p);
    if (c.finals && c.finals.platine && !extraMeta.platine) extraMeta.platine = c.platineMeta || {};
    direct();
    if (Object.keys(finalsOf()).length) { if (document.body) mountFinalButton(); else document.addEventListener('DOMContentLoaded', mountFinalButton); }
    if (c.encourage !== false && ENC_SKIP.indexOf(c.game) < 0) enc(function (Enc) {
      function go() { Enc.watch(c.encourageWatch || {}); }
      if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', go); else go();
    });
  }

  window.SigmaKit = { init: init, levelComplete: levelComplete, openFinal: openFinal, addFinal: addFinal, _finals: function () { return finalsOf(); }, _meta: function () { return extraMeta; }, medal: medal, tiers: TIERS, fanfare: fanfare, maki: maki,
    stars: stars, trophy: trophy, passport: load, starsFor: starsFor, _norm: norm, _cfg: function () { return cfg; },
    encourage: function (ok, o) { var X = E(); if (!X) return ''; return ok ? X.ok(o || {}) : X.ko(o || {}); } };
})();
