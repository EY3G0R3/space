import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((3440, 1440))
clock = pygame.time.Clock()
running = True
dt = 0

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


class Ship:
    def __init__(self):
        self.radius = random.randint(5, 15)
        self.color = random.choice(["yellow", "blue", "orange", "pink", "cyan"])
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(0, screen.get_height())


    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


    def move(self):
        self.x += random.randint(-10, 10)
        self.y += random.randint(-10, 10)
        self.draw()


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


    def tick(self):
        self.move()
        if self.x < 0 or self.y < 0 or self.x > screen.get_width() or self.y > screen.get_height():
            bullets.remove(self)



stars = []
ships = []
bullets = []

for i in range(0, 1):
    stars.append(Star())

for i in range(0, 3):
    ships.append(Ship())


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
         if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
             running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for star in stars:
        star.move()

    for ship in ships:
        ship.move()

    for bullet in bullets:
        bullet.tick()

    # shooting
    for ship in ships:
        if random.randint(0, 100) > 95:
            bullet_velocity_x = random.randint(-10, 10)
            bullet_velocity_y = random.randint(-10, 10)
            color = random.choice(["red", "green"])
            bullet1 = Bullet(color, ship.x, ship.y, bullet_velocity_x, bullet_velocity_y)
            bullet2 = Bullet(color, ship.x, ship.y, bullet_velocity_x, bullet_velocity_y)
            bullet3 = Bullet(color, ship.x, ship.y, bullet_velocity_x, bullet_velocity_y)
            bullet1.move()
            bullet1.move()
            bullet1.move()
            bullet1.move()
            bullet2.move()
            bullet2.move()
            bullets.append(bullet1)
            bullets.append(bullet2)
            bullets.append(bullet3)

    # removing stars that are out of bounds
    for star in stars:
        if star.x > screen.get_width():
            stars.remove(star)
            continue
        if star.y > screen.get_height():
            stars.remove(star)
            continue

    # add new stars
    if random.randint(0, 100) > 70:
        stars.append(Star())

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(100) / 1000
