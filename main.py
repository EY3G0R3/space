#!/usr/bin/python3

import os
import sys
import random
import pygame

import state
from star import Star
from ship import Ship


def add_player():
    state.player = Ship()
    state.player.color = "blue"
    state.player.radius = 5
    state.player.x = state.screen.get_width() / 2
    state.player.y = state.screen.get_height() / 2
    state.ships.append(state.player)


def run():
    # handle command line for embedding
    if len(sys.argv) > 1:
        os.environ["SDL_WINDOWID"] = sys.argv[1]

    # Init pygame and screen
    pygame.init()
    state.screen = pygame.display.set_mode((3440, 1440))
    clock = pygame.time.Clock()
    running = True

    # Create the universe
    for _ in range(0, 1):
        state.stars.append(Star())

    for _ in range(0, 3):
        state.ships.append(Ship())

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                else:
                    # destroy a random ship to give visual feedback
                    if state.ships:
                        state.ships[random.randrange(-1, len(state.ships))].destroy()

        # Clear
        state.screen.fill("black")

        # Ticks
        for star in list(state.stars):
            star.tick()

        for ship in list(state.ships):
            ship.tick()

        for bullet in list(state.bullets):
            bullet.tick()

        for death in list(state.deaths):
            death.tick()

        # Add new stars
        if random.randint(0, 100) > 70:
            state.stars.append(Star())

        # Display
        pygame.display.flip()

        # Cap FPS
        clock.tick(100)

    pygame.quit()
