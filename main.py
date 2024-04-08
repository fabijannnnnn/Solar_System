import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1024, 768
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Solar System")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
RED = (255, 100, 50)
GREY = (150, 150, 150)
ORANGE = (195, 145, 25)
LIGHT_BEIGE = (216, 202, 157)
BEIGE = (226, 191, 125)
LIGHT_BLUE = (175, 219, 245)
DARK_BLUE = (2, 0, 121)


SUN_MASS = 1.98892 * 10 ** 30
EARTH_MASS = 5.9742 * 10 ** 24
MARS_MASS = 6.3903 * 10 ** 23
VENUS_MASS = 4.8675 * 10 * 24
MERCURY_MASS = 3.30 * 10 ** 23
JUPITER_MASS = 1.97 * 10 ** 27
SATURN_MASS = 5.683 * 10 ** 26
URANUS_MASS = 8.681 * 10 ** 25
NEPTUNE_MASS = 1.024 * 10 ** 26

FONT = pygame.font.SysFont("arial", 14)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.y = y
        self.radius = radius
        self.mass = mass
        self.x = x
        self.colour = color

        self.orbit = []
        self.sun = False
        self.distance_from_sun = 0

        self.x_velocity = 0
        self.y_velocity = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(win, self.colour, (x, y), self.radius)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_from_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_width() / 2))

        pygame.draw.circle(win, self.colour, (x, y), self.radius)

    def attraction(self, other_obj):
        other_obj_x, other_obj_y = other_obj.x, other_obj.y
        distance_x = other_obj_x - self.x
        distance_y = other_obj_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other_obj.sun:
            self.distance_from_sun = distance

        force = self.G * self.mass * other_obj.mass / distance ** 2
        alpha = math.atan2(distance_y, distance_x)
        force_x = math.cos(alpha) * force
        force_y = math.sin(alpha) * force

        return force_x, force_y

    def update_pos(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_force_x += fx
            total_force_y += fy

        self.x_velocity += total_force_x / self.mass * self.TIMESTEP
        self.y_velocity += total_force_y / self.mass * self.TIMESTEP
        # F = m / a
        # a = f / m

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 35, YELLOW, SUN_MASS)
    sun.sun = True

    mercury = Planet(-0.3871 * Planet.AU, 0, 6, GREY, MERCURY_MASS)
    mercury.y_velocity = 47.87 * 1000

    venus = Planet(-0.7233 * Planet.AU, 0, 13, ORANGE, VENUS_MASS)
    venus.y_velocity = 35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 15, BLUE, EARTH_MASS)
    earth.y_velocity = 29.78 * 1000

    mars = Planet(-1.5237 * Planet.AU, 0, 12, RED, MARS_MASS)
    mars.y_velocity = 24.07 * 1000

    jupiter = Planet(-5.2043 * Planet.AU, 0, 25, LIGHT_BEIGE, JUPITER_MASS)
    jupiter.y_velocity = 13.07 * 1000

    saturn = Planet(-9.5820 * Planet.AU, 0, 22, BEIGE, SATURN_MASS)
    saturn.y_velocity = 9.69 * 1000

    uranus = Planet(-19.2184 * Planet.AU, 0, 19, LIGHT_BLUE, URANUS_MASS)
    uranus.y_velocity = 6.81 * 1000

    neptune = Planet(-30.069 * Planet.AU, 0, 18, DARK_BLUE, NEPTUNE_MASS)
    neptune.y_velocity = 5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        # WIN.fill(WHITE)
        # pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
