#!/usr/bin/env python3
"""
ASCII Art Generator

Convert images, animated GIFs, and webcam feeds into Unicode ASCII art.
Supports multiple symbol sets, real-time terminal rendering, and GIF export.
"""

import sys
import signal
import time
import argparse
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Symbol sets for different visual styles
SYMBOL_SETS = {
    'braille': ["⣿", "⣾", "⣶", "⣦", "⣤", "⣄", "⣀", "⡀", " "],
    'circles': ["●", "◉", "◎", "◯", "○", "◌", "°", "·", ".", " "],
    'blocks': ["█", "▓", "▒", "░", "▒", "░", "·", ".", " "],
    'ascii': ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]
}


def get_thresholds(num_symbols):
    """Generate threshold values for symbol mapping."""
    return [i * (255 / num_symbols) for i in range(num_symbols)]


def ascii_to_text(array, symbols):
    """Convert index array to text using provided symbols."""
    return '\n'.join(''.join(symbols[c % len(symbols)] for c in row) for row in array)


def generateAscii(grayscale_img, target_width=None):
    """
    Convert grayscale image to ASCII index array.
    
    Args:
        grayscale_img: Grayscale image as numpy array
        target_width: Target width in characters (None preserves original)
    
    Returns:
        2D numpy array of grayscale values
    """
    if target_width is None:
        height, width = grayscale_img.shape
        newWidth = int(width)
        newHeight = int(height)
    else:
        newWidth = target_width
        newHeight = int(newWidth * (grayscale_img.shape[0] / grayscale_img.shape[1]) * (5.5 / 9.5))
    
    resizedImage = cv2.resize(grayscale_img, (newWidth, newHeight))
    return resizedImage


def map_to_symbols(image_array, symbols):
    """Map grayscale values to symbol indices."""
    thresholds = get_thresholds(len(symbols))
    thresh_img = np.zeros(image_array.shape)
    
    for i, threshold in enumerate(thresholds):
        thresh_img[image_array > threshold] = i
    
    return thresh_img.astype(int)


def get_monospace_font_path():
    """
    Find suitable monospace font for current platform.
    
    Returns:
        Path to font file or None if not found
    """
    font_candidates = []
    
    # Platform-specific font candidates
    if sys.platform == 'win32':
        font_dir = r'C:\Windows\Fonts'
        font_candidates = [
            os.path.join(font_dir, 'consola.ttf'),  # Consolas
            os.path.join(font_dir, 'cour.ttf'),     # Courier New
            os.path.join(font_dir, 'lucon.ttf'),    # Lucida Console
        ]
    elif sys.platform == 'darwin':  # macOS
        font_dirs = ['/System/Library/Fonts', '/Library/Fonts']
        font_names = ['Menlo.ttc', 'Monaco.dfont', 'Courier New.ttf']
        for font_dir in font_dirs:
            for font_name in font_names:
                font_candidates.append(os.path.join(font_dir, font_name))
    else:  # Linux and others
        font_dirs = [
            '/usr/share/fonts',
            '/usr/local/share/fonts',
            os.path.expanduser('~/.fonts'),
        ]
        font_names = [
            'DejaVuSansMono.ttf',
            'LiberationMono-Regular.ttf',
            'FreeMono.ttf',
            'UbuntuMono-R.ttf',
        ]
        # Recursively search font directories
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for font_name in font_names:
                        if font_name in files:
                            font_candidates.append(os.path.join(root, font_name))
    
    # Return first existing font
    for font_path in font_candidates:
        if os.path.exists(font_path):
            return font_path
    
    return None


def render_ascii_to_image(indices, symbols, font_path=None, font_size=15):
    """
    Render ASCII index array to PIL Image.
    
    Args:
        indices: 2D numpy array of symbol indices
        symbols: List of symbols to use
        font_path: Path to font file (None for default)
        font_size: Font size in points
    
    Returns:
        PIL Image object with rendered ASCII art
    """
    # Load font
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size)
        else:
            # Try to use default monospace font
            font = ImageFont.load_default()
            if font_path is None:
                print("Warning: Using PIL default font (may not be monospace)")
    except Exception as e:
        print(f"Warning: Could not load font: {e}")
        font = ImageFont.load_default()
    
    # Calculate character dimensions
    # Use a sample character to measure size
    try:
        # For truetype fonts, use getbbox
        bbox = font.getbbox("M")
        char_w = bbox[2] - bbox[0]
        char_h = bbox[3] - bbox[1]
    except:
        # Fallback for default font
        char_w = 10
        char_h = 18
    
    # Add padding for better spacing
    char_w = max(char_w, int(font_size * 0.6))
    char_h = max(char_h, int(font_size * 1.2))
    
    # Calculate canvas size
    img_w = indices.shape[1] * char_w
    img_h = indices.shape[0] * char_h
    
    # Create black canvas
    canvas = Image.new("RGB", (img_w, img_h), color=(0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    
    # Draw characters
    for y, row in enumerate(indices):
        for x, idx in enumerate(row):
            char = symbols[idx % len(symbols)]
            draw.text((x * char_w, y * char_h), char, fill=(255, 255, 255), font=font)
    
    return canvas


def process_static_image(img, width, symbols):
    """Process a static image and return ASCII text."""
    ascii_array = generateAscii(img, width)
    symbol_indices = map_to_symbols(ascii_array, symbols)
    return ascii_to_text(symbol_indices, symbols)


def play_gif_terminal(pil_img, width, symbols, export_path=None, export_only=False, font_path=None, font_size=15):
    """
    Play animated GIF in terminal using ANSI escape codes, optionally export to GIF.
    
    Args:
        pil_img: PIL Image object (animated GIF)
        width: Target width in characters
        symbols: List of symbols to use for rendering
        export_path: Path to save exported GIF (None to skip export)
        export_only: If True, skip terminal playback
        font_path: Font path for GIF export
        font_size: Font size for GIF export
    """
    try:
        n_frames = pil_img.n_frames
    except (AttributeError, ValueError):
        n_frames = 1
    
    # Set up signal handler for clean exit
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    # Collect frames for export if requested
    ascii_frames = [] if export_path else None
    frame_duration = None
    
    # Process all frames
    frame_height = 0
    for frame_idx in range(n_frames):
        pil_img.seek(frame_idx)
        rgb_img = pil_img.convert('RGB')
        
        grayscale_frame = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2GRAY)
        ascii_array = generateAscii(grayscale_frame, width)
        symbol_indices = map_to_symbols(ascii_array, symbols)
        
        # Get frame duration from first frame
        if frame_idx == 0:
            frame_duration = pil_img.info.get('duration', 100)
            text_lines_init = ascii_to_text(symbol_indices, symbols).splitlines()
            frame_height = len(text_lines_init)
        
        # Render to image if exporting
        if export_path:
            if frame_idx == 0:
                print(f"Processing {n_frames} frames for GIF export...")
            rendered_frame = render_ascii_to_image(symbol_indices, symbols, font_path, font_size)
            ascii_frames.append(rendered_frame)
            
            # Progress indicator
            if (frame_idx + 1) % 10 == 0 or frame_idx == n_frames - 1:
                print(f"  Processed {frame_idx + 1}/{n_frames} frames")
    
    # Save GIF if export requested
    if export_path and ascii_frames:
        print(f"Saving GIF to {export_path}...")
        ascii_frames[0].save(
            export_path,
            save_all=True,
            append_images=ascii_frames[1:],
            duration=frame_duration,
            loop=0
        )
        print(f"✓ GIF exported successfully: {export_path}")
        print(f"  Frames: {len(ascii_frames)}, Duration: {frame_duration}ms per frame")
    
    # Skip terminal playback if export-only mode
    if export_only:
        return
    
    # Terminal playback
    print("\nStarting terminal playback (Press Ctrl+C to exit)...")
    time.sleep(1)
    
    # Reserve space for the animation
    for _ in range(frame_height):
        sys.stdout.write('\n')
    
    if frame_height > 0:
        sys.stdout.write(f'\033[{frame_height}A')
    
    sys.stdout.flush()
    
    # Animation loop
    while True:
        for frame_idx in range(n_frames):
            pil_img.seek(frame_idx)
            rgb_img = pil_img.convert('RGB')
            
            grayscale_frame = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2GRAY)
            ascii_array = generateAscii(grayscale_frame, width)
            symbol_indices = map_to_symbols(ascii_array, symbols)
            text_lines = ascii_to_text(symbol_indices, symbols).splitlines()
            
            # Draw each line
            for index in range(frame_height):
                sys.stdout.write('\r\033[2K')
                
                if index < len(text_lines):
                    sys.stdout.write(text_lines[index])
                
                if index < frame_height - 1:
                    sys.stdout.write('\n')
            
            sys.stdout.flush()
            
            # Use frame duration from GIF metadata
            duration_ms = pil_img.info.get('duration', 0)
            if duration_ms:
                time.sleep(min(duration_ms / 750.0, 5))
            
            # Move cursor back to top
            if frame_height > 1:
                sys.stdout.write(f'\033[{frame_height - 1}A')
                sys.stdout.write('\r')
                sys.stdout.flush()


def webcam_mode(width, symbols, export_path=None, duration=10, fps=30, font_path=None, font_size=15):
    """
    Capture and display real-time ASCII art from webcam, optionally export to GIF.
    
    Args:
        width: Target width in characters
        symbols: List of symbols to use for rendering
        export_path: Path to save exported GIF (None to skip export)
        duration: Recording duration in seconds (for export)
        fps: Frames per second (for export)
        font_path: Font path for GIF export
        font_size: Font size for GIF export
    """
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot access webcam. Please check:")
        print("  - Camera is connected and not in use by another application")
        print("  - Camera permissions are granted")
        print("  - Camera drivers are installed")
        sys.exit(1)
    
    # Clear screen
    print("\033[2J", end="")
    print("Webcam ASCII Art Mode")
    if export_path:
        print(f"Recording for {duration} seconds to {export_path}...")
    else:
        print("Press Ctrl+C or 'q' to quit")
    print()
    
    # Give user a moment to read the message
    time.sleep(1)
    
    # Clear screen again for clean display
    print("\033[2J", end="")
    
    # Collect frames for export if requested
    ascii_frames = [] if export_path else None
    start_time = time.time()
    frame_delay = 1.0 / fps if export_path else 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("\nError: Failed to capture frame from webcam")
                break
            
            # Convert to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Generate ASCII
            ascii_array = generateAscii(gray_frame, width)
            symbol_indices = map_to_symbols(ascii_array, symbols)
            
            # Render to image if exporting
            if export_path:
                rendered_frame = render_ascii_to_image(symbol_indices, symbols, font_path, font_size)
                ascii_frames.append(rendered_frame)
                
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    print(f"\n\nRecording complete! Captured {len(ascii_frames)} frames")
                    break
            
            # Display with cursor reset to top-left
            print("\033[H", end="")
            print(ascii_to_text(symbol_indices, symbols))
            sys.stdout.flush()
            
            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Frame rate control for export
            if export_path and frame_delay > 0:
                time.sleep(frame_delay)
    
    except KeyboardInterrupt:
        print("\n\nExiting webcam mode...")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
    
    # Save GIF if export requested and frames collected
    if export_path and ascii_frames:
        print(f"\nSaving GIF to {export_path}...")
        frame_duration_ms = int(1000 / fps)
        ascii_frames[0].save(
            export_path,
            save_all=True,
            append_images=ascii_frames[1:],
            duration=frame_duration_ms,
            loop=0
        )
        print(f"✓ Webcam GIF exported successfully: {export_path}")
        print(f"  Frames: {len(ascii_frames)}, FPS: {fps}, Duration: {len(ascii_frames)/fps:.1f}s")


def main():
    parser = argparse.ArgumentParser(
        description='Generate ASCII art from images, GIFs, or webcam',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg                    # Display static image
  %(prog)s image.jpg -w 120             # Set width to 120 characters
  %(prog)s image.jpg -o output.txt      # Save to text file
  %(prog)s animation.gif                # Play animated GIF
  %(prog)s animation.gif --export-gif output.gif  # Export GIF as ASCII GIF
  %(prog)s --webcam                     # Real-time webcam ASCII art
  %(prog)s --webcam --export-gif cam.gif --duration 5  # Record 5s webcam to GIF
        """
    )
    
    # Input source (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('image', nargs='?', type=str, 
                            help='Path to input image or GIF')
    input_group.add_argument('--webcam', '-c', action='store_true',
                            help='Use webcam as input source')
    
    # Display options
    parser.add_argument('--width', '-w', type=int, default=80,
                       help='Output width in characters (default: 80)')
    parser.add_argument('--symbols', type=str, default='braille',
                       choices=list(SYMBOL_SETS.keys()),
                       help='Symbol set to use (default: braille)')
    
    # Output options
    parser.add_argument('-o', '--output', type=str,
                       help='Output file path for static images (text file)')
    parser.add_argument('--export-gif', type=str,
                       help='Export animated GIF with ASCII art rendering')
    parser.add_argument('--export-only', action='store_true',
                       help='Export GIF without terminal playback (requires --export-gif)')
    
    # GIF export options
    parser.add_argument('--duration', type=int, default=10,
                       help='Recording duration in seconds for webcam (default: 10)')
    parser.add_argument('--fps', type=int, default=30,
                       help='Frames per second for webcam GIF export (default: 30)')
    parser.add_argument('--font', type=str,
                       help='Custom font path for GIF export')
    parser.add_argument('--font-size', type=int, default=15,
                       help='Font size for GIF export (default: 15)')
    
    args = parser.parse_args()
    
    # Validate width
    if args.width <= 0:
        print('Error: width must be greater than 0')
        sys.exit(1)
    
    # Validate export-only flag
    if args.export_only and not args.export_gif:
        print('Error: --export-only requires --export-gif')
        sys.exit(1)
    
    # Validate duration for webcam export
    if args.duration <= 0:
        print('Error: --duration must be greater than 0')
        sys.exit(1)
    
    # Validate FPS
    if args.fps <= 0 or args.fps > 60:
        print('Error: --fps must be between 1 and 60')
        sys.exit(1)
    
    # Get selected symbol set
    symbols = SYMBOL_SETS[args.symbols].copy()
    symbols.reverse()  # Reverse for intensity mapping
    
    # Get font path for GIF export
    font_path = args.font
    if args.export_gif and not font_path:
        font_path = get_monospace_font_path()
        if font_path:
            print(f"Using font: {os.path.basename(font_path)}")
        else:
            print("Warning: No monospace font found, using default font")
    
    # Webcam mode
    if args.webcam:
        if args.output:
            print('Error: --output is not supported with --webcam')
            sys.exit(1)
        
        webcam_mode(
            args.width, 
            symbols, 
            export_path=args.export_gif,
            duration=args.duration,
            fps=args.fps,
            font_path=font_path,
            font_size=args.font_size
        )
        return
    
    # Image/GIF mode
    img = cv2.imread(args.image, 0)
    
    if img is None:
        print(f'Error: Cannot load image at path: {args.image}')
        sys.exit(1)
    
    pil_img = Image.open(args.image)
    is_gif = args.image.lower().endswith('.gif')
    
    if is_gif:
        if args.output:
            print('Error: --output is not supported for animated GIF input')
            print('Use --export-gif to save as an ASCII GIF file')
            sys.exit(1)
        
        play_gif_terminal(
            pil_img, 
            args.width, 
            symbols,
            export_path=args.export_gif,
            export_only=args.export_only,
            font_path=font_path,
            font_size=args.font_size
        )
    else:
        if args.export_gif:
            print('Error: --export-gif is only supported for animated GIF input or --webcam')
            sys.exit(1)
        
        text = process_static_image(img, args.width, symbols)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"ASCII art saved to: {args.output}")
        else:
            print(text, end='')


if __name__ == "__main__":
    main()
