from simulation.simulation_consts import * #import all the constants
from simulation.bot import Bot
from simulation.bullet import Bullet
from simulation.drop import Drop
from simulation.collision_algorithm import CollisionAlgorithm
from simulation.player_context.game import Game #import Game (for giving information to the bot code)

import pygame
from datetime import datetime #import datetime (to get the current date and time)
from moviepy.editor import ImageSequenceClip #import ImageSequenceClip (for saving the mp4 file)

# User code has access to the following modules:
import random as rnd
import numpy as np
import math

import database.db_access as db
import json

# Restricted python imports
from RestrictedPython import compile_restricted_exec, safe_globals
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
from RestrictedPython.Guards import guarded_iter_unpack_sequence, full_write_guard

from io import StringIO #import StringIO (for capturing the bot output)
import sys
import traceback

class Simulation:

    def __init__(self, logger):
        
        self.__logger = logger

        self.__logger.debug("Initializing pygame...")
        pygame.init()
        self.__logger.debug("Pygame initialized")
        
        self.__logger.debug("Creating the screen...")
        self.__screen = pygame.display.set_mode((MAP_WIDTH + MAP_PADDING * 2, MAP_HEIGHT + MAP_PADDING * 2), pygame.NOFRAME)
        self.__logger.debug("Screen created")

        self.__logger.debug("Initializing simulation object variables...")
        self.__clock = pygame.time.Clock()
        self.__current_tick = 0
        self.__frames = []
        self.__id_counter = 0
        self.__entities = {
            "bots": {},
            "dead_bots": {},
            "bullets": {},
            "bullets_to_remove": {},
            "drops_points": {},
            "drops_health": {},
            "drops_shield": {},
            "drops_to_remove": {}
        }
        self.__collision_detector = CollisionAlgorithm()
        self.__logger.debug("Simulation object variables initialized")
    
    def get_id(self):
        self.__id_counter += 1
        return self.__id_counter
    
    def run(self):

        self.__logger.debug("Preparing to run the simulation...")
        list_of_bots = db.get_bots_to_execute()
        for bot in list_of_bots:
            config = json.loads(bot["config"])
            sim_id = self.get_id()
            self.__entities["bots"][sim_id] = Bot(sim_id, 
                                                  bot["id"], 
                                                  bot["username"], 
                                                  rnd.randint(100, MAP_WIDTH - 100), # At least 50 inside the play-zone
                                                  rnd.randint(100, MAP_HEIGHT - 100), 
                                                  bot["code"], 
                                                  config["health"], 
                                                  config["shield"], 
                                                  config["attack"])
        self.__logger.info("Bots participating: " + str([bot.get_name() for bot in self.__entities["bots"].values()]))
        self.__logger.debug("Simulation prepared")

        self.__logger.debug("Running the simulation loop...")
        running = True
        while self.__current_tick < DURATION and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.__perform_actions()
            self.__update_frame()
            pygame.display.flip()

            self.__save_frame()

            self.__current_tick += 1
            self.__clock.tick(FPS)

        pygame.quit()
        self.__logger.debug("Simulation loop finished")

        self.__logger.debug("Performing post-simulation tasks...")

        all_bots = [val for d in (self.__entities["bots"], self.__entities["dead_bots"]) for val in d.values()]
        for bot in all_bots:
            db.update_info(bot.get_db_id(), bot.get_last_position(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bot.get_events(), 0 if bot.get_last_position() == -1 else 1)

        self.__logger.debug("Post-simulation tasks performed")

    def __generate_actions(self, bot):
        def move(dx, dy):
            bot.move(dx, dy, self.__current_tick)

        def dash(dx, dy):
            bot.dash(dx, dy, self.__current_tick)
        
        def shoot(dx, dy):
            if bot.shoot(self.__current_tick):
                sim_id = self.get_id()
                self.__entities["bullets"][sim_id] = Bullet(sim_id, 
                                                            bot.x(), 
                                                            bot.y(), 
                                                            dx, 
                                                            dy, 
                                                            BULLET_DAMAGE,
                                                            bot.id())
        
        def super_shot(dx, dy):
            pass

        def melee():
            pass

        def super_melee():
            pass
        
        return move, shoot, melee, dash, super_shot, super_melee

    def __execute_bot_code(self, bot, bots_to_remove):

        # Create an object to give information about the state of the game to the bot code
        game = Game(bot, self.__entities, self.__generate_actions(bot), self.__current_tick)

        # Create a dictionary with the names that the user code has access to
        player_globals = safe_globals.copy()

        # Add the names that the user code has access to
        player_globals["game"] = game
        player_globals["rnd"] = rnd
        player_globals["np"] = np
        player_globals["math"] = math

        # Internal names to make the restricted execution work
        player_globals["__metaclass__"] = type
        player_globals["__name__"] = "simulation_sandbox"
        player_globals["_getiter_"] = default_guarded_getiter
        player_globals["_getitem_"] = default_guarded_getitem
        player_globals["_iter_unpack_sequence_"] = guarded_iter_unpack_sequence
        player_globals["_write_"] = full_write_guard

        # Capture the bot output
        temp_out = StringIO()
        sys.stdout = temp_out
        sys.stderr = temp_out

        # Name of the file that will be used to compile the bot code
        filename = "<user_string>"

        # Compile the bot code
        bot_code_compiled = compile_restricted_exec(bot.code(), filename=filename)

        try:
            # Log any warnings while compiling the bot code
            if bot_code_compiled.warnings:
                self.__logger.warning(f"Warning while compiling the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {bot_code_compiled.warnings}")
            
            # Check for errors while compiling the bot code
            if bot_code_compiled.errors:
                # Print and log the errors
                for error in bot_code_compiled.errors:
                    temp_out.write(error)
                self.__logger.warning(f"Error while compiling the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {bot_code_compiled.errors}")
            else:
                # If there are no errors, execute the bot code
                exec(bot_code_compiled.code, player_globals, {}) #execute the bot code
        except:
            # If there is an error while executing the bot code, print and log the error
            self.__logger.warning(f"Error while executing the bot code with db_id = {bot.get_db_id()} and name = {bot.get_name()}: {traceback.format_exc()}")
            cl, exc, tb = sys.exc_info() #cl: class, exc: exception, tb: traceback
            tb2 = traceback.extract_tb(tb)
            for i in range(len(tb2)-1, -1, -1): #iterate through the traceback in reverse order
                if tb2[i].filename == filename: #get the last traceback frame that is in the user code
                    break

            # Print the error
            temp_out.write(f"Line {tb2[i].lineno}: {cl.__name__}: {exc}")
            
            bot.set_last_position(-1)
            bots_to_remove.append(bot.id())
        finally:

            # Get the bot output
            event = temp_out.getvalue()
            if event != "":
                bot.add_event(event)

            # Restore the standard output and error
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

            # Close the StringIO object
            temp_out.close()

    def get_entities(self): # Can the entities be modified? !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return self.__entities

    def __perform_actions(self):
        bots_to_remove = []

        # Move and spawn all entities
        for bot in self.__entities["bots"].values():
            self.__execute_bot_code(bot, bots_to_remove)

        for bullet in self.__entities["bullets"].values():
            if bullet.to_remove():
                self.__entities["bullets_to_remove"][bullet.id()] = self.__entities["bullets"][bullet.id()]
                continue
            bullet.move()

        self.__spawn_drops()
        
        # Check for collisions
        collisions = self.__collision_detector.check_collisions(self.__entities["bots"], self.__entities["bullets"], self.__entities["drops_points"] | self.__entities["drops_health"] | self.__entities["drops_shield"])
        self.__collision_handler(collisions)

        # Remove the bots, bullets and drops that have to be removed
        for bot_id in bots_to_remove:
            db_bot = self.__entities["bots"][bot_id].get_db_id()
            self.__entities["dead_bots"][bot_id] = self.__entities["bots"].pop(bot_id)
            self.__logger.debug(f"Bot with db_id = {db_bot} removed")
        
        for bullet_id in self.__entities["bullets_to_remove"].keys():
            self.__entities["bullets"].pop(bullet_id)
        self.__entities["bullets_to_remove"].clear() # Clear the list of bullets to remove

        

    def __spawn_drops(self):


        def spawn(drop):
            sim_id = self.get_id()
            self.__entities["drops_" + drop][sim_id] = Drop(sim_id, 
                                                            rnd.randint(MAP_PADDING + DROP_RADIUS, MAP_WIDTH + MAP_PADDING - DROP_RADIUS), 
                                                            rnd.randint(MAP_PADDING + DROP_RADIUS, MAP_HEIGHT + MAP_PADDING - DROP_RADIUS), 
                                                            drop)

        # If empty, replenish health and shield drops:
        if len(self.__entities["drops_health"]) < NUMBER_OF_HEALTH_DROPS:
            spawn("health")
        
        if len(self.__entities["drops_shield"]) < NUMBER_OF_SHIELD_DROPS:
            spawn("shield")
        
        # Point drops: Minimum ammount: ceil(players/4); Maximum ammount: max((players-1), 1);
        if (len(self.__entities["drops_points"]) < math.ceil(len(self.__entities["bots"]))) or (self.__current_tick % TIME_BETWEEN_DROPS == 0):
            if len(self.__entities["drops_points"]) < max((len(self.__entities["bots"]) - 1), 1):
                spawn("points")
    
    # Gets a list of the bots and the entities they are colliding with
    def __collision_handler(self, collisions):
        if collisions:
            for bot, entity in collisions:
                if type(entity) == Bullet:
                    self.__entities["bullets_to_remove"][entity.id()] = entity
                    bot.receive_shield_damage(BULLET_DAMAGE)
                    print("Bot {} was hit by bullet {}".format(bot.id(), entity.id()))
                if type(entity) == Drop:
                    print("Bot {} picked up drop {}".format(bot.id(), entity.id()))

    def __update_frame(self):
        self.__screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.__screen, DARK_GRAY, pygame.Rect(MAP_PADDING, MAP_PADDING, MAP_WIDTH, MAP_HEIGHT)) 
        for bot in self.__entities["bots"].values():
            pygame.draw.circle(self.__screen, BOT_COLOR, bot.pos(), BOT_RADIUS)
        for bullet in self.__entities["bullets"].values():
            pygame.draw.circle(self.__screen, BULLET_COLOR, bullet.pos(), BULLET_RADIUS)
        for drop in self.__entities["drops_points"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_POINTS, drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_health"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_HEALTH, drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_shield"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_SHIELD, drop.pos(), DROP_RADIUS)
    
    def __save_frame(self):
        frame = pygame.surfarray.array3d(self.__screen)
        
        frame = np.rot90(frame, k=-1)
        frame = np.fliplr(frame)

        self.__frames.append(frame)
    
    def save_replay(self):

        self.__logger.debug("Saving the mp4 file...")
        video_clip = ImageSequenceClip(self.__frames, fps=FPS)
        video_clip.write_videofile(SIM_MP4_NAME, fps=FPS)
        self.__logger.debug("Mp4 file saved")

        self.__logger.debug("Saving the simulation info file...")
        with open(SIM_INFO_NAME, "w") as f:
            f.write(f"Last simulation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        self.__logger.debug("Simulation info file saved")