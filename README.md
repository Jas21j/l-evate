# L-evate

Motion graphics, drawn in code. L-evate is a [Claude Code](https://claude.com/claude-code) skill for launch films, product explainers, and social cuts. One `render(t)` function draws every frame, and the soundtrack is synthesised from the same cue list, so picture and sound cannot drift. One page renders to 16:9, 9:16, 1:1, and 4:5 by recomposing, never cropping.

[![The L-evate film: one function draws every frame, sound from the same timeline, every format recomposed](media/l-evate.gif)](media/l-evate-16x9.mp4)

The film above was made with L-evate, about L-evate. Watch it with sound: [16:9 MP4](media/l-evate-16x9.mp4) · [9:16 MP4](media/l-evate-9x16.mp4). Its scene source is in [`examples/l-evate-film`](examples/l-evate-film), and it builds and renders with the commands below.

L-evate was first built for the [devLaunchr](https://github.com/Jas21j/devlaunchr) launch film. See both films, and the method behind them, at [salesmansolutions.net/public-works/l-evate](https://www.salesmansolutions.net/public-works/l-evate).

## What it does

- **RISE method**: References (real brand tokens, logos, and screenshots), Idea (one change per beat), Style (one accent, springs, grain), Examine (stills at every quarter, in every format, before rendering).
- **Pure functions of time**: closed-form springs (`M.MORPH`, `M.FAST`, `M.SLOW`), mask-rise headlines, seeded randomness, and a cursor that drives every UI change.
- **Sound from the same timeline**: scenes register cues with `L.cue()`; `audio.py` synthesises every voice from sines and filtered noise, levels each one, and masters to −16 LUFS.
- **Render**: Playwright captures four sub-frames per frame (180° shutter) and ffmpeg blends them into motion blur.

## How it changes the workflow

Because the film is text, a change is an edit rather than a re-export. Move one time in the timeline and the picture, the sound, and every format follow it.

| Step | File | What it removes |
| --- | --- | --- |
| Brief | `SKILL.md` | Starting from a blank timeline. Claude writes a beat table first, then the scene. |
| Build | `engine/build.py` | Separate projects per aspect ratio. One page opens as 16:9, 9:16, 1:1, or 4:5. |
| Examine | `engine/stills.js` | Finding a clipped headline after a long render. Stills at every quarter, in every format, come first. |
| Sound | `engine/audio.py` | Stock music licences and syncing by hand. Every sound is synthesised from the cue list. |
| Render | `engine/render.js` | Choppy motion. Four sub-frames per frame become motion blur; formats render in parallel. |
| Learn | `LEARNINGS.md` | Repeating mistakes. Each project appends notes that Claude reads before the next one. |

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
- `examples/l-evate-film/`: the scene for the film above, with its five reference stills. Build it, then run `audio.py` on the cues from `stills.js` to regenerate `assets/soundtrack.wav` (41 s) before rendering.
- `examples/devlaunchr-launch.html`: the scene source for the devLaunchr film. Its screenshots and soundtrack are not included, so it is a reference rather than a buildable example.
- `LEARNINGS.md`: notes from each project, newest first.
- `media/`: the L-evate film as MP4 (16:9, 9:16) and the README GIF.

Not included yet: the `scripts/brand.sh` helper mentioned in `SKILL.md`. Pull a site's brand tokens with Firecrawl's `branding` format directly. The engine API reference lives in the [motion-broll](https://github.com/Barty-Bart/motion-graphics) repository.

## Credits

- [motion-broll](https://github.com/Barty-Bart/motion-graphics) by Bart (MIT). `engine/motion.js` is used unchanged; the render and stills approach is adapted.
- The RISE method by Jack Roberts, "Motion, drawn in code". The structure, five-frame check, and ten tells are summarised in our own words.
- Geist and Geist Mono (SIL OFL 1.1, Vercel). DM Sans (SIL OFL 1.1, The DM Sans Project Authors).

## License

MIT for L-evate's own files. See `LICENSE`, `LICENSE-motion-broll.txt`, and the font licences in `engine/fonts`.
