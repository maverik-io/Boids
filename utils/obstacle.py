import pygame as pg
from pygame.math import Vector2


class Obstacle:
    obstacles = []

    def __init__(self, pos: Vector2, bad=False):
        self.pos = pos.copy()
        self.bad = bad
        Obstacle.obstacles.append(self)

    def draw(self, screen):
        pg.draw.circle(screen, 'red' if self.bad else 'grey', self.pos, 5)
