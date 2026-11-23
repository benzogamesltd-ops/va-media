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
- 1080×1920, 30 fps, **8–12 s**, new scene every 1–2 s, brand reveal at the end with CTA "Follow / Подпишись / Folgt uns" (reveal ≤ 2 s).
- **Retention rules (MANDATORY — data 2026-11-23: Facebook reel "How an AI agent thinks" had 244 views but avg watch 2 s, 3.4 % completion, biggest drop at 0:01; its first ~0.4 s was an empty dark gradient):**
  1. **Frame 0 is never empty.** At t = 0 the full hook text and the hero visual are already on screen, bright and readable. No fade-in from black, no "build-up" intro. Animate *in place* instead (scale punch 1.08→1, glow pulse, camera push, glitch flicker).
  2. **Hook = 3–6 huge words** (≥ 120 px, Montserrat 800–900, center of the frame between 30 % and 60 % height — clear of the top status bar and the bottom caption/UI), max contrast. Use curiosity, a bold claim that is true, or a direct "you": e.g. "This video was made by AI", "Your next employee never sleeps", "Stop doing this by hand", "Watch an AI build this in 10 s". Avoid soft lecture titles like "How X works".
  3. **Something changes every ~0.7 s in the first 3 s** (pattern interrupts: a number counting, a card slamming in, a color flash, a zoom) and a visible payoff promise ("wait for #3", progress dots, a counter).
  4. **Make it loop**: the last frame flows back into the first (same background/hero position) so replays count; keep the brand reveal short.
  5. Music hits on frame 0 (no silent intro): kick + impact at t = 0.
  6. The cover is a separate bold frame, but the video's own first frame must also work as a thumbnail.
- **Captions**: first line ≤ 8 words that repeat the hook + a question to the viewer; hashtags at the end.
- Subtitles: main language line big, smaller English line under it (unless the reel is English).
- Music: original track generated in code by `tools/techno.py` — **every reel gets a different track**. Owner's choice (2026-11-23): **techno + deep house**, sometimes hybrids. Rotation: look at the music lines of the last reels in reels/LOG.md. (1) If none of the last 3 reels was a hybrid → this reel is a HYBRID: `classic_techno` (a Mozart theme over a techno beat) or `bayan_electro` (accordion/bayan tune over an electro beat) — alternate between the two. (2) Otherwise pick one of: deep_house, melodic_techno, acid_techno, hard_techno, minimal, tech_house, trance, electro, synthwave, drum_and_bass — not used in the last 3 reels, and deep_house at least every 3rd reel. Pure `mozart` / `accordion` without a beat are NOT used. Use a NEW random seed every run. The script prints "style=… bpm=… seed=…" — write it into reels/LOG.md. The track hits on t=0 and ends without a long fade (loopable). Match the visuals to the music (deep_house → smooth night-city/space; hard/acid → aggressive glitch; classic_techno → elegant gold & marble meets neon; bayan_electro → playful, warm, folk-meets-future).
- Cover: 1080×1920 JPEG, hook text centered so the 3:4 profile-grid crop keeps it.

## Signature (MANDATORY, owner's request 2026-11-23)
Every caption, post text, group post and comment/message reply we publish ends with a signature line in the text's language:
- RU: «Сообщение создано SMM-агентом VA Corporation 🤖»
- DE: „Diese Nachricht wurde vom SMM-Agenten von VA Corporation erstellt 🤖“
- EN: "This message was created by the VA Corporation SMM agent 🤖"
- other languages: translate the same sentence.
In posts the signature goes after the CTA and BEFORE the hashtags. In comment/message replies append it as a short last line ("— SMM-агент VA Corporation 🤖" / "— SMM-Agent von VA Corporation 🤖" / "— VA Corporation SMM agent 🤖").

## Honesty
Never invent facts: no fake products, clients, numbers, awards, prices, releases or partnerships. No real people, brands or copyrighted characters. "This reel/banner was made by AI" is true and allowed.

## Holiday season: 1 December – 7 January (MANDATORY in this period)
Every banner, reel, caption and cover in this period gets Christmas / New Year design and greetings. Before 1 Dec and after 7 Jan: normal style.

**Design:** keep the brand (sun mark, wordmark, palettes — still NO PINK) and add a festive layer: falling snow particles and bokeh lights, golden/ice garland light strings, glowing glass ornaments (spheres) hanging from top, frost/ice-crystal edges, gift boxes with light ribbons, fireworks bursts (round, radial sparks) for New Year, a glowing countdown clock / "2027" numerals, warm gold + ice blue + deep green (#0F5132 / #14532D) accents. The VA sun can wear a soft halo like a festive light. Avoid triangle-shaped trees and any star/pentagram/hexagram shapes — use round ornaments, snow dots, bokeh, garlands, spirals of light instead.

**Reels:** festive scene + greeting before the brand reveal; music: `python3 tools/techno.py ... --festive` (techno + sleigh bells + bell arpeggio).

**Greetings by language and date** (use the matching one on the day's posts; at least one festive post per day; key days → all posts that day are greetings):
| Date (2026–27) | 🇷🇺 RU | 🇩🇪 DE | 🇬🇧 EN |
|---|---|---|---|
| 1–23 Dec | «Скоро праздники!», «С наступающим Новым годом!» | Adventszeit; 6 Dec «Frohen Nikolaustag!»; Advent Sundays 6, 13, 20 Dec «Einen schönen 2./3./4. Advent!» | "Holiday season is here!", "Happy holidays!" |
| 24–26 Dec | «С католическим Рождеством!» (24–25), «Тёплых праздников!» | «Frohe Weihnachten!» (24 Heiligabend: «Frohe Weihnachten und besinnliche Feiertage!») | "Merry Christmas!" |
| 27–30 Dec | «С наступающим 2027!» | «Einen guten Rutsch ins neue Jahr!» | "Happy New Year in advance!" |
| 31 Dec | «С наступающим Новым годом!» countdown | «Guten Rutsch! Frohes Silvester!» | "Happy New Year's Eve!" |
| 1 Jan | «С Новым 2027 годом!» | «Frohes neues Jahr 2027!» | "Happy New Year 2027!" |
| 2–6 Jan | «Счастливых праздников!», итоги / планы на год | «Frohes neues Jahr!» | "New year, new ideas!" |
| 7 Jan | «С Рождеством Христовым!» | «Frohes orthodoxes Weihnachtsfest an alle, die heute feiern!» | "Merry Christmas to everyone celebrating today!" |
Wishes may be warm and on-brand ("пусть ваши идеи сбываются, а рутину берут на себя AI-агенты") but never invent company facts, results or offers.

## Prices (MANDATORY for replies, comments and DMs)
Approved price list: **PRICES.md** in this repo. When anyone asks about price/cost/"how much", answer with the relevant "from" prices from PRICES.md, always add "+ VAT" and that monthly maintenance depends on project complexity, offer the free first consultation and WhatsApp/Telegram +34 641 387 122. Never invent other prices or discounts.
