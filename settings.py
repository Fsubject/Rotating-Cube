import numpy as np

# Window settings
WIN_WIDTH, WIN_HEIGHT = 1200, 800

# Color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Matrices
PROJECTION_MATRIX = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])

CUBE_VERTICES = np.array([ # All the cube points in a matrix created with numpy
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [1, 1, -1], # Front face

    [-1, -1, -1], # Back faces
    [-1, -1, 1],
    [-1, 1, 1],
    [-1, 1, -1]
])

CUBE_FACES = [
    [0, 1, 2, 3], # Front
    [3, 2, 6, 7], # Right
    [7, 4, 5, 6], # Middle
    [0, 1, 5, 4], # Left
    [0, 4, 7, 3], # Bottom
    [1, 5, 6, 2]  # Top
]

STRANGE_VERTICES = np.array([
    [-1, -1, 0],
    [1, -1, 0],
    [1, 1, 0],
    [-1, 1, 0],
    [0, 0, 2], # Pyramid top
    [0, 0, -2] # Pyramid bottom
])
