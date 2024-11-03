import numpy as np


# All changes in the 3D space (rotation, scaling, ...) are done by multiplying the object vertices with a specific matrix
# Vertices' = Vertices x Matrix
# -> https://en.wikipedia.org/wiki/Rotation_matrix#Basic_3D_rotations
def rotate_x(angle: float) -> np.ndarray:
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])


def rotate_y(angle: float) -> np.ndarray:
    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])


def rotate_z(angle: float) -> np.ndarray:
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])


# A.K.A -> Euclidian distance formula
def get_points_distance(A, B) -> int:
    A_x, B_x = A[0], B[0]
    A_y, B_y = A[1], B[1]
    A_z, B_z = A[2], B[2]
    return np.sqrt(pow((A_x + B_x), 2) + pow((A_y + B_y), 2) + pow((A_z + B_z), 2))
