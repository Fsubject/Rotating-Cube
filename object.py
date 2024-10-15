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


class Object:
    def __init__(self, window: pygame.surface.Surface, camera, name: str, vertices: np.ndarray, faces: dict, colors: dict, materials: dict):
        self.window = window
        self.camera = camera

        self.vertices = vertices
        self.faces = faces
        self.name = name

        self.x_pos, self.y_pos, self.z_pos = 0, 0, 0
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.scale = 1000
        self.rotation_speed = 0

        self.show_vertices = True

        # Coloring the model
        self.colors = colors
        self.materials = materials

    def reset(self) -> None:
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
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

            vertex = np.dot(vertex, self.camera.rotation)
            vertex[0] += self.camera.pos[0]
            vertex[1] += self.camera.pos[1]

            projection_matrix = perspective_matrix(self.camera.pos, vertex[2])
            vertex = np.dot(vertex, projection_matrix)

            x = ((vertex[0] * self.scale) + settings.WIN_WIDTH / 2) + self.x_pos
            y = ((vertex[1] * self.scale) + settings.WIN_HEIGHT / 2) + self.y_pos

            screen_vertices.append((float(x), float(y), float(vertex[2])))
            vertices_pos.append((float(vertex[0]), float(vertex[1]), float(vertex[2])))

            if self.show_vertices:
                pygame.draw.circle(self.window, settings.L_GREY, (x, y), 4)  # Draw a vertex (a point) of the cube

        self.draw_polygons(screen_vertices, vertices_pos)

        # https://technology.cpm.org/general/3dgraph/

    def draw_polygons(self, screen_vertices, vertices_pos) -> None:
        temp_faces = []
        for i, face in enumerate(self.faces):
            z_distance = 0
            for vertex_idx in face:
                z_distance += m_func.return_points_distance(self.camera.pos, vertices_pos[vertex_idx])

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

            pygame.draw.polygon(self.window, self.materials[color], polygon, 0)
            i += 1

    def move_pos(self, x, y, z):
        self.x_pos += x
        self.y_pos += y
        self.z_pos += z
