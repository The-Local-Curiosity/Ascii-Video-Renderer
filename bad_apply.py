import cv2
import numpy as np
import sys
import time
import os
import subprocess

# Terminal (given by you)
size = os.get_terminal_size()
TERM_COLS = size.columns
TERM_LINES = size.lines

# Half size as requested
OUT_W = TERM_COLS 
OUT_H = TERM_LINES 

# Printable ASCII range (33..126). 127 is DEL (non-printable) so excluded.
CHARS = "".join(chr(i) for i in range(33, 127))  # 94 chars: '!' .. '~'

def start_audio(video_path):
    # -nodisp: no window, just audio
    # -autoexit: stop when audio ends
    # -loglevel quiet: less spam
    return subprocess.Popen(
        ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", video_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def frame_to_ascii(frame_bgr, out_w=OUT_W, out_h=OUT_H):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (out_w, out_h), interpolation=cv2.INTER_AREA)

    n = len(CHARS)  # 94

    lines = []
    for row in resized:
        line_parts = []
        for I in row:
            I = int(I)

            # 1) Bucket intensity into n ranges -> CHARS
            # Brightest (255) -> index 0
            # Dimmest (0) -> index n-1
            bucket = (255 - I) * n // 256   # 0..n-1
            ch = CHARS[bucket]

            # 2) Use the *exact* intensity for grayscale color (232..255)
            color = 232 + (I * 23 // 255)

            # Render: bucket character + exact grayscale brightness
            line_parts.append(f"\x1b[38;5;{color}m{ch}\x1b[0m")

        lines.append("".join(line_parts))
    return "\n".join(lines)


def clear_screen():
    # ANSI clear + cursor home
    sys.stdout.write("\x1b[2J\x1b[H")


def main(video_path: str):
    if not os.path.exists(video_path):
        print(f"Video not found: {video_path}")
        sys.exit(1)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Could not open video.")
        sys.exit(1)

    fps = cap.get(cv2.CAP_PROP_FPS)
    if not fps or fps <= 0:
        fps = 30.0
    frame_delay = 1.0 / fps

    audio_proc = start_audio(video_path)
    try:
        start_time = time.time()
        prev_time = time.time()
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            ascii_frame = frame_to_ascii(frame)

            clear_screen()
            sys.stdout.write(ascii_frame)
            sys.stdout.flush()

            # keep roughly original FPS
            now = time.time()
            elapsed = now - prev_time
            sleep_time = frame_delay - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
            prev_time = time.time()

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sys.stdout.write("\n")
        sys.stdout.flush()
        if audio_proc and audio_proc.poll() is None:
            audio_proc.terminate()



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ascii_bad_apple.py <path_to_video>")
        sys.exit(0)

    main(sys.argv[1])
