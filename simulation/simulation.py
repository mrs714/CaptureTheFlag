from simulation.simulation_consts import * #import all the constants
from simulation.bot import Bot
from simulation.bullet import Bullet
from simulation.drop import Drop
from simulation.collision_algorithm import CollisionAlgorithm
from simulation.player_context.game import Game #import Game (for giving information to the bot code)

# Give the classes to the users
from simulation.player_context.bot_info import BotInfo
from simulation.player_context.drop_info import DropInfo
from simulation.player_context.bullet_info import BulletInfo

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
import os # Create folders if needed
import shutil # Remove full directories
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
        self.__frames_number = 10000 # Used to give name to the frames, it has to start high enough to avoid sorting errors (1, 10, 2, 3...)
        self.__id_counter = 0
        self.__entities = {
            "bots": {},
            "dead_bots": {},
            "bullets": {},
            "drops_points": {},
            "drops_health": {},
            "drops_shield": {}
        }
        self.__storage = {} # Storage for the players, associated to the db id
        self.__collision_detector = CollisionAlgorithm()
        self.__text_font = pygame.font.SysFont(None, 24)
        self.__logger.debug("Simulation object variables initialized")
        self.__bot_scores = [] # List of tuples (bot_name, score)
    
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
            self.__storage[bot["id"]] = {} # A dictionary for each player, to store the information they want
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

        # Make a list of tuples, bots and their puntuations
        bot_list = [(bot.get_name(), bot.get_points()) for bot in (self.__entities["bots"] | self.__entities["dead_bots"]).values()]
        self.__bot_scores = sorted(bot_list, key=lambda bot: bot[1], reverse=True)
        self.__logger.info("Bots sorted by points: " + str(self.__bot_scores))

        # Update db info
        all_bots = [val for d in (self.__entities["bots"], self.__entities["dead_bots"]) for val in d.values()]
        for bot in all_bots:
            db.update_info(bot.get_db_id(), -1 if bot.get_last_position() == -1 else bot_list.index((bot.get_name(), bot.get_points())) + 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), bot.get_events(), 0 if bot.get_last_position() == -1 else 1)
        self.__logger.debug("Post-simulation tasks performed")

    def get_bots_in_range(self, x, y, radius):
        return [bot.id() for bot in self.__entities["bots"].values() if (bot.x() - x)**2 + (bot.y() - y)**2 <= radius**2]
    
    def kill_bot(self, bot_id, bots_to_remove):
        #if bot_id in self.__entities["bots"]:
         #   self.__entities["bots"][bot_id].set_last_position(len(self.__entities["bots"]) + 1)
          # Pablo check, però la posició es determina en funció dels punts un cop acabada la partida no?
        bots_to_remove.append(bot_id)

    def __generate_actions(self, bot, bots_to_remove):
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
                                                            "normal",
                                                            bot.id())
        
        def super_shot(dx, dy):
            if bot.super_shot(self.__current_tick):
                sim_id = self.get_id()
                self.__entities["bullets"][sim_id] = Bullet(sim_id, 
                                                            bot.x(), 
                                                            bot.y(), 
                                                            dx, 
                                                            dy, 
                                                            BULLET_DAMAGE * 2,
                                                            "super",
                                                            bot.id())

        def melee():
            if bot.melee(self.__current_tick):
                for bot_id in self.get_bots_in_range(bot.x(), bot.y(), BOT_MELEE_RADIUS):
                    if bot_id == bot.id():
                        continue
                    if self.__entities["bots"][bot_id].receive_life_damage(MELEE_DAMAGE): # True if dead
                        self.__logger.debug("Bot {} was killed by melee from player {}".format(self.__entities["bots"][bot_id].get_name(), bot.get_name()))
                        self.kill_bot(bot_id, bots_to_remove)

        def super_melee():
            if bot.super_melee(self.__current_tick):
                for bot_id in self.get_bots_in_range(bot.x(), bot.y(), BOT_MELEE_RADIUS):
                    if bot_id == bot.id():
                        continue
                    if self.__entities["bots"][bot_id].recieve_shield_damage_extra(MELEE_DAMAGE): # True if dead
                        self.__logger.debug("Bot {} was killed by a super melee from player {}".format(self.__entities["bots"][bot_id].get_name(), bot.get_name()))
                        self.kill_bot(bot_id, bots_to_remove)
        
        return move, shoot, melee, dash, super_shot, super_melee
    
    def __generate_functions(self, bot): # Functions for the user
        
        bot_id = bot.id()
        
        def save_data(name, value): # Saves data in the storage - persistent storage
            self.__storage[bot_id][name] = value
        
        def get_data(name):
            return self.__storage.get(bot_id, {}).get(name, "Nothing stored here...")
        
        def print(string):
            bot.add_event("\nPrint: " + str(string) + "\n")

        def vector_to(x, y): # Returns vector to go to map coordinates
            return (x - bot.x(), y - bot.y())
        
        def vector_from_to(x, y, x2, y2):
            return (x2 - x, y2 - y)
        
        def unit_vector(vector):
            # Normalize the vector: 
            assert(vector[0] != 0 and vector[1] != 0)
            norm = np.linalg.norm(vector)
            return (vector[0]/norm, vector[1]/norm)
        
        def vector_length(vector):
            return np.linalg.norm(vector)
        
        def get_bots_in_range_melee(): # Tuple: (is there a bot in melee range, list with the ids of the bots in melee range)
            return self.get_bots_in_range(bot.x(), bot.y(), BOT_MELEE_RADIUS) != [], self.get_bots_in_range(bot.x(), bot.y(), BOT_MELEE_RADIUS)
        
        def nearest_object(type = "bot"): # Returns the id of the nearest enemy
            if type == "bot":
                return min([bot.id() for bot in self.__entities["bots"].values() if bot.id() != bot_id], key=lambda bot_id: (self.__entities["bots"][bot_id].x() - bot.x())**2 + (self.__entities["bots"][bot_id].y() - bot.y())**2)
            elif type == "bullet":
                return min([bullet.id() for bullet in self.__entities["bullets"].values()], key=lambda bullet_id: (self.__entities["bullets"][bullet_id].x() - bot.x())**2 + (self.__entities["bullets"][bullet_id].y() - bot.y())**2)
            elif type == "points":
                return min([drop.id() for drop in self.__entities["drops_points"].values()], key=lambda drop_id: (self.__entities["drops_points"][drop_id].x() - bot.x())**2 + (self.__entities["drops_points"][drop_id].y() - bot.y())**2)
            elif type == "health":
                return min([drop.id() for drop in self.__entities["drops_health"].values()], key=lambda drop_id: (self.__entities["drops_health"][drop_id].x() - bot.x())**2 + (self.__entities["drops_health"][drop_id].y() - bot.y())**2)
            elif type == "shield":
                return min([drop.id() for drop in self.__entities["drops_shield"].values()], key=lambda drop_id: (self.__entities["drops_shield"][drop_id].x() - bot.x())**2 + (self.__entities["drops_shield"][drop_id].y() - bot.y())**2)

        def get_objects_in_range(type = "bot", radius = MAP_HEIGHT / 10):
            if type == "bot":
                return [bot.id() for bot in self.__entities["bots"].values() if bot.id() != bot_id and (bot.x() - bot.x())**2 + (bot.y() - bot.y())**2 <= radius**2]
            elif type == "bullet":
                return [bullet.id() for bullet in self.__entities["bullets"].values() if (bullet.x() - bot.x())**2 + (bullet.y() - bot.y())**2 <= radius**2]
            elif type == "points":
                return [drop.id() for drop in self.__entities["drops_points"].values() if (drop.x() - bot.x())**2 + (drop.y() - bot.y())**2 <= radius**2]
            elif type == "health":
                return [drop.id() for drop in self.__entities["drops_health"].values() if (drop.x() - bot.x())**2 + (drop.y() - bot.y())**2 <= radius**2]
            elif type == "shield":
                return [drop.id() for drop in self.__entities["drops_shield"].values() if (drop.x() - bot.x())**2 + (drop.y() - bot.y())**2 <= radius**2]
                
        def get_attr(entity_id, type, attribute):
            if type == "bot":
                return getattr(self.__entities["bots"][entity_id].get_info(), attribute)
            elif type == "bullet":
                return self.__entities["bullets"][entity_id].get_info().attribute
            elif type == "points":
                return getattr(self.__entities["drops_points"][entity_id].get_info(), attribute)
                return self.__entities["drops_points"][entity_id].get_info().attribute
            elif type == "health":
                return self.__entities["drops_health"][entity_id].get_info().attribute
            elif type == "shield":
                return self.__entities["drops_shield"][entity_id].get_info().attribute
        

        return save_data, get_data, print, vector_to, vector_from_to, unit_vector, vector_length, get_bots_in_range_melee, nearest_object, get_objects_in_range, get_attr


    def __execute_bot_code(self, bot, bots_to_remove):

        # Create an object to give information about the state of the game to the bot code
        game = Game(bot, self.__entities, self.__generate_actions(bot, bots_to_remove), self.__current_tick, self.__generate_functions(bot))

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
        bullets_to_remove = []
        drops_to_remove = []

        # Move and spawn all entities
        for bot in self.__entities["bots"].values():
            self.__execute_bot_code(bot, bots_to_remove)

        for bullet in self.__entities["bullets"].values():
            if bullet.to_remove():
                bullets_to_remove.append(self.__entities["bullets"][bullet.id()].id())
                continue
            bullet.move()

        self.__spawn_drops()
        
        # Check for collisions
        collisions = self.__collision_detector.check_collisions(self.__entities["bots"], self.__entities["bullets"], self.__entities["drops_points"] | self.__entities["drops_health"] | self.__entities["drops_shield"])
        self.__collision_handler(collisions, bots_to_remove, bullets_to_remove, drops_to_remove)

        # Remove the bots, bullets and drops that have to be removed
        bots_to_remove = list(set(bots_to_remove))
        for bot_id in bots_to_remove:
            db_bot = self.__entities["bots"][bot_id].get_db_id()
            self.__entities["dead_bots"][bot_id] = self.__entities["bots"].pop(bot_id)
            self.__logger.debug(f"Bot with db_id = {db_bot} removed")
        
        # Check bullets aren't repeated
        bullets_to_remove = list(set(bullets_to_remove))
        for bullet_id in bullets_to_remove:
            self.__entities["bullets"].pop(bullet_id)  

        # Check drops aren't repeated
        drops_to_remove = list(set(drops_to_remove))
        for drop_id, drop_type in drops_to_remove:
            self.__entities[str("drops_" + drop_type)].pop(drop_id, None)

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
    def __collision_handler(self, collisions, bots_to_remove, bullets_to_remove, drops_to_remove):
        if collisions:
            for bot, entity in collisions:
                if type(entity) == Bullet:
                    bullets_to_remove.append(entity.id())
                    if entity.get_type() == "normal":
                        if (bot.receive_shield_damage(BULLET_DAMAGE)):
                            self.__logger.debug("Bot {} was killed by bullet from player {}".format(bot.get_name(), self.__entities["bots"][entity.get_owner_id()].get_name()))
                            self.kill_bot(bot.id(), bots_to_remove)
                    else: 
                        if (bot.receive_life_damage(MELEE_DAMAGE)):
                            self.__logger.debug("Bot {} was killed by a super bullet from player {}".format(bot.get_name(), self.__entities["bots"][entity.get_owner_id()].get_name()))
                            self.kill_bot(bot.id(), bots_to_remove)
                   
                if type(entity) == Drop:
                    drops_to_remove.append((entity.id(), entity.type()))
                    bot.get_drop(entity.type())

    def __update_frame(self):
        self.__screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.__screen, DARK_GRAY, pygame.Rect(MAP_PADDING, MAP_PADDING, MAP_WIDTH, MAP_HEIGHT)) 
        for bot in self.__entities["bots"].values():
            pygame.draw.circle(self.__screen, BOT_COLOR, bot.pos(), BOT_RADIUS)
            name = self.__text_font.render(str(bot.get_name()), True, WHITE)
            life = self.__text_font.render(str(bot.get_life()), True, ORANGE)
            shield = self.__text_font.render(str(bot.get_defense()), True, CYAN)
            points = self.__text_font.render(str(bot.get_points()), True, GREEN)
            self.__screen.blit(name, (bot.x() - BOT_RADIUS, bot.y() + 2 * BOT_RADIUS))
            self.__screen.blit(life, (bot.x() - BOT_RADIUS, bot.y() + 3 * BOT_RADIUS))
            self.__screen.blit(shield, (bot.x() - BOT_RADIUS, bot.y() + 4 * BOT_RADIUS))
            self.__screen.blit(points, (bot.x() - BOT_RADIUS, bot.y() + 5 * BOT_RADIUS))
        for bullet in self.__entities["bullets"].values():
            if bullet.get_type() == "normal":
                pygame.draw.circle(self.__screen, BULLET_COLOR, bullet.pos(), BULLET_RADIUS)
            else:
                pygame.draw.circle(self.__screen, random_color(), bullet.pos(), BULLET_RADIUS * 1.5)
        for drop in self.__entities["drops_points"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_POINTS, drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_health"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_HEALTH, drop.pos(), DROP_RADIUS)
        for drop in self.__entities["drops_shield"].values():
            pygame.draw.circle(self.__screen, DROP_COLOR_SHIELD, drop.pos(), DROP_RADIUS)
        
    
    def __save_frame(self):
        # Take a frame, rotate it and flip it, and append it to the list of frames
        frame = pygame.surfarray.array3d(self.__screen)
        
        #frame = np.rot90(frame, k=-1)
        #frame = np.fliplr(frame)
        frame = pygame.surfarray.make_surface(frame)

        self.__frames.append(frame)

        # This eats memory, as *every* frame is stored at once on RAM. To solve this:
        if len(self.__frames) > math.ceil(MAX_FRAMES_ON_RAM) or self.__current_tick == DURATION - 1:
            
            # Create the folders if they don't exist
            if not os.path.exists(SIM_FRAMES_PATH):
                if not os.path.exists(SIM_FOLDER):
                    os.makedirs(SIM_FOLDER, exist_ok=True)
                os.makedirs(SIM_FRAMES_PATH, exist_ok=True)
            
            for frame in self.__frames:
                pygame.image.save(frame, os.path.join(SIM_FRAMES_PATH, str(self.__frames_number) + ".png"))
                self.__frames_number += 1
            self.__frames = []
    
    def save_replay(self, start_time, number_of_simulations):
        # We want to save the files apart so that they are available for download while they are being generated
        
        # Create video
        self.__logger.debug("Saving the mp4 file...")
        video_clip = ImageSequenceClip(SIM_FRAMES_PATH, fps=FPS)

        # Prepare directories
        if not os.path.exists(SIM_PLACEHOLDER_FOLDER):
            os.makedirs(SIM_PLACEHOLDER_FOLDER, exist_ok=True)

        # Save the video to the placeholder folder
        video_clip.write_videofile(SIM_VIDEO_PLACEHOLDER_PATH, fps=FPS)
        self.__logger.debug("Mp4 file saved")
        
        # Save the simulation info file
        self.__logger.debug("Saving the simulation info file...")
        
        # Prepare directory

        # Save the file to the placeholder folder
        with open(SIM_INFO_PLACEHOLDER_PATH, "w") as f:
            time_elapsed = datetime.now() - start_time
            # IF THE FORMAT IS CHANGED, REPLAYS() IN APP.PY MUST BE CHANGED TOO
            f.write(f"Last simulation: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} Duration: {str(time_elapsed)} Winner: {self.__bot_scores[0][0] if self.__bot_scores != [] else 'None'} Score: {self.__bot_scores[0][1] if self.__bot_scores != [] else 0} Number of simulations: {number_of_simulations}") 
        self.__logger.debug("Simulation info file saved")

        # Move everything to the correct folder (overwrite if needed)
        shutil.move(SIM_VIDEO_PLACEHOLDER_PATH, SIM_MP4_NAME)
        shutil.move(SIM_INFO_PLACEHOLDER_PATH, SIM_INFO_NAME)

        # Wrap everything up
        shutil.rmtree(SIM_FRAMES_PATH)
        shutil.rmtree(SIM_PLACEHOLDER_FOLDER)
