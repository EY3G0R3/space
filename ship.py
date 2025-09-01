import random
import math
import pygame

import state
import utils
from bullet import Bullet
from effects import DeathFX


class Ship:
    def __init__(self):
        self.radius = random.randint(20, 20)
        self.color = random.choice(["yellow", "blue", "orange", "pink", "cyan"])
        self.x = random.randint(0, state.screen.get_width())
        self.y = random.randint(0, state.screen.get_height())
        # Cache last facing angle so stationary ships keep orientation
        self._angle = random.uniform(0, math.tau)
        self.change_direction()

    def change_direction(self):
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def draw(self):
        # Determine facing based on velocity; keep previous if stationary
        if self.vx != 0 or self.vy != 0:
            self._angle = math.atan2(self.vy, self.vx)

        size = self.radius

        # Define a simple ship hull in model space (pointing +X)
        # Nose, top tail, bottom tail, plus small fins for flair
        hull = [
            (size, 0),  # nose
            (-0.6 * size, -0.5 * size),
            (-0.2 * size, 0),
            (-0.6 * size, 0.5 * size),
        ]

        # Rotation matrix
        c = math.cos(self._angle)
        s = math.sin(self._angle)

        def transform(pt):
            px, py = pt
            rx = px * c - py * s
            ry = px * s + py * c
            return (int(self.x + rx), int(self.y + ry))

        hull_pts = [transform(p) for p in hull]

        # Draw filled hull and a crisp outline
        pygame.draw.polygon(state.screen, self.color, hull_pts)
        pygame.draw.polygon(state.screen, "white", hull_pts, 2)

        # Engine glow at tail center
        tail_local = (-0.65 * size, 0)
        tail_world = transform(tail_local)
        flame_color = random.choice(["orange", "yellow", "red"]) if (self.vx or self.vy) else "gray"
        pygame.draw.circle(state.screen, flame_color, tail_world, max(2, int(size * 0.2)))

    def move(self):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if utils.is_inside_screen_area(new_x, new_y):
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

    def shoot_at_target(self, target):
        if not target:
            print("target need to be set")
            return

        distance = utils.distance(self.x, self.y, target.x, target.y)

        if distance < 500:
            self.shoot_laser(target)
        elif distance < 1000:
            self.shoot_machinegun(target)
        elif distance < 2000:
            self.shoot_gliding_bombs(target)
        else:
            self.shoot_torpedo(target)

    def shoot_laser(self, target):
        pygame.draw.line(state.screen, "red", (self.x, self.y), (target.x, target.y), 2)

    def shoot_machinegun(self, target):
        distance_x = target.x - self.x
        distance_y = target.y - self.y

        vx = distance_x / 500
        vy = distance_y / 500

        color = self.color

        for i in range(0, 5):
            bullet = Bullet(self, color, self.x, self.y, vx, vy)
            bullet.move()
            state.bullets.append(bullet)

    def shoot_gliding_bombs(self, target):
        distance_x = target.x - self.x
        distance_y = target.y - self.y - 500  # aim above

        vx = distance_x / 100
        vy = distance_y / 100

        color = self.color

        for i in range(0, 3):
            bullet = Bullet(
                self,
                color,
                self.x,
                self.y,
                vx,
                vy,
                0,
                0.1,
            )
            bullet.radius = 5
            bullet.move()
            state.bullets.append(bullet)

    def shoot_torpedo(self, target):
        distance_x = target.x - self.x
        distance_y = target.y - self.y

        vx = distance_x / 1000
        vy = distance_y / 1000

        ax = vx / 5
        ay = vy / 5

        color = self.color

        for i in range(0, 1):
            bullet = Bullet(
                self,
                color,
                self.x,
                self.y,
                vx,
                vy,
                ax,
                ay,
            )
            bullet.radius = 3
            bullet.move()
            state.bullets.append(bullet)

    def tick(self):
        if self == state.player:  # do nothing, controlled by the player (future)
            self.draw()
            return

        if utils.percentage_chance(5):
            self.change_direction()

        self.move()

        if utils.percentage_chance(2):
            target = self.choose_random_target()
            if target:
                self.shoot_at_target(target)
