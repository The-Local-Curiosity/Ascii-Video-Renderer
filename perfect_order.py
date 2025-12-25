from PIL import Image, ImageDraw, ImageFont
import os

def find_mono_font():
    candidates = [
        r"C:\Windows\Fonts\CascadiaMono.ttf",
        r"C:\Windows\Fonts\CascadiaCode.ttf",
        r"C:\Windows\Fonts\consola.ttf",   # Consolas
        r"C:\Windows\Fonts\lucon.ttf",     # Lucida Console
        r"C:\Windows\Fonts\cour.ttf",      # Courier New (sometimes)
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def build_ramp(chars, font_path, font_size=18):
    font = ImageFont.truetype(font_path, font_size)

    scores = []
    # generous canvas so glyph isn't clipped
    W, H = font_size * 3, font_size * 3

    for ch in chars:
        img = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(img)
        d.text((0, 0), ch, 255, font=font)
        ink = sum(img.getdata())  # higher = more filled
        scores.append((ink, ch))

    scores.sort(reverse=True)  # densest first
    return "".join(ch for _, ch in scores)

if __name__ == "__main__":
    font_path = find_mono_font()
    if not font_path:
        raise SystemExit("No known monospace font found in C:\\Windows\\Fonts")

    print("Using font:", font_path)

    chars = "".join(chr(i) for i in range(32, 127))  # include space
    ramp = build_ramp(chars, font_path, font_size=18)
    print(ramp)
