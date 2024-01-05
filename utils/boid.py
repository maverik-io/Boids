import random

import pygame as pg
from pygame.math import Vector2

from utils import Obstacle


def poly_points(pos, heading):
    points = [
        pos + Vector2(0, 10).rotate(heading + 180),
        pos + Vector2(-5, -5).rotate(heading + 180),
        pos + Vector2(0, -2).rotate(heading + 180),
        pos + Vector2(5, -5).rotate(heading + 180),
    ]
    return points


class Boid:
    boids = []

    separation_factor = 0.05
    alignment_factor = 0.05
    cohesion_factor = 0.05

    turn_factor = 2

    visual_range = 75
    avoidance_range = 30

    do_trails = False
    do_circles = False

    edge_mode = 'wrap'

    def __init__(self, pos: Vector2, debug=False):
        self.speed = 10
        self.acc = Vector2()
        self.pos = pos.copy()

        self.vel = Vector2(
            random.choice((-1, 1)) * random.random(),
            random.choice((-1, 1)) * random.random(),
        ).normalize() * random.random() * self.speed

        self.trail = []

        self.debug_vectors = None
        self.debug = debug

        self.boids.append(self)

    def separation(self):
        sep = Vector2(0, 0)
        for boid in self.boids:
            if (boid.pos - self.pos).length() < self.visual_range:
                if boid == self:
                    continue
                if (boid.pos - self.pos).length() < self.avoidance_range:
                    sep -= boid.pos - self.pos

        for obstacle in Obstacle.obstacles:
            if (obstacle.pos - self.pos).length() < self.visual_range:
                if obstacle.bad:
                    sep -= obstacle.pos - self.pos
                elif (obstacle.pos - self.pos).length() < self.avoidance_range:
                    sep -= obstacle.pos - self.pos

        return sep

    def alignment(self):
        align = Vector2()
        n = 0
        for boid in self.boids:
            if (boid.pos - self.pos).length() < self.visual_range:
                align += boid.vel
                n += 1

        align /= n if n > 1 else 1
        return align

    def cohesion(self):
        center: Vector2 = Vector2(0, 0)
        n = 0
        for boid in self.boids:
            if (boid.pos - self.pos).length() < self.visual_range:
                center += boid.pos
                n += 1

        center /= n if n > 0 else 1
        return center - self.pos

    def move(self):
        separation_vector = self.separation()
        alignment_vector = self.alignment()
        cohesion_vector = self.cohesion()

        if self.debug:
            self.debug_vectors = [
                self.pos + separation_vector * self.separation_factor,
                self.pos + alignment_vector * self.alignment_factor,
                self.pos + cohesion_vector * self.cohesion_factor,
            ]

        self.acc = (
                separation_vector * self.separation_factor
                + alignment_vector * self.alignment_factor
                + cohesion_vector * self.cohesion_factor
        )

    def update(self):
        match self.edge_mode:
            case 'reflect':
                pass

            case 'turn':
                if self.pos.x < 100:
                    self.acc.x += self.turn_factor
                elif self.pos.y < 100:
                    self.acc.y += self.turn_factor
                elif self.pos.x > 1500:
                    self.acc.x -= self.turn_factor
                elif self.pos.y > 850:
                    self.acc.y -= self.turn_factor

            case 'wrap':
                if self.pos.x < 0:
                    self.pos.x = 1600
                elif self.pos.y < 0:
                    self.pos.y = 950
                elif self.pos.x > 1600:
                    self.pos.x = 0
                elif self.pos.y > 950:
                    self.pos.y = 0

        self.vel += self.acc
        self.vel = self.vel.normalize() * self.speed if self.vel.length() > self.speed else self.vel
        self.pos += self.vel

        self.trail.append(self.pos.copy())
        self.trail = self.trail[-int(500 / self.speed):]

    def draw(self, screen):
        pg.draw.polygon(screen, 'red' if self.debug else '#12bac9',
                        poly_points(self.pos.copy(), 180 - self.vel.angle_to(Vector2(0, 1))))
        if self.do_circles:
            pg.draw.circle(screen, 'red' if self.debug else '#12bac9', self.pos, self.visual_range, 1)
            pg.draw.circle(screen, 'red' if self.debug else '#12bac9', self.pos, self.avoidance_range, 1)
        if len(self.trail) >= 2 and self.do_trails:
            pg.draw.lines(screen, 'red' if self.debug else '#12bac9', False, self.trail)
        if self.debug:
            for i, point in enumerate(self.debug_vectors):
                pg.draw.line(screen, ['green', 'blue', 'red'][i], self.pos, point, 2)
                pg.draw.circle(screen, ['green', 'blue', 'red'][i], self.pos, 2)
