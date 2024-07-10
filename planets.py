import pygame
import math
import constants as c


class Window:
    def __init__(self, font_type="arial", font_size = 14):
        self.font_type = font_type
        self.font_size = font_size
        self.win = None
        self.font = None

    def initialize(self):
        self.win = pygame.display.set_mode((c.Constants.WIDTH, c.Constants.HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Solar System")
        self.font = pygame.font.SysFont(self.font_type, self.font_size)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, name, x, y, radius, color, mass, y_velocity = 0):
        self.name = name
        self.x = x
        self.y = y
        self.original_radius = radius  # Store original radius
        self.radius = radius  # Current radius for drawing
        self.colour = color
        self.mass = mass
        self.x_velocity = 0
        self.y_velocity = y_velocity

        self.orbit = []
        self.sun = name == "Sun"
        self.distance_from_sun = 0

    def draw(self, win, zoom_factor, font):
        scaled_radius = int(self.original_radius * zoom_factor)
        x = self.x * self.SCALE * zoom_factor + c.Constants.WIDTH / 2
        y = self.y * self.SCALE * zoom_factor + c.Constants.HEIGHT / 2
        pygame.draw.circle(win, self.colour, (int(x), int(y)), scaled_radius)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * self.SCALE * zoom_factor + c.Constants.WIDTH / 2
                py = py * self.SCALE * zoom_factor + c.Constants.HEIGHT / 2
                updated_points.append((int(px), int(py)))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)

        if not self.sun:
            distance_text = font.render(f"{round(self.distance_from_sun / 1000, 1)}km", 1, c.Constants.WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_width() / 2))

        # Display planet name
        planet_name = font.render(self.name, 1, c.Constants.WHITE)
        win.blit(planet_name, (x - planet_name.get_width() / 2, y + scaled_radius))

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

        self.x += self.x_velocity * self.TIMESTEP
        self.y += self.y_velocity * self.TIMESTEP
        self.orbit.append((self.x, self.y))

# TODO
# change expected input of int to float in y.velocity
class Planets:
    sun = Planet("Sun", 0, 0, 35, c.Constants.YELLOW, c.Constants.SUN_MASS)
    sun.sun = True

    mercury = Planet("Mercury", -0.3871 * Planet.AU, 0, 6, c.Constants.GREY, c.Constants.MERCURY_MASS, y_velocity = 47.87 * 1000)
    venus = Planet("Venus", -0.7233 * Planet.AU, 0, 13, c.Constants.ORANGE, c.Constants.VENUS_MASS, y_velocity = 35.02 * 1000)
    earth = Planet("Earth", -1 * Planet.AU, 0, 15, c.Constants.BLUE, c.Constants.EARTH_MASS, y_velocity = 29.78 * 1000)
    mars = Planet("Mars", -1.5237 * Planet.AU, 0, 12, c.Constants.RED, c.Constants.MARS_MASS, y_velocity = 24.07 * 1000)
    jupiter = Planet("Jupiter", -5.2043 * Planet.AU, 0, 25, c.Constants.LIGHT_BEIGE, c.Constants.JUPITER_MASS, y_velocity = 13.07 * 1000)
    saturn = Planet("Saturn", -9.5820 * Planet.AU, 0, 22, c.Constants.BEIGE, c.Constants.SATURN_MASS, y_velocity = 9.69 * 1000)
    uranus = Planet("Uranus", -19.2184 * Planet.AU, 0, 19, c.Constants.LIGHT_BLUE, c.Constants.URANUS_MASS, y_velocity = 6.81 * 1000)
    neptune = Planet("Neptune", -30.069 * Planet.AU, 0, 18, c.Constants.DARK_BLUE, c.Constants.NEPTUNE_MASS, y_velocity = 5.43 * 1000)
