import cv2
import os
import shutil
import time

# ASCII characters (dark → light)
ASCII_CHARS = "@%#*+=-:. "

def frame_to_ascii(frame, new_width=80):
    """
    Convert a video frame to ASCII art.
    """
    # Get terminal size
    cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    height, width = frame.shape

    # Adjust width to fit terminal
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 corrects aspect ratio for text
    if new_height > rows - 2:   # leave margin
        new_height = rows - 2

    # Resize frame
    resized = cv2.resize(frame, (new_width, new_height))

    # Map pixels to ASCII
    ascii_frame = ""
    for row in resized:
        for pixel in row:
            # Convert pixel to int to avoid overflow with uint8
            index = int(pixel) * len(ASCII_CHARS) // 256
            # Ensure index is within bounds
            index = max(0, min(index, len(ASCII_CHARS) - 1))
            ascii_frame += ASCII_CHARS[index]
        ascii_frame += "\n"

    return ascii_frame


def play_video(video_path="C:/Users/rinsu/Downloads/VID_20250630_163251911.mp4", width=100):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.03

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Convert frame → ASCII
            ascii_frame = frame_to_ascii(gray, width)

            # Clear screen & print
            os.system("cls" if os.name == "nt" else "clear")
            print(ascii_frame)

            # Control playback speed
            time.sleep(delay)
    finally:
        cap.release()


if __name__ == "__main__":
    # Use the default video path from the function definition
    play_video(width=100)
