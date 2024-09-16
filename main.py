import numpy as np
import pygame
import settings


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


def connect_vertices(window, model, vertices_pos):
    if model == "cube":
        for faces in settings.CUBE["CUBE_FACES"]:
            pygame.draw.lines(window, settings.GREEN, True, (vertices_pos[faces[0]], vertices_pos[faces[1]], vertices_pos[faces[2]], vertices_pos[faces[3]]), 2)
    elif model == "strange":
        pygame.draw.lines(window, settings.GREEN, True, (vertices_pos[:4]), 2)
        pygame.draw.lines(window, settings.GREEN, True, (vertices_pos[:4]), 2)

        for i in range(4):
            pygame.draw.line(window, settings.GREEN, (vertices_pos[i][0], vertices_pos[i][1]),
                             (vertices_pos[4][0], vertices_pos[4][1]), 2)

        for i in range(4):
            pygame.draw.line(window, settings.GREEN, (vertices_pos[i][0], vertices_pos[i][1]),
                             (vertices_pos[5][0], vertices_pos[5][1]), 2)

    # OLD SYSTEM

    """if model == "cube":
        pygame.draw.line(window, settings.GREEN, (vertices_pos[0][0], vertices_pos[0][1]), (vertices_pos[3][0], vertices_pos[3][1]), 2)
        pygame.draw.line(window, settings.GREEN, (vertices_pos[7][0], vertices_pos[7][1]), (vertices_pos[4][0], vertices_pos[4][1]), 2)

        for i in range(7):
            pygame.draw.line(window, settings.GREEN, (vertices_pos[i][0], vertices_pos[i][1]), (vertices_pos[i + 1][0], vertices_pos[i + 1][1]), 2)

        pygame.draw.line(window, settings.GREEN, (vertices_pos[0][0], vertices_pos[0][1]), (vertices_pos[7][0], vertices_pos[7][1]), 2)
        pygame.draw.line(window, settings.GREEN, (vertices_pos[1][0], vertices_pos[1][1]), (vertices_pos[6][0], vertices_pos[6][1]), 2)
        pygame.draw.line(window, settings.GREEN, (vertices_pos[2][0], vertices_pos[2][1]), (vertices_pos[5][0], vertices_pos[5][1]), 2)
    elif model == "strange":
        pygame.draw.lines(window, settings.GREEN, True, (vertices_pos[:4]), 2)
        pygame.draw.lines(window, settings.GREEN, True, (vertices_pos[:4]), 2)

        for i in range(4):
            pygame.draw.line(window, settings.GREEN, (vertices_pos[i][0], vertices_pos[i][1]), (vertices_pos[4][0], vertices_pos[4][1]), 2)

        for i in range(4):
            pygame.draw.line(window, settings.GREEN, (vertices_pos[i][0], vertices_pos[i][1]), (vertices_pos[5][0], vertices_pos[5][1]), 2)"""

    # https://technology.cpm.org/general/3dgraph/


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

    # Cube settings
    cube_scale = 120
    show_vertices = True
    angle_x = 0
    angle_y = 0
    angle_z = 0
    rotation_speed = 0
    model = "cube"

    while running:
        clock.tick(60)
        window.fill(settings.BLACK)

        fps_text = nice_font.render(str(round(clock.get_fps())), False, settings.GREEN)

        # Check for pygame event #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_z:
                    cube_scale += 10
                elif event.key == pygame.K_s:
                    cube_scale -= 10
                elif event.key == pygame.K_UP:
                    rotation_speed += 0.01
                    rotation_speed += 0.01
                elif event.key == pygame.K_DOWN:
                    rotation_speed -= 0.01
                    rotation_speed -= 0.01
                elif event.key == pygame.K_c:
                    if show_vertices:
                        show_vertices = False
                    else:
                        show_vertices = True
                elif event.key == pygame.K_w:
                    if model == "cube":
                        model = "strange"
                    elif model == "strange":
                        model = "cube"

        rotation_x_matrix, rotation_y_matrix, rotation_z_matrix = create_rotations_matrices(angle_x, angle_y, angle_z)

        # All changes in the 3D space (rotation, scaling, ...) are done by multiplying the object vertices with a matrix
        # Vertices' = Vertices x Matrix

        angle_x += rotation_speed
        angle_y += rotation_speed

        if model == "cube":
            rotate_x = np.dot(settings.CUBE["CUBE_VERTICES"], rotation_x_matrix)
        elif model == "strange":
            rotate_x = np.dot(settings.STRANGE_VERTICES, rotation_x_matrix)
        else:
            rotate_x = np.dot(settings.CUBE["CUBE_VERTICES"], rotation_x_matrix)

        rotate_y = np.dot(rotate_x, rotation_y_matrix)
        rotate_z = np.dot(rotate_y, rotation_z_matrix)

        vertices_2d = np.dot(rotate_z, settings.PROJECTION_MATRIX)

        print(vertices_2d)
        print()

        vertices_pos = [] # WARNING: An objects in space is define by points called object vertices <----
        for vertex in vertices_2d:
            x = (vertex[0] * cube_scale) + settings.WIN_WIDTH / 2
            y = (vertex[1] * cube_scale) + settings.WIN_HEIGHT / 2

            vertices_pos.append((int(x), int(y)))  # Keep track of the vertices position

            if show_vertices:
                pygame.draw.circle(window, settings.WHITE, (x, y), 3)  # Draw a vertex of the cube

        connect_vertices(window, model, vertices_pos)

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

# Made by me (Fsubject)
