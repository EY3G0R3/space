import math
import random
import pygame

import state
from utils import find_collision, is_outside_screen_area


class Bullet:
    def __init__(self, parent, color, x, y, vx, vy, ax=0, ay=0, kind="generic"):
        self.parent = parent
        self.radius = 1
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.accel_x = ax
        self.accel_y = ay
        self.kind = kind
        self._angle = 0.0

    def draw(self):
        if self.kind == "torpedo":
            # Oriented small rocket sprite
            if self.vx != 0 or self.vy != 0:
                self._angle = math.atan2(self.vy, self.vx)

            size = max(4, int(self.radius * 3))
            length = size * 3
            width = max(3, int(size * 0.7))
            nose_len = max(3, int(size * 0.8))
            fin_len = max(3, int(size * 0.6))

            # Model-space points (pointing +X)
            nose = (length / 2, 0)
            back = (-length / 2, 0)
            body = [
                (back[0], -width / 2),
                (length / 2 - nose_len, -width / 2),
                (nose[0], 0),
                (length / 2 - nose_len, width / 2),
                (back[0], width / 2),
            ]
            fin_top = [
                (back[0], -width / 2),
                (back[0] - fin_len, 0),
                (back[0], -width / 3),
            ]
            fin_bot = [
                (back[0], width / 2),
                (back[0] - fin_len, 0),
                (back[0], width / 3),
            ]

            c = math.cos(self._angle)
            s = math.sin(self._angle)

            def xf(pt):
                px, py = pt
                rx = px * c - py * s
                ry = px * s + py * c
                return (int(self.x + rx), int(self.y + ry))

            body_pts = list(map(xf, body))
            fin_top_pts = list(map(xf, fin_top))
            fin_bot_pts = list(map(xf, fin_bot))
            tail_pos = xf((back[0] - 2, 0))

            # Draw body
            pygame.draw.polygon(state.screen, self.color, body_pts)
            pygame.draw.polygon(state.screen, "white", body_pts, 1)
            pygame.draw.polygon(state.screen, self.color, fin_top_pts)
            pygame.draw.polygon(state.screen, self.color, fin_bot_pts)

            # Exhaust flame flicker
            flame_color = random.choice(["orange", "yellow", "red"]) if (self.vx or self.vy) else "gray"
            pygame.draw.circle(state.screen, flame_color, tail_pos, max(2, int(size * 0.4)))
        else:
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
