/* Bouchons minimaux des services Google Apps Script utilisés par Code.gs (tests hors ligne).
   chargerCodeGs(options) → { ctx, ss, mails, horloge } : Code.gs exécuté dans un contexte vm isolé. */
'use strict';
const fs = require('fs'), path = require('path'), vm = require('vm');

function noop() { return this; }
function chain(target) {
  const P = new Proxy(target, { get(t, k) { if (k in t) { const v = t[k]; return typeof v === 'function' ? function () { const r = v.apply(t, arguments); return r === t ? P : r; } : v; } if (typeof k === 'symbol' || k === 'then') return undefined; return function () { return P; }; } });
  return P;
}
function Sheet(name, ss) {
  const s = { name, data: [], formats: {} };
  const grow = (r, c) => { while (s.data.length < r) s.data.push([]); s.data.forEach(row => { while (row.length < c) row.push(''); }); };
  const width = () => s.data.reduce((m, r) => Math.max(m, r.length), 0);
  function Range(r, c, nr, nc) {
    nr = nr || 1; nc = nc || 1;
    return chain({
      getValues() { const out = []; for (let i = 0; i < nr; i++) { const row = []; for (let j = 0; j < nc; j++) { const v = (s.data[r - 1 + i] || [])[c - 1 + j]; row.push(v === undefined ? '' : v); } out.push(row); } return out; },
      getValue() { return this.getValues()[0][0]; },
      setValues(v) {
        if (v.length !== nr || v.some(row => row.length !== nc)) throw new Error('setValues : dimensions ' + v.length + 'x' + (v[0] || []).length + ' ≠ ' + nr + 'x' + nc);
        grow(r - 1 + nr, c - 1 + nc);
        for (let i = 0; i < nr; i++) for (let j = 0; j < nc; j++) {
          let x = v[i][j];
          if (typeof x === 'string' && x.startsWith("'")) x = x.slice(1); /* comme Sheets : l'apostrophe force le texte et ne s'affiche pas */
          else if (typeof x === 'string' && /^[=+\-@]/.test(x)) s.formulaInjection = (s.formulaInjection || 0) + 1;
          s.data[r - 1 + i][c - 1 + j] = x;
        }
        return this;
      },
      setValue(x) { this.setValues([[x]]); return this; },
      setNumberFormats(f) { s.formats[r + ':' + c] = f; return this; },
      setNumberFormat(f) { s.formats[r + ':' + c] = f; return this; }
    });
  }
  return chain({
    _s: s, getName: () => name,
    getRange(r, c, nr, nc) { return Range(r, c, nr, nc); },
    getLastRow() { for (let i = s.data.length - 1; i >= 0; i--) if (s.data[i].some(v => v !== '' && v != null)) return i + 1; return 0; },
    getLastColumn() { return width(); },
    getDataRange() { return Range(1, 1, Math.max(1, this.getLastRow()), Math.max(1, width())); },
    appendRow(row) { const r = this.getLastRow() + 1; Range(r, 1, 1, row.length).setValues([row]); return this; }
  });
}
function Spreadsheet(tz) {
  const sheets = {};
  return chain({
    sheets, getId: () => 'CLASSEUR-TEST', getUrl: () => 'https://docs.google.com/spreadsheets/d/CLASSEUR-TEST',
    getSpreadsheetTimeZone: () => tz,
    getSheetByName: n => sheets[n] || null,
    insertSheet(n) { if (sheets[n]) throw new Error('existe'); sheets[n] = Sheet(n, this); return sheets[n]; }
  });
}
/* Utilities.formatDate : motifs utilisés par Code.gs (yyyy MM dd HH mm ss XXX), fuseau IANA. */
function formatDate(d, tz, fmt) {
  const parts = new Intl.DateTimeFormat('en-GB', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' }).formatToParts(d);
  const g = t => parts.find(p => p.type === t).value;
  const loc = Date.UTC(+g('year'), +g('month') - 1, +g('day'), +g('hour'), +g('minute'), +g('second'));
  const offMin = Math.round((loc - Math.floor(d.getTime() / 1000) * 1000) / 60000);
  const off = offMin === 0 ? 'Z' : (offMin > 0 ? '+' : '-') + String(Math.floor(Math.abs(offMin) / 60)).padStart(2, '0') + ':' + String(Math.abs(offMin) % 60).padStart(2, '0');
  return fmt.replace(/'([^']*)'/g, '\u0001$1\u0001').replace(/yyyy|MM|dd|HH|mm|ss|XXX/g, m => ({ yyyy: g('year'), MM: g('month'), dd: g('day'), HH: g('hour'), mm: g('minute'), ss: g('second'), XXX: off }[m])).replace(/\u0001/g, '');
}

function chargerCodeGs(opt) {
  opt = opt || {};
  const tz = opt.tz || 'Indian/Mayotte';
  const ss = Spreadsheet(tz), mails = [], props = {}, triggers = [], logs = [];
  const horloge = { decalage: 0 };
  let verrou = false, uuid = 0;
  const RealDate = Date;
  class FakeDate extends RealDate {
    constructor(...a) { if (a.length) super(...a); else super(RealDate.now() + horloge.decalage); }
    static now() { return RealDate.now() + horloge.decalage; }
  }
  const ctx = {
    console: { log: (...a) => logs.push(a.join(' ')), error: (...a) => logs.push('ERR ' + a.join(' ')) },
    Date: FakeDate, JSON, Math, Object, Array, String, Number, Error, RegExp, isFinite, isNaN, parseInt, parseFloat,
    SpreadsheetApp: {
      getActiveSpreadsheet: () => (opt.sansClasseurActif ? null : ss),
      openById: id => ss,
      getUi: () => { if (!opt.ui) throw new Error('Cannot call SpreadsheetApp.getUi() from this context.'); return chain({ createMenu: () => chain({ addItem: noop, addSeparator: noop, addToUi: noop }), alert: t => logs.push('ALERTE ' + t) }); }
    },
    MailApp: { sendEmail: m => { mails.push(m); }, getRemainingDailyQuota: () => 100 },
    LockService: { getScriptLock: () => ({ tryLock: () => { if (verrou || opt.verrouOccupe) return false; verrou = true; return true; }, waitLock: () => { verrou = true; }, releaseLock: () => { verrou = false; } }) },
    ContentService: { MimeType: { JSON: 'application/json' }, createTextOutput: s => ({ _c: s, setMimeType(m) { this._m = m; return this; }, getContent() { return this._c; }, getMimeType() { return this._m; } }) },
    Utilities: { formatDate, getUuid: () => 'uuid-' + (++uuid) },
    PropertiesService: { getScriptProperties: () => ({ getProperty: k => (k in props ? props[k] : null), setProperty: (k, v) => { props[k] = String(v); } }) },
    ScriptApp: {
      getProjectTriggers: () => triggers.slice(),
      deleteTrigger: t => { triggers.splice(triggers.indexOf(t), 1); },
      newTrigger: f => { const t = { f, getHandlerFunction: () => f }; return { timeBased: () => ({ everyHours: h => ({ create: () => { t.h = h; triggers.push(t); return t; } }) }) }; }
    },
    Session: { getEffectiveUser: () => ({ getEmail: () => 'prof@example.org' }), getScriptTimeZone: () => tz }
  };
  vm.createContext(ctx);
  const src = fs.readFileSync(path.join(__dirname, '..', 'Code.gs'), 'utf8');
  vm.runInContext(src, ctx, { filename: 'Code.gs' });
  return { ctx, ss, mails, props, triggers, logs, horloge };
}
module.exports = { chargerCodeGs, formatDate };
