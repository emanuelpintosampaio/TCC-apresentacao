// A gotícula 3D e as moléculas de CO2.
//
// Dois modos:
//  - "palco": durante a viagem do começo da página, story.js passa a cada quadro
//    a posição, o tamanho e a fase da gotícula (setStage).
//  - "âncoras": no resto da página, a gotícula segue os elementos .drop-anchor
//    (data-temp e data-mass vão de 0 a 1) conforme o scroll.
//
// A gota é quase transparente: o que se vê dentro dela é o vídeo que está atrás
// (a onda, e depois o fundo do mar), invertido como numa lente, com a borda
// escura e o brilho de uma gota d'água de verdade. (O shader também tem um modo
// para fundo claro, uMode = 1, que hoje não é usado.) As moléculas de CO2 são O=C=O em bolas e
// varetas (carbono preto, oxigênios vermelhos, ligações duplas).

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
    // ondulação da superfície e o gradiente dela, para corrigir a normal
    float f = uWobble * (0.50 * sin(a1) + 0.35 * sin(a2) + 0.25 * sin(a3));
    vec3  g = uWobble * (0.50 * K1 * cos(a1) + 0.35 * K2 * cos(a2) + 0.25 * K3 * cos(a3));
    vec3 n = normalize(p);
    vN = normalize(normalMatrix * normalize(n - (g - n * dot(g, n))));
    gl_Position = projectionMatrix * modelViewMatrix * vec4(p * (1.0 + f), 1.0);
  }
`;

const DROP_FRAG = /* glsl */ `
  precision highp float;
  uniform sampler2D uBg;       // vídeo que está atrás da gota
  uniform float uBgReady;
  uniform vec4 uCover;         // como o vídeo cobre a tela: x, y, largura, altura (px)
  uniform vec2 uView;          // tamanho da tela (px CSS)
  uniform float uDpr;
  uniform vec2 uCenter;        // centro da gota (px CSS, a partir do topo)
  uniform float uRadius;
  uniform float uGain;
  uniform sampler2D uEnv;      // reserva enquanto o vídeo não carrega
  uniform float uOpacity;
  uniform float uTemp;
  uniform float uMode;         // 0 = sobre o vídeo, 1 = sobre o fundo branco
  uniform vec2 uLight;
  varying vec3 vN;

  vec3 bg(vec2 p) {
    vec2 uv = (p - uCover.xy) / uCover.zw;
    uv = clamp(vec2(uv.x, 1.0 - uv.y), 0.002, 0.998);
    return texture2D(uBg, uv).rgb * uGain;
  }
  vec3 env(vec3 d) {
    d = normalize(d);
    float u = atan(d.z, d.x) / 6.2831853 + 0.5;
    float v = asin(clamp(d.y, -1.0, 1.0)) / 3.14159265 + 0.5;
    return texture2D(uEnv, vec2(1.0 - abs(2.0 * fract(u) - 1.0), v)).rgb;
  }

  void main() {
    vec3 N = normalize(vN);
    vec3 V = vec3(0.0, 0.0, 1.0);
    float nv = clamp(dot(N, V), 0.0, 1.0);
    float fres = 0.02 + 0.98 * pow(1.0 - nv, 5.0);

    // Pixel atual em px CSS, com a origem no topo da tela
    vec2 frag = vec2(gl_FragCoord.x, uView.y * uDpr - gl_FragCoord.y) / uDpr;
    vec2 d = frag - uCenter;

    // Uma gota é uma lente: mostra a cena de trás invertida e encolhida.
    // Cada cor com uma força um pouco diferente, para a franja colorida da borda.
    vec2 bend = N.xy * vec2(1.0, -1.0) * uRadius * 0.18;
    vec3 refr = vec3(
      bg(uCenter - d * 1.10 + bend).r,
      bg(uCenter - d * 1.16 + bend).g,
      bg(uCenter - d * 1.22 + bend).b
    );
    vec3 fallback = env(refract(-V, N, 0.75)) * 0.8;
    refr = mix(fallback, refr, uBgReady);

    vec3 refl = env(reflect(-V, N));

    vec3 L = normalize(vec3(uLight, 0.8));
    vec3 H = normalize(L + V);
    // brilho principal (pequeno e forte) e um reflexo largo e suave, como uma janela
    float spec  = pow(max(dot(N, H), 0.0), 2600.0) * 1.6;
    float spec2 = pow(max(dot(N, H), 0.0), 40.0) * 0.16;
    vec3 L2 = normalize(vec3(-uLight * 0.6 + vec2(0.35, 0.1), 0.9));
    float spec3 = pow(max(dot(N, normalize(L2 + V)), 0.0), 380.0) * 0.4;
    // luz que atravessa a gota e se concentra no lado oposto (cáustica em crescente)
    float caustic = pow(max(dot(N, normalize(vec3(-L.xy, 0.25))), 0.0), 9.0);
    float rim = pow(1.0 - nv, 3.0);
    // faixa escura perto da borda (reflexão interna total) e um fio de luz bem na borda
    float band = smoothstep(0.42, 0.06, nv) * (1.0 - smoothstep(0.06, 0.0, nv));
    float edge = smoothstep(0.10, 0.0, nv);

    vec3 tint = mix(vec3(1.0, 0.8, 0.8), vec3(0.74, 0.94, 1.0), uTemp);

    // --- sobre o vídeo ---
    vec3 colV = refr * mix(vec3(1.0), tint, 0.22) * 1.1;
    colV *= 1.0 - band * 0.55;
    colV = mix(colV, refl, fres * 0.6);
    colV += tint * caustic * 0.75 + vec3(0.85, 0.97, 1.0) * edge * 0.55;
    colV += vec3(spec + spec2 + spec3);
    float aV = 0.3 + 0.35 * fres + band * 0.35 + edge * 0.4 + caustic * 0.3 + spec + spec3;

    // --- sobre o branco ---
    vec3 deep = vec3(0.07, 0.36, 0.52);
    vec3 colW = mix(vec3(0.93, 0.98, 1.0), deep, band * 0.9 + rim * 0.25);
    colW = mix(colW, vec3(0.55, 0.85, 0.98), caustic * 0.6);
    colW += vec3(spec + spec3) + edge * 0.15;
    float aW = 0.07 + band * 0.55 + rim * 0.35 + caustic * 0.35 + spec + spec3;

    vec3 col = mix(colV, colW, uMode);
    float a = mix(aV, aW, uMode);
    gl_FragColor = vec4(col, clamp(a, 0.0, 1.0) * uOpacity);
  }
`;

// Brilho suave em volta da gota
const HALO_VERT = /* glsl */ `
  varying vec2 vUv;
  void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
`;
const HALO_FRAG = /* glsl */ `
  precision highp float;
  uniform float uOpacity;
  uniform float uMode;
  varying vec2 vUv;
  void main() {
    vec2 q = vUv - 0.5;
    // no branco, a sombra fica um pouco abaixo da gota
    q.y += uMode * 0.06;
    float d = length(q) * 2.0;
    float a = exp(-d * d * 7.0) * mix(0.16, 0.10, uMode) * smoothstep(1.0, 0.55, d) * uOpacity;
    vec3 c = mix(vec3(0.45, 0.85, 1.0), vec3(0.05, 0.35, 0.5), uMode);
    gl_FragColor = vec4(c * a, a);
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

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true, powerPreference: 'high-performance' });
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

  // ---------------- Fundo que a gota refrata ----------------
  let envLoaded;
  const envReady = new Promise((res) => { envLoaded = res; });
  const env = new THREE.TextureLoader().load(new URL('../media/env.jpg', import.meta.url).href, (t) => envLoaded(t));
  env.wrapS = THREE.MirroredRepeatWrapping;
  env.colorSpace = THREE.SRGBColorSpace;
  const bgSources = new Map();   // elemento <video> -> textura
  let bgVideo = null;

  function textureFor(video) {
    if (!bgSources.has(video)) {
      const tex = new THREE.VideoTexture(video);
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.minFilter = THREE.LinearFilter;
      // Vídeo parado (o da onda, rolado pelo scroll): atualiza a cada quadro novo
      const bump = () => { tex.needsUpdate = true; };
      for (const ev of ['seeked', 'loadeddata', 'timeupdate']) video.addEventListener(ev, bump);
      bgSources.set(video, tex);
    }
    return bgSources.get(video);
  }

  // ---------------- A gota ----------------
  const uTime = { value: 0 };
  const dropMat = new THREE.ShaderMaterial({
    vertexShader: DROP_VERT,
    fragmentShader: DROP_FRAG,
    transparent: true, depthWrite: false, depthTest: false,
    uniforms: {
      uTime,
      uWobble: { value: reducedMotion ? 0 : 0.025 },
      uBg: { value: env },
      uBgReady: { value: 0 },
      uCover: { value: new THREE.Vector4(0, 0, 1, 1) },
      uView: { value: new THREE.Vector2(1, 1) },
      uDpr: { value: 1 },
      uCenter: { value: new THREE.Vector2(0, 0) },
      uRadius: { value: 100 },
      uGain: { value: 0.9 },
      uEnv: { value: env },
      uOpacity: { value: 0 },
      uTemp: { value: 0 },
      uMode: { value: 1 },
      uLight: { value: new THREE.Vector2(-0.45, 0.6) },
    },
  });
  const drop = new THREE.Mesh(new THREE.IcosahedronGeometry(1, 32), dropMat);
  drop.renderOrder = 2;
  const haloMat = new THREE.ShaderMaterial({
    vertexShader: HALO_VERT, fragmentShader: HALO_FRAG,
    uniforms: { uOpacity: { value: 0 }, uMode: { value: 0 } },
    transparent: true, depthWrite: false, depthTest: false,
    blending: THREE.CustomBlending, blendSrc: THREE.OneFactor, blendDst: THREE.OneMinusSrcAlphaFactor,
  });
  const halo = new THREE.Mesh(new THREE.PlaneGeometry(4.4, 4.4), haloMat);
  halo.renderOrder = 0;
  scene.add(halo, drop);

  // ---------------- Moléculas de CO2 ----------------
  const NMOL = mobile ? 26 : 40;
  const atomGeo = new THREE.SphereGeometry(1, 24, 18);
  // material com verniz: brilho nítido e reflexo do ambiente
  const atomMat = new THREE.MeshPhysicalMaterial({ roughness: 0.3, metalness: 0.0, clearcoat: 1, clearcoatRoughness: 0.05, envMapIntensity: 0.55 });
  const atoms = new THREE.InstancedMesh(atomGeo, atomMat, NMOL * 3);
  atoms.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  atoms.frustumCulled = false;
  atoms.renderOrder = 1;   // antes da gota: as de dentro ficam "atrás do vidro"
  for (let i = 0; i < NMOL; i++) {
    atoms.setColorAt(i * 3, C_COLOR);
    atoms.setColorAt(i * 3 + 1, O_COLOR);
    atoms.setColorAt(i * 3 + 2, O_COLOR);
  }
  // ligações duplas C=O: duas varetas entre o carbono e cada oxigênio
  const stickGeo = new THREE.CylinderGeometry(1, 1, 1, 12, 1);
  const stickMat = new THREE.MeshPhysicalMaterial({ color: 0xc9d2d8, roughness: 0.3, clearcoat: 0.6, envMapIntensity: 0.8 });
  const sticks = new THREE.InstancedMesh(stickGeo, stickMat, NMOL * 4);
  sticks.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
  sticks.frustumCulled = false;
  sticks.renderOrder = 1;
  scene.add(atoms, sticks);

  // reflexos do ambiente nas moléculas (a partir do quadro da onda)
  const pmrem = new THREE.PMREMGenerator(renderer);
  envReady.then((tex) => {
    tex.mapping = THREE.EquirectangularReflectionMapping;
    const rt = pmrem.fromEquirectangular(tex);
    atomMat.envMap = stickMat.envMap = rt.texture;
    atomMat.needsUpdate = stickMat.needsUpdate = true;
  });

  const rnd = (a, b) => a + Math.random() * (b - a);
  const mols = [];
  for (let i = 0; i < NMOL; i++) {
    // posição no ar: anel em volta da gota, em unidades do raio
    const ang = rnd(0, Math.PI * 2);
    const dist = rnd(1.35, 2.5);
    // posição dentro: ponto aleatório numa esfera de raio 0,7
    const u = rnd(-1, 1), th = rnd(0, Math.PI * 2), rr = Math.cbrt(Math.random()) * 0.7;
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
  function resize() {
    W = window.innerWidth; H = window.innerHeight;
    dpr = Math.min(window.devicePixelRatio || 1, mobile ? 1.5 : 2);
    renderer.setPixelRatio(dpr);
    renderer.setSize(W, H, false);
    camera.right = W; camera.bottom = -H;
    camera.updateProjectionMatrix();
    dropMat.uniforms.uView.value.set(W, H);
    dropMat.uniforms.uDpr.value = dpr;
  }
  resize();
  window.addEventListener('resize', resize);

  // Retângulo que um vídeo em "object-fit: cover" ocupa na tela
  function cover(video) {
    const vw = video.videoWidth || 1280, vh = video.videoHeight || 720;
    const s = Math.max(W / vw, H / vh);
    return [(W - vw * s) / 2, (H - vh * s) / 2, vw * s, vh * s];
  }

  // ---------------- Âncoras (modo do resto da página) ----------------
  const anchors = [...document.querySelectorAll('.drop-anchor')].map((el) => ({
    el,
    temp: parseFloat(el.dataset.temp ?? '0'),
    mass: parseFloat(el.dataset.mass ?? '0'),
    x: 0, y: 0, r: 0,
  }));

  function measure() {
    const sx = window.scrollX, sy = window.scrollY;
    for (const a of anchors) {
      const b = a.el.getBoundingClientRect();
      a.x = b.left + b.width / 2 + sx;
      a.y = b.top + b.height / 2 + sy;
      a.r = b.width / 2;
    }
    anchors.sort((p, q) => p.y - q.y);
  }

  function anchorTarget() {
    if (!anchors.length) return null;
    measure();
    const sx = window.scrollX, sy = window.scrollY;
    const s = sy + H / 2;
    let i = 0;
    while (i < anchors.length - 2 && s > anchors[i + 1].y) i++;
    const a = anchors[i], b = anchors[Math.min(i + 1, anchors.length - 1)];
    const gap = Math.max(1, b.y - a.y);
    const win = Math.min(gap, H * 1.15);
    const t = smooth(clamp01((s - (a.y + gap / 2 - win / 2)) / win));
    return {
      x: lerp(a.x, b.x, t) - sx,
      y: lerp(a.y, b.y, t) - sy,
      r: lerp(a.r, b.r, t),
      temp: lerp(a.temp, b.temp, t),
      absorb: lerp(a.mass, b.mass, t),
      release: 0,
      air: 0,
      // fica mais translúcida enquanto viaja, para não atrapalhar a leitura
      alpha: 1 - Math.sin(Math.PI * t) * (mobile ? 0.8 : 0.45),
    };
  }

  // ---------------- Estado ----------------
  let stage = null;
  let bgReady = 0;
  let mode = 0;
  const cur = { x: W / 2, y: H / 2, r: 0, temp: 0, absorb: 0, release: 0, air: 0, alpha: 0, init: false };
  const mouse = { x: 0, y: 0, sx: 0, sy: 0 };
  let highlight = null;
  let hlPulse = 0;

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

    const tg = stage || anchorTarget();
    if (!tg) return;
    if (!cur.init) Object.assign(cur, tg, { init: true });

    // No palco a posição já vem suave do scroll; nas âncoras há inércia
    const k = stage || reducedMotion ? 1 - Math.exp(-dt * 30) : 1 - Math.exp(-dt * 7);
    const kAlpha = 1 - Math.exp(-dt * (stage ? 30 : 5));
    const px = cur.x, py = cur.y;
    cur.x = lerp(cur.x, tg.x, k);
    cur.y = lerp(cur.y, tg.y, k);
    // saltos grandes (mudança de cena) não atravessam a tela
    if (Math.hypot(tg.x - cur.x, tg.y - cur.y) > Math.max(W, H) * 0.7) { cur.x = tg.x; cur.y = tg.y; }
    for (const key of ['r', 'temp', 'absorb', 'release', 'air']) cur[key] = lerp(cur[key], tg[key], k);
    cur.alpha = lerp(cur.alpha, tg.alpha, kAlpha);

    mouse.sx = lerp(mouse.sx, mouse.x, 1 - Math.exp(-dt * 3));
    mouse.sy = lerp(mouse.sy, mouse.y, 1 - Math.exp(-dt * 3));
    hlPulse = lerp(hlPulse, highlight ? 1 : 0, 1 - Math.exp(-dt * 6));

    const r = Math.max(0.001, cur.r * (1 + hlPulse * 0.06 * Math.sin(time * 4.5)));
    const bob = reducedMotion ? 0 : Math.sin(time * 0.9) * Math.min(r, 160) * 0.035;
    const cx = cur.x + mouse.sx * Math.min(r, 200) * 0.04;
    const cy = cur.y + bob + mouse.sy * Math.min(r, 200) * 0.04;

    // Estica um pouco na direção do movimento
    const vx = Math.abs(cur.x - px) / Math.max(dt, 1e-3);
    const vy = Math.abs(cur.y - py) / Math.max(dt, 1e-3);
    const ax = reducedMotion ? 0 : Math.min(0.16, vx / (r * 60 + 500));
    const ay = reducedMotion ? 0 : Math.min(0.16, vy / (r * 60 + 500));

    const visible = r > 1.5 && cur.alpha > 0.01;
    drop.visible = halo.visible = visible;
    drop.position.set(cx, -cy, 0);
    halo.position.set(cx, -cy, -1);
    drop.scale.set(r * (1 + ax - ay * 0.45), r * (1 + ay - ax * 0.45), r);
    halo.scale.setScalar(r);

    // Fundo refratado
    const vid = stage?.video || bgVideo;
    if (vid && vid.readyState >= 2) {
      dropMat.uniforms.uBg.value = textureFor(vid);
      bgReady = lerp(bgReady, 1, 1 - Math.exp(-dt * 6));
      dropMat.uniforms.uCover.value.set(...cover(vid));
      dropMat.uniforms.uGain.value = stage?.gain ?? 0.55;
    } else {
      bgReady = lerp(bgReady, 0, 1 - Math.exp(-dt * 6));
    }
    dropMat.uniforms.uBgReady.value = bgReady;
    mode = 0;   // fundo escuro na página toda
    dropMat.uniforms.uMode.value = mode;
    haloMat.uniforms.uMode.value = mode;
    dropMat.uniforms.uCenter.value.set(cx, cy);
    dropMat.uniforms.uRadius.value = r;
    dropMat.uniforms.uOpacity.value = cur.alpha;
    dropMat.uniforms.uTemp.value = clamp01(cur.temp);
    dropMat.uniforms.uLight.value.set(-0.45 + mouse.sx * 0.3, 0.6 - mouse.sy * 0.3);
    dropMat.uniforms.uWobble.value = reducedMotion ? 0 : 0.025 * Math.min(1, 120 / Math.max(r, 1) + 0.3);
    haloMat.uniforms.uOpacity.value = cur.alpha;

    // ---- moléculas ----
    const s = Math.min(9, Math.max(mobile ? 3.2 : 3.8, r * 0.048));
    const absorb = clamp01(cur.absorb + (highlight === 'm' ? 0.35 * hlPulse : 0));
    for (let i = 0; i < NMOL; i++) {
      const m = mols[i];
      const u = smooth(clamp01((absorb - m.tAbs) / 0.1));      // 0 = no ar, 1 = dentro
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
      if (u < 1) scale *= cur.air;                    // no ar, só aparecem no palco
      if (vRel > 0) scale *= 1 - ss(0.55, 1, vRel);  // dissolvem
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
    // Vídeo que fica atrás da gota fora do palco
    setBackground(video) { bgVideo = video; },
    setHighlight(name) { highlight = name; },
    // Uma molécula que ainda está no ar, perto da gota (para o rótulo "CO₂")
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
