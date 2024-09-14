import numpy as np
import math
import pygame

WIN_WIDTH, WIN_HEIGHT = 1200, 800

projection_matrix = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
])

cube_matrix = np.array([ # All the cube points in a matrix created with numpy
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1]
])


def create_rotation_matrix(angle_x, angle_y, angle_z):
    rotation_x_matrix = np.array([
        [1, 0, 0],
        [0, math.cos(angle_x), -math.sin(angle_x)],
        [0, math.sin(angle_x), math.cos(angle_x)],
    ])

    rotation_y_matrix = np.array([
        [math.cos(angle_y), 0, math.sin(angle_y)],
        [0, 1, 0],
        [-math.sin(angle_y), 0, math.cos(angle_y)],
    ])

    rotation_z_matrix = np.array([
        [math.cos(angle_z), -math.sin(angle_z), 0],
        [math.sin(angle_z), math.cos(angle_z), 0],
        [0, 0, 1],
    ])

    # https://en.wikipedia.org/wiki/Rotation_matrix#Basic_3D_rotations <---

    return rotation_x_matrix, rotation_y_matrix, rotation_z_matrix


def connect_points(window, points_pos):
    for i in range(8):
        for j in range(8):
            pygame.draw.line(window, (0, 255, 0), (points_pos[i][0], points_pos[i][1]), (points_pos[j][0], points_pos[j][1]))


def main():
    pygame.init()

    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    pygame.display.set_caption("Rotating cube - Fsubject")

    angle_x = 0
    angle_y = 0
    angle_z = 0

    while running:
        clock.tick(60)
        window.fill((0, 0, 0))

        # Check for pygame event #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle_x += 0.01
                    angle_y += 0.01
                elif event.key == pygame.K_DOWN:
                    angle_x -= 0.01
                    angle_y -= 0.01

        rotation_x_matrix, rotation_y_matrix, rotation_z_matrix = create_rotation_matrix(angle_x, angle_y, angle_z)

        angle_x += 0.01
        angle_y += 0.01

        rotate_x = np.dot(cube_matrix, rotation_x_matrix)
        rotate_y = np.dot(rotate_x, rotation_y_matrix)
        rotate_z = np.dot(rotate_y, rotation_z_matrix)

        points_2d = np.dot(rotate_z, projection_matrix)

        print(points_2d)
        print("\n")

        points_pos = []
        for point in points_2d:
            x = (point[0] * 100) + WIN_WIDTH / 2
            y = (point[1] * 100) + WIN_HEIGHT / 2

            points_pos.append((int(x), int(y))) # Keep track of the points position

            pygame.draw.circle(window, (255, 255, 255), (x, y), 3) # Draw a point of the cube

        connect_points(window, points_pos)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

# Made by me (Fsubject)
