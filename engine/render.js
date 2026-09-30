// Render a built scene to video, frame by frame, with motion blur.
//
//   NODE_PATH=motion/node_modules node render.js dist/film.html out/film-16x9.mp4 \
//     [--fmt 16x9] [--fps 30] [--audio out/soundtrack.wav] [--from 0] [--to T] [--sub 4] [--nograin]
//
// Each output frame blends `sub` sub-frames across a 180° shutter (ffmpeg tmix).
// With --audio the soundtrack is muxed in as AAC. Transparent scenes (bg null)
// are not supported here; use motion-broll's render for alpha panels.
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
const args=process.argv.slice(2);const opt=k=>{const i=args.indexOf('--'+k);return i>=0?args[i+1]:undefined;};
const [html,out]=args.filter((a,i)=>!a.startsWith('--')&&!(args[i-1]||'').startsWith('--'));
(async()=>{
  const fmt=opt('fmt')||'16x9', FPS=+(opt('fps')||30), K=+(opt('sub')||4), audio=opt('audio');
  const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1920}});
  const errs=[];p.on('pageerror',e=>errs.push(e.message));
  await p.goto('file://'+path.resolve(html)+'?render&fmt='+fmt+(args.includes('--nograin')?'&nograin':''));await p.evaluate(()=>document.fonts.ready);
  await p.waitForFunction(()=>[...document.images].every(i=>i.complete));
  const info=await p.evaluate(()=>window.LEV_META);
  await p.setViewportSize({width:info.W,height:info.H});
  const from=+(opt('from')||0), to=+(opt('to')||info.T), N=Math.round((to-from)*FPS), sub=1/(FPS*2*K);
  const silent=audio?out.replace(/\.mp4$/,'.silent.mp4'):out;
  const vf=`format=gbrp,tmix=frames=${K}:weights='${Array(K).fill(1).join(' ')}',select='eq(mod(n\\,${K})\\,${K-1})',setpts=N/(${FPS})/TB`;
  const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate',String(FPS*K),'-c:v','png','-i','-','-vf',vf,'-r',String(FPS),
    '-c:v','libx264','-crf','15','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',silent]);
  ff.stderr.on('data',d=>process.stderr.write(d));
  const t0=Date.now();
  for(let f=0;f<N;f++){
    for(let k=0;k<K;k++){const t=Math.max(0,from+f/FPS+(k-(K-1)/2)*sub);await p.evaluate(t=>seek(t),t);
      const buf=await p.screenshot({type:'png'});if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));}
    if(f%150===0) process.stdout.write(`\r${fmt} frame ${f}/${N} ${((Date.now()-t0)/1000).toFixed(0)}s`);
  }
  ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();
  if(audio){
    await new Promise((res,rej)=>{const m=spawn('ffmpeg',['-loglevel','error','-y','-i',silent,'-ss',String(from),'-t',String(to-from),'-i',audio,
      '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out]);m.on('close',c=>c===0?res():rej(new Error('mux failed')));});
    require('fs').unlinkSync(silent);
  }
  console.log(`\nrendered ${out} ${N} frames in ${((Date.now()-t0)/1000).toFixed(0)}s`,errs.length?'ERR '+errs[0]:'');
})();
