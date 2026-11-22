# VA Corporation — Brand & Motion Guide

Studio-grade rules for every banner and reel. Read this before designing anything.

## Positioning
VA Corporation builds **AI agents, games and IT products**. Tone: visionary, cinematic, premium, confident — never childish, never clip-art. Think film title sequences, sci-fi interfaces, product launches.

## Logo
- Mark: a glowing golden **sun disk** with "VA" (radial gradient #FFF7DE → #FFC15E → #F07A1A, soft outer glow).
- Wordmark: "VA CORPORATION" in wide letter-spacing (0.3–0.7em), or "VA Corporation" in bold.
- Tagline: "AI agents · Games · Software".
- Never use triangles, pentagrams, hexagrams, inverted stars or occult-looking geometry.

## Palette (pick one world per piece; vary day to day)
| World | Background | Accents | Text |
|---|---|---|---|
| Solar Dawn | #8CCBFF → #CFE8FF → #FFE4C2 | #FFC15E, #F07A1A, #2F5BEA | #0F1B3D |
| Nebula | #0B1033 → #1E1B6B → #5B21B6 | #22D3EE, #FACC15 | #FFFFFF |
| Aurora | #052E2B → #0E8F7C → #67E8F9 | #A3E635, #FACC15 | #FFFFFF |
| Plasma | #FF7A2F → #F59E0B → #6C4DFF | #FFFFFF, #FFE066 | #FFFFFF |
| Ice Orbit | #E0F2FE → #BAE6FD → #F5F3FF | #6366F1, #06B6D4 | #0F172A |
| Deep Indigo | #0B1033 → #1E2A78 | #FFC15E, #7DD3FC | #F2F5FA |
**NO PINK / MAGENTA / ROSE anywhere** (no #DB2777, #F472B6, #EC4899, #FF3D7F-type hues, no pink gradients or glows). Avoid flat pure black backgrounds. Text contrast ≥ 4.5:1 always.

## Typography (installed locally)
- Display: Montserrat 800–900, tight tracking (-0.02em) for hooks; wide tracking for wordmarks.
- Body / subtitles: Inter 500–700.
- Hierarchy: one hero line (90–150px on 1080 wide), one support line (34–48px), max ~8 words per screen.

## Fantastic visual toolkit (CSS only, no network)
- Layered depth: 3–5 parallax layers (stars/particles, nebula blobs with blur(60–120px), planet/orb, UI glass cards, type).
- Glassmorphism HUD cards: rgba(255,255,255,.12) + backdrop-filter blur + 1px light border, monospace micro-labels ("AGENT_01 · ONLINE").
- Light: radial glows, lens-flare rings, gradient rims on spheres, conic-gradient halos, scanlines at 4–6% opacity.
- Particles: 80–200 absolutely positioned dots with seeded random positions and twinkle/drift keyframes.
- 3D: perspective(1200px) with rotateX/rotateY on grids (synthwave floor), orbiting rings via rotate on wrappers.
- Kinetic type: words slam in (scale 1.6→1, 200–300ms), mask reveals (clip-path inset), typewriter + blinking cursor, letter-by-letter stagger.
- Easing: cubic-bezier(.2,.8,.2,1) for entrances, cubic-bezier(.7,0,.3,1) for transitions. Nothing linear except particles/orbits.

## Banners (feed posts)
- Size **1080×1350 JPEG** (4:5). Safe zone: keep text 90px from edges.
- Layout: hero visual (orb/planet/HUD/scene) + 1 headline (≤7 words) + 1 sub line + small brand lockup bottom (sun mark + "VA Corporation").
- Each banner must feel like a poster/key art, not a slide. Rich depth, light and texture.

## Reels
- 1080×1920, 30 fps, 10–15 s, new scene every 1.5–2.5 s, hook in the first second, brand reveal at the end with CTA "Follow / Подпишись / Folgt uns".
- Subtitles: main language line big, smaller English line under it (unless the reel is English).
- Music: original **techno** generated in code (numpy), 125–132 BPM, four-on-the-floor kick with long sub tail, offbeat open hi-hats + 16th closed hats, clap on 2 and 4, rolling 16th-note bassline, an acid-style resonant filtered saw/square lead (303 feel) with filter sweep, white-noise risers before scene cuts and the brand reveal, impact hit on the logo, short fade-out. Normalize to about -1 dBFS, stereo if possible.
- Cover: 1080×1920 JPEG, hook text centered so the 3:4 profile-grid crop keeps it.

## Honesty
Never invent facts: no fake products, clients, numbers, awards, prices, releases or partnerships. No real people, brands or copyrighted characters. "This reel/banner was made by AI" is true and allowed.
