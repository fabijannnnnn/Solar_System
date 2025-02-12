import pygame
from planets import Planets, Window


def main():
    pygame.init()

    window = Window(font_size = 14)
    # init window with font size
    window.initialize()

    run = True
    clock = pygame.time.Clock()
    zoom_factor = 1.0

    planets = [Planets.sun, Planets.earth, Planets.mars, Planets.mercury,
               Planets.venus, Planets.jupiter, Planets.saturn, Planets.uranus,
               Planets.neptune]

    while run:
        clock.tick(60)
        window.win.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    zoom_factor *= 1.1
                elif event.button == 5:  # Scroll down
                    zoom_factor /= 1.1

        for planet in planets:
            planet.update_pos(planets)
            planet.draw(window.win, zoom_factor, window.font)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
