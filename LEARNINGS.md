# Learnings (append after every project; newest first)

## 2026-10-01 · L-evate's own film (41 s, 16:9 + 9:16, README GIF)
- **A tool explaining itself: use its own past output as the References.** The sound beat draws the devLaunchr film's real waveform (RMS/peak envelope at 40 pts/s from its MP4) under that film's real `L.cue` times from `examples/devlaunchr-launch.html`; the markers land on real transients. The Examine beat is a real stills.js-style sheet (3 columns, white 6 px padding) of the devLaunchr film at 0/25/50/75/100%.
- **Data in a fragment**: build.py only inlines the fragment, so measured data (the envelope JSON) is written into the scene once, replacing a `/*@env*/null` marker.
- **Cursor CSS trap**: `#cursor{display:none}` in the scene CSS plus `style.display=''` in JS means the cursor never appears. If any beat uses the cursor, hide it from JS only.
- **Dense cue markers**: labels collide when cues are <0.6 s apart on a narrow lane; alternate labels above/below the lane and give the card bottom padding for them.
- **Demo a pure function by scrubbing backwards**: the cursor drags the scrubber back and the frame matches; it shows `seek(t)` purity better than any caption.
- Render time on this 8-core Mac: 41 s × 30 fps × 4 sub-frames, 16:9 and 9:16 in parallel, ~14–15 min. GIF cut (12 fps, `--sub 1 --nograin`) took 25 s and came to 6.1 MB at 1280 px.
- This ffmpeg build has no libwebp; Pillow writes the WebP posters.

## 2026-10-01 · Salesman Solutions desktop batch 2 (The Middle · On the GRID · The Sound of the Work, time-lapses + user music)
- **Cut to the track's structure, not just its BPM.** Kick-band envelope (35–150 Hz, 200 ms smoothing) crossing ~14 dB under its 95th percentile gives clean IN/OUT section events. "Ticking Clock" is stop-start, so the time-lapses *run while the kick runs and freeze when it drops*; DONE stamps fill the gaps. Autocorrelation and grid fits drift to double-time: check the inter-onset histogram (0.31/0.62 s pairs = eighths/quarters) and constrain the search window; plot envelope + grid (`tools/gridplot.py`) to confirm by eye.
- **Key-match the sonic logo.** Chroma vs Krumhansl profiles: E major → jingle E5 B5 E6; C major → C5 G5 C6.
- **User music as a bed**: decode, place, fade, and sum *before* `master()` with the synth cues (accents at ~0.6 of their PEAK) and clip foley (~0.25). Whisper with VAD confirmed every track instrumental before laying supers over them.
- **Brand grade in numpy**: monochrome S-curve plus a hue/saturation mask (85–165°, sat 0.13–0.24) limited to the floor (rows below a per-clip fraction) pulls the crew's muted green tape to #3CE04B and keeps palms grey. ffmpeg `colorhold` on the brand hex killed the real tape.
- **8 GB machines**: grading 3 clips × 6 processes of float64 1080p frames got the job (and the app) killed. Grade one source at a time, 3 workers, float32.
- **A foley graph ran away and filled the disk** (85 GB WAV): `amix → apad → atrim=duration` never terminated with one odd input. Always give ffmpeg hard output stops (`-t T -fs 64M`) and pad with `apad=whole_dur`.
- **Freeze on sharp frames**: Laplacian variance per frame (`tools/sharpness.py`) picks freeze points and finds smeared passes (a worker crossing the lens); `skip` ranges step over them inside a time-lapse.
- **Knockout type**: `clip-path:url(#clip)` on the footage `<img>`, with an SVG `<clipPath>` holding `<text>`; brighten the clipped footage (`brightness(1.35)`) and add a 2 px white outline or dark letters vanish on black.
- **One scope**: build.py joins every `<script>` block, so shared kit constants (e.g. `NS`) collide with scene declarations, and a `//` comment inside a one-line function swallows its closing brace. `tools/errors.js` prints the page error when `LEV_META` is undefined.
- **Map illustration**: a schematic transit line (stations on kick hits, eased legs) on CSS grid paper; plan dashed white ahead, `pathLength=1` green dasharray behind the marker. Tight station spacing (380 px) keeps windows on screen long enough to play; label plates must sit above windows.

## 2026-10-01 · Salesman Solutions commercials (Nobody Claps 16:9 · Opening Night 9:16, over Higgsfield footage)
- **Footage plates without the Astra helpers**: one `<img>` per film, src swapped to `work/frames/<film>/<fmt>/<shot>/NNNN.jpg` by t, and `window.FRAMES_READY = () => img.decode()`. Copies of `stills.js`/`render.js` await it after every seek; JPEG q93 × 3 sub-frames at 24 fps (match the source) rendered 720 frames in ~3 min, two films in parallel on 8 cores. Project copy: `SalesmanSolutions/motion/tools/`.
- **One timeline for picture, frames and foley**: the scene publishes `window.LEV_SHOTS` (id, source in, dur, at); `stills.js` dumps it next to the cues; `footage.py` cuts plate frames and lays each clip's own sound at its cut. Change a trim in the scene and everything downstream follows.
- **Mix foley under the synth score before mastering** (`tools/mix.py` imports `audio.py`'s `mix`/`master`), so the limiter sees the real mix: −16.3 LUFS, −1.3 dBFS peak.
- **Lines on real edges**: measure on frames extracted with the exact plate filter (`scale=…:force_original_aspect_ratio=increase,crop=W:H`), and put lines and the plate inside one `#world` div so a slow push-in keeps them locked. For a plate that pushes in on its own, measure the edge at 2–3 times and interpolate.
- **Odometer digits must only roll forward**: 5:52 → 6:00 rolled 5→0 backwards through "42". Unroll each digit's targets into monotonic positions (`prev + (d - prev%10 + 10) % 10`) on a multi-cycle reel.
- **Engine cursor**: build.py always injects `#cursor`; `L.film` scenes without a cursor need `#cursor{display:none}`.
- **Shared code**: `build.py` only reads one fragment. `tools/build.py` expands `/*@include path*/` and hands the engine a duck-typed source (`stem`, `parent`, `read_text`).
- **Logo blueprint**: `potrace -a 0` on the official logo PNG gives exact polygons; each edge as an SVG line with `pathLength=1` draws on, then the fill lands. One `key` cue per edge sounds like a plotter.
- **Payoff text vs. a pushing plate**: a lower-third that cleared the subject on frame 1 collided with the white shelf by the last frame. Check the last frame of every shot, not only the middle.

## 2026-09-28 · Astra vs Opus 5.5 (screen-recording edit, 18:02 → 6:56 + 0:57 vertical)
- **Real video inside a scene**: feed footage as a JPEG sequence (`FR.layer`) and have the renderer `await FRAMES_READY()` (img.decode) after each `seek(t)`. Masks, 3D tilts, shadows and captions then wrap live footage, and one opaque MP4 per chapter replaces giant alpha ProRes + ffmpeg overlay graphs. Project copy: `GPt Astra VS  Opus.5.5/motion/scenes/shared/shared.js`, `engine/render.js`.
- **Render speed**: JPEG screenshots (q≈93) + 3 sub-frames ran ~6× faster than PNG × 4 with no visible loss (0.15 s/frame solo, ~1 s/frame with 6 jobs on 8 cores). Frame-align chapter lengths (`round(end·30) − round(start·30)`) so concatenated chapters never drift from the voice.
- **Privacy on screen recordings**: never trust a time range. Classify every frame (Chrome tab-strip colour → "fullscreen site" only), exclude overlay/tab-switch frames and foreign tabs, crop to the viewport, and look for floating widgets, account dropdowns and other projects' images inside "safe" pages (Higgsfield showed username/plan/credits and other work within seconds of the right assets).
- **Voice cutting from Whisper**: word times drift ~0.4 s and plosive closures read as pauses. Snap with a median-smoothed envelope: onset = end of last ≥50 ms quiet run; offset = first ≥200 ms quiet run after the last word *sounds* (anchor on Whisper's word end when plausible, <1.2 s). Re-transcribe the cut with a disfluency prompt and slice-transcribe any doubt: it caught real stutters ("it- it", "what- what") and an "um" Whisper had labelled "model".
- **Webcam in a dark room** is lit only by the screen: measure cam luminance per 10 s and show the cam only where it is readable; grade with curves (lift mids, keep blacks) rather than gamma, which washes the room grey.
- **Engine gotcha**: elements created with `mk('div')` are in-flow blocks; `L.place` then centres them on the full stage width. Give every placed element `position:absolute`.

## 2026-09-27 · GitHub README demo
- GitHub only plays video uploaded through its web editor (user-attachments). An MP4 committed to the repo is not embedded. For a README, use an animated GIF, or have the user drag the MP4 into the README editor for a player with sound.
- Render GIF cuts with `render.js --fps 12 --sub 1 --nograin` (grain regenerated every frame defeats GIF frame differencing). 23 s at 1280 px came to 4.6 MB instead of tens of MB. Convert with `palettegen=stats_mode=diff` and `paletteuse=diff_mode=rectangle`.
- Start the cut on a settled, readable frame: it doubles as the poster image and is what reduced-motion viewers see.
- Social stills: capture with a generic home such as `/Users/Shared/demo`, so log lines don't show temp-folder paths or a username. Check Ports-style panels for real processes before posting.

## 2026-09-27 · devLaunchr launch film (first project)
- **Harness focus.** A capture window that takes focus receives the user's keystrokes as menu shortcuts (⌘K, ⌘⇧O fired "randomly"). Patch `BrowserWindow.prototype.show = showInactive` and `setFocusable(false)`.
- **Real before/after beats mock-ups.** Two screenshots of the same view, before and after one action, plus DOM rects × DPR. Crossfade only inside the element's rect (`clip-path: inset(... round r)`). Crop sprites out of the "after" image for stamp animations.
- **Screen-blending neon art on black** hides dark strokes (the logo's black "D" vanished). Use the product's real app icon instead.
- **Audio mixing bugs seen:** (1) an un-normalised reverb impulse response gave about 88× gain, turning the whole mix into a wall. Normalise the IR to unit energy. (2) Peak-normalising the whole mix lets one jingle bury every click. Level each voice explicitly, then master to a LUFS target with a limiter. `loudnorm` in linear mode falls back to dynamic mode when true-peak blocks the gain, which squashes transients.
- **Layering voices** of different lengths needs a padding sum (`layer()`).
- **Verify copy against source.** The film caught an overclaim in the app itself ("starts on its own after install" was false for a manual install).
- **Scene hygiene.** Every element hides outside its time window. End-card text sat at (0,0) on every frame until it was hidden.
- Render speed: 1920×1080 at 30 fps × 4 sub-frames is roughly real-time × 10 on 8 cores. Render formats in parallel.
