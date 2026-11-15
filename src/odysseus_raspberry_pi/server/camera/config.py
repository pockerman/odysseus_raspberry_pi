import cv2

# (width, height) of the frames captured from the Pi camera
SCREEN_SIZE = (640, 480)

# JPEG encoding parameters passed to cv2.imencode
ENCODE_PARAMS = [cv2.IMWRITE_JPEG_QUALITY, 80]

# Delay, in seconds, between two consecutive captured frames
CAMERA_SLEEP_TIME = 0.05

# Camera mounting rotation in degrees, one of 0, 90, 180, 270
CAMERA_ROTATION = 0

# The generated square path of /odysseus/camera/square-path, see square_path.py

# Seconds between switching to the next side of the square
SQUARE_PATH_PERIOD = 5.0

# Seconds between two frames of the stream
SQUARE_PATH_FRAME_TIME = 0.05

# The side of the square, as a fraction of the frame height
SQUARE_PATH_SIDE = 0.5

# The width of the line, as a fraction of the frame height
SQUARE_PATH_LINE_WIDTH = 0.035
