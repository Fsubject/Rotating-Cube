# Made entirely by Fsubject
import settings
import math_func as m_func
import numpy as np
import pygame


def perspective_matrix(camera, z_vertex) -> np.ndarray:
    z = 1 / (-camera[2] - z_vertex)
    return np.array([
        [z, 0, 0],
        [0, z, 0],
        [0, 0, z]
    ])


def perspective_projection2():
    fov = np.radians(90)
    aspect = 1920 / 1080
    near = 0.1
    far = 1000.0

    f = 1 / np.tan(fov / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -(2 * far * near) / (far - near), 0]
    ])


class Object:
    def __init__(self, window: pygame.surface.Surface, camera, name: str, vertices: np.ndarray, faces: dict, colors: dict, materials: dict) -> None:
        self.window = window
        self.camera = camera

        self.vertices = vertices
        self.faces = faces
        self.name = name

        self.pos = np.array([0, 0, 0])
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.scale = 1000
        self.rotation_speed = 0

        self.show_vertices = True

        # Coloring the model
        self.colors = colors
        self.materials = materials

    def reset(self) -> None:
        self.pos = np.array([0, 0, 0])
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.scale = 1000
        self.rotation_speed = 0

    def project(self) -> None:
        rotation_x_m = m_func.rotate_x(self.angle_x)
        rotation_y_m = m_func.rotate_y(self.angle_y)
        rotation_z_m = m_func.rotate_z(self.angle_z)

        screen_vertices = [] # Vertices ready for the screen
        vertices_pos = [] # Actual position of the vertices (without the scaling up and everything...)
        for raw_vertex in self.vertices:
            vertex = np.dot(raw_vertex, rotation_x_m)
            vertex = np.dot(vertex, rotation_y_m)
            vertex = np.dot(vertex, rotation_z_m)

            vertex[0] -= self.camera.pos[0]
            vertex[1] -= self.camera.pos[1]

            vertex = np.dot(vertex, self.camera.view_matrix)

            projection_matrix = perspective_matrix(self.camera.pos, vertex[2])
            vertex = np.dot(vertex, projection_matrix)

            x = ((vertex[0] * self.scale) + settings.WIN_WIDTH / 2) + self.pos[0]
            y = ((vertex[1] * self.scale) + settings.WIN_HEIGHT / 2) + self.pos[1]

            screen_vertices.append((float(x), float(y), float(vertex[2])))
            vertices_pos.append((float(vertex[0]), float(vertex[1]), float(vertex[2])))

            if self.show_vertices:
                pygame.draw.circle(self.window, settings.L_GREY, (x, y), 4)  # Draw a vertex (a point) of the cube

        self.draw_polygons(screen_vertices, vertices_pos)

        # https://technology.cpm.org/general/3dgraph/

    def draw_polygons(self, screen_vertices: list, vertices_pos: list) -> None:
        temp_faces = []
        for face_idx, face in enumerate(self.faces):
            z_distance = 0
            for vertex_idx in face:
                z_distance += m_func.get_points_distance(self.camera.pos, vertices_pos[vertex_idx])

            avg_z = z_distance / len(face)

            face_color = None
            for color in self.colors:
                if face_idx in self.colors[color]:
                    face_color = color

            temp_faces.append((face, avg_z, face_color))

        faces_arr = np.array(temp_faces, dtype=[("faces", "O"), ("distance", "F"), ("color", "U100")]) # https://www.w3schools.com/python/numpy/numpy_data_types.asp
        faces_arr[::-1].sort(order="distance", axis=0)

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

            pygame.draw.polygon(self.window, self.materials[color], polygon, 0)
