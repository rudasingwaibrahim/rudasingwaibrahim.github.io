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

   Format d'une question d'Épreuve finale :
   { type:'qcm',   level:3, prompt:'html', choices:['html',…], answer:indexBonneRéponse, explain:'html' }
   { type:'trous', level:2, prompt:'Le résultat est {0} et le signe est {1}.',
     blanks:[{answers:['−3','-3'], size:4}, {answers:['moins']}], explain:'html' }
   Les réponses des trous sont comparées après normalisation (espaces, − et -,
   virgule décimale, ×/x/*, casse) ; donner toutes les écritures acceptées.
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

  /* ---------------- styles communs ---------------- */
  var CSS = [
    ':root{--sk-or:#ff7a00;--sk-ink:light-dark(#15191d,#e9edf0);--sk-bg:light-dark(#ffffff,#101418);--sk-mut:light-dark(#56616b,#9ba7b1);',
    '--sk-panel:light-dark(#f1f3f5,#1a2027);--sk-line:light-dark(#cfd5da,#323c46);--sk-ok:light-dark(#23803a,#5fd27c);--sk-ko:light-dark(#c0392b,#ff8c7a);--sk-gold:#f5b301}',
    '.sk-ov{position:fixed;inset:0;z-index:20000;background:rgba(10,14,20,.55);display:flex;align-items:center;justify-content:center;padding:16px;',
    '-webkit-backdrop-filter:blur(3px);backdrop-filter:blur(3px);animation:skfade .2s ease-out}',
    '@keyframes skfade{from{opacity:0}to{opacity:1}}',
    '.sk-card{background:var(--sk-bg);color:var(--sk-ink);border-radius:22px;width:min(720px,100%);max-height:calc(100dvh - 32px);overflow:auto;',
    'box-shadow:0 30px 80px -30px rgba(0,0,0,.6);font:17px/1.5 Lexend,system-ui,sans-serif;animation:skpop .35s cubic-bezier(.2,1.4,.4,1)}',
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
    '.sk-btn{min-height:48px;padding:0 20px;border-radius:12px;border:0;background:var(--sk-ink);color:var(--sk-bg);font:600 16px Lexend,system-ui,sans-serif;cursor:pointer}',
    '.sk-btn.or{background:var(--sk-or);color:#1d0e00}.sk-btn.gh{background:transparent;color:var(--sk-ink);border:1.5px solid var(--sk-line)}',
    '.sk-btn:disabled{opacity:.35;cursor:not-allowed}',
    '.sk-btn:focus-visible,.sk-ch:focus-visible,.sk-in:focus-visible{outline:3px solid var(--sk-or);outline-offset:2px}',
    '.sk-prog{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}',
    '.sk-prog span{width:14px;height:14px;border-radius:50%;background:var(--sk-line)}',
    '.sk-prog span.c{background:var(--sk-or);box-shadow:0 0 0 3px rgba(255,122,0,.2)}.sk-prog span.g{background:var(--sk-ok)}.sk-prog span.r{background:var(--sk-ko)}',
    '.sk-q{font-size:clamp(19px,2.6vw,23px);font-weight:600;line-height:1.45;margin:4px 0 14px}',
    '.sk-tag{display:inline-block;font-size:13px;font-weight:600;color:var(--sk-mut);margin-bottom:4px}',
    '.sk-chs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:10px}',
    '.sk-ch{min-height:56px;padding:10px 16px;border-radius:14px;border:1.5px solid var(--sk-line);background:var(--sk-bg);color:var(--sk-ink);',
    'font:600 19px Lexend,system-ui,sans-serif;text-align:left;cursor:pointer}',
    '.sk-ch:hover:not(:disabled){border-color:var(--sk-or);background:rgba(255,122,0,.1)}',
    '.sk-ch.ok{border-color:var(--sk-ok);background:light-dark(#eaf7ee,#13261a)}.sk-ch.ko{border-color:var(--sk-ko);background:light-dark(#fdecea,#2a1513)}',
    '.sk-ch:disabled{cursor:default}',
    '.sk-in{width:5.5em;height:46px;margin:2px 4px;padding:0 8px;font:700 20px Lexend,system-ui,sans-serif;text-align:center;border:1.5px solid var(--sk-line);',
    'border-bottom:3px solid var(--sk-or);border-radius:10px;background:var(--sk-bg);color:var(--sk-ink);vertical-align:middle}',
    '.sk-in.ok{border-color:var(--sk-ok);color:var(--sk-ok)}.sk-in.ko{border-color:var(--sk-ko);color:var(--sk-ko)}',
    '.sk-fb{margin-top:14px;padding:12px 14px;border-radius:12px;line-height:1.5}',
    '.sk-fb.ok{background:light-dark(#eaf7ee,#13261a)}.sk-fb.ko{background:light-dark(#fff1e6,#2a1d12)}',
    '.sk-fb>b:first-child{display:block;font-size:18px;margin-bottom:2px}',
    '.sk-res{font:700 clamp(48px,9vw,72px)/1 Lexend,system-ui,sans-serif}.sk-res small{font-size:.4em;color:var(--sk-mut)}',
    '.sk-verdict{display:inline-block;margin-top:8px;padding:6px 14px;border-radius:999px;font-weight:700}',
    '.sk-verdict.a{background:light-dark(#eaf7ee,#13261a);color:var(--sk-ok)}.sk-verdict.b{background:rgba(255,122,0,.15);color:light-dark(#b45300,#ffb066)}',
    '.sk-verdict.c{background:light-dark(#fdecea,#2a1513);color:var(--sk-ko)}',
    '.sk-list{margin:12px 0 0;padding-left:1.2em}.sk-list li{margin:4px 0}',
    '.sk-trophy{display:flex;align-items:center;gap:10px;margin-top:12px;font-weight:700}',
    '.sk-trophy svg{width:44px;height:44px}',
    '.sk-launch{position:absolute;left:max(12px,env(safe-area-inset-left));top:12px;z-index:9000}',
    '.sk-final-btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 6px;border-radius:999px;border:1.5px solid var(--sk-gold);',
    'background:light-dark(#fff8e1,#2a2410);color:var(--sk-ink);font:600 15px Lexend,system-ui,sans-serif;cursor:pointer;box-shadow:0 6px 18px -10px rgba(0,0,0,.4)}',
    '.sk-final-btn svg{width:34px;height:34px}',
    '.sk-final-btn:hover{background:light-dark(#ffefb3,#3a3112)}',
    '.sk-maki .arm-r{transform-box:fill-box;transform-origin:10% 90%}',
    '.sk-maki.joie .arm-r,.sk-maki.bravo .arm-r{animation:skwave 1.2s ease-in-out infinite}',
    '@keyframes skwave{0%,100%{transform:rotate(0)}50%{transform:rotate(-22deg)}}',
    '.sk-maki .tail{transform-box:fill-box;transform-origin:0% 0%;animation:sktail 3s ease-in-out infinite}',
    '@keyframes sktail{50%{transform:rotate(6deg)}}',
    '@media (prefers-reduced-motion:reduce){.sk-ov,.sk-card,.sk-big .sk-stars svg,.sk-maki .arm-r,.sk-maki .tail{animation:none!important}}',
    '@media (max-width:520px){.sk-head{padding:18px 16px 6px}.sk-head svg{width:72px;height:72px}.sk-body{padding:6px 16px 18px}.sk-final-btn .l{display:none}.sk-final-btn .s{display:inline}}'
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
    var msg = n === 3 ? 'Sans faute : bravo !' : n === 2 ? 'Très bien joué !' : 'Niveau terminé : rejoue-le pour gagner plus d\'étoiles.';
    return new Promise(function (res) {
      var m = modal('<div class="sk-head">' + maki(n === 3 ? 'bravo' : 'joie') + '<div><h2>Niveau ' + o.level + ' réussi !</h2><p>' + cfg.title + name + '</p></div></div>' +
        '<div class="sk-body sk-big"><div>' + stars(n) + '</div><p style="margin:10px 0 0;font-size:18px"><b>' + o.score + ' / ' + o.total + '</b> du premier coup. ' + msg + '</p>' +
        (n < prev ? '<p style="margin:4px 0 0;color:var(--sk-mut)">Ton record reste ' + prev + ' étoile' + (prev > 1 ? 's' : '') + '.</p>' : '') +
        '<div class="sk-row">' +
        (last ? '<button class="sk-btn or" data-v="final" data-auto>Passer l\'Épreuve finale</button>' : '<button class="sk-btn or" data-v="next" data-auto>Niveau suivant →</button>') +
        '<button class="sk-btn gh" data-v="replay">Rejouer ce niveau</button>' +
        (last ? '' : '<button class="sk-btn gh" data-v="final">Épreuve finale</button>') + '</div></div>', function (v) { if (v === 'final') setTimeout(openFinal, 60); res(v || 'close'); });
      m.el.addEventListener('click', function (e) { var b = e.target.closest('[data-v]'); if (b) m.close(b.dataset.v); });
    });
  }

  /* ---------------- Épreuve finale ---------------- */
  function norm(s) {
    return String(s).toLowerCase().replace(/\s+/g, '').replace(/[−–—]/g, '-').replace(/,/g, '.').replace(/[×*·]/g, 'x').replace(/^\+/, '');
  }
  function shuffle(a) { for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function openFinal() {
    if (!cfg || !cfg.buildFinal) return;
    var Q = cfg.buildFinal(), i = 0, score = 0, res = [];
    var m = modal('<div class="sk-head">' + maki('pense') + '<div><h2>Épreuve finale</h2><p>' + cfg.title + ' · ' + Q.length + ' questions, sans aide. Montre que c\'est acquis !</p></div></div><div class="sk-body" id="sk-fin"></div>');
    var box = m.el.querySelector('#sk-fin');
    function prog() { return '<div class="sk-prog">' + Q.map(function (_, k) { return '<span class="' + (k < res.length ? (res[k] ? 'g' : 'r') : k === i ? 'c' : '') + '"></span>'; }).join('') + '</div>'; }
    function show() {
      var q = Q[i], h = prog() + '<span class="sk-tag">Question ' + (i + 1) + ' sur ' + Q.length + (q.type === 'qcm' ? ' · QCM' : ' · Texte à trous') + '</span>';
      if (q.type === 'qcm') {
        var order = shuffle(q.choices.map(function (_, k) { return k; }));
        h += '<div class="sk-q">' + q.prompt + '</div><div class="sk-chs">' + order.map(function (k) { return '<button class="sk-ch" data-k="' + k + '">' + q.choices[k] + '</button>'; }).join('') + '</div>';
      } else {
        var t = q.prompt.replace(/\{(\d+)\}/g, function (_, n) { var b = q.blanks[+n]; return '<input class="sk-in" data-b="' + n + '" autocomplete="off" autocapitalize="off" spellcheck="false" style="width:' + ((b.size || 4) + 1.5) + 'em" aria-label="Trou ' + (+n + 1) + '">'; });
        h += '<form class="sk-q" id="sk-tf">' + t + '<div class="sk-row"><button class="sk-btn or" type="submit">Valider</button></div></form>';
      }
      h += '<div id="sk-fb"></div>';
      box.innerHTML = h; box.parentNode.scrollTop = 0;
      var f = box.querySelector('.sk-ch,.sk-in'); if (f) f.focus();
      if (q.type === 'qcm') box.querySelectorAll('.sk-ch').forEach(function (b) { b.onclick = function () { answer(+b.dataset.k === q.answer, b); }; });
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
      if (q.type === 'qcm') box.querySelectorAll('.sk-ch').forEach(function (b) { b.disabled = true; if (+b.dataset.k === q.answer) b.classList.add('ok'); else if (b === btn) b.classList.add('ko'); });
      else {
        box.querySelectorAll('.sk-in').forEach(function (inp) { inp.disabled = true; inp.classList.add(inp.dataset.good === '1' ? 'ok' : 'ko'); });
        var sb = box.querySelector('#sk-tf button'); if (sb) sb.remove();
      }
      var sol = q.type === 'trous' && !ok ? '<br>Réponse attendue : ' + q.blanks.map(function (b) { return '<b style="display:inline">' + b.answers[0] + '</b>'; }).join(', ') + '.' : '';
      fanfare(ok ? 'ok' : 'none');
      box.querySelector('#sk-fb').innerHTML = '<div class="sk-fb ' + (ok ? 'ok' : 'ko') + '"><b>' + (ok ? 'Exact !' : 'Pas tout à fait.') + '</b>' + (q.explain || '') + sol + '</div>' +
        '<div class="sk-row"><button class="sk-btn" id="sk-nx">' + (i < Q.length - 1 ? 'Question suivante →' : 'Voir mon résultat') + '</button></div>';
      box.querySelector('.sk-prog').outerHTML = prog();
      var nx = box.querySelector('#sk-nx'); nx.focus(); nx.onclick = function () { i++; if (i < Q.length) show(); else end(); };
    }
    function end() {
      var tot = Q.length, need = Math.ceil(0.8 * tot), v = score >= need ? 'a' : score / tot >= 0.5 ? 'b' : 'c';
      var p = load(), g = gameRec(p, cfg.game); g.title = cfg.title;
      var best = g.final ? Math.max(g.final.best, score) : score;
      g.final = { best: best, last: score, total: tot, acquis: (g.final && g.final.acquis) || v === 'a', date: new Date().toISOString().slice(0, 10) };
      save(p); fanfare(v === 'a' ? 'trophy' : 'level');
      var weak = {}; Q.forEach(function (q, k) { if (!res[k] && q.level) weak[q.level] = true; });
      var wl = Object.keys(weak).sort(function (a, b) { return a - b; });
      var advice = wl.length ? '<p style="margin:14px 0 4px"><b>À revoir :</b></p><ul class="sk-list">' + wl.map(function (l) {
        return '<li>Niveau ' + l + (cfg.levelNames && cfg.levelNames[l - 1] ? ' · ' + cfg.levelNames[l - 1] : '') + '</li>'; }).join('') + '</ul>' : '';
      var head = v === 'a' ? 'C\'est acquis !' : v === 'b' ? 'Presque acquis' : 'À retravailler';
      box.parentNode.querySelector('.sk-head').innerHTML = maki(v === 'a' ? 'bravo' : v === 'b' ? 'joie' : 'pense') +
        '<div><h2>' + head + '</h2><p>' + cfg.title + ' · Épreuve finale</p></div>';
      box.innerHTML = '<div class="sk-res">' + score + '<small> / ' + tot + '</small></div>' +
        '<span class="sk-verdict ' + v + '">' + (v === 'a' ? 'Acquis : ' + need + ' bonnes réponses ou plus' : v === 'b' ? 'En cours d\'acquisition' : 'Pas encore acquis') + '</span>' +
        (v === 'a' ? '<div class="sk-trophy">' + trophy() + '<span>Trophée ajouté à ton Passeport Sigma Arcade !</span></div>'
          : '<p style="margin:12px 0 0">Il faut ' + need + ' bonnes réponses sur ' + tot + ' pour obtenir le trophée. Tu peux recommencer quand tu veux : les questions changent à chaque fois.</p>') +
        advice +
        '<div class="sk-row"><button class="sk-btn or" id="sk-again">Recommencer l\'épreuve</button><button class="sk-btn gh" id="sk-close">Fermer</button>' +
        '<a class="sk-btn gh" href="/sigma-arcade/" style="display:inline-flex;align-items:center;text-decoration:none">Mon Passeport</a></div>';
      box.querySelector('#sk-again').onclick = function () { m.close(); setTimeout(openFinal, 60); };
      box.querySelector('#sk-close').onclick = function () { m.close(); };
    }
    show();
  }

  /* ---------------- bouton « Épreuve finale » ---------------- */
  function mountFinalButton() {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'sk-final-btn sk-launch';
    b.innerHTML = trophy() + '<span class="l">Épreuve finale</span><span class="s" style="display:none">Épreuve</span>'; b.title = 'Épreuve finale : QCM et textes à trous';
    b.onclick = openFinal;
    var hdr = document.querySelector('header');
    if (hdr) { b.classList.remove('sk-launch'); b.style.margin = '8px 0 0'; hdr.appendChild(b); }
    else document.body.appendChild(b);
  }

  function init(c) {
    cfg = c; var p = load(); gameRec(p, c.game).title = c.title; save(p);
    if (c.buildFinal) { if (document.body) mountFinalButton(); else document.addEventListener('DOMContentLoaded', mountFinalButton); }
  }

  window.SigmaKit = { init: init, levelComplete: levelComplete, openFinal: openFinal, fanfare: fanfare, maki: maki,
    stars: stars, trophy: trophy, passport: load, starsFor: starsFor, _norm: norm, _cfg: function () { return cfg; } };
})();
