// The E in RISE: render stills and look at them before rendering video.
//
//   NODE_PATH=motion/node_modules node stills.js dist/film.html out/check.png [--fmt 16x9] [t1 t2 …]
//
// With no times it renders the five checkpoints: 0%, 25%, 50%, 75%, 100%.
// Also dumps the page's cue list to <out>.cues.json, which audio.py reads.
const {chromium}=require('playwright');const path=require('path');const fs=require('fs');const {execFileSync}=require('child_process');
const args=process.argv.slice(2);const fi=args.indexOf('--fmt');const fmt=fi>=0?args[fi+1]:'16x9';
const rest=args.filter((a,i)=>a!=='--fmt'&&args[i-1]!=='--fmt');const [html,out,...ts]=rest;
(async()=>{
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.resolve(html)+'?render&fmt='+fmt);await p.evaluate(()=>document.fonts.ready);
  await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
  const info=await p.evaluate(()=>window.LEV_META);await p.setViewportSize({width:info.W,height:info.H});
  const times=ts.length?ts.map(Number):[0,0.25,0.5,0.75,1].map(u=>+(u*info.T).toFixed(3));
  const dir=fs.mkdtempSync('/tmp/lev-stills-');
  for(let i=0;i<times.length;i++){await p.evaluate(t=>seek(t),times[i]);await p.screenshot({path:`${dir}/${String(i).padStart(3,'0')}.png`});}
  fs.writeFileSync(out.replace(/\.png$/,'.cues.json'),JSON.stringify(await p.evaluate(()=>window.LEV_CUES),null,1));
  await b.close();
  const cols=Math.min(info.W>info.H?3:5,times.length),rows=Math.ceil(times.length/cols),w=info.W>info.H?800:432;
  execFileSync('ffmpeg',['-loglevel','error','-y','-i',`${dir}/%03d.png`,'-vf',`scale=${w}:-1,tile=${cols}x${rows}:padding=6:color=white`,'-frames:v','1',out]);
  console.log('stills',out,times.join(' '),errs.length?'ERR '+errs.join(' | '):'');
})();
