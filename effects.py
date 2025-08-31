import random
import pygame

import state


class DeathFX:
    def __init__(self, x, y):
        self.radius = 5
        self.color = random.choice(["yellow", "orange", "red"])
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(state.screen, self.color, (self.x, self.y), self.radius)

    def tick(self):
        self.radius += 5
        self.draw()

        if self.radius > random.randint(100, 200):
            self.destroy()

    def destroy(self):
        if self in state.deaths:
            state.deaths.remove(self)
