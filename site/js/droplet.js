// A gotícula 3D e as moléculas de CO2, só na viagem do começo da página.
//
// story.js passa a cada quadro a posição, o tamanho e a fase da gotícula
// (setStage). Fora da viagem ela some e o desenho para.
//
// A gota é desenhada em três camadas, como uma gota d'água de verdade:
//  1. o corpo: uma lente que mostra a cena de trás invertida e nítida, mais
//     escura no alto, com a luz concentrada embaixo e uma faixa escura na borda;
//  2. as moléculas de CO2 (O=C=O em bolas e varetas) dentro e em volta dela;
//  3. o brilho do vidro por cima de tudo: o reflexo forte, uma janela de luz
//     suave e um fio de luz na borda.

import * as THREE from '../vendor/three/three.module.min.js';

const DROP_VERT = /* glsl */ `
  uniform float uTime;
  uniform float uWobble;
  varying vec3 vN;

  const vec3 K1 = vec3( 2.1,  1.3, 0.7);
  const vec3 K2 = vec3(-1.2,  2.4, 1.1);
  const vec3 K3 = vec3( 0.6, -1.7, 2.6);

  void main() {
    vec3 p = position;                       // esfera de raio 1
    float a1 = dot(K1, p) + uTime * 1.1;
    float a2 = dot(K2, p) + uTime * 1.7 + 1.3;
    float a3 = dot(K3, p) - uTime * 1.3 + 2.1;
    // ondulação leve da superfície e o gradiente dela, para corrigir a normal
    float f = uWobble * (0.50 * sin(a1) + 0.35 * sin(a2) + 0.25 * sin(a3));
    vec3  g = uWobble * (0.50 * K1 * cos(a1) + 0.35 * K2 * cos(a2) + 0.25 * K3 * cos(a3));
    vec3 n = normalize(p);
    vN = normalize(normalMatrix * normalize(n - (g - n * dot(g, n))));
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p * (1.0 + f), 1.0);
  }
`;

// Partes comuns às duas camadas da gota
const DROP_COMMON = /* glsl */ `
  uniform vec2 uView;          // tamanho da tela (px CSS)
  uniform float uDpr;
  uniform vec2 uCenter;        // centro da gota (px CSS, a partir do topo)
  uniform float uRadius;
  uniform float uOpacity;
  uniform vec2 uLight;
  varying vec3 vN;

  // posição do pixel em relação ao centro da gota: (0,0) no centro, comprimento 1 na borda
  vec2 local() {
    vec2 frag = vec2(gl_FragCoord.x, uView.y * uDpr - gl_FragCoord.y) / uDpr;
    return (frag - uCenter) / uRadius;
  }
`;

const BODY_FRAG = /* glsl */ `
  precision highp float;
  ${DROP_COMMON}
  uniform sampler2D uBg;       // a cena que está atrás da gota
  uniform float uBgReady;
  uniform vec4 uCover;         // como essa cena cobre a tela: x, y, largura, altura (px)
  uniform float uGain;
  uniform sampler2D uEnv;      // reserva enquanto a cena não carrega
  uniform float uTemp;

  vec3 bg(vec2 p) {
    vec2 uv = (p - uCover.xy) / uCover.zw;
    uv = clamp(vec2(uv.x, 1.0 - uv.y), 0.002, 0.998);
    return texture2D(uBg, uv).rgb;
  }
  vec3 env(vec2 q) {
    return texture2D(uEnv, clamp(vec2(0.5 + q.x * 0.3, 0.5 - q.y * 0.3), 0.0, 1.0)).rgb;
  }

  void main() {
    vec2 q = local();
    float rr = length(q);
    if (rr > 1.0) discard;

    // Lente de água: a cena de trás aparece ampliada no meio e comprimida na
    // borda, como através de uma bolinha de vidro. Um pouco de dispersão nas cores perto da borda.
    float k = 0.55 + 0.55 * rr * rr;
    vec2 off = q * uRadius * k;
    float disp = 0.04 * rr * rr;
    vec3 scene = vec3(
      bg(uCenter + off * (1.0 + disp)).r,
      bg(uCenter + off).g,
      bg(uCenter + off * (1.0 - disp)).b
    );
    vec3 col = mix(env(q), scene * uGain, uBgReady);

    // água limpa: um pouco mais clara, com cor e um leve tom azul
    float lum = dot(col, vec3(0.299, 0.587, 0.114));
    col = mix(vec3(lum), col, 1.18) * vec3(0.94, 1.0, 1.05) * 1.06;
    // sombra suave em cima, luz embaixo (a gota funciona como lente para a luz do céu)
    col *= 0.86 + 0.22 * smoothstep(-1.0, 0.8, q.y);
    // em cena escura (debaixo d'água) a gota não vira uma bola preta: um leve brilho de água
    col += vec3(0.03, 0.08, 0.1) * (1.0 - smoothstep(0.0, 0.35, lum));

    // luz concentrada em crescente, embaixo e à direita, dentro da borda
    float side = max(dot(normalize(q + 1e-4), normalize(vec2(0.45, 0.9))), 0.0);
    float crescent = smoothstep(0.62, 0.86, rr) * (1.0 - smoothstep(0.88, 0.95, rr)) * pow(side, 2.0);
    vec3 glow = mix(vec3(1.0, 0.88, 0.9), vec3(0.8, 0.97, 1.0), uTemp);
    col += glow * crescent * 0.55;

    // contorno: uma faixa escura e fina logo antes da borda
    float band = smoothstep(0.84, 0.96, rr);
    col *= 1.0 - band * 0.55;

    // transparente o bastante para a gota parecer água; borda suave, sem serrilhado
    float a = (1.0 - smoothstep(0.975, 1.0, rr)) * mix(0.9, 0.97, band);
    gl_FragColor = vec4(col, a * uOpacity);
  }
`;

const GLINT_FRAG = /* glsl */ `
  precision highp float;
  ${DROP_COMMON}

  // elipse suave girada, em coordenadas da gota
  float blob(vec2 q, vec2 c, vec2 r, float ang, float soft) {
    float cs = cos(ang), sn = sin(ang);
    vec2 d = q - c;
    d = vec2(cs * d.x + sn * d.y, -sn * d.x + cs * d.y) / r;
    return 1.0 - smoothstep(1.0 - soft, 1.0, length(d));
  }

  void main() {
    vec2 q = local();
    float rr = length(q);
    if (rr > 1.0) discard;
    // a luz vem do alto à esquerda e acompanha um pouco o mouse
    vec2 l = normalize(vec2(uLight.x, -uLight.y));
    vec2 hp = l * 0.52;
    float ang = atan(l.y, l.x) + 1.5708;

    // reflexo em forma de janela (largo e suave) e um ponto forte de luz
    float window = blob(q, hp, vec2(0.30, 0.13), ang, 0.7) * 0.32;
    float sparkle = blob(q, hp * 1.08, vec2(0.055, 0.055), 0.0, 0.8) * 1.1;
    // um reflexo pequeno e fraco do lado oposto
    float back = blob(q, -hp * 1.25, vec2(0.08, 0.04), ang, 0.9) * 0.22;
    // fio de luz fino bem na borda, mais forte do lado da luz
    float lit = 0.35 + 0.65 * max(dot(normalize(q + 1e-4), l), 0.0);
    float rim = smoothstep(0.93, 0.985, rr) * (1.0 - smoothstep(0.985, 1.0, rr)) * lit;

    vec3 c = vec3(window + sparkle + back) + vec3(0.85, 0.97, 1.0) * rim * 0.7;
    // soma por cima (brilho), sem escurecer nada
    gl_FragColor = vec4(c * uOpacity, 0.0);
  }
`;

const clamp01 = (x) => Math.min(1, Math.max(0, x));
const lerp = (a, b, t) => a + (b - a) * t;
const smooth = (t) => t * t * (3 - 2 * t);
const ss = (a, b, x) => smooth(clamp01((x - a) / (b - a)));

// Cores e tamanhos (em unidades de "s", calculado pelo raio da gota).
// Bolas e varetas: carbono preto no meio, oxigênios vermelhos, ligações duplas.
const C_COLOR = new THREE.Color(0x141414);
const O_COLOR = new THREE.Color(0xd4101e);   // vermelho puro, sem puxar para o laranja
const C_R = 0.66, O_R = 0.6, BOND = 1.95;   // raio do C, raio do O, distância entre C e O
const STICK_R = 0.11, STICK_GAP = 0.2;      // espessura e afastamento das duas varetas

export function initDroplet({ canvas, reducedMotion = false }) {
  const mobile = window.matchMedia('(max-width: 860px)').matches;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: !mobile, powerPreference: 'high-performance' });
  renderer.setClearColor(0x000000, 0);
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(0, 1, 0, -1, -2000, 2000);
  camera.position.z = 1000;

  scene.add(new THREE.AmbientLight(0xffffff, 0.75));
  const sun = new THREE.DirectionalLight(0xffffff, 2.2);
  sun.position.set(-0.5, 0.8, 1);
  scene.add(sun);
  const fill = new THREE.DirectionalLight(0x9fdcff, 0.7);
  fill.position.set(0.7, -0.4, 0.6);
  scene.add(fill);

  // ---------------- Cena atrás da gota ----------------
  let envLoaded;
  const envReady = new Promise((res) => { envLoaded = res; });
  const env = new THREE.TextureLoader().load(new URL('../media/env.jpg', import.meta.url).href, (t) => envLoaded(t));
  env.colorSpace = THREE.SRGBColorSpace;
  const bgSources = new Map();   // elemento (vídeo ou canvas) -> textura

  function textureFor(src) {
    if (!bgSources.has(src)) {
      // a cena pode ser o vídeo da onda ou um canvas (os quadros da onda no celular)
      const tex = src instanceof HTMLCanvasElement ? new THREE.CanvasTexture(src) : new THREE.VideoTexture(src);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.minFilter = THREE.LinearFilter;
      // vídeo parado (rolado pelo scroll): atualiza a cada quadro novo
      const bump = () => { tex.needsUpdate = true; };
      for (const ev of ['seeked', 'loadeddata', 'timeupdate']) src.addEventListener(ev, bump);
      bgSources.set(src, tex);
    }
    return bgSources.get(src);
  }

  // ---------------- A gota (corpo e brilho) ----------------
  const uTime = { value: 0 };
  const shared = {
    uView: { value: new THREE.Vector2(1, 1) },
    uDpr: { value: 1 },
    uCenter: { value: new THREE.Vector2(0, 0) },
    uRadius: { value: 100 },
    uOpacity: { value: 0 },
    uLight: { value: new THREE.Vector2(-0.45, 0.6) },
    uEnv: { value: env },
    uTime,
    uWobble: { value: reducedMotion ? 0 : 0.02 },
  };
  const bodyMat = new THREE.ShaderMaterial({
    vertexShader: DROP_VERT,
    fragmentShader: BODY_FRAG,
    transparent: true, depthWrite: false, depthTest: false,
    uniforms: {
      ...shared,
      uBg: { value: env },
      uBgReady: { value: 0 },
      uCover: { value: new THREE.Vector4(0, 0, 1, 1) },
      uGain: { value: 0.9 },
      uTemp: { value: 0 },
    },
  });
  const glintMat = new THREE.ShaderMaterial({
    vertexShader: DROP_VERT,
    fragmentShader: GLINT_FRAG,
    uniforms: shared,
    transparent: true, depthWrite: false, depthTest: false,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneFactor,
  });
  const sphere = new THREE.IcosahedronGeometry(1, mobile ? 18 : 32);
  const body = new THREE.Mesh(sphere, bodyMat);
  const glint = new THREE.Mesh(sphere, glintMat);
  body.renderOrder = 0;    // 1º o corpo,
  glint.renderOrder = 2;   // 3º o brilho por cima das moléculas
  scene.add(body, glint);

  // ---------------- Moléculas de CO2 ----------------
  const NMOL = mobile ? 26 : 40;
  const atomGeo = mobile ? new THREE.SphereGeometry(1, 14, 10) : new THREE.SphereGeometry(1, 24, 18);
  // material com verniz: brilho nítido e reflexo do ambiente
  // transparent: true (com opacidade 1) põe as moléculas na mesma fila de desenho da gota,
  // e a ordem fica corpo, moléculas, brilho
  const atomMat = new THREE.MeshPhysicalMaterial({ roughness: 0.3, metalness: 0.0, clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 0.55, transparent: true, depthWrite: true });
  const atoms = new THREE.InstancedMesh(atomGeo, atomMat, NMOL * 3);
  atoms.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  atoms.frustumCulled = false;
  atoms.renderOrder = 1;   // 2º as moléculas, sobre o corpo e sob o brilho
  for (let i = 0; i < NMOL; i++) {
    atoms.setColorAt(i * 3, C_COLOR);
    atoms.setColorAt(i * 3 + 1, O_COLOR);
    atoms.setColorAt(i * 3 + 2, O_COLOR);
  }
  // ligações duplas C=O: duas varetas entre o carbono e cada oxigênio
  const stickGeo = new THREE.CylinderGeometry(1, 1, 1, 12, 1);
  const stickMat = new THREE.MeshPhysicalMaterial({ color: 0xc9d2d8, roughness: 0.3, clearcoat: 0.6, envMapIntensity: 0.8, transparent: true, depthWrite: true });
  const sticks = new THREE.InstancedMesh(stickGeo, stickMat, NMOL * 4);
  sticks.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  sticks.frustumCulled = false;
  sticks.renderOrder = 1;
  scene.add(atoms, sticks);

  // reflexos do ambiente nas moléculas (a partir do quadro da onda)
  const pmrem = new THREE.PMREMGenerator(renderer);
  envReady.then((tex) => {
    const t2 = tex.clone();
    t2.mapping = THREE.EquirectangularReflectionMapping;
    t2.needsUpdate = true;
    const rt = pmrem.fromEquirectangular(t2);
    atomMat.envMap = stickMat.envMap = rt.texture;
    atomMat.needsUpdate = stickMat.needsUpdate = true;
  });

  const rnd = (a, b) => a + Math.random() * (b - a);
  const mols = [];
  for (let i = 0; i < NMOL; i++) {
    // posição no ar: anel em volta da gota, em unidades do raio
    const ang = rnd(0, Math.PI * 2);
    const dist = rnd(1.35, 2.5);
    // posição dentro: ponto aleatório numa esfera de raio 0,62 (longe da faixa escura)
    const u = rnd(-1, 1), th = rnd(0, Math.PI * 2), rr = Math.cbrt(Math.random()) * 0.62;
    const sq = Math.sqrt(1 - u * u);
    mols.push({
      air: new THREE.Vector2(Math.cos(ang) * dist, Math.sin(ang) * dist * 0.8),
      dist,
      inside: new THREE.Vector3(rr * sq * Math.cos(th), rr * u, rr * sq * Math.sin(th)),
      spin: new THREE.Vector3(rnd(-1, 1), rnd(-1, 1), rnd(-1, 1)).normalize(),
      spinSpeed: rnd(0.3, 0.9) * (Math.random() < 0.5 ? -1 : 1),
      orbit: rnd(0.15, 0.4) * (Math.random() < 0.5 ? -1 : 1),
      phase: rnd(0, Math.PI * 2),
      bulge: rnd(-0.9, 0.9),
      tAbs: 0,   // ordem em que é absorvida: as mais próximas primeiro
      out: new THREE.Vector2(rnd(-1, 1), rnd(0.35, 1)).normalize(),   // saída no mar
      outDist: rnd(0.5, 1.2),
      tRel: rnd(0, 0.55),
      size: rnd(0.85, 1.12),
    });
  }
  [...mols].sort((a, b) => a.dist - b.dist).forEach((m, k) => {
    m.tAbs = clamp01((k / NMOL) * 0.9 + rnd(-0.04, 0.04));
  });

  // ---------------- Tela ----------------
  let W = 1, H = 1, dpr = 1;
  const touch = window.matchMedia('(pointer: coarse)').matches;
  function resize() {
    // no celular, a barra de endereço aparece e some durante o scroll e muda a altura
    // da tela; refazer o canvas a cada vez faz a gota piscar, então mudanças pequenas
    // só de altura são ignoradas (o canvas usa a maior altura já vista)
    const nw = window.innerWidth, nh = window.innerHeight;
    if (touch && nw === W && nh <= H && H - nh < 180) return;
    const sameWidth = nw === W;
    W = nw; H = touch && sameWidth ? Math.max(nh, H) : nh;   // girar o celular recalcula tudo
    dpr = Math.min(window.devicePixelRatio || 1, mobile ? 1.35 : 2);
    renderer.setPixelRatio(dpr);
    renderer.setSize(W, H, false);
    canvas.style.height = `${H}px`;
    camera.right = W; camera.bottom = -H;
    camera.updateProjectionMatrix();
    shared.uView.value.set(W, H);
    shared.uDpr.value = dpr;
    needsClear = true;
  }
  let needsClear = false;
  resize();
  window.addEventListener('resize', resize);

  // Retângulo que a cena (vídeo em "object-fit: cover" ou canvas) ocupa na tela
  function cover(src) {
    if (src instanceof HTMLCanvasElement) return [0, 0, W, document.querySelector('.stage__pin')?.offsetHeight || H];
    const vw = src.videoWidth || 1280, vh = src.videoHeight || 720;
    const s = Math.max(W / vw, H / vh);
    return [(W - vw * s) / 2, (H - vh * s) / 2, vw * s, vh * s];
  }

  // ---------------- Estado ----------------
  let stage = null;
  let bgReady = 0;
  let idle = false;
  const cur = { x: W / 2, y: H / 2, r: 0, temp: 0, absorb: 0, release: 0, air: 0, alpha: 0, init: false };
  const mouse = { x: 0, y: 0, sx: 0, sy: 0 };

  window.addEventListener('pointermove', (e) => {
    mouse.x = (e.clientX / W) * 2 - 1;
    mouse.y = (e.clientY / H) * 2 - 1;
  }, { passive: true });

  const m4 = new THREE.Matrix4();
  const q = new THREE.Quaternion();
  const v3 = new THREE.Vector3();
  const sc = new THREE.Vector3();
  const axisX = new THREE.Vector3();
  const perp = new THREE.Vector3();
  const qStick = new THREE.Quaternion();
  const yUp = new THREE.Vector3(0, 1, 0);
  const zero = new THREE.Matrix4().makeScale(0, 0, 0);
  const molScreen = Array.from({ length: NMOL }, () => ({ x: 0, y: 0, on: false }));

  const clock = new THREE.Clock();
  let raf = 0;

  function frame() {
    raf = requestAnimationFrame(frame);
    if (document.hidden) return;
    const dt = Math.min(clock.getDelta(), 0.05);
    const time = clock.elapsedTime;
    uTime.value = time;

    // fora da viagem a gota some aos poucos e depois o desenho para
    const tg = stage || { ...cur, alpha: 0, air: 0 };
    if (!stage && cur.alpha < 0.005) {
      if (!idle || needsClear) { renderer.clear(); idle = true; needsClear = false; }
      return;
    }
    idle = false;
    if (!cur.init) Object.assign(cur, tg, { init: true });

    const k = 1 - Math.exp(-dt * 30);
    const kAlpha = 1 - Math.exp(-dt * (stage ? 30 : 8));
    const px = cur.x, py = cur.y;
    cur.x = lerp(cur.x, tg.x, k);
    cur.y = lerp(cur.y, tg.y, k);
    // saltos grandes (mudança de cena) não atravessam a tela
    if (Math.hypot(tg.x - cur.x, tg.y - cur.y) > Math.max(W, H) * 0.7) { cur.x = tg.x; cur.y = tg.y; }
    for (const key of ['r', 'temp', 'absorb', 'release', 'air']) cur[key] = lerp(cur[key], tg[key], k);
    cur.alpha = lerp(cur.alpha, tg.alpha, kAlpha);

    mouse.sx = lerp(mouse.sx, mouse.x, 1 - Math.exp(-dt * 3));
    mouse.sy = lerp(mouse.sy, mouse.y, 1 - Math.exp(-dt * 3));

    const r = Math.max(0.001, cur.r);
    const bob = reducedMotion ? 0 : Math.sin(time * 0.9) * Math.min(r, 160) * 0.03;
    const cx = cur.x + mouse.sx * Math.min(r, 200) * 0.03;
    const cy = cur.y + bob + mouse.sy * Math.min(r, 200) * 0.03;

    // estica um pouco na direção do movimento
    const vx = Math.abs(cur.x - px) / Math.max(dt, 1e-3);
    const vy = Math.abs(cur.y - py) / Math.max(dt, 1e-3);
    const ax = reducedMotion ? 0 : Math.min(0.12, vx / (r * 60 + 500));
    const ay = reducedMotion ? 0 : Math.min(0.12, vy / (r * 60 + 500));

    const visible = r > 1.5 && cur.alpha > 0.01;
    body.visible = glint.visible = visible;
    for (const m of [body, glint]) {
      m.position.set(cx, -cy, 0);
      m.scale.set(r * (1 + ax - ay * 0.45), r * (1 + ay - ax * 0.45), r);
    }

    // cena refratada
    const src = stage?.video;
    const ready = src && (src instanceof HTMLCanvasElement ? src.dataset.ready === '1' : src.readyState >= 2);
    if (ready) {
      bodyMat.uniforms.uBg.value = textureFor(src);
      bgReady = lerp(bgReady, 1, 1 - Math.exp(-dt * 6));
      bodyMat.uniforms.uCover.value.set(...cover(src));
      bodyMat.uniforms.uGain.value = (stage?.gain ?? 0.9) * 1.25;
    } else {
      bgReady = lerp(bgReady, 0, 1 - Math.exp(-dt * 6));
    }
    bodyMat.uniforms.uBgReady.value = bgReady;
    bodyMat.uniforms.uTemp.value = clamp01(cur.temp);
    shared.uCenter.value.set(cx, cy);
    shared.uRadius.value = r;
    shared.uOpacity.value = cur.alpha;
    shared.uLight.value.set(-0.45 + mouse.sx * 0.25, 0.6 - mouse.sy * 0.25);
    shared.uWobble.value = reducedMotion ? 0 : 0.02 * Math.min(1, 120 / Math.max(r, 1) + 0.3);

    // ---- moléculas ----
    const s = Math.min(9, Math.max(mobile ? 3.2 : 3.8, r * 0.048));
    for (let i = 0; i < NMOL; i++) {
      const m = mols[i];
      const u = smooth(clamp01((cur.absorb - m.tAbs) / 0.1));  // 0 = no ar, 1 = dentro
      const vRel = clamp01((cur.release - m.tRel) / 0.42);     // saída no mar

      // ponto dentro da gota (girando devagar)
      const ang = time * m.orbit + m.phase;
      const ix = m.inside.x * Math.cos(ang) - m.inside.z * Math.sin(ang);
      const iz = m.inside.x * Math.sin(ang) + m.inside.z * Math.cos(ang);
      const iy = m.inside.y + Math.sin(time * 0.7 + m.phase) * 0.04;
      let x = cx + ix * r, y = cy + iy * r, z = iz * r;

      if (u < 1) {
        // no ar, em volta da gota, flutuando; depois um caminho curvo até ela
        const drift = reducedMotion ? 0 : 0.12;
        const axp = cx + (m.air.x + Math.sin(time * 0.35 + m.phase) * drift) * r;
        const ayp = cy + (m.air.y + Math.cos(time * 0.3 + m.phase) * drift) * r;
        const bx = -(ayp - cy) * m.bulge * 0.35, by = (axp - cx) * m.bulge * 0.35;
        const w = Math.sin(Math.PI * u);
        x = lerp(axp, x, u) + bx * w;
        y = lerp(ayp, y, u) + by * w;
        z = lerp(r * 0.4, z, u);
      }
      if (vRel > 0) {
        // no mar: sai da gota e se espalha para baixo
        const e = 1 - Math.pow(1 - vRel, 2);
        x += m.out.x * e * (r * 1.6 + H * 0.22 * m.outDist);
        y += m.out.y * e * (r * 1.2 + H * 0.3 * m.outDist) + Math.sin(time * 1.3 + m.phase) * 6 * e;
      }

      let scale = s * m.size * Math.min(1, r / 30);   // some junto quando a gota fica minúscula
      if (u < 1) scale *= cur.air;                    // as que estão no ar aparecem aos poucos
      if (vRel > 0) scale *= 1 - ss(0.55, 1, vRel);  // dissolvem no mar
      else scale *= Math.min(1, cur.alpha * 1.6);

      const mol = molScreen[i];
      mol.x = x; mol.y = y; mol.on = scale > 0.5 && u < 0.05;

      if (scale < 0.05) {
        for (let k2 = 0; k2 < 3; k2++) atoms.setMatrixAt(i * 3 + k2, zero);
        for (let k2 = 0; k2 < 4; k2++) sticks.setMatrixAt(i * 4 + k2, zero);
        continue;
      }
      q.setFromAxisAngle(m.spin, time * m.spinSpeed + m.phase);
      axisX.set(1, 0, 0).applyQuaternion(q);
      // carbono no centro
      m4.compose(v3.set(x, -y, z), q, sc.setScalar(scale * C_R));
      atoms.setMatrixAt(i * 3, m4);
      // a vareta é um cilindro em pé (eixo Y): gira até o eixo da molécula
      qStick.setFromUnitVectors(yUp, axisX);
      perp.set(0, 1, 0).applyQuaternion(q).multiplyScalar(STICK_GAP * scale);
      // dois oxigênios, um de cada lado: O=C=O
      for (const [slot, sign] of [[1, 1], [2, -1]]) {
        const d = BOND * scale * sign;
        m4.compose(v3.set(x + axisX.x * d, -y + axisX.y * d, z + axisX.z * d), q, sc.setScalar(scale * O_R));
        atoms.setMatrixAt(i * 3 + slot, m4);
        // ligação dupla: duas varetas paralelas no meio do caminho entre C e O
        const h = d / 2;
        for (const [k2, side] of [[0, 1], [1, -1]]) {
          m4.compose(
            v3.set(x + axisX.x * h + perp.x * side, -y + axisX.y * h + perp.y * side, z + axisX.z * h + perp.z * side),
            qStick, sc.set(scale * STICK_R, BOND * scale, scale * STICK_R),
          );
          sticks.setMatrixAt(i * 4 + (slot - 1) * 2 + k2, m4);
        }
      }
    }
    atoms.instanceMatrix.needsUpdate = true;
    sticks.instanceMatrix.needsUpdate = true;

    renderer.render(scene, camera);
  }
  frame();

  return {
    // Palco: { x, y, r, alpha, temp, absorb, release, air, video, gain } ou null
    setStage(state) { stage = state; },
    // avisa que o canvas da cena mudou (um quadro novo da onda)
    bgDirty() { const src = stage?.video; if (src && bgSources.has(src)) bgSources.get(src).needsUpdate = true; },
    // uma molécula que ainda está no ar, perto da gota (para o rótulo "CO₂")
    nearestAirMolecule() {
      let best = null, bd = Infinity;
      for (const m of molScreen) {
        if (!m.on) continue;
        const d = Math.hypot(m.x - cur.x, m.y - cur.y);
        if (d > cur.r * 1.5 && d < bd && m.x > 40 && m.x < W - 40 && m.y > 80 && m.y < H - 60) { bd = d; best = m; }
      }
      return best;
    },
    destroy() { cancelAnimationFrame(raf); window.removeEventListener('resize', resize); renderer.dispose(); },
  };
}
