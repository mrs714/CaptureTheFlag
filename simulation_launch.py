from simulation.simulation import Simulation
from time import sleep
from simulation.simulation_consts import *
from log import setup_logger
import atexit
import argparse # Used to parse the arguments passed to the script
from datetime import datetime #import datetime (to get the current date and time)
import os
import shutil # Used to delete the frames folder before running the simulation again

def parse_arguments():
    parser = argparse.ArgumentParser(description="Simulation Script")
    parser.add_argument("--map-width", type=int, default=MAP_WIDTH, help="Width of the map")
    parser.add_argument("--map-height", type=int, default=MAP_HEIGHT, help="Height of the map")
    parser.add_argument("--duration", type=int, default=INTER_SIMULATION_TIME, help="Duration of the simulation")
    return parser.parse_args()

if __name__ == '__main__':
    
    args = parse_arguments()
    # Set constants based on command-line arguments
    MAP_WIDTH = args.map_width
    MAP_HEIGHT = args.map_height
    INTER_SIMULATION_TIME = args.duration

    logger, handlers = setup_logger("simulation", "logs/simulation")
    
    logger.info("Starting the simulation engine...")

    number_of_simulations = 1
    end_time = None
    start_time = None

    while True:

        if os.path.exists(SIM_FRAMES_PATH):
            shutil.rmtree(SIM_FRAMES_PATH) # Clean previous data
        expected_time = end_time - start_time if end_time else "?"
        start_time = datetime.now() 
        print(f"""\n\nStarting simulation {number_of_simulations} at {start_time}.
        Map size: {MAP_WIDTH}x{MAP_HEIGHT}
        Duration: {DURATION} seconds
        FPS: {FPS}
        Expected time for the simulation: {expected_time}\n\n""")

        logger.info(f"Creating the simulation {number_of_simulations} object...")
        # Create an empty simulation
        sim = Simulation(logger)
        logger.info(f"Simulation {number_of_simulations} created")

        logger.info(f"Running the simulation {number_of_simulations}...")
        # Run the simulation
        sim.run()
        logger.info(f"The simulation {number_of_simulations} has run successfully")

        logger.info(f"Saving the animation {number_of_simulations}...")

        # Save the animation
        sim.save_replay(start_time, number_of_simulations)
        logger.info(f"Simulation {number_of_simulations} saved")

        logger.info(f"Sleeping...")
        # Wait x seconds before running the simulation again
        end_time = datetime.now()
        print(f"{number_of_simulations} simulation(s) done. Waiting {INTER_SIMULATION_TIME} seconds before running the next simulation...\n\n")
        sleep(INTER_SIMULATION_TIME)

        number_of_simulations += 1

@atexit.register
def clean_up():
    global handlers
    for handler in handlers:
        handler.close()