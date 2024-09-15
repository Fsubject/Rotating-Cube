import numpy as np
import pygame
from settings import *


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


def connect_points(window, points_pos):
    pygame.draw.line(window, GREEN, (points_pos[0][0], points_pos[0][1]), (points_pos[3][0], points_pos[3][1]))
    pygame.draw.line(window, GREEN, (points_pos[7][0], points_pos[7][1]), (points_pos[4][0], points_pos[4][1]))

    for i in range(7):
        pygame.draw.line(window, GREEN, (points_pos[i][0], points_pos[i][1]),
                         (points_pos[i + 1][0], points_pos[i + 1][1]))

    pygame.draw.line(window, GREEN, (points_pos[0][0], points_pos[0][1]), (points_pos[7][0], points_pos[7][1]))
    pygame.draw.line(window, GREEN, (points_pos[1][0], points_pos[1][1]), (points_pos[6][0], points_pos[6][1]))
    pygame.draw.line(window, GREEN, (points_pos[2][0], points_pos[2][1]), (points_pos[5][0], points_pos[5][1]))

    """pygame.draw.lines(window, GREEN, True, (points_pos[:4]))
    pygame.draw.lines(window, GREEN, True, (points_pos[:4]))

    for i in range(4):
        pygame.draw.line(window, GREEN, (points_pos[i][0], points_pos[i][1]), (points_pos[4][0], points_pos[4][1]))

    for i in range(4):
        pygame.draw.line(window, GREEN, (points_pos[i][0], points_pos[i][1]), (points_pos[5][0], points_pos[5][1]))"""

    # https://technology.cpm.org/general/3dgraph/


def main():
    pygame.init()
    pygame.font.init()

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("Rotating cube")

    # Font settings / texts
    nice_font = pygame.font.Font("resources/Silkscreen-Regular.ttf", 25)
    controls = [nice_font.render("[C] Toggle cube points", False, GREEN),
                nice_font.render("[UP] Increase rotation speed", False, GREEN),
                nice_font.render("[DOWN] Decrease rotation speed", False, GREEN),
                nice_font.render("[Z] Scale up cube", False, GREEN),
                nice_font.render("[S] Scale down cube", False, GREEN)]

    # Cube settings
    cube_scale = 120
    toggle_draw_point = True
    angle_x = 0
    angle_y = 0
    angle_z = 0
    rotation_speed = 0

    while running:
        clock.tick(60)
        window.fill(BLACK)

        # Check for pygame event #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
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
                    if toggle_draw_point:
                        toggle_draw_point = False
                    else:
                        toggle_draw_point = True

        rotation_x_matrix, rotation_y_matrix, rotation_z_matrix = create_rotations_matrices(angle_x, angle_y, angle_z)

        angle_x += rotation_speed
        angle_y += rotation_speed

        rotate_x = np.dot(model, rotation_x_matrix)
        rotate_y = np.dot(rotate_x, rotation_y_matrix)
        rotate_z = np.dot(rotate_y, rotation_z_matrix)

        points_2d = np.dot(rotate_z, projection_matrix)

        print(points_2d)
        print()

        points_pos = []
        for point in points_2d:
            x = (point[0] * cube_scale) + WIN_WIDTH / 2
            y = (point[1] * cube_scale) + WIN_HEIGHT / 2

            points_pos.append((int(x), int(y)))  # Keep track of the points position

            if toggle_draw_point:
                pygame.draw.circle(window, WHITE, (x, y), 3)  # Draw a point of the cube

        connect_points(window, points_pos)

        i = 0
        for text in controls:
            i += 30
            window.blit(text, (40, 10 + i))

        pygame.display.flip()

    print("Exiting")
    pygame.quit()


if __name__ == "__main__":
    main()

# Made by me (Fsubject)
