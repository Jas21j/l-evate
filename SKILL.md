---
name: l-evate
description: Make launch films, product explainers and social cuts as motion graphics drawn in code, with a soundtrack synthesised from the same timeline. Merges the RISE method (References, Idea, Style, Examine) with the motion-broll engine (pure seek(t), closed-form springs, sub-frame motion blur) and adds multi-format recomposition, cue-driven audio, film texture and real-screenshot references. Use when asked for a motion graphic, launch video, promo, explainer, animated demo, social cut, or jingle for a product.
---

# L-evate

One `render(t)` function draws every frame. The same file registers every
sound with `L.cue()`, so picture and sound cannot drift. One page renders to
16:9, 9:16, 1:1 and 4:5 by recomposing, never cropping.

`$SKILL` = this folder. Work in a `motion/` (or `marketing/<film>/`) folder in the user's project.

## 0. Setup (once per project)

```bash
mkdir -p motion/{scenes/assets,dist,out,work} && cd motion
echo '{"private":true}' > package.json && npm install playwright && npx playwright install chromium
```
Needs Node 18+, Python 3 with numpy, ffmpeg (libx264, aac).

## 1. R: References (never draw from memory)

- **Brand**: take the product's own tokens (colours, fonts, logo) from its code, or pull a site's with Firecrawl `formats:["branding"]` (`scripts/brand.sh`). Use the real logo or app icon file. Never redraw a logo.
- **Product**: capture real screenshots from the running product. For an Electron app, boot the built main process in a harness with a throwaway `userData`/`home`, seeded fixtures and `setVersion()`, and never let its window take focus (see LEARNINGS). Capture **before/after pairs of the same view** plus `getBoundingClientRect()` rects × DPR. A masked crossfade between them is a real state change, not a mock.
- **Facts**: only show numbers you measured or the user supplied. Measure them (test counts, scan times) when you can. Use the product's own copy for any UI you redraw, and grep the source to confirm it.

## 2. I: Idea (one arc, one change per beat)

Write a beat table before code: `time | headline | visual | the one change | sound`.
- Launch film (30–45s): problem → mark → 4–6 capability beats → end card with URL.
- Loop (8–12s): beginning, one change, and an end that lands exactly on the first frame.
- Hold every line of text ≥1.2s (≥1.4s for headlines). Put a sound on every change.

## 3. S: Style

State it in one line: ground, ink, one accent, font, texture, pace, and what moves first.
Defaults: the product's own dark surface, film grain (`grain`), vignette light fall-off, spring motion (`M.MORPH/FAST/SLOW`), mask-rise headlines, the cursor drives every UI change, and the accent stays under ~10% of the frame.
Banned: invented features or numbers, fake logos, linear motion, flat fills, particle/glow soup, template look.

## 4. Build

Write `scenes/<name>.html` (a fragment) plus `scenes/assets/`. Skeleton:

```html
<title>…</title><style>…</style>
<div data-slot="stage"> …elements… </div><!--/stage-->
<script>
const LAY=L.pick({'16x9':{…}, tall:{…}, default:{…}});   // recompose per format
const K={intro:0.4, click:2.1, …};                        // the timeline, in seconds
L.cue(K.click,'click'); L.cue(K.click+0.5,'ding');        // sound lives next to picture
L.cueTyping('npm run dev', 1.0, 30);                      // one key sound per character
L.film({T:10, bg:'#09090b', audio:'assets/soundtrack.wav', grain:{amount:0.07}, vignette:0.6,
  render:t=>{ /* pure function of t: set styles only */ }});
</script>
```
Runtime (`engine/lev.js`, on top of `engine/motion.js`): `L.pick`, `L.seg`, `L.sp` (spring 0→1), `L.typed`, `L.count`, `L.rng` (seeded), `L.rise` (mask-rise text), `L.place`, `L.cue`, `L.cueTyping`, `L.film`. The engine's `M.track`, `M.ctrack`, `M.vis/apply`, `M.path`, `M.presses` all work. See `reference/engine-api.md` (motion-broll) for patterns.

```bash
python3 $SKILL/engine/build.py dist scenes/<name>.html          # self-contained page + assets
open "dist/<name>.html?fmt=9x16"                                  # preview with scrubber and sound
```

## 5. E: Examine (before rendering video)

```bash
NODE_PATH=./node_modules node $SKILL/engine/stills.js dist/<name>.html work/check.png --fmt 16x9        # 0/25/50/75/100%
NODE_PATH=./node_modules node $SKILL/engine/stills.js dist/<name>.html work/beats.png --fmt 9x16 2.1 2.6 …
```
Look at every sheet, in every format. Check the ten tells in `reference/checklist.md`, fix, and look again.

## 6. Sound

`stills.js` writes `<out>.cues.json` from the page. Then:
```bash
python3 $SKILL/engine/audio.py work/check.cues.json scenes/assets/soundtrack.wav --T 42 [--loop]
```
Voices: key, click, tick, pop, thud, whoosh(_in/_out), sub, ding, blip_down, swell, jingle `{notes,step,big}`, chord `{chord,until}`, drone `{until}`. Every voice is levelled explicitly (`PEAK`/`RMS` tables), then mastered to −16 LUFS with a look-ahead limiter. Check it with `ffmpeg -af ebur128` and a `showwavespic` image. Use `--loop` for loops: it folds the tail onto the start.

## 7. Render

```bash
NODE_PATH=./node_modules node $SKILL/engine/render.js dist/<name>.html out/<name>-16x9.mp4 --fmt 16x9 --fps 30 --audio dist/assets/soundtrack.wav
```
Four sub-frames per frame (180° shutter) are blended into motion blur. Formats render in parallel on a multi-core machine. For transparent overlay panels, use motion-broll's own `render.js` (ProRes 4444).

## Files

- `engine/motion.js`: motion-broll engine (MIT), unchanged.
- `engine/lev.js`: film runtime (formats, cues, texture, preview player).
- `engine/build.py`, `render.js`, `stills.js`, `audio.py`, `base.css`, `fonts/` (Geist, Geist Mono, DM Sans; OFL).
- `reference/checklist.md`: the ten tells and five-frame check.
- `LEARNINGS.md`: **read it first and append to it after every project.**
- `examples/`: finished films to use as a quality bar.
- `CREDITS.md`: sources and licences.
