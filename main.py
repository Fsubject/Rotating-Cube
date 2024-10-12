# Made entirely by Fsubject
import numpy as np
import pygame
import os
import settings
from object import Object


def retrieve_obj_files(directory: str) -> tuple[dict, dict, dict, dict, list]:
    models_vertices = {}
    models_faces = {}
    models_materials = {}
    models_colors = {}
    list_models = []

    for file in os.listdir(directory):
        if file.endswith(".obj"):
            if file == "cube.obj":
                list_models.insert(0, file.split(".")[0])
            else:
                list_models.append(file.split(".")[0])

    for model_file_name in list_models:
        materials = get_materials(model_file_name)
        models_materials[model_file_name] = materials

        vertices, faces, faces_color = sort_obj_file(model_file_name)
        models_vertices[model_file_name] = vertices
        models_faces[model_file_name] = faces
        models_colors[model_file_name] = faces_color

    print()
    return models_vertices, models_faces, models_materials, models_colors, list_models


def sort_obj_file(file_name: str) -> tuple[np.ndarray, list, dict]:
    with open(f"resources/{file_name}.obj", "r") as file:
        vertices, faces, faces_color = [], [], {"Default": []}

        actual_mtl = None
        faces_i = 0
        for line in file:
            if line.startswith("v "):  # sorting v lines (vertex)
                sorted_line = line.split(" ")[1:]
                vertices.append([float(sorted_line[0]), float(sorted_line[1]), float(sorted_line[2])])
            elif line.startswith("usemtl"):
                material_name = line.split(" ")[1][:-1]
                faces_color[material_name] = []
                actual_mtl = material_name
            elif line.startswith("f "):  # sorting f lines (faces)
                temp_faces = []
                sorted_line = line.split(" ")

                for i in range(len(sorted_line)):
                    sorted_face_index = sorted_line[i].split("/")[0]

                    if sorted_face_index != "f" and sorted_face_index != "":
                        temp_faces.append(int(sorted_face_index) - 1)

                faces.append(temp_faces)

                if actual_mtl is not None:
                    faces_color[actual_mtl].append(faces_i)
                else:
                    faces_color["Default"].append(faces_i)

                faces_i += 1

        print(f"resources/{file_name}.obj has been loaded ({len(vertices)} vertices, {len(faces)} faces)")

        return np.array(vertices), faces, faces_color


def get_materials(model_name: str) -> dict:
    try:
        with open(f"resources/{model_name}.mtl") as file:
            materials = {}
            actual_mtl = None
            for line in file:
                if line.startswith("newmtl"):
                    material_name = line.split(" ")[1][:-1]
                    materials[material_name] = None
                    actual_mtl = material_name

                if actual_mtl is not None:
                    if line.startswith("Kd"):
                        Kd_data = line.split(" ")
                        materials[actual_mtl] = (float(Kd_data[1]) * 255, float(Kd_data[2]) * 255, float(Kd_data[3][:-1]) * 255)

            return materials
    except FileNotFoundError:
        print(f"WARNING: couldn't find the material file for the model: {model_name}")
        return {"Default": settings.GREEN}


def main() -> None:
    pygame.init()
    pygame.font.init()

    print()

    window = pygame.display.set_mode((settings.WIN_WIDTH, settings.WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = settings.RUN_LOOP

    pygame.display.set_caption("Rotating cube")

    # Init fonts
    mid_font = pygame.font.Font("resources/font/Silkscreen-Regular.ttf", 25)
    small_font = pygame.font.Font("resources/font/Silkscreen-Regular.ttf", 14)

    # Render static texts
    """controls = [mid_font.render("[C] Toggle figure vertices", False, settings.GREEN),
                mid_font.render("[UP - DOWN] Change rotation speed", False, settings.GREEN),
                mid_font.render("[Z - S] Change figure scale", False, settings.GREEN),
                mid_font.render("[W] Switch to another figure", False, settings.GREEN),
                mid_font.render("[F1] Hide controls", False, settings.GREEN)]"""
    controls = [mid_font.render("[C] Toggle figure vertices", False, settings.GREEN),
                mid_font.render("[UP] Increase rotation speed", False, settings.GREEN),
                mid_font.render("[DOWN] Decrease rotation speed", False, settings.GREEN),
                mid_font.render("[Z] Scale up figure", False, settings.GREEN),
                mid_font.render("[S] Scale down figure", False, settings.GREEN),
                mid_font.render("[W] Switch to another figure", False, settings.GREEN),
                mid_font.render("[R] Reset figure settings", False, settings.GREEN)]

    # Model
    models_vertices, models_faces, models_materials, models_colors, list_models = retrieve_obj_files("resources")

    object_ = Object("cube", models_vertices["cube"], models_faces["cube"], models_colors["cube"], models_materials["cube"])

    # Settings
    show_vertices = True
    show_controls = True

    while running:
        clock.tick(settings.MAX_FRAMERATE)
        window.fill((15, 15, 15))

        # Render dynamic texts
        fps_text = mid_font.render(str(round(clock.get_fps())), False, settings.GREEN)
        loaded_text = small_font.render(f"Current model: {object_.name}.obj", False, settings.GREEN)

        # Check for pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:  # Faster than if/elif/else
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_z:
                        settings.CAMERA += np.array([0, 0, 1])
                    case pygame.K_s:
                        settings.CAMERA -= np.array([0, 0, 1])
                    case pygame.K_UP:
                        object_.rotation_speed += 0.01
                    case pygame.K_DOWN:
                        object_.rotation_speed -= 0.01
                    case pygame.K_w:
                        for i in range(len(list_models)):
                            if list_models[i] == object_.name:
                                if list_models[i] == list_models[-1]:
                                    object_ = Object(list_models[0], models_vertices[list_models[0]], models_faces[list_models[0]], models_colors[list_models[0]], models_materials[list_models[0]])
                                    break
                                else:
                                    object_ = Object(list_models[i + 1], models_vertices[list_models[i + 1]], models_faces[list_models[i + 1]], models_colors[list_models[i + 1]], models_materials[list_models[i + 1]])
                                    break
                            else:
                                i += 1
                    case pygame.K_c:
                        show_vertices = False if show_vertices is True else True # Ternary operator -> takes less place
                    case pygame.K_F1:
                        show_controls = False if show_controls is True else True
                    case pygame.K_r:
                        object_.reset()

        # Project object_ on the screen
        object_.project(window, show_vertices)

        object_.angle_x += object_.rotation_speed
        object_.angle_y += object_.rotation_speed

        # Attach texts to the screen
        if show_controls:
            i = 0
            for text in controls:
                window.blit(text, (20, 20 + i))
                i += 30

        window.blit(fps_text, (1140, 20))
        window.blit(loaded_text, (20, 760))

        pygame.display.flip()

    print("Exiting")
    pygame.quit()


if __name__ == "__main__":
    main()

# Made entirely by Fsubject
