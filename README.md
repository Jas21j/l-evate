# L-evate

Motion graphics, drawn in code. L-evate is a [Claude Code](https://claude.com/claude-code) skill for launch films, product explainers, and social cuts. One `render(t)` function draws every frame, and the soundtrack is synthesised from the same cue list, so picture and sound cannot drift. One page renders to 16:9, 9:16, 1:1, and 4:5 by recomposing, never cropping.

It was built for the [devLaunchr](https://github.com/Jas21j/devlaunchr) launch film. See it, and the method behind it, at [salesmansolutions.net/public-works/l-evate](https://www.salesmansolutions.net/public-works/l-evate).

## What it does

- **RISE method**: References (real brand tokens, logos, and screenshots), Idea (one change per beat), Style (one accent, springs, grain), Examine (stills at every quarter, in every format, before rendering).
- **Pure functions of time**: closed-form springs (`M.MORPH`, `M.FAST`, `M.SLOW`), mask-rise headlines, seeded randomness, and a cursor that drives every UI change.
- **Sound from the same timeline**: scenes register cues with `L.cue()`; `audio.py` synthesises every voice from sines and filtered noise, levels each one, and masters to −16 LUFS.
- **Render**: Playwright captures four sub-frames per frame (180° shutter) and ffmpeg blends them into motion blur.

## Install

Copy this folder into your Claude Code skills directory, for example `~/.claude/skills/l-evate`, then ask Claude for a launch film, explainer, or social cut. `SKILL.md` holds the full workflow; read `LEARNINGS.md` before a new project.

Requirements: Node 18+, Playwright with Chromium, Python 3 with NumPy, and ffmpeg (libx264, AAC).

## Quick start

```bash
mkdir -p motion/{scenes/assets,dist,out,work} && cd motion
echo '{"private":true}' > package.json && npm install playwright && npx playwright install chromium
python3 $SKILL/engine/build.py dist scenes/<name>.html
NODE_PATH=./node_modules node $SKILL/engine/stills.js dist/<name>.html work/check.png --fmt 16x9
python3 $SKILL/engine/audio.py work/check.cues.json scenes/assets/soundtrack.wav --T 42
NODE_PATH=./node_modules node $SKILL/engine/render.js dist/<name>.html out/<name>-16x9.mp4 --fmt 16x9 --audio dist/assets/soundtrack.wav
```

`$SKILL` is the path to this folder.

## Layout

- `SKILL.md`: the workflow Claude follows.
- `engine/`: `motion.js` (motion-broll engine, unchanged), `lev.js` (film runtime), `build.py`, `stills.js`, `render.js`, `audio.py`, `base.css`, and fonts.
- `reference/checklist.md`: the ten tells and the five-frame check.
- `examples/devlaunchr-launch.html`: the scene source for the devLaunchr film. Its screenshots and soundtrack are not included, so it is a reference rather than a buildable example.
- `LEARNINGS.md`: notes from each project, newest first.

Not included yet: the `scripts/brand.sh` helper mentioned in `SKILL.md`. Pull a site's brand tokens with Firecrawl's `branding` format directly. The engine API reference lives in the [motion-broll](https://github.com/Barty-Bart/motion-graphics) repository.

## Credits

- [motion-broll](https://github.com/Barty-Bart/motion-graphics) by Bart (MIT). `engine/motion.js` is used unchanged; the render and stills approach is adapted.
- The RISE method by Jack Roberts, "Motion, drawn in code". The structure, five-frame check, and ten tells are summarised in our own words.
- Geist and Geist Mono (SIL OFL 1.1, Vercel). DM Sans (SIL OFL 1.1, The DM Sans Project Authors).

## License

MIT for L-evate's own files. See `LICENSE`, `LICENSE-motion-broll.txt`, and the font licences in `engine/fonts`.
