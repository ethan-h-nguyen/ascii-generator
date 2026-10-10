# ASCII Generator

A Python CLI tool that converts static images and animated GIFs into Unicode Braille-pattern terminal art.

The converter maps grayscale intensity levels to a 9-character Braille palette:

```text
⣿ ⣾ ⣶ ⣦ ⣤ ⣄ ⣀ ⡀ [space]
```

## Features

- Convert static images into Unicode terminal art
- Play animated GIFs as terminal animations
- Preserve GIF frame timing from frame metadata
- Set output width with `-w` or `--width`
- Save static conversions to a text file with `-o` or `--output`
- Render animated frames in-place using ANSI terminal control sequences

## Built With

- Python
- OpenCV
- NumPy
- Pillow

## Installation

Clone the repository:

```bash
git clone https://github.com/ehn77/ascii-generator.git
cd ascii-generator
```

Install dependencies:

```bash
python3 -m pip install opencv-python numpy Pillow
```

## Usage

### Static Image

```bash
python3 ascii_generator.py assets/Shizuka.jpg
```

### Set Output Width

```bash
python3 ascii_generator.py assets/Shizuka.jpg --width 80
```

Short form:

```bash
python3 ascii_generator.py assets/Shizuka.jpg -w 80
```

### Save Static Output

```bash
python3 ascii_generator.py assets/Shizuka.jpg --output output.txt
```

Short form:

```bash
python3 ascii_generator.py assets/Shizuka.jpg -o output.txt
```

### Animated GIF

```bash
python3 ascii_generator.py assets/test.gif --width 20
```

Animated GIFs play directly in the terminal using their frame-duration metadata.

`--output` is not supported for animated GIF input.

## CLI

```text
usage: ascii_generator.py [-h] [--width WIDTH] [-o OUTPUT] image
```

Arguments:

- `image` — path to the input image
- `-w`, `--width` — output width in characters
- `-o`, `--output` — output text file path for static images
- `-h`, `--help` — display command help

The configured width must be greater than `0`.

## How It Works

1. Load the source image or GIF frame.
2. Convert the image to grayscale.
3. Resize the grayscale image.
4. Divide grayscale intensity into thresholds.
5. Map each threshold level to a Unicode Braille-pattern character.
6. Join the resulting character grid into terminal text.

For animated GIFs, the process repeats for each frame. The terminal renderer redraws frames using ANSI cursor positioning and uses each frame's duration metadata for playback timing.

## Project Structure

```text
ascii-generator/
├── ascii_generator.py
├── assets/
│   ├── Shizuka.jpg
│   ├── consider.jpg
│   └── test.gif
├── .gitignore
└── README.md
```

## Notes

The default conversion path preserves the source image dimensions. Use `--width` to control output size and apply the terminal character aspect-ratio correction.

Static output can be redirected to a text file with `--output`. Animated GIF output is terminal-only.
