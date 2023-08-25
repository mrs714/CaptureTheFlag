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

    def draw_frame(self, screen, entities):
        self.__entities = entities

        self.__draw_map()

        self.__draw_bots()
        self.__draw_bullets()
        self.__draw_drops()

    def __random_color(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))
    
    def __draw_map(self):
        self.__screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.__screen, DARK_GRAY, pygame.Rect(MAP_PADDING, MAP_PADDING, MAP_WIDTH, MAP_HEIGHT)) 

    def __draw_bots(self):
        for bot in self.__entities["bots"].values():

            normalized_color = bot.get_life() / bot.get_health() # 0 to 1
            blue = math.ceil(255 * normalized_color)
            bot_color = (BOT_COLOR[0], BOT_COLOR[1], blue)
            pygame.draw.circle(self.__screen, bot_color, bot.pos(), BOT_RADIUS)

            self.__draw_bot_shield(bot)

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
        for bullet in self.__entities["bullets"].values():
            if bullet.get_type() == "normal":
                pygame.draw.circle(self.__screen, BULLET_COLOR, bullet.pos(), BULLET_RADIUS)
                self.__draw_speed_lines(bullet)
            else:
                pygame.draw.circle(self.__screen, self.__random_color(), bullet.pos(), BULLET_RADIUS * 1.5)

    def __draw_speed_lines(self, bullet):
        # Draws ten random black lines from the back of the bullet in the -direction of travel

        # Get the center of the bullet and the -direction vector
        start_point = (bullet.x(), bullet.y())
        direction_unit_vector = (-bullet.get_vector_direction()[0], -bullet.get_vector_direction()[1])

        for i in range(5):
            # First, randomize the direction of the vector +- 90º:
            degrees = randint(-70, 70)

            # Rotate the vector direction x degrees:
            angle_radians = math.radians(degrees)
            x, y = direction_unit_vector
            start_x = start_point[0] + (x * math.cos(angle_radians) - y * math.sin(angle_radians)) * BULLET_RADIUS
            start_y = start_point[1] + (x * math.sin(angle_radians) + y * math.cos(angle_radians)) * BULLET_RADIUS
            
            length = randint(10, 50)

            end_x = start_x + direction_unit_vector[0] * length
            end_y = start_y + direction_unit_vector[1] * length

            pygame.draw.line(self.__screen, BLACK, (start_x, start_y), (end_x, end_y))
    
    def __draw_drops(self):
        for drop in self.__entities["drops_points"].values():
            pygame.draw.circle(self.__screen, self.__drop_color(drop, DROP_COLOR_POINTS_MIN, DROP_COLOR_POINTS_MAX), drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_health"].values():
            pygame.draw.circle(self.__screen, self.__drop_color(drop, DROP_COLOR_HEALTH_MIN, DROP_COLOR_HEALTH_MAX), drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_shield"].values():
            pygame.draw.circle(self.__screen, self.__drop_color(drop, DROP_COLOR_SHIELD_MIN, DROP_COLOR_SHIELD_MAX), drop.pos(), DROP_RADIUS)

    def __drop_color(self, drop, min_color, max_color): 

        def map_range(value, input_min, input_max, output_min, output_max):
            return output_min + (value - input_min) * (output_max - output_min) / (input_max - input_min)

        blinking = drop.get_state()["blinking"]
        drop_color = drop.get_state()["color"]
        min_difference = min(255 - min_color[0], 255 - min_color[1], 255 - min_color[2])    
        
        if drop_color == None:
            drop.set_state({"blinking": blinking, "color": min_color})
            return min_color
        if blinking:
            multiplier = map_range(min_difference, 0, 255, 1.01, 1.1)
            new_color = (drop_color[0] * multiplier, drop_color[1] * multiplier, drop_color[2] * multiplier)
            if new_color[0] > max_color[0] or new_color[1] > max_color[1] or new_color[2] > max_color[2]:
                new_color = max_color
                blinking = False
            drop.set_state({"blinking": blinking, "color": new_color})
            return new_color
        else:
            multiplier = map_range(min_difference, 0, 255, 0.99, 0.9)
            new_color = (drop_color[0] * multiplier, drop_color[1] * multiplier, drop_color[2] * multiplier)
            if new_color[0] < min_color[0] or new_color[1] < min_color[1] or new_color[2] < min_color[2]:
                new_color = min_color
                blinking = True
            drop.set_state({"blinking": blinking, "color": new_color})
            return new_color



    def __draw_bot_shield(self, bot):
        normalized_shield = int((bot.get_defense() / bot.get_shield()) * 10) # 1 to 10
        pygame.draw.circle(self.__screen, CYAN if normalized_shield > 0 else RED, bot.pos(), BOT_RADIUS + normalized_shield, max(normalized_shield, 1))