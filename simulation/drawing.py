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
            else:
                pygame.draw.circle(self.__screen, self.__random_color(), bullet.pos(), BULLET_RADIUS * 1.5)
    
    def __draw_drops(self):
        for drop in self.__entities["drops_points"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_POINTS, drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_health"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_HEALTH, drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_shield"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_SHIELD, drop.pos(), DROP_RADIUS)

    def __draw_bot_shield(self, bot):
        normalized_shield = math.ceil((bot.get_defense() / bot.get_shield()) * 10) # 1 to 10
        pygame.draw.circle(self.__screen, CYAN, bot.pos(), BOT_RADIUS + normalized_shield, max(normalized_shield, 1))