import random
import math
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


class ExhaustFX:
    def __init__(self, x, y, dir_x=0.0, dir_y=0.0, strength=1.0):
        # Particles travel opposite to shot direction with slight spread
        self.particles = []
        mag = math.hypot(dir_x, dir_y)
        if mag == 0:
            dir_x, dir_y = -1.0, 0.0
        else:
            dir_x, dir_y = dir_x / mag, dir_y / mag

        count = random.randint(8, 12)
        base_angle = math.atan2(dir_y, dir_x)
        for _ in range(count):
            jitter = random.uniform(-0.6, 0.6)
            ang = base_angle + jitter
            speed = random.uniform(1.5, 4.0) * (1.0 + 0.5 * strength)
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            life = random.randint(12, 24)
            radius = random.randint(2, 3)
            color = random.choice(["orange", "yellow", "red"])
            self.particles.append([x, y, vx, vy, life, radius, color])

    def draw(self):
        for px, py, _, __, ___, r, color in self.particles:
            pygame.draw.circle(state.screen, color, (int(px), int(py)), max(1, int(r)))

    def tick(self):
        next_particles = []
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            # shrink slightly
            p[5] = max(1, p[5] - 0.1)
            if p[4] > 0:
                next_particles.append(p)
        self.particles = next_particles
        self.draw()
        if not self.particles:
            self.destroy()

    def destroy(self):
        if self in state.effects:
            state.effects.remove(self)
