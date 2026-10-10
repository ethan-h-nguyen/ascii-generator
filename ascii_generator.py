import cv2
import numpy as np

symbols = [
    "⣿", "⣾", "⣶", "⣦", "⣤", "⣄", "⣀", "⡀", " "
]

symbols.reverse()

thresholds = [i * (255/len(symbols)) for i in range(len(symbols))]

def ascii_to_text(array):
    return '\n'.join(''.join(symbols[c % len(symbols)] for c in row) for row in array)

def generateAscii(grayscale_img, target_width=None):
    if target_width is None:
        height, width = grayscale_img.shape
        newWidth = int(width)
        newHeight = int(height)
    else:
        newWidth = target_width
        newHeight = int(newWidth * (grayscale_img.shape[0] / grayscale_img.shape[1]) * (5.5 / 9.5))
    
    resizedImage = cv2.resize(grayscale_img, (newWidth,newHeight))
    thresh_img = np.zeros(resizedImage.shape)

    for i, threshold in enumerate(thresholds):
        thresh_img[resizedImage > threshold] = i

    return thresh_img.astype(int)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate ASCII art from image')
    parser.add_argument('image', type=str, help='Path to input image')
    parser.add_argument('--width', '-w', type=int, default=80, help='Output width (default: 80)')
    parser.add_argument('-o', '--output', type=str, help='Output file path (optional)')
    
    args = parser.parse_args()
    
    if args.width <= 0:
        print(f'Error: width must be greater than 0')
        import sys
        sys.exit(1)
    
    import sys
    from PIL import Image
    
    img = cv2.imread(args.image, 0)
    
    if img is None:
        print(f'Error: Cannot load image at path: {args.image}')
        sys.exit(1)
    
    pil_img = Image.open(args.image)
    is_gif = args.image.lower().endswith('.gif')
    
    if is_gif:
        if args.output:
            print(f'Error: --output is not supported for animated GIF input')
            sys.exit(1)
        
        try:
            n_frames = pil_img.n_frames
        except (AttributeError, ValueError):
            n_frames = 1
        
        import signal
        signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
        
        frame_height = 0

        pil_img.seek(0)
        rgb_frame = pil_img.convert('RGB')
        grayscale_init = cv2.cvtColor(np.array(rgb_frame), cv2.COLOR_RGB2GRAY)
        asciiArtInit = generateAscii(grayscale_init, args.width)
        text_lines_init = ascii_to_text(asciiArtInit).splitlines()
        frame_height = len(text_lines_init)

        for _ in range(frame_height):
            sys.stdout.write('\n')

        if frame_height > 0:
            sys.stdout.write(f'\033[{frame_height}A')

        sys.stdout.flush()

        while True:
            for frame_idx in range(n_frames):
                pil_img.seek(frame_idx)
                rgb_img = pil_img.convert('RGB')
                
                grayscale_frame = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2GRAY)
                
                asciiArt = generateAscii(grayscale_frame, args.width)
                text_lines = ascii_to_text(asciiArt).splitlines()

                for index in range(frame_height):
                    sys.stdout.write('\r\033[2K')

                    if index < len(text_lines):
                        sys.stdout.write(text_lines[index])

                    if index < frame_height - 1:
                        sys.stdout.write('\n')

                sys.stdout.flush()

                duration_ms = pil_img.info.get('duration', 0)
                if duration_ms:
                    import time
                    time.sleep(min(duration_ms / 750.0, 5))

                if frame_height > 1:
                    sys.stdout.write(f'\033[{frame_height - 1}A')
                    sys.stdout.write('\r')
                    sys.stdout.flush()

    else:
        asciiArt = generateAscii(img, args.width)
        text = ascii_to_text(asciiArt)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print(text, end='')
