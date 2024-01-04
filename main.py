import random
import pygame as pg
from sys import exit
from pygame.math import Vector2

from utils import Boid


def debug(*nums):
    nums = [str(num) for num in nums]
    txt = '|'.join(nums)

    label = pg.font.SysFont('monospace', 40).render(txt, True, 'white', 'black')
    rect = label.get_rect(topleft=(0, 0))

    screen.blit(label, rect)


pg.init()
screen = pg.display.set_mode((1600, 950))
clock = pg.time.Clock()

number_of_boids = 60

for i in range(number_of_boids):
    Boid(Vector2(random.randint(0, 1600), random.randint(0, 950)))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            match event.button:
                case 1:
                    Boid(Vector2(*event.pos))
                case 3:
                    if Boid.do_trails and not Boid.do_circles:
                        Boid.do_circles = True
                    elif Boid.do_trails and Boid.do_circles:
                        Boid.do_trails = False
                    elif not Boid.do_trails and  Boid.do_circles:
                        Boid.do_circles = False
                    elif not Boid.do_trails and not Boid.do_circles:
                        Boid.do_trails = True

    screen.fill('#444444')
    for boid in Boid.boids:
        boid.move()
        boid.update()
        boid.draw(screen)

    debug(f'{clock.get_fps():.0f}', len(Boid.boids))

    pg.display.update()
    clock.tick(60)
