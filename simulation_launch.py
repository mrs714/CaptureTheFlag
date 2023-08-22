from simulation.simulation import Simulation
from time import sleep
from simulation.simulation_consts import *
from log import setup_logger
import atexit
import argparse # Used to parse the arguments passed to the script
from datetime import datetime #import datetime (to get the current date and time)

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

    while True:
        start_time = datetime.now() 
        logger.info("Creating the simulation object...")
        # Create an empty simulation
        sim = Simulation(logger)
        logger.info("Simulation created")

        logger.info("Running the simulation...")
        # Run the simulation
        sim.run()
        logger.info("The simulation has run successfully")

        logger.info("Saving the animation...")

        # Save the animation
        end_time = datetime.now()
        sim.save_replay(end_time - start_time)
        logger.info("Simulation saved")

        logger.info("Sleeping...")
        # Wait x seconds before running the simulation again
        sleep(INTER_SIMULATION_TIME)

@atexit.register
def clean_up():
    global handlers
    for handler in handlers:
        handler.close()