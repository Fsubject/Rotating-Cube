import settings
import math_func as m_func
import pygame
import numpy as np


class Camera:
    def __init__(self):
        self.pos = np.array([0.0, 0.0, -10.0])

        self.speed = 0.065
        self.rotation_speed = 0.0035

        self.angle_x = 0
        self.angle_y = 0
        self.rotation = self.cam_rotation()

    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        mouse_rel = pygame.mouse.get_rel()

        if keys[pygame.K_z]:
            self.pos[2] += self.speed
        if keys[pygame.K_s]:
            self.pos[2] -= self.speed
        if keys[pygame.K_q]:
            self.pos[0] += self.speed
        if keys[pygame.K_d]:
            self.pos[0] -= self.speed
        if keys[pygame.K_a]:
            self.pos[1] += self.speed
        if keys[pygame.K_e]:
            self.pos[1] -= self.speed

        if mouse_rel[0] != 0:
            if pygame.mouse.get_pressed()[0]:
                self.angle_y += mouse_rel[0] * self.rotation_speed

        if mouse_rel[1] != 0:
            if pygame.mouse.get_pressed()[0]:
                self.angle_x += mouse_rel[1] * self.rotation_speed

        self.rotation = self.cam_rotation()

    def cam_rotation(self):
        rotation_x_m = m_func.rotate_x(self.angle_x)
        rotation_y_m = m_func.rotate_y(self.angle_y)
        return np.dot(rotation_x_m, rotation_y_m)
