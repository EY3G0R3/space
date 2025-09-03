import random
import math
import pygame

import state


class DeathFX:
    """A fancier composite death effect.

    Components:
    - Initial flash
    - Shockwave ring
    - Sparks (colored hot debris)
    - Smoke puffs
    """

    def __init__(self, x, y, base_color=None):
        self.x = float(x)
        self.y = float(y)
        # color palette derived from an optional ship color
        base = base_color or random.choice(["yellow", "orange", "red"])
        self.palette = self._palette_for(base)

        # Flash
        self.flash_time = 6
        self.flash_radius = 10

        # Shockwave
        self.ring_r = 6
        self.ring_dr = 6
        self.ring_w = 2
        self.ring_r_max = random.randint(120, 200)

        # Sparks (hot bits)
        self.sparks = []  # [x, y, vx, vy, life, r, color]
        count = random.randint(28, 42)
        for _ in range(count):
            ang = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.5, 6.0)
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            life = random.randint(18, 34)
            r = random.uniform(1.0, 2.5)
            color = random.choice(self.palette)
            self.sparks.append([self.x, self.y, vx, vy, life, r, color])

        # Smoke (cooling debris)
        self.smoke = []  # [x, y, vx, vy, life, r]
        smoke_count = random.randint(8, 14)
        for _ in range(smoke_count):
            ang = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.4, 1.4)
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            life = random.randint(28, 48)
            r = random.uniform(2.0, 4.0)
            self.smoke.append([self.x, self.y, vx, vy, life, r])

    def _palette_for(self, base):
        by_name = {
            "yellow": [(255, 255, 180), (255, 220, 100), (255, 200, 60)],
            "orange": [(255, 200, 120), (255, 160, 60), (255, 120, 40)],
            "red": [(255, 150, 120), (255, 100, 80), (255, 60, 60)],
            "blue": [(180, 220, 255), (140, 200, 255), (100, 180, 255)],
            "pink": [(255, 180, 220), (255, 150, 210), (255, 120, 200)],
            "cyan": [(180, 255, 255), (140, 240, 255), (100, 220, 255)],
        }
        return by_name.get(base, by_name["orange"])

    def _draw_flash(self):
        if self.flash_time > 0:
            try:
                pygame.draw.circle(
                    state.screen,
                    (255, 255, 255),
                    (int(self.x), int(self.y)),
                    max(2, int(self.flash_radius)),
                )
            except Exception:
                pass

    def _draw_ring(self):
        if self.ring_r < self.ring_r_max:
            try:
                pygame.draw.circle(
                    state.screen,
                    (255, 255, 255),
                    (int(self.x), int(self.y)),
                    int(self.ring_r),
                    max(1, int(self.ring_w)),
                )
            except Exception:
                pass

    def _draw_sparks(self):
        for px, py, _, __, ___, r, color in self.sparks:
            try:
                pygame.draw.circle(
                    state.screen, color, (int(px), int(py)), max(1, int(r))
                )
            except Exception:
                pass

    def _draw_smoke(self):
        for px, py, _, __, ___, r in self.smoke:
            try:
                pygame.draw.circle(
                    state.screen, (150, 150, 150), (int(px), int(py)), max(1, int(r))
                )
            except Exception:
                pass

    def draw(self):
        self._draw_flash()
        self._draw_ring()
        self._draw_sparks()
        self._draw_smoke()

    def tick(self):
        # Update shockwave
        if self.ring_r < self.ring_r_max:
            self.ring_r += self.ring_dr
            self.ring_w = max(1, self.ring_w - 0.05)

        # Update flash
        if self.flash_time > 0:
            self.flash_time -= 1
            self.flash_radius *= 1.2

        # Update sparks
        next_sparks = []
        for p in self.sparks:
            p[0] += p[2]
            p[1] += p[3]
            # slight drag
            p[2] *= 0.98
            p[3] *= 0.98
            # subtle outward push to maintain burst feel
            dx = p[0] - self.x
            dy = p[1] - self.y
            dist = math.hypot(dx, dy) + 1e-5
            p[2] += (dx / dist) * 0.02
            p[3] += (dy / dist) * 0.02
            p[4] -= 1
            p[5] = max(0.5, p[5] - 0.04)
            if p[4] > 0 and p[5] > 0.5:
                next_sparks.append(p)
        self.sparks = next_sparks

        # Update smoke
        next_smoke = []
        for p in self.smoke:
            p[0] += p[2]
            p[1] += p[3]
            # gentle drift outward and slight upward float
            p[3] -= 0.01
            p[2] *= 0.99
            p[3] *= 0.99
            p[4] -= 1
            p[5] = min(12.0, p[5] + 0.08)
            if p[4] > 0:
                next_smoke.append(p)
        self.smoke = next_smoke

        # Render
        self.draw()

        # End condition
        if (
            self.flash_time <= 0
            and self.ring_r >= self.ring_r_max
            and not self.sparks
            and not self.smoke
        ):
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


class TrailSmokeFX:
    """Short-lived gray smoke puffs for trails.

    Particles drift opposite to the provided direction with slight spread.
    Keep it tiny and cheap since it emits frequently.
    """

    def __init__(self, x, y, dir_x=0.0, dir_y=0.0, strength=1.0):
        self.particles = []
        mag = math.hypot(dir_x, dir_y)
        if mag == 0:
            dir_x, dir_y = -1.0, 0.0
        else:
            dir_x, dir_y = dir_x / mag, dir_y / mag

        count = random.randint(2, 4)
        base_angle = math.atan2(dir_y, dir_x)
        for _ in range(count):
            jitter = random.uniform(-0.4, 0.4)
            ang = base_angle + jitter
            speed = random.uniform(0.6, 1.4) * (0.8 + 0.6 * strength)
            vx = math.cos(ang) * speed
            vy = math.sin(ang) * speed
            life = random.randint(10, 18)
            radius = random.uniform(1.0, 2.4)
            self.particles.append([x, y, vx, vy, life, radius])

    def draw(self):
        for px, py, _, __, ___, r in self.particles:
            pygame.draw.circle(
                state.screen, (170, 170, 170), (int(px), int(py)), max(1, int(r))
            )

    def tick(self):
        next_particles = []
        for p in self.particles:
            p[0] += p[2]
            p[1] += p[3]
            p[2] *= 0.98
            p[3] *= 0.98
            p[4] -= 1
            p[5] = min(4.0, p[5] + 0.05)
            if p[4] > 0:
                next_particles.append(p)
        self.particles = next_particles
        self.draw()
        if not self.particles:
            self.destroy()

    def destroy(self):
        if self in state.effects:
            state.effects.remove(self)
