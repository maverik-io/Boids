import random
import pygame as pg
from sys import exit
from pygame.math import Vector2

from utils import Boid, Obstacle


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
add_mode = 'obstacle'

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
                    if add_mode == 'boid':
                        Boid(Vector2(*event.pos))
                    elif add_mode == 'obstacle':
                        Obstacle(Vector2(*event.pos))
                    elif add_mode == 'bad_obstacle':
                        Obstacle(Vector2(*event.pos), True)

                case 2:
                    if add_mode == 'obstacle':
                        add_mode = 'boid'
                    elif add_mode == 'boid':
                        add_mode = 'bad_obstacle'
                    elif add_mode == 'bad_obstacle':
                        add_mode = 'obstacle'
                case 3:
                    if Boid.do_trails and not Boid.do_circles:
                        Boid.do_circles = True
                    elif Boid.do_trails and Boid.do_circles:
                        Boid.do_trails = False
                    elif not Boid.do_trails and Boid.do_circles:
                        Boid.do_circles = False
                    elif not Boid.do_trails and not Boid.do_circles:
                        Boid.do_trails = True

    screen.fill('#444444')
    for boid in Boid.boids:
        boid.move()
        boid.update()
        boid.draw(screen)

    for obstacle in Obstacle.obstacles:
        obstacle.draw(screen)

    debug(f'{clock.get_fps():.0f}', len(Boid.boids), f'Current: {add_mode}')

    pg.display.update()
    clock.tick(60)
