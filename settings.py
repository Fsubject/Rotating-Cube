import numpy as np

# Window settings
WIN_WIDTH, WIN_HEIGHT = 1200, 800
MAX_FRAMERATE = 60

RUN_LOOP = True

# Color
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Static projection matrix
PROJECTION_MATRIX = np.array([
    [1, 0, 0], # x
    [0, 1, 0], # y
    [0, 0, 0], # z
])
