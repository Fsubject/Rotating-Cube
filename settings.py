import numpy as np
import ctypes

# Window settings
WIN_WIDTH, WIN_HEIGHT = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)
MAX_FRAMERATE = 60

RUN_LOOP = True

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
L_GREY = (190, 190, 190)
BG = (15, 15, 15)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 153)

# Static projection matrix (https://en.wikipedia.org/wiki/Orthographic_projection < Perspective projection)
# http://matrixmultiplication.xyz/
PROJECTION_MATRIX = np.array([
    [1, 0, 0], # x
    [0, 1, 0], # y
    [0, 0, 0] # z
])

CUBE_FACE_COLOR = [GREEN, RED, BLUE, WHITE, GREEN, RED, BLUE, WHITE]
