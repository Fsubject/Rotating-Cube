# Made entirely by Fsubject
import settings
import numpy as np
import pygame


def rotations_matrices(angle_x: float, angle_y: float, angle_z: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    # All changes in the 3D space (rotation, scaling, ...) are done by multiplying the object vertices with a specific matrix
    # Vertices' = Vertices x Matrix

    rotation_x_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])

    rotation_y_matrix = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    rotation_z_matrix = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])

    # https://en.wikipedia.org/wiki/Rotation_matrix#Basic_3D_rotations

    return rotation_x_matrix, rotation_y_matrix, rotation_z_matrix


def perspective_matrix(z_vertex) -> np.ndarray:
    z = 1 / (-settings.CAMERA[2] - z_vertex)
    return np.array([
        [z, 0, 0],
        [0, z, 0],
        [0, 0, 1]
    ])


def return_points_distance(A, B) -> int:
    A_x, B_x = A[0], B[0]
    A_y, B_y = A[1], B[1]
    A_z, B_z = A[2], B[2]
    return np.sqrt(pow((A_x + B_x), 2) + pow((A_y + B_y), 2) + pow((A_z + B_z), 2)) # Euclidian distance formula


class Object:
    def __init__(self, name: str, vertices: np.ndarray, faces: dict, colors: dict, materials: dict):
        self.vertices = vertices
        self.faces = faces
        self.name = name

        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.scale = 1000
        self.rotation_speed = 0

        # Coloring the model
        self.colors = colors
        self.Kd = materials

    def reset(self) -> None:
        self.scale = 1000
        self.rotation_speed = 0
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

    def project(self, window: pygame.surface.Surface, show_vertices: bool) -> None:
        rotation_x_matrix, rotation_y_matrix, rotation_z_matrix = rotations_matrices(self.angle_x, self.angle_y, self.angle_z)

        screen_vertices = [] # Vertices ready for the screen
        vertices_pos = [] # Actual position of the vertices (without the scaling up and everything...)
        for raw_vertex in self.vertices:
            vertex = np.dot(raw_vertex, rotation_x_matrix)
            vertex = np.dot(vertex, rotation_y_matrix)
            vertex = np.dot(vertex, rotation_z_matrix)

            projection_matrix = perspective_matrix(vertex[2])

            vertex = np.dot(vertex, projection_matrix)

            x = (vertex[0] * self.scale) + settings.WIN_WIDTH / 2  # PROBLEM: when a model is too big, scale it down isn't enough because it reverses
            y = (vertex[1] * self.scale) + settings.WIN_HEIGHT / 2  # at some point

            screen_vertices.append((float(x), float(y), float(vertex[2])))
            vertices_pos.append((float(vertex[0]), float(vertex[1]), float(vertex[2])))

            if show_vertices:
                pygame.draw.circle(window, settings.WHITE, (x, y), 4)  # Draw a vertex (a point) of the cube

        self.draw_polygons(window, screen_vertices, vertices_pos)

        # https://technology.cpm.org/general/3dgraph/

    def draw_polygons(self, window, screen_vertices, vertices_pos) -> None:
        temp_faces = []
        for i, face in enumerate(self.faces):
            z_distance = 0
            for vertex_idx in face:
                z_distance += return_points_distance(settings.CAMERA, vertices_pos[vertex_idx])

            avg_z = z_distance / len(face)

            face_color = None
            for color in self.colors:
                if i in self.colors[color]:
                    face_color = color

            temp_faces.append((face, avg_z, face_color))

        faces_arr = np.array(temp_faces, dtype=[("faces", "O"), ("distance", "f4"), ("color", "U100")])
        faces_arr[::-1].sort(order="distance", axis=0)

        i = 0
        for face, distance, color in faces_arr:
            if len(face) == 4:
                polygon = [
                    (screen_vertices[face[0]][0], screen_vertices[face[0]][1]),
                    (screen_vertices[face[1]][0], screen_vertices[face[1]][1]),
                    (screen_vertices[face[2]][0], screen_vertices[face[2]][1]),
                    (screen_vertices[face[3]][0], screen_vertices[face[3]][1])
                ]
            else:
                polygon = [
                    (screen_vertices[face[0]][0], screen_vertices[face[0]][1]),
                    (screen_vertices[face[1]][0], screen_vertices[face[1]][1]),
                    (screen_vertices[face[2]][0], screen_vertices[face[2]][1])
                ]

            pygame.draw.polygon(window, self.Kd[color], polygon, 0)
            i += 1
