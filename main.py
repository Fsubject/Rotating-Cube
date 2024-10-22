# Made entirely by Fsubject
import numpy as np
import pygame
import os
import settings
from object import Object
from camera import Camera


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
    materials = {"Default": settings.GREEN}

    try:
        with open(f"resources/{model_name}.mtl") as file:
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

            file.close()
    finally:
        return materials


def main() -> None:
    pygame.init()
    pygame.font.init()

    print()

    window = pygame.display.set_mode((settings.WIN_WIDTH, settings.WIN_HEIGHT), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    running = settings.RUN_LOOP

    pygame.display.set_caption("Rotating cube")

    # Init fonts
    mid_font = pygame.font.Font("resources/font/Silkscreen-Regular.ttf", 20)
    small_font = pygame.font.Font("resources/font/Silkscreen-Regular.ttf", 14)

    # Render static texts
    controls = [mid_font.render("[C] Toggle figure vertices", False, settings.L_GREY),
                mid_font.render("[UP] Increase rotation speed", False, settings.L_GREY),
                mid_font.render("[DOWN] Decrease rotation speed", False, settings.L_GREY),
                mid_font.render("[Z] Scale up figure", False, settings.L_GREY),
                mid_font.render("[S] Scale down figure", False, settings.L_GREY),
                mid_font.render("[W] Switch to another figure", False, settings.L_GREY),
                mid_font.render("[R] Reset figure settings", False, settings.L_GREY)]

    fps_offset = 0 if window.get_width() > settings.WIN_WIDTH else 60

    # Model
    camera = Camera()

    models_vertices, models_faces, models_materials, models_colors, list_models = retrieve_obj_files("resources")

    object_ = Object(window, camera, "cube", models_vertices["cube"], models_faces["cube"], models_colors["cube"], models_materials["cube"])

    # Settings
    show_controls = False
    editing = False

    while running:
        clock.tick(settings.MAX_FRAMERATE)
        window.fill(settings.BG)

        # Check for pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:  # Faster than if/elif/else
                    case pygame.K_ESCAPE:
                        running = False
                    case pygame.K_UP:
                        object_.rotation_speed += 0.01
                    case pygame.K_DOWN:
                        object_.rotation_speed -= 0.01
                    case pygame.K_w:
                        for i in range(len(list_models)):
                            if list_models[i] == object_.name:
                                if list_models[i] == list_models[-1]:
                                    object_ = Object(window, camera, list_models[0], models_vertices[list_models[0]], models_faces[list_models[0]], models_colors[list_models[0]], models_materials[list_models[0]])
                                    break
                                else:
                                    object_ = Object(window, camera, list_models[i + 1], models_vertices[list_models[i + 1]], models_faces[list_models[i + 1]], models_colors[list_models[i + 1]], models_materials[list_models[i + 1]])
                                    break
                            else:
                                i += 1
                    case pygame.K_c:
                        object_.show_vertices = False if object_.show_vertices is True else True # Ternary operator -> takes less place
                    case pygame.K_F1:
                        show_controls = False if show_controls is True else True
                    case pygame.K_r:
                        object_.reset()
                    case pygame.K_LCTRL:
                        editing = False if editing is True else True
            elif event.type == pygame.MOUSEMOTION:
                if editing:
                    object_.move_obj((event.rel[0], event.rel[1], 0))
            elif event.type == pygame.MOUSEWHEEL:
                if editing:
                    object_.move_obj((0, 0, event.y))

        # Camera
        camera.update()

        # Project object_ on the screen
        object_.project()

        object_.angle_x += object_.rotation_speed
        object_.angle_y += object_.rotation_speed

        # Render dynamic texts
        fps_text = mid_font.render(str(round(clock.get_fps())), False, settings.L_GREY)
        loaded_text = small_font.render(f"Current model: {object_.name}.obj", False, settings.L_GREY)
        cam_pos_text = small_font.render(f"{round(camera.pos[0], 3)}, {round(camera.pos[1], 3)}, {round(camera.pos[2], 3)}", False, settings.L_GREY)

        # Attach texts to the screen
        if show_controls:
            i = 0
            for text in controls:
                window.blit(text, (20, 20 + i))
                i += 30

        window.blit(fps_text, (settings.WIN_WIDTH - fps_offset, 20))
        window.blit(loaded_text, (20, settings.WIN_HEIGHT - 40))
        window.blit(cam_pos_text, (settings.WIN_WIDTH - 200, settings.WIN_HEIGHT - 40))

        pygame.display.flip()

    print("Exiting")
    pygame.quit()


if __name__ == "__main__":
    main()

# Made entirely by Fsubject
