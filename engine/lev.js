/* L-evate film runtime. Sits on motion.js (window.M) and adds what a launch
   film needs beyond one morphing shape: formats that recompose instead of crop,
   one cue list that drives both picture and sound, real texture, and a preview
   player with audio. Every frame is still a pure function of t. */
(function(){
const M = window.M, L = window.L = {};

// ------------------------------------------------------------------ formats
L.FORMATS = {'16x9':[1920,1080], '9x16':[1080,1920], '1x1':[1080,1080], '4x5':[1080,1350]};
const q = new URLSearchParams(location.search);
L.fmt = q.get('fmt') || window.LEV_FMT || '16x9';
if(!L.FORMATS[L.fmt]) L.fmt = '16x9';
[L.W, L.H] = L.FORMATS[L.fmt];
L.portrait = L.H > L.W; L.square = L.W === L.H; L.wide = L.W > L.H;
/** Per-format value: {'16x9':a, '9x16':b, default:c}. 'tall' matches 9x16 and 4x5. */
L.pick = o => (L.fmt in o) ? o[L.fmt] : (L.H > L.W && 'tall' in o) ? o.tall : o.default;

// ------------------------------------------------------------------ time
L.seg = (t,a,b)=>M.clamp((t-a)/(b-a));
/** 0→1 spring step response starting at t0. */
L.sp = (t,t0,s=M.MORPH)=>M.S(t-t0,s[0],s[1]);
/** Eased 0→1 over [t0, t0+d]. */
L.ein = (t,t0,d=0.5)=>M.eo((t-t0)/d);
L.eio = (t,t0,d=0.5)=>M.eio((t-t0)/d);
/** Characters of `text` typed by time t at `cps` characters per second. */
L.typed = (text,t,t0,cps=30)=>text.slice(0,Math.max(0,Math.min(text.length,Math.floor((t-t0)*cps))));
L.typeEnd = (text,t0,cps=30)=>t0+text.length/cps;
L.count = (t,t0,t1,a,b)=>Math.round(M.lerp(a,b,M.eio(L.seg(t,t0,t1))));
/** Seeded PRNG so "random" layouts are identical on every frame and render. */
L.rng = seed=>()=>{seed|=0;seed=seed+0x6D2B79F5|0;let r=Math.imul(seed^seed>>>15,1|seed);r=r+Math.imul(r^r>>>7,61|r)^r;return((r^r>>>14)>>>0)/4294967296};

// ------------------------------------------------------------------ cues
/* One list, two consumers. The scene registers every sound it needs at load
   time with L.cue(); the audio builder reads window.LEV_CUES from the page, so
   picture and sound can never drift apart. */
const CUES = window.LEV_CUES = [];
L.cue = (t,sound,opts={})=>{CUES.push({t:+t.toFixed(4),sound,...opts}); return t;};
/** Typing cue helper: one key sound per visible character (spaces are quiet). */
L.cueTyping = (text,t0,cps=30,sound='key')=>{for(let i=0;i<text.length;i++) if(text[i]!==' ') L.cue(t0+(i+1)/cps,sound,{v:0.5+0.5*((i*7)%5)/5});};

// ------------------------------------------------------------------ elements
const $ = L.$ = id=>document.getElementById(id);
/** Show/hide with the engine's blur swap. Returns the vis object (or null if hidden). */
L.vis = (el,t,tin,tout,o={},extra='')=>{const v=M.vis(t,tin,tout,o); return M.apply(el,v,extra)?v:null;};
/** Mask-rise text: the element slides up out of its overflow-hidden parent. */
L.rise = (el,t,tin,tout=null,o={})=>{
  const a=tin==null?1:L.sp(t,tin+(o.delay||0),o.spring||[16,0.9]);
  const b=tout==null?0:M.eio((t-tout)/(o.lout||0.35));
  const y=(1-a)*(o.dy??105)+(-b*(o.dy??105)*0.6);
  el.style.transform=`translateY(${y.toFixed(2)}%)`;
  el.style.opacity=(M.clamp(a*1.4)*(1-b)).toFixed(4);
  return a*(1-b);
};
/** Position an absolutely-placed element by its centre, with scale. */
L.place = (el,x,y,s=1,extra='')=>{el.style.transform=`translate(${x.toFixed(2)}px,${y.toFixed(2)}px) translate(-50%,-50%) scale(${s.toFixed(5)})${extra}`;};

// ------------------------------------------------------------------ texture
/* RISE tells 4 and 10: no flat colour, no texture-free frames. A vignette gives
   light fall-off; grain is regenerated 12 times a second from a seed, so it
   looks alive but every frame renders identically on every pass. */
function grainTiles(n=6,size=256,seed=7){
  const r=L.rng(seed), tiles=[];
  for(let k=0;k<n;k++){
    const c=document.createElement('canvas'); c.width=c.height=size;
    const x=c.getContext('2d'), img=x.createImageData(size,size);
    for(let i=0;i<img.data.length;i+=4){const v=128+(r()+r()+r()-1.5)*110; img.data[i]=img.data[i+1]=img.data[i+2]=v; img.data[i+3]=255;}
    x.putImageData(img,0,0); tiles.push(c.toDataURL());
  }
  return tiles;
}

// ------------------------------------------------------------------ film
/**
 * L.film({ T, bg, render(t), grain:{amount,fps}, vignette, audio })
 * Sizes the stage to the format, installs texture, exposes window.seek(t) and
 * window.DURATION for the renderer, and in the browser plays a looping preview
 * with the soundtrack and a scrubber.
 */
L.film = cfg=>{
  const stage=$('stage'), wrap=$('wrap');
  stage.style.width=L.W+'px'; stage.style.height=L.H+'px'; wrap.style.width=L.W+'px'; wrap.style.height=L.H+'px';
  stage.style.background=cfg.bg||'#09090b';
  // ?nograin: GIF export. Per-frame grain defeats GIF's frame differencing and
  // multiplies the file size, so animated-image cuts render without it.
  const g=cfg.grain===false||q.has('nograin')?null:{amount:0.07,fps:12,...(cfg.grain||{})};
  let tiles=null, grain=null;
  if(g){tiles=grainTiles(); grain=document.createElement('div'); grain.id='lev-grain'; grain.style.opacity=g.amount; stage.appendChild(grain);}
  if(cfg.vignette!==0){const v=document.createElement('div'); v.id='lev-vignette'; v.style.opacity=cfg.vignette??0.55; stage.appendChild(v);}
  const seek=t=>{
    cfg.render(t);
    if(grain){const f=Math.floor(t*g.fps), r=L.rng(f*9973+1); grain.style.backgroundImage=`url(${tiles[f%tiles.length]})`; grain.style.backgroundPosition=`${Math.floor(r()*256)}px ${Math.floor(r()*256)}px`;}
  };
  window.seek=seek; window.DURATION=cfg.T; window.LEV_META={fmt:L.fmt,W:L.W,H:L.H,T:cfg.T};
  const RENDER=q.has('render');
  document.body.classList.add(RENDER?'render':'preview');
  seek(0);
  if(RENDER) return seek;

  // ---- preview player: fit, loop, scrub, sound, format switcher
  const fit=()=>{const k=Math.min(innerWidth/L.W,(innerHeight-64)/L.H);wrap.style.transform=`translate(-50%,-50%) scale(${k})`;};
  fit(); addEventListener('resize',fit);
  const bar=document.createElement('div'); bar.id='lev-bar';
  bar.innerHTML=`<button id="lev-play">Pause</button><input id="lev-scrub" type="range" min="0" max="${cfg.T}" step="0.01" value="0"><span id="lev-time">0.00</span>
    ${Object.keys(L.FORMATS).map(f=>`<a href="?fmt=${f}" class="${f===L.fmt?'on':''}">${f.replace('x',':')}</a>`).join('')}`;
  document.body.appendChild(bar);
  const audio=cfg.audio?new Audio(cfg.audio):null;
  let playing=true, t0=performance.now(), cur=0;
  const play=$('lev-play'), scrub=$('lev-scrub'), time=$('lev-time');
  const syncAudio=()=>{if(!audio) return; audio.currentTime=cur; if(playing) audio.play().catch(()=>{}); else audio.pause();};
  play.onclick=()=>{playing=!playing; play.textContent=playing?'Pause':'Play'; t0=performance.now()-cur*1000; syncAudio();};
  scrub.oninput=()=>{cur=+scrub.value; t0=performance.now()-cur*1000; seek(cur); time.textContent=cur.toFixed(2); if(audio) audio.currentTime=cur;};
  addEventListener('keydown',e=>{if(e.key===' '){e.preventDefault();play.onclick();}});
  const loop=()=>{
    if(playing){cur=(performance.now()-t0)/1000; if(cur>=cfg.T+0.6){t0=performance.now(); cur=0; if(audio){audio.currentTime=0;audio.play().catch(()=>{});}}
      seek(Math.min(cur,cfg.T)); scrub.value=cur; time.textContent=Math.min(cur,cfg.T).toFixed(2);}
    requestAnimationFrame(loop);
  };
  addEventListener('click',()=>{if(audio&&playing&&audio.paused){audio.currentTime=cur;audio.play().catch(()=>{});}},{once:true});
  requestAnimationFrame(loop);
  return seek;
};
})();
