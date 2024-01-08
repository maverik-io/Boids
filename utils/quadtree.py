import pygame as pg
from pygame import Rect, Vector2


class QuadTree:
    def __init__(self, boundary: Rect, max_points=4, depth=0):
        self.boundary = boundary
        self.max_points = max_points
        self.points = []
        self.depth = depth
        self.divided = False

        self.ne = None
        self.nw = None
        self.se = None
        self.sw = None

    def __str__(self):
        sp = ' ' * self.depth * 2
        s = str(self.boundary) + '\n'
        s += sp + ', '.join(str(point) for point in self.points)
        if not self.divided:
            return s
        return s + '\n' + '\n'.join([
            sp + 'nw: ' + str(self.nw), sp + 'ne: ' + str(self.ne),
            sp + 'se: ' + str(self.se), sp + 'sw: ' + str(self.sw)])

    def divide(self):
        cx, cy = self.boundary.center[0], self.boundary.center[1]
        w, h = self.boundary.width / 2, self.boundary.height / 2
        self.nw = QuadTree(Rect(cx - w, cy - h, w, h),
                           self.max_points, self.depth + 1)
        self.ne = QuadTree(Rect(cx, cy - h, w, h),
                           self.max_points, self.depth + 1)
        self.se = QuadTree(Rect(cx, cy, w, h),
                           self.max_points, self.depth + 1)
        self.sw = QuadTree(Rect(cx - w, cy, w, h),
                           self.max_points, self.depth + 1)
        self.divided = True

    def insert(self, point: Vector2, data):
        if not self.boundary.collidepoint(point):
            return False
        if len(self.points) < self.max_points:
            self.points.append((point, data))
            return True
        if not self.divided:
            self.divide()
        return (self.ne.insert(point, data) or
                self.nw.insert(point, data) or
                self.se.insert(point, data) or
                self.sw.insert(point, data))

    def query(self, boundary, found_points):
        if not self.boundary.colliderect(boundary):
            return False
        for point in self.points:
            if boundary.collidepoint(point[0]):
                found_points.append(point)
        if self.divided:
            self.nw.query(boundary, found_points)
            self.ne.query(boundary, found_points)
            self.se.query(boundary, found_points)
            self.sw.query(boundary, found_points)
        return found_points

    def query_circle(self, boundary, centre, radius, found_points):
        if not self.boundary.colliderect(boundary):
            return []
        for point in self.points:
            point_pos = point[0]
            if (boundary.collidepoint(point_pos) and
                    point_pos.distance_to(centre) <= radius):
                found_points.append(point)
        if self.divided:
            self.nw.query_circle(boundary, centre, radius, found_points)
            self.ne.query_circle(boundary, centre, radius, found_points)
            self.se.query_circle(boundary, centre, radius, found_points)
            self.sw.query_circle(boundary, centre, radius, found_points)
        return found_points

    def query_radius(self, centre, radius, found_points):
        boundary = Rect(centre.x - radius, centre.y - radius, 2 * radius, 2 * radius)
        return self.query_circle(boundary, centre, radius, found_points)

    def __len__(self):
        no_of_points = len(self.points)
        if self.divided:
            no_of_points += len(self.nw) + len(self.ne) + len(self.se) + len(self.sw)
        return no_of_points

    def get_rects(self, rects):
        rects.append(self.boundary)
        rects.extend([Rect(boid[0][0] - 5, boid[0][1] - 5, 10, 10) for boid in self.points])
        if self.divided:
            self.ne.get_rects(rects)
            self.nw.get_rects(rects)
            self.se.get_rects(rects)
            self.sw.get_rects(rects)
        return rects

    def draw(self, screen, color):
        for rect in self.get_rects([]):
            pg.draw.rect(screen, color, rect, 2)
