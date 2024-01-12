import pygame as pg

from utils import Obstacle, Boid

pg.font.init()

font_size = 28
font = pg.font.Font('Assets/Fonts/Jetbrains_Mono.ttf', font_size)

no_of_rows = 24


class Ui:
    enabled = True
    row_height = font_size + 5
    x = 1480
    y = (950 - (no_of_rows * row_height)) / 2 - 5
    width = 420

    frame_count = 0
    info_bg = pg.Surface((width + 20, 20 + row_height * no_of_rows), pg.SRCALPHA)
    info_bg.set_alpha(100)
    pg.draw.rect(info_bg, 'black', (0, 0, width + 20, 20 + row_height * no_of_rows), 0, 10)

    _open = pg.Surface((50, 100), pg.SRCALPHA)
    _close = pg.Surface((50, 100), pg.SRCALPHA)
    _open.set_alpha(100)
    _close.set_alpha(100)
    close_rect = _close.get_rect(midright=(x + 2, 475))
    open_rect = _open.get_rect(midright=(1900 + 2, 475))

    collision_intercept_zones = {
        0: [open_rect],
        1: [pg.Rect(x, y, width + 20, 20 + row_height * no_of_rows), close_rect],
    }

    open_icon = font.render('<', True, 'white')
    close_icon = font.render('>', True, 'white')
    open_icon_rect = open_icon.get_rect(center=open_rect.center)
    close_icon_rect = close_icon.get_rect(center=close_rect.center)

    pg.draw.rect(_open, 'black', open_rect.move(-open_rect.x, -open_rect.y), 0, border_top_left_radius=10,
                 border_bottom_left_radius=10)
    pg.draw.rect(_close, 'black', close_rect.move(-close_rect.x, -close_rect.y), 0, border_top_left_radius=10,
                 border_bottom_left_radius=10)

    factor_rects = {
        'separation': pg.Rect(x + 225, y + 8 + 9 * row_height, 180, row_height),
        'alignment': pg.Rect(x + 225, y + 8 + 10 * row_height, 180, row_height),
        'cohesion': pg.Rect(x + 225, y + 8 + 11 * row_height, 180, row_height),
        'avoidance': pg.Rect(x + 225, y + 8 + 12 * row_height, 180, row_height),
        'goal': pg.Rect(x + 225, y + 8 + 13 * row_height, 180, row_height),
    }

    toggle_binary_rects = {
        'quads': pg.Rect(x + 225, y + 8 + 15 * row_height, 180, row_height),
        'oquads': pg.Rect(x + 225, y + 8 + 16 * row_height, 180, row_height),
        'bquads': pg.Rect(x + 225, y + 8 + 17 * row_height, 180, row_height),
        'circles': pg.Rect(x + 335, y + 8 + 7 * row_height, 80, row_height),
        'trails': pg.Rect(x + 135, y + 8 + 7 * row_height, 80, row_height),
    }

    toggle_state_rects = {
        'click': pg.Rect(x + 225, y + 8 + 5 * row_height, 180, row_height),
        'boundary': pg.Rect(x + 225, y + 8 + 6 * row_height, 180, row_height),
        'fps': pg.Rect(x + 225, y + 8 + 21 * row_height, 180, row_height),
    }

    @staticmethod
    def draw(fps, screen, o, b, add_mode, goal_pos, fps_limit):

        pos = pg.mouse.get_pos()

        lines = [
            f'Boids      : {len([x for x in filter((lambda boid: not boid.is_predator), Boid.boids)]):>10}',
            f'Predators  : {len([x for x in filter((lambda boid: boid.is_predator), Boid.boids)]):>10}',
            f'Obstacles  : {len([x for x in filter((lambda obstacle: not obstacle.bad), Obstacle.obstacles)]):>10}',
            f'Bad Obs..  : {len([x for x in filter((lambda obstacle: obstacle.bad), Obstacle.obstacles)]):>10}',
            '',
            'Click      :',
            'Boundaries :',
            'Trails:      Radii:',
            '',
            f'Separation : <{Boid.separation_factor:^8.2f}>',
            f'Alignment  : <{Boid.alignment_factor:^8.2f}>',
            f'Cohesion   : <{Boid.cohesion_factor:^8.2f}>',
            f'Avoidance  : <{Boid.avoidance_factor:^8.2f}>',
            f'Goal       : <{Boid.goal_factor:^8.2f}>',
            '',
            # f'QuadTrees  : {"Enabled" if Boid.use_quadtree else "Disabled":^10}',
            f'QuadTrees  :',
            'Show oQuads:  ',
            'Show bQuads:  ',
            '',
            f'Frames     : {Ui.frame_count:>10}',
            f'FPS        : {fps:>10.0f}',
            'FPS Limit  :',  # '30 | 60 | ∞',
            '',
            '.play-pause'

        ]

        if Ui.enabled:
            screen.blit(Ui.info_bg, (Ui.x, Ui.y))
            pg.draw.rect(screen, 'white', (Ui.x, Ui.y, Ui.width + 20, 20 + Ui.row_height * no_of_rows), 2, 10)

            for rect in Ui.factor_rects.values():
                pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)

                if rect.collidepoint(pos):
                    pg.draw.rect(screen, '#12bac9', rect.inflate(-6, -6), 2, 10)

            for name, rect in Ui.toggle_binary_rects.items():
                match name:
                    case 'quads':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        if Boid.use_quadtree:
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-14, -14), 0, 5)
                    case 'oquads':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        if o:
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-14, -14), 0, 5)
                    case 'bquads':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        if b:
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-14, -14), 0, 5)
                    case 'trails':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        if Boid.do_trails:
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-14, -14), 0, 5)
                    case 'circles':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        if Boid.do_circles:
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-14, -14), 0, 5)
            for name, rect in Ui.toggle_state_rects.items():
                match name:
                    case 'click':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        txt = font.render(add_mode.title(), True, 'white')
                        txt_rect = txt.get_rect(center=rect.center)

                        screen.blit(txt, txt_rect)

                        if rect.collidepoint(pos):
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-6, -6), 2, 10)
                    case 'boundary':
                        pg.draw.rect(screen, '#444444', rect.inflate(-6, -6), 0, 10)
                        txt = font.render(Boid.edge_mode.title(), True, 'white')
                        txt_rect = txt.get_rect(center=rect.center)

                        screen.blit(txt, txt_rect)

                        if rect.collidepoint(pos):
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-6, -6), 2, 10)

                    case 'fps':
                        pg.draw.rect(screen, '#444444', rect.inflate(-3, 0), 0, 10)
                        txt = font.render(fps_limit, True, 'white')
                        txt_rect = txt.get_rect(center=rect.center)

                        screen.blit(txt, txt_rect)

                        if rect.collidepoint(pos):
                            pg.draw.rect(screen, '#12bac9', rect.inflate(-3, 0), 2, 10)

            for i, line in enumerate(lines):
                if line == '':
                    pg.draw.line(screen, 'white', (Ui.x, Ui.y + (Ui.row_height + 10) / 2 + i * Ui.row_height),
                                 (Ui.x + Ui.width, Ui.y + (Ui.row_height + 10) / 2 + i * Ui.row_height), 2)
                else:
                    label = font.render(line, True, 'white')
                    rect = label.get_rect(topleft=(Ui.x + 10, Ui.y + 5 + i * Ui.row_height))
                    screen.blit(label, rect)

            screen.blit(Ui._close, Ui.close_rect)
            pg.draw.rect(screen, 'white', Ui.close_rect, 2, border_top_left_radius=10,
                         border_bottom_left_radius=10)
            screen.blit(Ui.close_icon, Ui.close_icon_rect)
        else:
            screen.blit(Ui._open, Ui.open_rect)
            pg.draw.rect(screen, 'white', Ui.open_rect, 2, border_top_left_radius=10,
                         border_bottom_left_radius=10)
            screen.blit(Ui.open_icon, Ui.open_icon_rect)

        if Boid.goal_exists:
            pg.draw.circle(screen, 'green' if Boid.goal_polarity > 0 else 'red', goal_pos, 10, 2)
