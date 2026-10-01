---
name: l-evate
description: Create exceptional launch films, product explainers, branded motion systems, social cuts, visual essays, interface films, cinematic promos, and experimental motion graphics drawn in code. L-evate provides a deterministic rendering engine, real-product grounding, synchronized sound, multi-format recomposition, and an examination loop — but the creative direction is intentionally open. Use when asked to make motion graphics, launch videos, promos, explainers, animated demos, social cuts, showreels, kinetic typography, product films, or experimental branded motion.
---

# L-evate

L-evate is a creative motion system, not a style template.

Its job is to provide a reliable technical instrument while preserving maximum creative authorship for whatever model, agent, or human is driving it.

One `render(t)` function draws every frame. The same file may register sound with `L.cue()`, so picture and sound can remain synchronized. A single scene may render to 16:9, 9:16, 1:1, and 4:5 through true recomposition rather than simple cropping.

`$SKILL` = this folder. Work in a `motion/` or `marketing/<film>/` directory inside the user's project.

---

## 0. Creative doctrine

Do not begin by imitating previous L-evate films.

Begin by understanding the product, brand, audience, objective, and available material. Then invent the strongest visual solution for this specific project.

The creator has unrestricted authorship over:

- visual concept;
- story structure;
- composition;
- pacing;
- transition language;
- camera logic;
- typography;
- hierarchy;
- color behavior;
- texture;
- dimensionality;
- rhythm;
- visual metaphors;
- sound design;
- scene density;
- interface treatment;
- degree of abstraction;
- use of real product footage;
- use of live-action or generated assets when the project permits them;
- the balance between UI, typography, symbols, diagrams, environments, data, imagery, and pure motion.

L-evate should not force a recognizable "L-evate look."

The quality bar is:

> Make the strongest piece that could reasonably exist for this product and objective, using the available evidence, assets, runtime, and time.

The engine is a capability layer. Creative direction is not owned by the framework.

---

## 0A. Model-agnostic execution

L-evate is model-agnostic.

Do not assume:
- Claude;
- Sonnet;
- Opus;
- GPT;
- Gemini;
- a specific coding agent;
- hidden chain-of-thought;
- browser access;
- terminal access;
- web research;
- image generation;
- video generation;
- MCP;
- a specific IDE;
- a specific orchestration framework.

Use whatever capabilities are actually available.

A text-only model can:
- design the concept;
- write the beat architecture;
- produce scene code;
- specify assets;
- create implementation instructions.

A coding agent can additionally:
- inspect repositories;
- run the product;
- capture screenshots;
- generate and modify files;
- render previews;
- inspect failures;
- iterate autonomously.

A multimodal model can additionally:
- critique frames;
- compare references;
- reason about composition;
- inspect screenshots, footage, and renders.

A tool-rich agent can additionally:
- research;
- source permitted assets;
- measure UI;
- render;
- test;
- revise;
- extend the engine.

The absence of one capability should change the workflow, not lower the ambition. Substitute the strongest available method and make unsupported assumptions explicit.

Never rely on a model-specific prompting trick as part of the core method. The skill should remain intelligible and executable across present and future model families.


---

## 1. Hard constraints vs creative choices

### Hard constraints

These protect truth, reproducibility, usability, and rendering integrity.

- Do not invent product features, claims, customer results, benchmark numbers, interfaces, or logos and present them as real.
- Use actual brand assets when they exist.
- Prefer real product screenshots, recordings, DOM measurements, or source-backed UI over fabricated representations when demonstrating actual product behavior.
- Clearly distinguish conceptual / illustrative visuals from literal product UI.
- Keep each frame valid when seeked directly at time `t`.
- Ensure critical text is readable long enough for the intended viewing context.
- Inspect output before final render.
- Verify all requested formats.
- Preserve audio/video sync.
- Do not expose private information, credentials, unrelated user content, or sensitive data from captures.
- Do not claim a metric unless it is supplied or measured.
- Do not silently crop a composition designed for another aspect ratio when recomposition is practical.

### Creative choices

These are **not rules**. Choose them only when they serve the concept.

- dark or light backgrounds;
- one accent or many;
- grain or pristine rendering;
- vignette or no vignette;
- springs, easing, linear motion, stepped motion, ballistic motion, simulation, procedural motion, or stillness;
- cursor-driven UI;
- mask-rise typography;
- quiet layouts;
- dense layouts;
- flat graphics;
- dimensional graphics;
- 2D, 2.5D, faux-3D, CSS 3D, canvas, SVG, DOM, image sequences, video plates, or mixtures;
- realistic product demo;
- abstract visual metaphor;
- cinematic storytelling;
- kinetic typography;
- infographic logic;
- editorial design;
- brutalist motion;
- restrained enterprise motion;
- playful motion;
- high-energy showreel pacing;
- ambient pacing;
- continuous camera movement;
- hard cuts;
- morphs;
- wipes;
- match cuts;
- object transformations;
- split screens;
- spatial transitions;
- repeated motifs;
- visual chaos followed by order;
- any other coherent visual language the model can implement reliably.

Previous examples are references, not templates.

---

## 2. Creative modes

Creative modes are optional lenses, not gates. Use, combine, ignore, or invent modes as the brief demands. Never force a project into a preset simply because a preset exists.

### OPEN mode — default

Maximum creative authorship.

Use when the user asks for:
- best possible launch film;
- showreel-quality work;
- "push it";
- premium motion;
- an original campaign;
- an immersive product film;
- an experimental or cinematic piece.

In OPEN mode:
- explore multiple substantially different visual directions before committing when the available model/tooling supports exploration;
- do not inherit prior L-evate scene grammar unless it is clearly the strongest answer;
- allow composition, typography, palette, transitions, and pacing to emerge from the project;
- use capabilities beyond the documented examples whenever they improve the result;
- write or generate helper functions, project-local rendering utilities, shaders, procedural systems, simulations, layout engines, or other supporting code when useful.

### BRAND mode

Creative freedom inside an existing design system.

Use when:
- the product already has strong visual language;
- brand fidelity matters more than stylistic novelty.

Extract:
- color;
- type;
- spacing;
- iconography;
- logo behavior;
- interaction style;
- imagery;
- voice;
- product geometry.

Then extend that language into motion rather than replacing it.

### DEMO mode

Clarity of product behavior comes first.

Use:
- real screenshots;
- screen recordings;
- measured rects;
- precise focus;
- camera crops;
- callouts;
- state changes;
- UI choreography.

Visual invention should make the product easier to understand, not obscure it.

### HOUSE mode

Only use when the user explicitly wants the established L-evate aesthetic or a prior project's style.

HOUSE mode may use:
- restrained accent colors;
- spring motion;
- mask-rise type;
- cursor-led interaction;
- film grain;
- vignette;
- quiet backgrounds;
- familiar L-evate scene grammar.

These are a preset, not the default.

---

## 3. R: References — understand before designing

References are evidence and creative fuel, not shackles.

Study:

### Brand
- source tokens;
- CSS variables;
- fonts;
- icons;
- logo assets;
- illustrations;
- photography;
- product screenshots;
- website;
- marketing language;
- prior campaigns.

### Product
Capture or inspect the real product when possible.

For web:
- browser screenshots;
- DOM geometry;
- interaction states;
- before/after states;
- component behavior.

For desktop:
- controlled harness;
- seeded fixtures;
- safe temporary user data;
- non-focus-stealing capture;
- real UI state.

For video or live-action:
- identify strong usable moments;
- inspect sharpness;
- inspect camera movement;
- preserve continuity;
- protect privacy.

### Competitive / cultural reference
When appropriate, study:
- film titles;
- broadcast packages;
- premium product launches;
- architecture;
- editorial motion;
- music videos;
- game UI;
- industrial visualization;
- scientific visualization;
- title sequences;
- luxury advertising;
- interface cinema;
- motion identity systems.

Do not copy a reference literally. Extract principles.

### Facts
Verify:
- product claims;
- UI copy;
- metrics;
- supported platforms;
- performance claims;
- pricing;
- feature names.

---

## 4. I: Idea — find the strongest organizing concept

Do not force every film into the same arc.

Possible structures include:

- problem → transformation → proof;
- cold open → escalation → reveal;
- one continuous transformation;
- a visual metaphor that evolves;
- product walkthrough;
- parallel worlds;
- before/after;
- countdown;
- journey through a system;
- zoom from macro to micro;
- information cascade;
- object assembly;
- reverse engineering;
- spatial tour;
- manifesto;
- rhythmic montage;
- single-take illusion;
- chaptered showreel;
- narrative scene;
- visual argument;
- pure sensory brand film.

Before coding, define:

`time | purpose | visual idea | change | sound | evidence/source`

The beat table is a planning tool, not a requirement that every beat contain only one visual change.

Multiple simultaneous changes are allowed when they are intentional, legible, and rhythmically controlled.

Interrogate the concept with questions such as:

- What is the most memorable visual idea here?
- What could only this product say?
- What visual metaphor makes the value instantly understandable?
- What can move, transform, assemble, fracture, reveal, accelerate, or reorganize?
- Where should the film surprise the viewer?
- What should remain still?
- What deserves scale?
- What can be demonstrated instead of explained?
- What visual payoff justifies the setup?

---

## 5. S: Style — invent, don't inherit

State the chosen visual language in one concise paragraph before implementation.

Include only what actually matters:
- spatial logic;
- palette;
- typography;
- texture;
- dimensionality;
- motion behavior;
- camera behavior;
- compositional density;
- imagery;
- sound character.

Do not default to:
- dark background;
- one accent;
- vignette;
- grain;
- springs;
- cursor;
- mask-rise headlines.

Use those only if they improve the project.

A strong style may contain contradictions:
- pristine UI inside rough live-action;
- brutal typography over elegant product imagery;
- silent stillness followed by violent acceleration;
- dense data visualization with minimal copy;
- bright daylight with severe black type;
- photoreal product footage interrupted by abstract diagrams.

Coherence matters more than conformity.

---

## 6. Build

Create `scenes/<name>.html` plus assets as needed.

Minimal skeleton:

```html
<title>…</title>
<style>…</style>

<div data-slot="stage">
  …
</div><!--/stage-->

<script>
const K = { … };

L.film({
  T: 10,
  render: t => {
    // The frame is a pure function of t.
  }
});
</script>
```

Runtime:
- `L.pick`
- `L.seg`
- `L.sp`
- `L.typed`
- `L.count`
- `L.rng`
- `L.rise`
- `L.place`
- `L.cue`
- `L.cueTyping`
- `L.film`

motion-broll primitives:
- `M.track`
- `M.ctrack`
- `M.vis/apply`
- `M.path`
- `M.presses`

These are primitives, not boundaries.

You may also use ordinary browser capabilities when useful:
- SVG;
- Canvas;
- CSS transforms;
- CSS 3D;
- filters;
- masks;
- clip paths;
- gradients;
- blend modes;
- custom easing;
- procedural geometry;
- image sequences;
- video frames;
- WebGL-compatible browser approaches if the render pipeline remains deterministic;
- project-local JS helpers.

If a creative idea requires a capability that does not exist, extend, wrap, replace, or bypass parts of the engine as needed. The engine is infrastructure, not a boundary. Preserve compatibility only where it remains useful.

---

## 6A. Frontier permission

There is no approved visual vocabulary.

The creator is explicitly permitted to push beyond conventional motion-design patterns and beyond prior L-evate examples.

Possible directions include, but are not limited to:
- generative geometry;
- procedural worlds;
- shader-driven graphics;
- volumetric illusions;
- simulated lighting;
- depth fields;
- particle systems;
- vector fields;
- fluid-like motion;
- physics-inspired systems;
- data-driven choreography;
- recursive layouts;
- infinite-canvas movement;
- nonlinear timelines;
- split temporalities;
- multi-camera compositions;
- spatial UI;
- impossible interfaces;
- abstract environments;
- typographic sculpture;
- image deformation;
- cinematic compositing;
- live-action integration;
- diagrammatic storytelling;
- interactive-feeling sequences;
- game-like visual systems;
- surreal transitions;
- mixed media;
- deliberately minimal compositions;
- deliberately maximal compositions.

These are not recommendations. They are evidence that the creative ceiling is not defined by the existing engine API.

If the strongest idea requires new primitives, invent them.

If the strongest idea requires a different rendering technique for part of the film, use it.

If the strongest idea is simpler than the engine's capabilities, keep it simple.

The criterion is not technical complexity. The criterion is whether the result is exceptional, coherent, truthful, and appropriate to the brief.


---

## 7. Composition across formats

Treat each aspect ratio as its own composition sharing one conceptual timeline.

Supported targets commonly include:
- 16:9;
- 9:16;
- 1:1;
- 4:5.

Do not assume:
- the same camera;
- the same scale;
- the same text placement;
- the same number of visible elements;
- the same spatial relationship.

Recompose.

The vertical version may legitimately use different staging from the horizontal version while preserving the same idea and timing.

---

## 8. Typography

Typography is a motion material, not merely captions.

Possible uses:
- monumental words;
- micro labels;
- kinetic type;
- type as mask;
- type as environment;
- type following paths;
- variable hierarchy;
- staggered letters;
- scrolling fields;
- dimensional type;
- typographic transitions;
- sparse supers;
- no text at all.

Requirements:
- important text must be readable;
- avoid accidental clipping;
- avoid unintended orphans;
- preserve brand type when brand fidelity requires it.

There is no universal minimum hold time. Duration should reflect:
- word count;
- hierarchy;
- movement;
- viewing platform;
- expected reading speed.

Use judgment and verify by watching.

---

## 9. Motion

No motion primitive is universally superior.

Use:
- springs;
- cubic easing;
- linear motion;
- acceleration;
- deceleration;
- constant velocity;
- stepped motion;
- physically modeled movement;
- overshoot;
- inertia;
- elastic motion;
- vibration;
- orbit;
- parallax;
- camera movement;
- scaling;
- rotation;
- path following;
- deformation;
- masking;
- morphing;
- frame-by-frame state changes;
- deliberate stillness.

"Linear motion is bad" is not a rule.

Linear motion is often correct for:
- machinery;
- conveyor systems;
- scans;
- progress;
- camera trucks;
- timelines;
- data streams;
- controlled technical diagrams.

Choose motion according to meaning.

---

## 10. Sound

Sound can come from the same cue timeline, but it does not need to place a sound on every visible change.

Design the soundscape intentionally.

Possible layers:
- silence;
- room tone;
- synth cues;
- UI foley;
- impacts;
- rhythm;
- drones;
- tonal beds;
- music;
- user-supplied tracks;
- licensed assets when permitted;
- recorded sound;
- voice.

Use `L.cue()` when synchronized procedural sound is useful.

Available synthesized voices include:
- key;
- click;
- tick;
- pop;
- thud;
- whoosh;
- whoosh_in;
- whoosh_out;
- sub;
- ding;
- blip_down;
- swell;
- jingle;
- chord;
- drone.

Audio should support the film's concept, not demonstrate that the cue engine exists.

---

## 11. E: Examine — challenge the work

Examination is mandatory. Style conformity is not.

Build preview:

```bash
python3 $SKILL/engine/build.py dist scenes/<name>.html
open "dist/<name>.html?fmt=16x9"
```

Generate still sheets:

```bash
NODE_PATH=./node_modules node $SKILL/engine/stills.js dist/<name>.html work/check.png --fmt 16x9
NODE_PATH=./node_modules node $SKILL/engine/stills.js dist/<name>.html work/beats.png --fmt 9x16 2.1 2.6 …
```

Check:

### Truth
- Is every factual claim supported?
- Is real product UI represented honestly?
- Are numbers real?
- Are logos correct?

### Composition
- Does each frame have a deliberate focal hierarchy?
- Are important elements legible?
- Are edges, crops, and safe areas intentional?
- Does the composition make sense in every requested format?

### Motion
- Does the motion communicate the intended feeling?
- Are transitions motivated?
- Does anything move only because the engine makes it easy?
- Is there enough contrast between motion and stillness?

### Story
- Can a viewer understand the central idea?
- Is there escalation, progression, contrast, discovery, or another intentional structure?
- Does the ending earn its payoff?

### Originality
- Does this feel specifically authored for this brief, or could it be mistaken for a prior L-evate piece with different branding?
- Which scene is visually unexpected?
- Is there at least one memorable visual idea?
- Did the work exploit the subject matter or merely decorate it?

### Craft
- no accidental clipping;
- no stale hidden elements;
- no privacy leaks;
- no broken seek states;
- no unintended frame discontinuities;
- no invalid format recomposition;
- no audio drift.

Then watch the film at speed. Still sheets do not reveal rhythm.

Iterate until the piece feels authored rather than assembled.

---

## 12. Creative self-critique loop

For ambitious work, use this internal loop before final rendering:

### Pass 1 — Concept
Generate or consider multiple substantially different conceptual directions when doing so can improve the result.

Reject the weakest.

### Pass 2 — Distinctiveness
Ask:
- Could this exact treatment advertise a different software product with only the logo changed?

If yes, redesign.

### Pass 3 — Product truth
Replace generic motion with product-specific behavior, geometry, language, data, or workflow.

### Pass 4 — Escalation
Ensure the strongest visual idea is not spent in the first few seconds unless the concept deliberately demands it.

### Pass 5 — Restraint
Remove effects that do not improve comprehension, emotion, rhythm, or memorability.

### Pass 6 — Surprise
Find one moment the viewer is unlikely to predict from the opening frame.

### Pass 7 — Finish
Inspect every format and final audio.

---

## 13. Render

```bash
NODE_PATH=./node_modules node $SKILL/engine/render.js \
  dist/<name>.html \
  out/<name>-16x9.mp4 \
  --fmt 16x9 \
  --fps 30 \
  --audio dist/assets/soundtrack.wav
```

The renderer can blend multiple sub-frames per output frame for motion blur.

Use motion blur when appropriate.

Do not assume every aesthetic needs it.

For intentionally crisp UI, stop-motion, pixel art, technical diagrams, or stepped animation, fewer subframes may be visually stronger.

---

## 14. Learn without becoming stylistically trapped

Read `LEARNINGS.md` before every project.

Its purpose is to remember:
- rendering bugs;
- capture failures;
- privacy hazards;
- performance constraints;
- audio mistakes;
- composition failures;
- implementation techniques.

Do **not** interpret prior project learnings as a mandatory visual style.

After each project, append:
- technical lessons;
- failed approaches;
- successful project-specific techniques;
- performance measurements;
- reusable engineering insights.

When recording aesthetic observations, label them as project-specific unless they are genuinely universal.

Example:

Bad:
> Always use one accent color.

Better:
> For the DevLaunchr film, limiting green to state changes kept the dense dark UI readable.

---

## 15. Examples

The examples are demonstrations of what is possible, not templates to emulate.

Use them to learn:
- deterministic scene construction;
- responsive layout;
- real screenshot integration;
- timeline organization;
- audio synchronization;
- asset handling;
- rendering techniques.

Do not copy their:
- pacing;
- scene sequence;
- palette;
- typography;
- transition grammar;
- headline structure;
- composition.

unless the brief specifically benefits from those choices.

---

## 16. Engine philosophy

L-evate should expand the creator's range, not shrink it.

The engine provides:
- deterministic time;
- browser rendering;
- multi-format output;
- reproducible motion;
- synchronized audio;
- product-grounded assets;
- inspection;
- iteration.

Everything else should remain open to invention.

When there is tension between:
1. a stylistic convention in an old example, and
2. a stronger concept for the current project,

choose the stronger concept.

When there is tension between:
1. creative freedom, and
2. truth, privacy, legibility, or render integrity,

protect truth, privacy, legibility, and render integrity.

---

## 17. Setup

```bash
mkdir -p motion/{scenes/assets,dist,out,work} && cd motion
echo '{"private":true}' > package.json
npm install playwright
npx playwright install chromium
```

Requirements:
- Node 18+;
- Python 3;
- NumPy;
- ffmpeg with libx264 and AAC;
- Chromium through Playwright.

---

## 18. Files

- `engine/motion.js` — motion-broll primitives.
- `engine/lev.js` — L-evate runtime.
- `engine/build.py` — self-contained scene build.
- `engine/render.js` — frame/video renderer.
- `engine/stills.js` — inspection sheets.
- `engine/audio.py` — procedural sound generation.
- `engine/base.css` — runtime base styles.
- `engine/fonts/` — bundled fonts.
- `reference/checklist.md` — legacy craft checklist; use technical checks, not stylistic rules, unless HOUSE mode is intended.
- `LEARNINGS.md` — accumulated technical and project-specific lessons.
- `examples/` — implementation references and quality demonstrations.
- `CREDITS.md` — sources and licenses.

---

# Final directive

Do not ask, "What does an L-evate video look like?"

Ask:

> "What is the strongest motion-design idea for this exact product, audience, objective, and material — and how can L-evate make that idea real?"

The engine should disappear behind the work.
