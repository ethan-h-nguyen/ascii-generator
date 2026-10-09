import cv2
import numpy as np

symbols = [
    "$", "@", "B", "%", "8", "&", "W", "M", "#", "*", "o", "a", "h", "k", "b", "d", 
    "p", "q", "w", "m", "Z", "O", "0", "Q", "L", "C", "J", "U", "Y", "X", "z", "c", 
    "v", "u", "n", "x", "r", "j", "f", "t", "/", "\\", "|", "(", ")", "1", "{", "}", 
    "[", "]", "?", "-", "_", "+", "~", "<", ">", "i", "!", "l", "I", ";", ":", ",", 
    "\"", "^", "`", "'", "."
]

symbols.reverse()

thresholds = [i * (255/len(symbols)) for i in range(len(symbols))]

def ascii_to_text(array):
    return '\n'.join(''.join(symbols[c % len(symbols)] for c in row) for row in array)

def generateAscii(grayscale_img, target_width=None):
    if target_width is None:
        height, width = grayscale_img.shape
        newWidth = int(width / 5.5)
        newHeight = int(height / 9.5)
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
        
        cursor_y = 0
        prev_height = None
        
        for frame_idx in range(n_frames):
            pil_img.seek(frame_idx)
            rgb_img = pil_img.convert('RGB')
            
            grayscale_frame = cv2.cvtColor(np.array(rgb_img), cv2.COLOR_RGB2GRAY)
            
            asciiArt = generateAscii(grayscale_frame, args.width)
            text_lines = ascii_to_text(asciiArt).split('\n')
            frame_height = len(text_lines)
            
            if frame_idx > 0:
                sys.stdout.write(f'\033[{frame_height}A')
                sys.stdout.write('\r')
                
                for line in text_lines:
                    sys.stdout.write('\033[2K')
                    sys.stdout.write(line)
                    sys.stdout.write('\n')
                    sys.stdout.flush()
                
            else:
                for line in text_lines:
                    sys.stdout.write(line)
                    sys.stdout.write('\n')
                    sys.stdout.flush()
            
            cursor_y += frame_height
            prev_height = frame_height
            
            if frame_idx < n_frames - 1:
                duration_ms = pil_img.info.get('duration', 0)
                if duration_ms:
                    import time
                    time.sleep(min(duration_ms / 1000.0, 5))
        print()
    else:
        asciiArt = generateAscii(img, args.width)
        text = ascii_to_text(asciiArt)
        
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print(text, end='')
