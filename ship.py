import random
import pygame

import state
from utils import is_inside_screen_area, percentage_chance
from bullet import Bullet
from effects import DeathFX


class Ship:
    def __init__(self):
        self.radius = random.randint(5, 15)
        self.color = random.choice(["yellow", "blue", "orange", "pink", "cyan"])
        self.x = random.randint(0, state.screen.get_width())
        self.y = random.randint(0, state.screen.get_height())
        self.change_direction()

    def change_direction(self):
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def draw(self):
        pygame.draw.circle(state.screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if is_inside_screen_area(new_x, new_y):
            self.x = new_x
            self.y = new_y

        self.draw()

    def destroy(self):
        state.deaths.append(DeathFX(self.x, self.y))
        if self in state.ships:
            state.ships.remove(self)
        state.ships.append(Ship())

    def choose_random_target(self):
        for _ in range(0, 5):
            index = random.randrange(0, len(state.ships))
            if state.ships[index] != self:
                return state.ships[index]
        return None  # couldn't find a suitable target

    def tick(self):
        if self == state.player:  # do nothing, controlled by the player (future)
            self.draw()
            return

        if percentage_chance(5):
            self.change_direction()

        self.move()

        if percentage_chance(2):
            target = self.choose_random_target()
            if not target:
                return

            distance_x = target.x - self.x
            distance_y = target.y - self.y

            bullet_velocity_x = distance_x / 500
            bullet_velocity_y = distance_y / 500

            color = self.color
            bullet1 = Bullet(
                self, color, self.x, self.y, bullet_velocity_x, bullet_velocity_y
            )
            bullet2 = Bullet(
                self, color, self.x, self.y, bullet_velocity_x, bullet_velocity_y
            )
            bullet3 = Bullet(
                self, color, self.x, self.y, bullet_velocity_x, bullet_velocity_y
            )
            bullet1.move()
            bullet1.move()
            bullet1.move()
            bullet1.move()
            bullet2.move()
            bullet2.move()
            state.bullets.append(bullet1)
            state.bullets.append(bullet2)
            state.bullets.append(bullet3)
