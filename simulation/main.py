from simulation import Simulation
from time import sleep
from simulation_consts import *
import log

if __name__ == '__main__':
    log.i("Starting the simulation engine...")

    while True:
        log.d("Creating the simulation object...")
        # Create an empty simulation
        sim = Simulation()
        log.d("Simulation created")

        log.d("Running the simulation...")
        # Run the simulation
        sim.run()
        log.d("The simulation has run successfully")

        log.d("Saving the animation...")
        # Save the animation
        sim.save_replay()
        log.d("Simulation saved")

        log.d("Sleeping...")
        # Wait x minutes before running the simulation again
        sleep(INTER_SIMULATION_TIME)
