from simulation_consts import *
import pygame
from datetime import datetime
import numpy as np
from moviepy.editor import ImageSequenceClip
import log
import sys

class Simulation:

    def __init__(self):
        log.d("Initializing pygame...")
        pygame.init()
        log.d("Pygame initialized")
        
        self.__screen = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        self.__clock = pygame.time.Clock()
        self.__current_tick = 0
        self.__frames = []
    
    def run(self):
        running = True

        while self.__current_tick < DURATION and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.__update_frame()
            pygame.display.flip()

            self.__save_frame()

            self.__current_tick += 1
            self.__clock.tick(FPS)

        pygame.quit()
    
    def __update_frame(self):
        self.__screen.fill((0, 0, 0))
        pygame.draw.circle(self.__screen, (255, 0, 0), (500, 500), 30)
    
    def __save_frame(self):
        frame = pygame.surfarray.array3d(self.__screen)
        
        frame = np.rot90(frame, k=-1)
        frame = np.fliplr(frame)

        self.__frames.append(frame)
    
    def save_replay(self):
        video_clip = ImageSequenceClip(self.__frames, fps=FPS)
        video_clip.write_videofile(SIM_MP4_NAME, fps=FPS)

        with open(SIM_INFO_NAME, "w") as f:
            f.write(f"Last simulation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")