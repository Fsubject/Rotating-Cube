import pygame
import numpy as np
import math_func as m_func


class Camera:
    def __init__(self) -> None:
        self.pos = np.array([0.0, 0.0, -10.0])
        self.target = np.array([0.0, 0.0, 0.0])
        self.world_up = np.array([0, 1, 0])

        self.speed = 0.2
        #self.view_matrix = self.get_view_matrix()

    def update(self) -> None:
        self.handle_inputs()
        #self.view_matrix = self.get_view_matrix()

    def handle_inputs(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.pos[2] += self.speed
        if keys[pygame.K_s]:
            self.pos[2] -= self.speed
        if keys[pygame.K_q]:
            self.pos[0] -= self.speed
        if keys[pygame.K_d]:
            self.pos[0] += self.speed
        if keys[pygame.K_a]:
            self.pos[1] += self.speed
        if keys[pygame.K_e]:
            self.pos[1] -= self.speed

    def get_view_matrix(self) -> np.ndarray:
        forward = self.target - self.pos
        forward = forward / np.linalg.norm(forward) # normalize the forward vector to have a length unit (x, y, z)

        right = np.cross(forward, self.world_up)
        right = right / np.linalg.norm(right)

        up = np.cross(right, forward)
        up = up / np.linalg.norm(up)

        return np.array([ # view matrix
            [right[0], right[1], right[2]],
            [up[0], up[1], up[2]],
            [forward[0], forward[1], forward[2]]
        ])
