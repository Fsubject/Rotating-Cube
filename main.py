import numpy as np
import pygame
import os
import settings
from object import Object


def retrieve_models(directory):
    models_vertices = {}
    models_faces = {}
    list_models = []

    for file in os.listdir(directory):
        if file.endswith(".obj"):
            list_models.append(file.split(".")[0])

    for model_file_name in list_models:
        vertices, faces = import_obj_file(model_file_name)
        models_vertices[model_file_name] = vertices
        models_faces[model_file_name] = faces

    return models_vertices, models_faces, list_models


def import_obj_file(file_name):
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

                    if sorted_face_index != "f":
                        temp_faces.append(int(sorted_face_index) - 1)

                faces.append(temp_faces)

        return np.array(vertices), faces


def main():
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((settings.WIN_WIDTH, settings.WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("Rotating cube")

    # Font settings / texts
    nice_font = pygame.font.Font("resources/Silkscreen-Regular.ttf", 25)

    controls = [nice_font.render("[C] Toggle figure vertices", False, settings.GREEN),
                nice_font.render("[UP] Increase rotation speed", False, settings.GREEN),
                nice_font.render("[DOWN] Decrease rotation speed", False, settings.GREEN),
                nice_font.render("[Z] Scale up figure", False, settings.GREEN),
                nice_font.render("[S] Scale down figure", False, settings.GREEN),
                nice_font.render("[W] Switch to another figure", False, settings.GREEN)]

    # Model
    models_vertices, models_faces, list_models = retrieve_models("resources")

    object_ = Object("cube", models_vertices["cube"], models_faces["cube"])

    # Settings
    show_vertices = True

    while running:
        clock.tick(60)
        window.fill(settings.BLACK)
        fps_text = nice_font.render(str(round(clock.get_fps())), False, settings.GREEN)

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
                elif event.key == pygame.K_c:
                    if show_vertices:
                        show_vertices = False
                    else:
                        show_vertices = True
                elif event.key == pygame.K_w:
                    for i in range(len(list_models)):
                        if list_models[i] == object_.name:
                            if list_models[i] == list_models[-1]:
                                object_ = Object(list_models[0], models_vertices[list_models[0]], models_faces[list_models[0]])
                            else:
                                object_ = Object(list_models[i + 1], models_vertices[list_models[i + 1]], models_faces[list_models[i + 1]])
                                break
                        else:
                            i += 1
                elif event.key == pygame.K_r:
                    object_.reset()

        # Project object_
        object_.project(window, object_.scale, show_vertices)

        object_.angle_x += object_.rotation_speed
        object_.angle_y += object_.rotation_speed

        # Attach texts to the screen
        i = 0
        for text in controls:
            window.blit(text, (30, 20 + i))
            i += 30

        window.blit(fps_text, (1140, 20))

        pygame.display.flip()

    print("Exiting")
    pygame.quit()


if __name__ == "__main__":
    main()

# Made 100% by Fsubject
