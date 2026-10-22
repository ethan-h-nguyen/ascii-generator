# Brag Plan: ASCII Generator

**Created:** 2026-10-22 20:03 UTC  
**Duration:** ~20 seconds  
**Format:** Landscape (1920×1080, 30fps)  
**Tone:** Playful, punchy — show the variety and versatility

---

## What is it?

A Python CLI that turns images, GIFs, and live webcam feeds into Unicode ASCII art with 4 symbol sets and GIF export.

## Who's it for?

Developers, artists, and terminal enthusiasts who want ASCII art that goes beyond static text — real-time feeds, multiple styles, exportable animations.

## What sets it apart?

- **4 visual styles** (Braille, circles, blocks, classic ASCII)
- **Live webcam mode** with real-time rendering
- **GIF export** — save ASCII animations as actual GIF files
- **Cross-platform** font detection

## The hook

Terminal characters coming alive — morphing between symbol sets, revealing the same image in completely different styles.

## Visual identity

- **Colors:** Terminal black background (#000), white/green terminal text (#00FF00 or #FFFFFF)
- **Fonts:** Monospace (Consolas, Monaco, Courier), large for demo visibility
- **Style:** Clean terminal aesthetic, code-focused, playful transitions

## Punchline

"ASCII art, but make it move." — 4 styles × 3 modes × unlimited possibilities

---

## Storyboard (20s total)

### Scene 1: HOOK — Symbol Morph (3s)
**0:00–0:03**

The same face rendered in 4 different symbol sets, rapidly transitioning:
- Braille patterns → Circles → Blocks → Classic ASCII
- Each transition shows the ASCII characters clearly
- Quick cuts (0.75s each)

**Visuals:**
- Black terminal background
- Large ASCII art (60-80 chars wide)
- Symbol sets labeled subtly in corner
- Smooth fade transitions

**Text:** None (pure visual hook)

---

### Scene 2: REVEAL — The Tool (3s)
**0:03–0:06**

Terminal command appears, typed out:
```
$ python ascii_generator.py image.jpg --symbols circles
```

Quick flash of the actual tool name and tagline:
**"ASCII Generator"**
**"Images • GIFs • Webcam"**

**Visuals:**
- Terminal prompt with typing animation
- Tool name and subtitle appear with slight scale-in
- Green terminal text on black

---

### Scene 3: HIGHLIGHT 1 — GIF Export (5s)
**0:06–0:11**

Show the exported GIF feature:
- Command: `python ascii_generator.py animation.gif --export-gif output.gif`
- Progress indicator appears
- Final exported GIF plays (the demo-export.gif we just made)

**Text overlay:**
"Export ASCII animations as actual GIFs"

**Visuals:**
- Split screen: command on left, output preview on right
- Progress bar animation
- Exported GIF loops 2-3 times

---

### Scene 4: HIGHLIGHT 2 — Live Webcam (5s)
**0:11–0:16**

Webcam mode demonstration:
- Command: `python ascii_generator.py --webcam --symbols braille`
- Simulated webcam feed turning into ASCII in real-time
- Show face/hand moving → ASCII updates live

**Text overlay:**
"Real-time webcam ASCII art"

**Visuals:**
- Small webcam preview in corner (or stock footage)
- Large ASCII output taking main focus
- Smooth motion showing real-time tracking

---

### Scene 5: HIGHLIGHT 3 — 4 Symbol Sets (3s)
**0:16–0:19**

Quick showcase of all 4 symbol sets side-by-side or in 2×2 grid:
- Braille (top-left)
- Circles (top-right)  
- Blocks (bottom-left)
- ASCII (bottom-right)

Same image rendered 4 ways simultaneously

**Text overlay:**
"4 symbol sets"

**Visuals:**
- Clean grid layout
- Each quadrant labeled
- Synchronized animation if using GIF source

---

### Scene 6: OUTRO — Call to Action (1s)
**0:19–0:20**

Final frame:
**"ASCII Generator"**
**"github.com/ehn77/ascii-generator"**

Simple, clean, readable

**Visuals:**
- White text on black
- Fade in from previous scene
- Hold long enough to read URL clearly

---

## Audio

**Music:** Upbeat electronic/chiptune style
- 120-140 BPM
- Playful but not chaotic
- Synth lead with light percussion
- Key: C major or G major (bright, energetic)

**Sound effects:**
- Typing sounds (subtle, blended) for terminal commands
- Soft "pop" or "whoosh" on symbol set transitions
- Gentle "ping" when GIF export completes
- All effects in same key as music, mixed softly underneath

**Mix:**
- Music: -12dB to -16dB (clear but not overpowering)
- Effects: -20dB to -24dB (texture, not jarring)
- No harsh transients
- Gentle fade out at end

---

## Creative notes

- **Show real output** — use the actual ASCII art generated from our assets
- **Readable pace** — text overlays stay 0.3s per word minimum
- **Terminal aesthetic** — stay true to the monospace, terminal vibe
- **Motion** — typing animations, fade transitions, nothing too flashy
- **Every frame postable** — any pause should look intentional and clean

---

## Data safety

No secrets, API keys, or personal data in this project. All assets are local test images. Safe to show everything.

---

## Technical approach

**Build method:** HTML5 Canvas + Web Audio API
- Render each frame as pure function of time
- Load Consolas font (or fallback monospace)
- Capture frames with Puppeteer/Playwright
- Generate audio with Tone.js or similar
- Composite with ffmpeg

**Resolution:** 1920×1080, 30fps
**Codec:** H.264, good quality
**Audio:** AAC, 128kbps

---

## Deliverables

1. `brag.mp4` — Final video with baked-in poster frame
2. `brag.jpg` — Hero frame for sharing
3. `share-copy.txt` — Social media caption
4. All intermediate files in `work/` subdirectory
