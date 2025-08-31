import math
import random


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))


def distance_squared(x1, y1, x2, y2):  # faster than distance()
    return (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)


def find_collision(x, y, parent):
    # Local import to avoid circular dependencies at import time
    import state

    for ship in state.ships:
        if (
            ship is not parent
            and distance_squared(x, y, ship.x, ship.y) < ship.radius * ship.radius
        ):
            return ship
    return None


def percentage_chance(percentage):
    return random.randint(0, 100) < percentage


def is_inside_screen_area(x, y):
    import state

    return (
        x >= 0
        and y >= 0
        and state.screen is not None
        and x < state.screen.get_width()
        and y < state.screen.get_height()
    )


def is_outside_screen_area(x, y):
    return not is_inside_screen_area(x, y)
