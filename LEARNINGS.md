# Learnings (append after every project; newest first)

## 2026-09-28 · Astra vs Opus 5.5 (screen-recording edit, 18:02 → 6:56 + 0:57 vertical)
- **Real video inside a scene**: feed footage as a JPEG sequence (`FR.layer`) and have the renderer `await FRAMES_READY()` (img.decode) after each `seek(t)`. Masks, 3D tilts, shadows and captions then wrap live footage, and one opaque MP4 per chapter replaces giant alpha ProRes + ffmpeg overlay graphs.
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
