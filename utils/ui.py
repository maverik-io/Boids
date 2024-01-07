import pygame as pg
from pygame.math import Vector2

from utils import Obstacle, Boid

pg.font.init()
font = pg.font.Font('Assets/Fonts/Jetbrains_Mono.ttf', 30)


def switch(param=None, target=None):
    match param:
        case 'circles':
            Boid.do_circles = not Boid.do_circles

        case 'trails':
            Boid.do_trails = not Boid.do_trails

        case 'add':
            match target:
                case 'separation':
                    Boid.separation_factor += 0.01
                case 'cohesion':
                    Boid.cohesion_factor += 0.01
                case 'alignment':
                    Boid.alignment_factor += 0.01
                case 'avoidance':
                    Boid.avoidance_factor += 0.01
                case 'goal':
                    Boid.goal_factor += 0.01

        case 'subtract':
            match target:
                case 'separation':
                    Boid.separation_factor -= 0.01
                case 'cohesion':
                    Boid.cohesion_factor -= 0.01
                case 'alignment':
                    Boid.alignment_factor -= 0.01
                case 'avoidance':
                    Boid.avoidance_factor -= 0.01
                case 'goal':
                    Boid.goal_factor -= 0.01

        case _:
            return [
                Boid.separation_factor,
                Boid.cohesion_factor,
                Boid.alignment_factor,
                Boid.avoidance_factor,
                Boid.goal_factor
            ]


class Ui:
    frame_count = 0
    info_bg = pg.Surface((450, 370), pg.SRCALPHA)
    info_bg.set_alpha(100)

    pg.draw.rect(info_bg, 'black', (0, 0, 450, 370), 0, 10)


    @staticmethod
    def draw(fps, screen):
        factors = switch()
        lines = [
            f'Boids     : {len([x for x in filter((lambda boid: not boid.is_predator), Boid.boids)])}',
            f'Predators : {len([x for x in filter((lambda boid: boid.is_predator), Boid.boids)])}',
            f'Frames    : {Ui.frame_count}',
            f'FPS       : {fps:.0f}',
            f'Separation Factor : {factors[0]}',
            f'Alignment Factor  : {factors[1]}',
            f'Cohesion Factor   : {factors[2]}',
            f'Avoidance Factor  : {factors[3]}',
            f'Goal Factor       : {factors[4]}',


        ]

        #pg.draw.rect(screen, 'black', (1395, 20, 450, 370), 0, 10)
        for i, line in enumerate(lines):
            label = font.render(line, True, 'white')
            rect = label.get_rect(topleft=(1405, 25 + i * 40))

            screen.blit(label, rect)

        Ui.frame_count += 1
