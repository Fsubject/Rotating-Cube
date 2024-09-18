import settings
import numpy as np


def create_rotations_matrices(angle_x, angle_y, angle_z):
    rotation_x_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)],
    ])

    rotation_y_matrix = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)],
    ])

    rotation_z_matrix = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1],
    ])

    # https://en.wikipedia.org/wiki/Rotation_matrix#Basic_3D_rotations

    return rotation_x_matrix, rotation_y_matrix, rotation_z_matrix


class Object:
    def __init__(self, faces, vertices):
        self.faces = faces
        self.vertices = vertices

    def project(self, window, angles):
        rotation_x_matrix, rotation_y_matrix, rotation_z_matrix = create_rotations_matrices(angles[0], angles[1], angles[2])

