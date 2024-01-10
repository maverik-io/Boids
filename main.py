import random
import pygame as pg
from sys import exit
from pygame.math import Vector2

from utils import Boid, Obstacle, Ui


def update(boid):
    boid.move(goal_pos)
    boid.update()
    boid.draw(screen)


pg.init()
screen = pg.display.set_mode((1900, 950))
pg.display.set_caption('Boids')
pg.mouse.set_visible(False)
clock = pg.time.Clock()

number_of_boids = 0
number_of_predator_boids = 10

add_mode = 'boid'

b_visualize = False
o_visualize = False

click_adds = ['boid', 'predator', 'obstacle', 'stink', 'control']
boundary_modes = ['turn', 'wrap']

goal_pos = Vector2()

rays = []

[Boid(Vector2(random.randint(0, 1600), random.randint(0, 950)), False) for _ in range(number_of_boids)]
[Boid(Vector2(random.randint(0, 1600), random.randint(0, 950)), True) for _ in range(number_of_predator_boids)]

# [Obstacle(Vector2(random.randint(0, 1600), random.randint(0, 950)), not (_ % 3)) for _ in range(50)]
Ui.info_bg = Ui.info_bg.convert_alpha()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            match event.button:
                case 1:
                    allowed = True
                    for rect in Ui.collision_intercept_zones[Ui.enabled]:
                        if rect.collidepoint(event.pos):
                            allowed = False
                    if allowed:
                        if add_mode == 'boid':
                            Boid(Vector2(*event.pos))

                        elif add_mode == 'predator':
                            Boid(Vector2(*event.pos), True)
                        elif add_mode == 'obstacle':
                            Obstacle(Vector2(*event.pos))
                        elif add_mode == 'stink':
                            Obstacle(Vector2(*event.pos), True)
                        elif add_mode == 'control':
                            goal_pos = Vector2(*event.pos)
                            Boid.goal_exists = True
                            

                    if Ui.enabled:
                        if Ui.close_rect.collidepoint(event.pos):
                            Ui.enabled = False

                        for key, value in Ui.toggle_binary_rects.items():
                            match key:
                                case 'quads':
                                    if value.collidepoint(event.pos):
                                        Boid.use_quadtree = not Boid.use_quadtree
                                        if not Boid.use_quadtree:
                                            o_visualize = False
                                            b_visualize = False
                                case 'oquads':
                                    if value.collidepoint(event.pos):
                                        o_visualize = not o_visualize if Boid.use_quadtree else False
                                case 'bquads':
                                    if value.collidepoint(event.pos):
                                        b_visualize = not b_visualize if Boid.use_quadtree else False
                                case 'trails':
                                    if value.collidepoint(event.pos):
                                        Boid.do_trails = not Boid.do_trails
                                case 'circles':
                                    if value.collidepoint(event.pos):
                                        Boid.do_circles = not Boid.do_circles

                    else:
                        if Ui.open_rect.collidepoint(event.pos):
                            Ui.enabled = True

                    for key, value in Ui.toggle_state_rects.items():
                        match key:
                            case 'click':
                                if value.collidepoint(event.pos):
                                    add_mode = click_adds[(click_adds.index(add_mode) + 1) % len(click_adds)]
                                    Boid.goal_exists = False
                            case 'boundary':
                                if value.collidepoint(event.pos):
                                    Boid.edge_mode = boundary_modes[(boundary_modes.index(Boid.edge_mode) + 1) % len(boundary_modes)]

                case 3:
                    shortest_distance = 10000000
                    obj = None
                    match add_mode:
                        case 'boid':
                            for boid in Boid.boids:
                                if (Vector2(*event.pos) - boid.pos).length() < shortest_distance:
                                    shortest_distance = (Vector2(*event.pos) - boid.pos).length()
                                    obj = boid

                            if obj is not None:
                                rays.append([event.pos, obj.pos, 0])
                                Boid.boids.remove(obj)

                case 4:
                    if Ui.enabled:
                        for key, value in Ui.factor_rects.items():
                            if value.collidepoint(event.pos):
                                match key:
                                    case 'separation':
                                        Boid.separation_factor = max((Boid.separation_factor - 0.01, 0))
                                    case 'alignment':
                                        Boid.alignment_factor = max((Boid.alignment_factor - 0.01, 0))
                                    case 'cohesion':
                                        Boid.cohesion_factor = max((Boid.cohesion_factor - 0.01, 0))
                                    case 'avoidance':
                                        Boid.avoidance_factor = max((Boid.avoidance_factor - 0.01, 0))
                                    case 'goal':
                                        Boid.goal_factor = max((Boid.goal_factor - 0.01, 0))

                case 5:
                    if Ui.enabled:
                        for key, value in Ui.factor_rects.items():
                            if value.collidepoint(event.pos):
                                match key:
                                    case 'separation':
                                        Boid.separation_factor = min((Boid.separation_factor + 0.01, 1))
                                    case 'alignment':
                                        Boid.alignment_factor = min((Boid.alignment_factor + 0.01, 1))
                                    case 'cohesion':
                                        Boid.cohesion_factor = min((Boid.cohesion_factor + 0.01, 1))
                                    case 'avoidance':
                                        Boid.avoidance_factor = min((Boid.avoidance_factor + 0.01, 1))
                                    case 'goal':
                                        Boid.goal_factor = min((Boid.goal_factor + 0.01, 1))

    screen.fill('#444444')

    Boid.update_quad(screen, b_visualize)
    [update(boid) for boid in Boid.boids]
    Obstacle.update_quad(screen, o_visualize)
    [obstacle.draw(screen) for obstacle in Obstacle.obstacles]

    i = 0
    for ray in rays.copy():
        start, end, timer = ray
        pg.draw.line(screen, 'green', start, end, 2)
        rays[i][2] += 1
        if timer > 1:
            rays.remove(ray)

    Ui.draw(clock.get_fps(), screen, o_visualize, b_visualize, add_mode, goal_pos)

    pg.draw.circle(screen, 'white', pg.mouse.get_pos(), 10, 4)

    pg.display.update()
    clock.tick(0)
