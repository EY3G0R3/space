import random
import pygame

import state
from utils import percentage_chance, is_outside_screen_area


class Star:
    def __init__(self):
        self.radius = random.randint(2, 3)
        self.color = random.choice(["white", "lightgray", "darkgray"])
        if percentage_chance(50):
            self.x = random.randint(0, state.screen.get_width())
            self.y = 0
        else:
            self.x = 0
            self.y = random.randint(0, state.screen.get_height())

    def draw(self):
        pygame.draw.circle(state.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += 4
        self.y += 2
        self.draw()

    def tick(self):
        self.move()
        if is_outside_screen_area(self.x, self.y):
            if self in state.stars:
                state.stars.remove(self)
