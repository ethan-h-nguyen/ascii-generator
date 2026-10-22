# ASCII Generator

A Python CLI tool that converts static images, animated GIFs, and live webcam feeds into Unicode ASCII art with multiple visual styles and export capabilities.

<p align="center">
  <a href="assets/demo.mp4">
    <img src="assets/consider.jpg" alt="ASCII Generator Demo" width="800">
  </a>
</p>
<p align="center">
  <strong>Watch the full launch demo:</strong>
  <a href="assets/demo.mp4">assets/demo.mp4</a>
</p>

## Features

### Core Capabilities
- 🖼️ **Static Images** — Convert images to terminal ASCII art or text files
- 🎬 **Animated GIFs** — Play animations in terminal with proper frame timing
- 📹 **Webcam Support** — Real-time ASCII art from your camera feed
- 💾 **GIF Export** — Save ASCII animations as actual GIF files
- 🎨 **Multiple Symbol Sets** — Choose from 4 different visual styles

### Symbol Sets

The tool supports four distinct symbol sets for different aesthetic effects:

**Braille** (default) — Dense Unicode Braille patterns
```text
⣿ ⣾ ⣶ ⣦ ⣤ ⣄ ⣀ ⡀ [space]
```

**Circles** — High visual distinction with circle characters
```text
● ◉ ◎ ◯ ○ ◌ ° · . [space]
```

**Blocks** — High contrast block characters
```text
█ ▓ ▒ ░ ▒ ░ · . [space]
```

**ASCII** — Traditional ASCII characters for maximum compatibility
```text
@ # S % ? * + ; : , . [space]
```

## Installation

Clone the repository:

```bash
git clone https://github.com/ehn77/ascii-generator.git
cd ascii-generator
```

Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Or install dependencies directly:

```bash
pip install opencv-python numpy Pillow
```

## Usage

### Static Images

Display an image as ASCII art in the terminal:

```bash
python ascii_generator.py assets/Shizuka.jpg
```

Set custom width:

```bash
python ascii_generator.py assets/Shizuka.jpg -w 120
```

Save to text file:

```bash
python ascii_generator.py assets/Shizuka.jpg -o output.txt
```

Use different symbol sets:

```bash
python ascii_generator.py assets/Shizuka.jpg --symbols circles
python ascii_generator.py assets/Shizuka.jpg --symbols blocks
python ascii_generator.py assets/Shizuka.jpg --symbols ascii
```

### Animated GIFs

Play GIF in terminal:

```bash
python ascii_generator.py assets/test.gif -w 40
```

Export GIF as ASCII GIF file:

```bash
python ascii_generator.py assets/test.gif --export-gif output.gif -w 30
```

Export without terminal playback:

```bash
python ascii_generator.py assets/test.gif --export-gif output.gif --export-only
```

Customize export with symbol sets and font size:

```bash
python ascii_generator.py animation.gif --export-gif out.gif --symbols circles --font-size 18
```

### Webcam Mode

Real-time webcam ASCII art:

```bash
python ascii_generator.py --webcam
```

With custom settings:

```bash
python ascii_generator.py --webcam -w 60 --symbols circles
```

Record webcam to GIF:

```bash
python ascii_generator.py --webcam --export-gif webcam.gif --duration 5 --fps 30
```

## CLI Reference

```text
usage: ascii_generator.py [-h] [--width WIDTH]
                          [--symbols {braille,circles,blocks,ascii}]
                          [-o OUTPUT] [--export-gif EXPORT_GIF]
                          [--export-only] [--duration DURATION] [--fps FPS]
                          [--font FONT] [--font-size FONT_SIZE]
                          (--webcam | image)
```

### Input Options

- `image` — Path to input image or GIF file
- `--webcam`, `-c` — Use webcam as input source (mutually exclusive with image)

### Display Options

- `--width WIDTH`, `-w WIDTH` — Output width in characters (default: 80)
- `--symbols {braille,circles,blocks,ascii}` — Symbol set for rendering (default: braille)

### Output Options

- `-o OUTPUT`, `--output OUTPUT` — Save static image as text file
- `--export-gif PATH` — Export animated GIF with ASCII rendering
- `--export-only` — Export GIF without terminal playback (requires `--export-gif`)

### GIF Export Options

- `--duration SECONDS` — Webcam recording duration in seconds (default: 10)
- `--fps FPS` — Frame rate for webcam GIF export (default: 30, max: 60)
- `--font PATH` — Custom font path for GIF export (auto-detected if not specified)
- `--font-size SIZE` — Font size for GIF export in points (default: 15)

## How It Works

1. **Load** — Read the source image, GIF frame, or webcam capture
2. **Convert** — Transform to grayscale
3. **Resize** — Scale to target width with aspect ratio correction (5.5:9.5 for terminal characters)
4. **Threshold** — Map grayscale intensity values to symbol indices
5. **Render** — Convert to text or draw on image canvas
6. **Display/Export** — Show in terminal or save as file

For animated GIFs, this process repeats for each frame. The terminal renderer uses ANSI escape codes for in-place updates, and frame timing is preserved from the source GIF metadata.

For GIF export, each ASCII frame is rendered as an image using TrueType fonts, then combined into an animated GIF with PIL.

## Font Detection

When exporting GIFs, the tool automatically detects monospace fonts:

- **Windows**: Consolas, Courier New, Lucida Console
- **macOS**: Menlo, Monaco, Courier New
- **Linux**: DejaVu Sans Mono, Liberation Mono, FreeMono, Ubuntu Mono

If no font is found, the tool falls back to PIL's default font with a warning. You can specify a custom font with `--font`.

## Examples

### Quick Start
```bash
# Static image with default settings
python ascii_generator.py photo.jpg

# Animated GIF with custom width
python ascii_generator.py animation.gif -w 80

# Webcam feed with circle symbols
python ascii_generator.py --webcam --symbols circles
```

### Advanced Usage
```bash
# Export high-quality ASCII GIF with large font
python ascii_generator.py input.gif --export-gif output.gif -w 100 --font-size 20 --symbols blocks

# Record 10-second webcam clip at 60 FPS
python ascii_generator.py --webcam --export-gif recording.gif --duration 10 --fps 60

# Static image with multiple symbol sets for comparison
python ascii_generator.py photo.jpg --symbols braille -o braille.txt
python ascii_generator.py photo.jpg --symbols circles -o circles.txt
python ascii_generator.py photo.jpg --symbols blocks -o blocks.txt
```

## Troubleshooting

### Webcam Issues

**Camera not accessible:**
- Check that the camera is connected and not in use by another application
- Verify camera permissions are granted to Python/terminal
- Ensure camera drivers are installed and up to date

### Font Issues

**Warning: Using PIL default font:**
- Install a monospace font for your platform
- Or specify a custom font with `--font /path/to/font.ttf`

### Performance

**Slow GIF export:**
- Reduce width with `-w` (smaller = faster)
- Use simpler symbol sets (braille is fastest)
- Reduce `--font-size` for smaller output files

**Choppy webcam display:**
- Reduce width with `-w 40` or lower
- Close other applications using the camera
- Try a lower resolution camera if available

## Terminal Compatibility

This tool requires a terminal with:
- UTF-8 encoding support (for Unicode symbols)
- ANSI escape code support (for animations)

Tested and working on:
- Windows Terminal
- macOS Terminal
- iTerm2
- GNOME Terminal
- Git Bash (MSYS)

## Project Structure

```text
ascii-generator/
├── ascii_generator.py       # Main script
├── requirements.txt         # Python dependencies
├── venv/                    # Virtual environment (created during setup)
├── assets/                  # Sample images and GIFs
│   ├── Shizuka.jpg
│   ├── consider.jpg
│   └── test.gif
├── .gitignore
└── README.md
```

## Technical Details

### Aspect Ratio Correction

Terminal characters are not square — they're typically taller than they are wide. This tool applies a 5.5:9.5 width-to-height ratio correction to prevent vertical stretching.

### Frame Timing

Animated GIFs preserve their original frame timing. The terminal playback uses a divisor of 750 to adjust for rendering overhead while keeping smooth animation.

### Symbol Mapping

Grayscale values (0-255) are divided into thresholds matching the number of symbols. Higher intensity values map to denser/darker symbols, creating the ASCII representation.

## Contributing

Contributions are welcome! Areas for enhancement:
- Additional symbol sets
- Color support with ANSI color codes
- Video file support (MP4, AVI, etc.)
- Performance optimizations
- GUI interface

## License

This project is open source. Check the repository for license details.

## Acknowledgments

Original concept and Braille symbol mapping from the ascii-generator project. Extended with webcam support, multiple symbol sets, and GIF export capabilities.
