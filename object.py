# Made entirely by Fsubject
import math_func
import settings
import math_func as m_func
import numpy as np
import pygame
from camera import Camera


def load_material_file(file_name: str) -> dict:
    materials = {}

    try:
        with open(f"resources/{file_name}.mtl", "r") as file:
            actual_mtl = None
            for line in file:
                if line.startswith("newmtl"):
                    material_name = line.split(" ")[1][:-1] # [:-1] removes last char because it contains '\n'
                    materials[material_name] = None
                    actual_mtl = material_name
                elif actual_mtl is not None:
                    if line.startswith("Kd"):
                        Kd_data = line.split(" ")
                        materials[actual_mtl] = (float(Kd_data[1]) * 255, float(Kd_data[2]) * 255, float(Kd_data[3][:-1]) * 255)

            file.close()
    except FileNotFoundError:
        materials[settings.default_mtl_name] = settings.GREEN
    finally:
        print(materials)
        return materials


def load_obj_file(file_name: str, num_materials: int) -> tuple[np.ndarray, dict]:
    with open(f"resources/{file_name}.obj", "r") as file:
        vertices = []
        faces = {settings.default_mtl_name: []}

        actual_mtl = None
        for line in file:
            if line.startswith("v "):
                cleaned_line = line.split(" ")[1:]
                vertices.append([
                    float(cleaned_line[0]),
                    float(cleaned_line[1]),
                    float(cleaned_line[2][:-1])
                ])
            elif line.startswith("usemtl"):
                mtl_name = line.split(" ")[1][:-1]
                actual_mtl = mtl_name

                if faces.get(mtl_name) is None:
                    faces[mtl_name] = []
            elif line.startswith("f"):
                cleaned_line = line.split(" ")[1:]

                face = []
                for i in cleaned_line:
                    if i.endswith("\n"):
                        i = i[:-1]

                    if i.find("/"):
                        i = i.split("/")[0]

                    face.append(int(i) - 1)

                if actual_mtl is None:
                    faces[settings.default_mtl_name].append(face)
                else:
                    faces[actual_mtl].append(face)

        print(f"resources/{file_name}.obj has been loaded ({len(vertices)} vertices, {len(faces)} faces)")

        return np.array(vertices), faces


class Object:
    def __init__(self, window: pygame.surface.Surface, camera: Camera, model_name: str) -> None:
        self.window = window
        self.camera = camera

        self.model_name = model_name
        self.vertices = np.array([])
        self.faces = {}
        self.materials = {}

        self.pos = np.array([0, 0, 0])
        self.angle_x, self.angle_y, self.angle_z = 0, 0, 0
        self.scale = 1000
        self.rotation_speed = 0

        self.show_vertices = True

    def load(self) -> None:
        self.materials = load_material_file(self.model_name)
        self.vertices, self.faces = load_obj_file(self.model_name, len(self.materials))

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

            projection_matrix = math_func.perspective_matrix(self.camera.pos, vertex[2])
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
        for material_name in self.faces:
            for face_idx, face in enumerate(self.faces[material_name]):
                total_z_distance = 0
                for vertex_idx in face:
                    total_z_distance += m_func.get_points_distance(self.camera.pos, vertices_pos[vertex_idx])

                avg_z = total_z_distance / len(face)

                face_color = self.materials[material_name]

                temp_faces.append((face, avg_z, face_color))

        faces_arr = np.array(temp_faces, dtype=[("face", "O"), ("distance", "F"), ("color", "O")])
        faces_arr[::-1].sort(order="distance") # Since .sort() only does ascending sorting, use [::-1] to then reverse the list

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

            pygame.draw.polygon(self.window, color, polygon, 3 if color == settings.GREEN else 0)
