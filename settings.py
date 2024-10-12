import numpy as np

# Window settings
WIN_WIDTH, WIN_HEIGHT = 1200, 800
MAX_FRAMERATE = 60

RUN_LOOP = True

# Colors
BG = (15, 15, 15)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 153)
WHITE = (255, 255, 255)

# Static projection matrix (https://en.wikipedia.org/wiki/Orthographic_projection < Perspective projection)
# http://matrixmultiplication.xyz/
PROJECTION_MATRIX = np.array([
    [1, 0, 0], # x
    [0, 1, 0], # y
    [0, 0, 0] # z
])

CAMERA = np.array([0, 1, -9])

CUBE_FACE_COLOR = [GREEN, RED, BLUE, WHITE, GREEN, RED, BLUE, WHITE]
