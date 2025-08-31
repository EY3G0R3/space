#!/usr/bin/python3

import os
import sys
import math
import pygame
import random

# TODO:
# ~~~~~
# * control our ship
# * better death animation - flying debris


class Star:
    def __init__(self):
        self.radius = random.randint(2, 3)
        self.color = random.choice(["white", "lightgray", "darkgray"])
        if random.randint(0, 1) == 1:
            self.x = random.randint(0, screen.get_width())
            self.y = 0
        else:
            self.x = 0
            self.y = random.randint(0, screen.get_height())

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += 4
        self.y += 2
        self.draw()

    def tick(self):
        self.move()
        if (
            self.x < 0
            or self.y < 0
            or self.x > screen.get_width()
            or self.y > screen.get_height()
        ):
            stars.remove(self)


class Ship:
    def __init__(self):
        self.radius = random.randint(5, 15)
        self.color = random.choice(["yellow", "blue", "orange", "pink", "cyan"])
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())
        self.change_direction()

    def change_direction(self):
        self.vx = random.randint(-5, 5)
        self.vy = random.randint(-5, 5)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        new_x = self.x + self.vx
        new_y = self.y + self.vy

        if (
            new_x > 0
            and new_y > 0
            and new_x < screen.get_width()
            and new_y < screen.get_height()
        ):
            self.x = new_x
            self.y = new_y

        self.draw()

    def destroy(self):
        deaths.append(DeathFX(self.x, self.y))
        ships.remove(self)
        ships.append(Ship())

    def choose_random_target(self):
        for attempt in range(0, 5):
            index = random.randrange(0, len(ships))
            if ships[index] != self:
                return ships[index]
        return None  # couldn't find a suitable target

    def tick(self):
        if self == player:  # do nothing, controlled by the player
            self.draw()
            return

        if random.randint(0, 100) > 95:
            self.change_direction()

        self.move()

        if random.randint(0, 100) > 95:
            target = self.choose_random_target()
            if not target:
                return

            distance_x = target.x - self.x
            distance_y = target.y - self.y

            bullet_velocity_x = distance_x / 100
            bullet_velocity_y = distance_y / 100

            color = random.choice(["red", "green"])
            bullet1 = Bullet(
                color, self.x, self.y, bullet_velocity_x, bullet_velocity_y
            )
            bullet2 = Bullet(
                color, self.x, self.y, bullet_velocity_x, bullet_velocity_y
            )
            bullet3 = Bullet(
                color, self.x, self.y, bullet_velocity_x, bullet_velocity_y
            )
            bullet1.move()
            bullet1.move()
            bullet1.move()
            bullet1.move()
            bullet2.move()
            bullet2.move()
            bullets.append(bullet1)
            bullets.append(bullet2)
            bullets.append(bullet3)


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def distance_squared(x1, y1, x2, y2):  # faster than distance()
    return (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)


def find_collision(x, y):
    for ship in ships:
        if distance_squared(x, y, ship.x, ship.y) < ship.radius * ship.radius:
            return ship
    return None


class Bullet:
    def __init__(self, color, x, y, vx, vy):
        self.radius = 2
        self.color = color
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.draw()

        ship = find_collision(self.x, self.y)
        if ship:
            ship.destroy()
            self.destroy()
            return

    def destroy(self):
        if self in bullets:
            bullets.remove(self)

    def tick(self):

        # Experimental bouncing code
        # new_x = self.x + self.vx
        # new_y = self.y + self.vy
        # if new_x < 0 or new_x > screen.get_width():
        #     self.vx = -self.vx
        # if new_y < 0 or new_y > screen.get_height():
        #     self.vy = -self.vy

        self.move()

        if (
            self.x < 0
            or self.y < 0
            or self.x > screen.get_width()
            or self.y > screen.get_height()
        ):
            self.destroy()


class DeathFX:
    def __init__(self, x, y):
        self.radius = 5
        self.color = random.choice(["yellow", "orange", "red"])
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def tick(self):
        self.radius += 5
        self.draw()

        if self.radius > random.randint(100, 200):
            self.destroy()

    def destroy(self):
        deaths.remove(self)


# handle command line
if len(sys.argv) > 1:
    # from documentation:
    # On some platforms it is possible to embed the pygame display into an already existing window.
    # To do this, the environment variable SDL_WINDOWID must be set to a string containing
    # the window id or handle. The environment variable is checked when the pygame display is initialized.
    # Be aware that there can be many strange side effects when running in an embedded display.
    os.environ["SDL_WINDOWID"] = sys.argv[1]

# Init pygame
pygame.init()
screen = pygame.display.set_mode((3440, 1440))
clock = pygame.time.Clock()
running = True
dt = 0


# Global unit lists
stars = []
ships = []
bullets = []
deaths = []
player = None


def add_player():
    global player
    global ships

    player = Ship()
    player.color = "blue"
    player.radius = 5
    player.x = screen.get_width() / 2
    player.y = screen.get_height() / 2

    ships.append(player)


# Create the universe
for i in range(0, 1):
    stars.append(Star())

for i in range(0, 3):
    ships.append(Ship())

# Main loop
while running:
    # poll for events
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
        ):  # pygame.QUIT event means the user clicked X to close your window
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                running = False
            else:
                # destroy a random ship to give visual feedback
                ships[random.randrange(-1, len(ships))].destroy()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for star in stars:
        star.tick()

    for ship in ships:
        ship.tick()

    for bullet in bullets:
        bullet.tick()

    for death in deaths:
        death.tick()

    # add new stars
    if random.randint(0, 100) > 70:
        stars.append(Star())

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 100
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(100) / 1000
