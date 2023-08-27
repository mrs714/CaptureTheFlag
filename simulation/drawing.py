from simulation.simulation_consts import *
import pygame.draw
from random import randint
import math

class Renderer:
    
    def __init__(self, screen, level): # "2": print all tags, "1": print only points, "0": print nothing
        self.__screen = screen
        self.__text_font = pygame.font.SysFont(None, 24)
        self.__level = level
        self.__entities = {}
        self.__tick = 0

    def draw_frame(self, screen, entities, tick):
        self.__entities = entities
        self.__tick = tick

        self.__draw_map()

        self.__draw_bots()
        self.__draw_bullets()
        self.__draw_drops()

        self.__draw_effects()

    def __random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    
    def __map_range(self, value, input_min, input_max, output_min, output_max): # Maps a value from one range to another
        return output_min + (value - input_min) * (output_max - output_min) / (input_max - input_min)

    
    def __draw_map(self):
        self.__screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.__screen, DARK_GRAY, pygame.Rect(MAP_PADDING, MAP_PADDING, MAP_WIDTH, MAP_HEIGHT)) 

    def __draw_bots(self):

        def draw_bot_shield(bot, hit):
            normalized_shield = int((bot.get_defense() / bot.get_shield()) * 10) # 1 to 10
            pygame.draw.circle(self.__screen, CYAN if normalized_shield > 0 and not hit else RED, bot.pos(), BOT_RADIUS + normalized_shield, 1) # Thin line
        
        for bot in self.__entities["bots"].values():

            normalized_color = bot.get_life() / bot.get_health() # 0 to 1
            blue = math.ceil(255 * normalized_color)
            bot_hit = bot.get_state()["last_hit"] == self.__tick
            bot_has_defense = bot.get_defense() != 0

            bot_color = (BOT_COLOR[0], BOT_COLOR[1], blue) if not (bot_hit and not bot_has_defense) else WHITE
            pygame.draw.circle(self.__screen, bot_color, bot.pos(), BOT_RADIUS)

            draw_bot_shield(bot, bot_hit)

            # Draw data
            name = self.__text_font.render(str(bot.get_name()), True, WHITE)
            self.__screen.blit(name, (bot.x() - BOT_RADIUS, bot.y() + 2 * BOT_RADIUS))

            if self.__level > 0:
                points = self.__text_font.render(str(bot.get_points()), True, GREEN)
                self.__screen.blit(points, (bot.x() - BOT_RADIUS, bot.y() + 3 * BOT_RADIUS))
            
            if self.__level > 1:
                life = self.__text_font.render(str(bot.get_life()), True, ORANGE)
                shield = self.__text_font.render(str(bot.get_defense()), True, CYAN)
                self.__screen.blit(life, (bot.x() - BOT_RADIUS, bot.y() + 4 * BOT_RADIUS))
                self.__screen.blit(shield, (bot.x() - BOT_RADIUS, bot.y() + 5 * BOT_RADIUS))

    def __draw_bullets(self):

        def draw_speed_lines(bullet, type):
            # Draws ten random black lines from the back of the bullet in the -direction of travel

            # Get the center of the bullet and the -direction vector
            start_point = (bullet.x(), bullet.y())
            direction_unit_vector = (-bullet.get_vector_direction()[0], -bullet.get_vector_direction()[1])

            for i in range(5 if type == "normal" else 10):

                # First, randomize the direction of the vector +- 90º:
                degrees = randint(-70, 70) if type == "normal" else randint(-90, 90)

                # Rotate the vector direction x degrees:
                angle_radians = math.radians(degrees)
                x, y = direction_unit_vector
                length = BULLET_RADIUS if type == "normal" else SUPER_BULLET_RADIUS
                start_x = start_point[0] + (x * math.cos(angle_radians) - y * math.sin(angle_radians)) * length
                start_y = start_point[1] + (x * math.sin(angle_radians) + y * math.cos(angle_radians)) * length
                
                length = randint(5, min((5 + 2 * bullet.get_state()["life_ticks"]), 50))

                end_x = start_x + direction_unit_vector[0] * length
                end_y = start_y + direction_unit_vector[1] * length

                pygame.draw.line(self.__screen, BLACK, (start_x, start_y), (end_x, end_y))

        for bullet in self.__entities["bullets"].values():
            type = bullet.get_type()
            if type == "normal":
                pygame.draw.circle(self.__screen, BULLET_COLOR, bullet.pos(), BULLET_RADIUS)
            else:
                pygame.draw.circle(self.__screen, self.__random_color(), bullet.pos(), SUPER_BULLET_RADIUS)
            draw_speed_lines(bullet, type)

    def __draw_drops(self):

        def drop_color(drop, min_color, max_color): 

            blinking = drop.get_state()["blinking"]
            drop_color = drop.get_state()["color"]
            min_difference = min(255 - min_color[0], 255 - min_color[1], 255 - min_color[2])    
            
            if drop_color == None:
                drop.set_state({"blinking": blinking, "color": min_color})
                return min_color
            if blinking:
                multiplier = self.__map_range(min_difference, 0, 255, 1.01, 1.1)
                new_color = (drop_color[0] * multiplier, drop_color[1] * multiplier, drop_color[2] * multiplier)
                if new_color[0] > max_color[0] or new_color[1] > max_color[1] or new_color[2] > max_color[2]:
                    new_color = max_color
                    blinking = False
                drop.set_state({"blinking": blinking, "color": new_color})
                return new_color
            else:
                multiplier = self.__map_range(min_difference, 0, 255, 0.99, 0.9)
                new_color = (drop_color[0] * multiplier, drop_color[1] * multiplier, drop_color[2] * multiplier)
                if new_color[0] < min_color[0] or new_color[1] < min_color[1] or new_color[2] < min_color[2]:
                    new_color = min_color
                    blinking = True
                drop.set_state({"blinking": blinking, "color": new_color})
                return new_color

        for drop in self.__entities["drops_points"].values():
            pygame.draw.circle(self.__screen, drop_color(drop, DROP_COLOR_POINTS_MIN, DROP_COLOR_POINTS_MAX), drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_health"].values():
            pygame.draw.circle(self.__screen, drop_color(drop, DROP_COLOR_HEALTH_MIN, DROP_COLOR_HEALTH_MAX), drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_shield"].values():
            pygame.draw.circle(self.__screen, drop_color(drop, DROP_COLOR_SHIELD_MIN, DROP_COLOR_SHIELD_MAX), drop.pos(), DROP_RADIUS)

    def __draw_effects(self):

        def draw_player_death_effect(effect):
            # Draw a white circle that travels outwards and one that travels inwards from the center of the bot
            step = effect.get_step()
            max_step = BOT_RADIUS * 3

            if step > max_step:
                effect.remove()

            if step < BOT_RADIUS: # Inward circle
                pygame.draw.circle(self.__screen, WHITE, effect.pos(), BOT_RADIUS - step)

            pygame.draw.circle(self.__screen, RED, effect.pos(), step, int(self.__map_range(step, 0, max_step, 5, 1)))

        def draw_pick_drop_effect(effect):
            # Draw x concentrical lines that start at the center and move outwards
            number_of_lines = 8
            line_length = 5

            step = 2 * effect.get_step()
            max_step = BOT_RADIUS * 3

            if step > max_step:
                effect.remove()

            center_x = effect.x()
            center_y = effect.y()

            # Calculate direction vector of the line
            for line in range(number_of_lines):
                degrees = line * (360 // number_of_lines)
                angle_radians = math.radians(degrees)

                # Rotate the vertical, unit vector x º
                x, y = 0, 1
                vector_x = (x * math.cos(angle_radians) - y * math.sin(angle_radians))
                vector_y = (x * math.sin(angle_radians) + y * math.cos(angle_radians))

                start_x = center_x + vector_x * step
                start_y = center_y + vector_y * step

                end_x = start_x + vector_x * (line_length + step)
                end_y = start_y + vector_y * (line_length + step)

                pygame.draw.line(self.__screen, WHITE, (start_x, start_y), (end_x, end_y), int(self.__map_range(step, 0, max_step, 5, 1)))

        for effect in self.__entities["effects"].values():
            if effect.type() == "player_death":
                draw_player_death_effect(effect)
            elif effect.type() == "pick_drop":
                draw_pick_drop_effect(effect)

