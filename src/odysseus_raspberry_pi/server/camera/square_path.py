"""
Generated frames of a square path, one side at a time.

No camera is involved. Each frame is a sheet of paper seen from above with one
side of a square drawn on it as a thick dark line. Every SQUARE_PATH_PERIOD
seconds the frame shows the next side, going counterclockwise as seen from
above: bottom, right, top, left. A robot that follows the line it sees drives
around the square, one side every period.

The square is centred in the frame, so the inside of the square is on the
left of a robot that drives the current side counterclockwise.
"""
import time

import cv2
import numpy as np

from odysseus_raspberry_pi.server.camera.config import (
    ENCODE_PARAMS,
    SCREEN_SIZE,
    SQUARE_PATH_FRAME_TIME,
    SQUARE_PATH_LINE_WIDTH,
    SQUARE_PATH_PERIOD,
    SQUARE_PATH_SIDE,
)

# The phase of the path is the same for every client: it starts with the server
_START = time.monotonic()


def square_corners(size=SCREEN_SIZE, side=SQUARE_PATH_SIDE):
    """
    The corners of the square in pixels, counterclockwise as seen from above,
    starting at the bottom left: bottom left, bottom right, top right, top left.
    Image rows grow downwards, so the bottom has the largest row
    """
    width, height = size
    half = side * height / 2.0
    cx, cy = width / 2.0, height / 2.0
    return [(cx - half, cy + half), (cx + half, cy + half),
            (cx + half, cy - half), (cx - half, cy - half)]


def side_frame(index, size=SCREEN_SIZE, side=SQUARE_PATH_SIDE, line_width=SQUARE_PATH_LINE_WIDTH):
    """
    The frame, in BGR, that shows side index (0 to 3) of the square: 0 is the
    bottom side, 1 the right, 2 the top and 3 the left
    """
    width, height = size
    # Paper, lit a little unevenly
    y, x = np.mgrid[0:height, 0:width].astype(np.float32)
    paper = 225.0 - 30.0 * (x / width + y / height) / 2.0
    frame = np.repeat(paper[:, :, None], 3, axis=2).astype(np.uint8)

    corners = square_corners(size, side)
    start = corners[index % 4]
    end = corners[(index + 1) % 4]
    thickness = max(2, int(round(line_width * height)))
    cv2.line(frame, (int(round(start[0])), int(round(start[1]))),
             (int(round(end[0])), int(round(end[1]))),
             color=(40, 40, 40), thickness=thickness, lineType=cv2.LINE_AA)
    return frame


def current_side(now=None, period=SQUARE_PATH_PERIOD):
    """
    The side to show at time now, from time.monotonic()
    """
    now = time.monotonic() if now is None else now
    return int((now - _START) // period) % 4


def encoded_side_frames():
    """
    The four frames as JPEG. They never change, so they are encoded once
    """
    frames = []
    for index in range(4):
        _, encoded = cv2.imencode('.jpg', side_frame(index), ENCODE_PARAMS)
        frames.append(encoded.tobytes())
    return frames


def square_path_generator(frame_time=SQUARE_PATH_FRAME_TIME):
    """
    Yield an MJPEG multipart stream of the current side of the square path
    """
    frames = encoded_side_frames()
    while True:
        frame = frames[current_side()]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Content-Length: ' + str(len(frame)).encode() + b'\r\n\r\n' + frame + b'\r\n')
        time.sleep(frame_time)
