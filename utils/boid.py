import random
import pygame as pg
from pygame.math import Vector2

from utils import Obstacle, QuadTree


def poly_points(pos, heading):
    points = [
        pos + Vector2(0, 10).rotate(heading + 180),
        pos + Vector2(-5, -5).rotate(heading + 180),
        pos + Vector2(0, -2).rotate(heading + 180),
        pos + Vector2(5, -5).rotate(heading + 180),
    ]
    return points


class Boid:
    boids_quad = QuadTree(pg.Rect(-100, -100, 2100, 1150))
    boids = []

    speed = 10

    separation_factor = 0.05
    alignment_factor = 0.05
    cohesion_factor = 0.05
    avoidance_factor = 0.1  # obstacle avoidance
    goal_factor = 0.05

    goal_exists = False

    turn_factor = 2

    visual_range = 75
    avoidance_range = 30

    do_trails = False
    do_circles = False

    edge_mode = 'turn'

    boid_color = '#12bac9'
    predator_color = 'red'

    use_quadtree = True

    def __init__(self, pos: Vector2, predator=False):
        self.acc = Vector2()
        self.pos = pos.copy()

        self.vel = Vector2(
            random.choice((-1, 1)) * random.random(),
            random.choice((-1, 1)) * random.random(),
        ).normalize() * random.random() * self.speed

        self.trail = []
        self.seeking_range = self.visual_range

        self.is_predator = predator

        self.boids.append(self)
        self.boids_quad.insert(self.pos, self)

    @staticmethod
    def update_quad(screen, visualize):
        Boid.boids_quad = QuadTree(pg.Rect(-100, -100, 2100, 1150))

        for boid in Boid.boids:
            Boid.boids_quad.insert(boid.pos, boid)
        if visualize:
            Boid.boids_quad.draw(screen, 'green')

    def calculate_vectors(self, goal_pos):
        separation = Vector2()
        alignment = Vector2()
        cohesion = Vector2()
        avoidance = Vector2()
        goal = Vector2()

        n = 0
        if self.use_quadtree:
            for _, boid in self.boids_quad.query_radius(self.pos, self.seeking_range, []):
                if (boid.pos - self.pos).length():
                    if boid == self:
                        continue
                    if boid.is_predator and not self.is_predator:
                        separation -= boid.pos - self.pos
                    elif (boid.pos - self.pos).length() < self.avoidance_range:
                        separation -= boid.pos - self.pos

                if not self.is_predator:
                    if (boid.pos - self.pos).length() < self.visual_range and not boid.is_predator:
                        cohesion += boid.pos
                        alignment += boid.vel
                        n += 1
                else:
                    if (boid.pos - self.pos).length() < self.visual_range and boid.is_predator:
                        cohesion += boid.pos
                        alignment += boid.vel
                        n += 1

                goal = (goal_pos - self.pos) if self.is_predator else Vector2()

                if n > 4:
                    self.seeking_range = max((self.seeking_range - 1, self.avoidance_range))
                else:
                    self.seeking_range = min((self.seeking_range + 1, self.visual_range))

            for _, obstacle in Obstacle.obstacles_quad.query_radius(self.pos, self.visual_range, []):
                if (obstacle.pos - self.pos).length() < self.visual_range:
                    if obstacle.bad:
                        avoidance -= obstacle.pos - self.pos
                    elif (obstacle.pos - self.pos).length() < self.avoidance_range:
                        avoidance -= obstacle.pos - self.pos
        else:
            for boid in self.boids:
                if (boid.pos - self.pos).length():
                    if boid == self:
                        continue
                    if boid.is_predator and not self.is_predator:
                        separation -= boid.pos - self.pos
                    elif (boid.pos - self.pos).length() < self.avoidance_range:
                        separation -= boid.pos - self.pos

                if not self.is_predator:
                    if (boid.pos - self.pos).length() < self.visual_range and not boid.is_predator:
                        cohesion += boid.pos
                        alignment += boid.vel
                        n += 1
                else:
                    if (boid.pos - self.pos).length() < self.visual_range and boid.is_predator:
                        cohesion += boid.pos
                        alignment += boid.vel
                        n += 1

                goal = (goal_pos - self.pos) if self.is_predator else Vector2()

            for obstacle in Obstacle.obstacles:
                if (obstacle.pos - self.pos).length() < self.visual_range:
                    if obstacle.bad:
                        avoidance -= obstacle.pos - self.pos
                    elif (obstacle.pos - self.pos).length() < self.avoidance_range:
                        avoidance -= obstacle.pos - self.pos

        cohesion /= n if n > 0 else 1
        alignment /= n if n > 1 else 1

        return separation, alignment, cohesion - self.pos, avoidance, goal

    def move(self, goal_pos):
        (separation_vector, alignment_vector,
         cohesion_vector, avoidance_vector,
         goal_vector) = self.calculate_vectors(goal_pos)

        self.acc = (
                separation_vector * self.separation_factor
                + alignment_vector * self.alignment_factor
                + cohesion_vector * self.cohesion_factor
                + avoidance_vector * self.avoidance_factor
                + goal_vector * self.goal_factor * int(self.goal_exists)
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
                elif self.pos.x > 1800:
                    self.acc.x -= self.turn_factor
                elif self.pos.y > 850:
                    self.acc.y -= self.turn_factor

            case 'wrap':
                if self.pos.x < 0:
                    self.pos.x = 1900
                elif self.pos.y < 0:
                    self.pos.y = 950
                elif self.pos.x > 1900:
                    self.pos.x = 0
                elif self.pos.y > 950:
                    self.pos.y = 0

        self.vel += self.acc
        self.vel = self.vel.normalize() * self.speed if self.vel.length() > self.speed else self.vel
        self.pos += self.vel

        self.trail.append(self.pos.copy())
        self.trail = self.trail[-int(500 / self.speed):]

    def draw(self, screen):
        pg.draw.polygon(screen, self.predator_color if self.is_predator else self.boid_color,
                        poly_points(self.pos.copy(), 180 - self.vel.angle_to(Vector2(0, 1))))
        if self.do_circles:
            pg.draw.circle(screen, self.predator_color if self.is_predator else self.boid_color, self.pos,
                           self.seeking_range, 1)
            pg.draw.circle(screen, self.predator_color if self.is_predator else self.boid_color, self.pos,
                           self.avoidance_range, 1)
        if len(self.trail) >= 2 and self.do_trails:
            pg.draw.lines(screen, self.predator_color if self.is_predator else self.boid_color, False, self.trail)
