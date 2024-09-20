import settings
import numpy as np
import pygame


def create_rotations_matrices(angle_x, angle_y, angle_z):
    # All changes in the 3D space (rotation, scaling, ...) are done by multiplying the object vertices with a specific matrix
    # Vertices' = Vertices x Matrix

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
    def __init__(self, name, vertices, faces):
        self.vertices = vertices
        self.faces = faces
        self.name = name

        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.scale = 120
        self.rotation_speed = 0

        # Test
        #self.Kd = Kd

    def reset(self):
        self.scale = 120
        self.rotation_speed = 0
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def project(self, window, show_vertices):
        rotation_x_matrix, rotation_y_matrix, rotation_z_matrix = create_rotations_matrices(self.angle_x, self.angle_y, self.angle_z)

        rotate_x = np.dot(self.vertices, rotation_x_matrix)
        rotate_y = np.dot(rotate_x, rotation_y_matrix)
        rotate_z = np.dot(rotate_y, rotation_z_matrix)

        multiplied_vertices = np.dot(rotate_z, settings.PROJECTION_MATRIX)

        # WARNING: An objects in space is define by points called object vertices <----
        vertices_pos = []
        for vertex in multiplied_vertices:
            x = (vertex[0] * self.scale) + settings.WIN_WIDTH / 2 # PROBLEM: when a model is too big, scale it down isn't enough because it reverses
            y = (vertex[1] * self.scale) + settings.WIN_HEIGHT / 2         # at some point

            vertices_pos.append((float(x), float(y)))  # Keep track of the vertices position

            if show_vertices:
                pygame.draw.circle(window, settings.WHITE, (x, y), 4)  # Draw a vertex (a point) of the cube

        for face in self.faces:
            if len(face) == 4:
                pygame.draw.polygon(window, settings.GREEN, (vertices_pos[face[0]], vertices_pos[face[1]], vertices_pos[face[2]], vertices_pos[face[3]]), 2)
            elif len(face) == 3:
                pygame.draw.polygon(window, settings.GREEN, (vertices_pos[face[0]], vertices_pos[face[1]], vertices_pos[face[2]]), 2)

            # Testing
            """if len(face) == 4:
                pygame.draw.polygon(window, (), (vertices_pos[face[0]], vertices_pos[face[1]], vertices_pos[face[2]], vertices_pos[face[3]]), 0)
            elif len(face) == 3:
                pygame.draw.polygon(window, (), (vertices_pos[face[0]], vertices_pos[face[1]], vertices_pos[face[2]]), 0)"""

            # https://www.pygame.org/docs/ref/draw.html

        # https://technology.cpm.org/general/3dgraph/
