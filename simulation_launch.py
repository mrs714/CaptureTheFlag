from simulation.simulation import Simulation
from time import sleep
from simulation.simulation_consts import *
from log import setup_logger
import atexit

if __name__ == '__main__':
    # Setup the logger
    logger, handlers = setup_logger("simulation", "logs/simulation")

    logger.info("Starting the simulation engine...")

    while True:
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
        sim.save_replay()
        logger.info("Simulation saved")

        logger.info("Sleeping...")
        # Wait x minutes before running the simulation again
        sleep(INTER_SIMULATION_TIME)

@atexit.register
def clean_up():
    global handlers
    for handler in handlers:
        handler.close()