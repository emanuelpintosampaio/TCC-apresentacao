// Interações da página: equações, linhas do tempo, revelação ao rolar,
// abas dos gráficos, contadores e o player. A viagem da gotícula fica em story.js.

import { initPlayer } from './player.js?v=5';
import { initStory } from './story.js?v=5';

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const $ = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => [...el.querySelectorAll(s)];

/* ------------------------------ Equações -------------------------------- */
if (window.renderMathInElement) {
  window.renderMathInElement(document.body, {
    delimiters: [
      { left: '\\[', right: '\\]', display: true },
      { left: '\\(', right: '\\)', display: false },
    ],
    throwOnError: false,
  });
}

/* --------------------------- Linhas do tempo ---------------------------- */
const NS = 'http://www.w3.org/2000/svg';
function svg(tag, attrs, parent) {
  const el = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  parent.append(el);
  return el;
}
function drawTimeline(el) {
  const [, , vw] = el.getAttribute('viewBox').split(' ').map(Number);
  const x0 = 12, x1 = vw - 12, y = 34;
  svg('line', { class: 'axis', x1: x0, y1: y, x2: x1, y2: y }, el);
  let k = 0;
  const tick = (x, h, cls = 'tick') => {
    const t = svg('line', { class: cls, x1: x, y1: y - h, x2: x, y2: y + h }, el);
    t.style.setProperty('--k', k++);
  };
  const kind = el.dataset.tl;
  if (kind === 'fixo') {
    for (let i = 0; i <= 8; i++) tick(x0 + ((x1 - x0) * i) / 8, 9);
  } else if (kind === 'sub') {
    for (let i = 0; i <= 4; i++) {
      const xa = x0 + ((x1 - x0) * i) / 4;
      tick(xa, 12);
      if (i < 4) for (let j = 1; j < 6; j++) tick(xa + ((x1 - x0) / 4) * (j / 6), 5, 'tick tick--sub');
    }
  } else {
    // passos pequenos no começo, que crescem conforme a dinâmica acalma
    const n = 15, g = 1.3, total = (g ** n - 1) / (g - 1);
    let acc = 0;
    for (let i = 0; i <= n; i++) {
      tick(x0 + (x1 - x0) * (acc / total), 9);
      acc += g ** i;
    }
  }
  const a = svg('text', { x: x0, y: 60, 'text-anchor': 'middle' }, el);
  a.textContent = '0';
  const b = svg('text', { x: x1, y: 60, 'text-anchor': 'middle' }, el);
  b.textContent = 'τ';
  const sub = svg('tspan', { dy: 3, 'font-size': 7 }, b);
  sub.textContent = 'f';
}
$$('.tl').forEach(drawTimeline);

/* ------------------------- Revelação ao rolar --------------------------- */
const fmt = (v, dec, sep) => {
  let s = v.toFixed(dec).replace('.', ',');
  if (sep) s = s.replace(/\B(?=(\d{3})+(?!\d))/g, sep);
  return s;
};
function countUp(el) {
  if (reduced) return;
  const end = parseFloat(el.dataset.count);
  const dec = parseInt(el.dataset.dec || '0', 10);
  const sep = el.dataset.sep || '';
  const pre = el.dataset.prefix || '', suf = el.dataset.suffix || '';
  const t0 = performance.now(), dur = 1500;
  const step = (now) => {
    const t = Math.min(1, (now - t0) / dur);
    el.textContent = pre + fmt(end * (1 - Math.pow(1 - t, 3)), dec, sep) + suf;
    if (t < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const revealObs = new IntersectionObserver((entries) => {
  let i = 0;
  for (const en of entries) {
    if (!en.isIntersecting) continue;
    en.target.style.setProperty('--i', i++);
    en.target.classList.add('is-in');
    $$('[data-count]', en.target).forEach(countUp);
    revealObs.unobserve(en.target);
  }
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
$$('.reveal').forEach((el) => revealObs.observe(el));

/* ------------------------------ Navegação ------------------------------- */
const nav = $('#nav');
const onScroll = () => nav.classList.toggle('is-stuck', window.scrollY > 40);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ------------------ Visualizador de figuras com abas -------------------- */
// Cada botão das abas traz data-src, data-alt e data-cap da figura que mostra
for (const box of $$('[data-viewer]')) {
  const img = $('img', box), cap = $('.viewer__cap', box);
  const groups = $$('.seg', box);
  const multi = groups.length > 1;   // duas abas combinadas (variável e raio)
  const state = {};
  const show = () => {
    let src, alt, capHtml;
    if (multi) {
      const v = state.var, r = state.ri;
      src = `site/media/grafico-${v}-${r}.webp`;
      const names = { raio: 'Raio', temperatura: 'Temperatura', massa: 'Massa de CO<sub>2</sub>' };
      const alts = { raio: 'do raio', temperatura: 'da temperatura', massa: 'da massa de CO2' };
      alt = `Evolução ${alts[v]} da gotícula de ${r} µm nos experimentos SCONTROL, ECONTROL e E3.`;
      capHtml = `${names[v]} ao longo do tempo na gotícula de ${r}&nbsp;µm, nos experimentos SCONTROL, ECONTROL e E3.`;
    } else {
      const b = $('.seg button.is-on', box);
      src = b.dataset.src; alt = b.dataset.alt; capHtml = b.dataset.cap;
    }
    img.classList.add('is-swap');
    const next = new Image();
    next.onload = next.onerror = () => { img.src = src; img.alt = alt || ''; img.classList.remove('is-swap'); };
    next.src = src;
    if (cap && capHtml) cap.innerHTML = capHtml;
  };
  for (const g of groups) {
    const on = $('button.is-on', g);
    if (on?.dataset.var) state.var = on.dataset.var;
    if (on?.dataset.ri) state.ri = on.dataset.ri;
    $$('button', g).forEach((b) => b.addEventListener('click', () => {
      $$('button', g).forEach((o) => { o.classList.toggle('is-on', o === b); o.setAttribute('aria-selected', String(o === b)); });
      if (b.dataset.var) state.var = b.dataset.var;
      if (b.dataset.ri) state.ri = b.dataset.ri;
      show();
    }));
  }
}

/* ------------------------------ História -------------------------------- */
const story = initStory();

/* ------------------------------ Player ---------------------------------- */
const player = initPlayer($('#player'));
$$('[data-open-player]').forEach((b) => b.addEventListener('click', () => player?.open({ full: true })));
if (player && location.hash === '#defesa') {
  window.addEventListener('load', () => story.scrollTo($('#defesa'), { immediate: true, offset: -64 }));
}
