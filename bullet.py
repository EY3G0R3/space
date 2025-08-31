import pygame

import state
from utils import find_collision, is_outside_screen_area


class Bullet:
    def __init__(self, parent, color, x, y, vx, vy, ax=0, ay=0):
        self.parent = parent
        self.radius = 1
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.accel_x = ax
        self.accel_y = ay

    def draw(self):
        pygame.draw.circle(state.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.vx += self.accel_x
        self.vy += self.accel_y
        self.x += self.vx
        self.y += self.vy
        self.draw()

        ship = find_collision(self.x, self.y, self.parent)
        if ship:
            ship.destroy()
            self.destroy()

    def destroy(self):
        if self in state.bullets:
            state.bullets.remove(self)

    def tick(self):
        self.move()

        if is_outside_screen_area(self.x, self.y):
            self.destroy()
