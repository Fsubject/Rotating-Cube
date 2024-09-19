# Made entirely by Fsubject
import numpy as np
import pygame
import os
import settings
from object import Object


def retrieve_obj_files(directory):
    models_vertices = {}
    models_faces = {}
    list_models = []

    for file in os.listdir(directory):
        if file.endswith(".obj"):
            if file == "cube.obj":
                list_models.insert(0, file.split(".")[0])
            elif file == "pyramid.obj":
                list_models.insert(1, file.split(".")[0])
            else:
                list_models.append(file.split(".")[0])

    for model_file_name in list_models:
        vertices, faces = sort_obj_file(model_file_name)
        models_vertices[model_file_name] = vertices
        models_faces[model_file_name] = faces

    print()
    return models_vertices, models_faces, list_models


def sort_obj_file(file_name):
    with open(f"resources/{file_name}.obj", "r") as file:
        vertices, faces = [], []

        lines = file.read().splitlines()

        for line in lines:
            if line.startswith("v "):
                sorted_line = line.split(" ")[1:]
                vertices.append([float(sorted_line[0]), float(sorted_line[1]), float(sorted_line[2])])
            elif line.startswith("f "):
                temp_faces = []
                sorted_line = line.split(" ")

                for i in range(len(sorted_line)):
                    sorted_face_index = sorted_line[i].split("/")[0]

                    if sorted_face_index != "f" and sorted_face_index != "":
                        temp_faces.append(int(sorted_face_index) - 1)

                faces.append(temp_faces)

        print(f"{file_name}.obj has been loaded ({len(vertices)} vertices, {len(faces)} faces)")

        return np.array(vertices), faces


def main():
    pygame.init()
    pygame.font.init()

    print()

    window = pygame.display.set_mode((settings.WIN_WIDTH, settings.WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("Rotating cube")

    # Init fonts
    mid_font = pygame.font.Font("resources/Silkscreen-Regular.ttf", 25)
    small_font = pygame.font.Font("resources/Silkscreen-Regular.ttf", 14)

    # Render static texts
    controls = [mid_font.render("[C] Toggle figure vertices", False, settings.GREEN),
                mid_font.render("[UP] Increase rotation speed", False, settings.GREEN),
                mid_font.render("[DOWN] Decrease rotation speed", False, settings.GREEN),
                mid_font.render("[Z] Scale up figure", False, settings.GREEN),
                mid_font.render("[S] Scale down figure", False, settings.GREEN),
                mid_font.render("[W] Switch to another figure", False, settings.GREEN)]

    # Model
    models_vertices, models_faces, list_models = retrieve_obj_files("resources")

    object_ = Object("cube", models_vertices["cube"], models_faces["cube"])

    # Settings
    show_vertices = True
    show_controls = True

    while running:
        clock.tick(settings.MAX_FRAMERATE)
        window.fill(settings.BLACK)

        # Render dynamic texts
        fps_text = mid_font.render(str(round(clock.get_fps())), False, settings.GREEN)
        loaded_text = small_font.render(f"Currently loaded: {object_.name}.obj", False, settings.GREEN)

        # Check for pygame event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_z:
                    object_.scale += 20
                elif event.key == pygame.K_s:
                    object_.scale -= 20
                elif event.key == pygame.K_UP:
                    object_.rotation_speed += 0.01
                elif event.key == pygame.K_DOWN:
                    object_.rotation_speed -= 0.01
                elif event.key == pygame.K_w:
                    for i in range(len(list_models)):
                        if list_models[i] == object_.name:
                            if list_models[i] == list_models[-1]:
                                object_ = Object(list_models[0], models_vertices[list_models[0]], models_faces[list_models[0]])
                                break
                            else:
                                object_ = Object(list_models[i + 1], models_vertices[list_models[i + 1]], models_faces[list_models[i + 1]])
                                break
                        else:
                            i += 1
                elif event.key == pygame.K_c:
                    if show_vertices:
                        show_vertices = False
                    else:
                        show_vertices = True
                elif event.key == pygame.K_F1:
                    if show_controls:
                        show_controls = False
                    else:
                        show_controls = True
                elif event.key == pygame.K_r:
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
