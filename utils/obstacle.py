import pygame as pg
from pygame.math import Vector2

from utils import QuadTree


class Obstacle:
    obstacles = []
    obstacles_quad = QuadTree(pg.Rect(-100, 100, 2000, 1050))

    @staticmethod
    def update_quad(screen, visualize):
        Obstacle.obstacles_quad = QuadTree(pg.Rect(-100, 100, 2000, 1050))

        for obstacle in Obstacle.obstacles:
            Obstacle.obstacles_quad.insert(obstacle.pos, obstacle)
        if visualize:
            Obstacle.obstacles_quad.draw(screen, 'blue')

    def __init__(self, pos: Vector2, bad=False):
        self.pos = pos.copy()
        self.bad = bad
        Obstacle.obstacles.append(self)
        Obstacle.obstacles_quad.insert(self.pos, self)

    def draw(self, screen):
        pg.draw.circle(screen, 'red' if self.bad else 'grey', self.pos, 5)
