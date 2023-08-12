from simulation import Simulation
from time import sleep
from simulation_consts import *
import log

if __name__ == '__main__':
    log.i("Starting the simulation engine...")

    while True:
        log.i("Creating the simulation object...")
        # Create an empty simulation
        sim = Simulation()
        log.i("Simulation created")

        log.i("Running the simulation...")
        # Run the simulation
        sim.run()
        log.i("The simulation has run successfully")

        log.i("Saving the animation...")
        # Save the animation
        sim.save_replay()
        log.i("Simulation saved")

        log.i("Sleeping...")
        # Wait x minutes before running the simulation again
        sleep(INTER_SIMULATION_TIME)
