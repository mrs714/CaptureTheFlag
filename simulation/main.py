from simulation import Simulation
from time import sleep
from simulation_consts import *
import log

if __name__ == '__main__':

    while True:
        log.d("Creating the simulation")
        # Create an empty simulation
        sim = Simulation()
        log.i("Simulation created")

        log.d("Preparing to run the simulation")
        # Run the simulation
        sim.run()
        log.i("The simulation has run successfully")

        log.d("Saving the animation")
        # Save the animation
        sim.save_replay()
        log.i("Simulation saved")

        log.d("Sleeping")
        # Wait 5 minutes before running the simulation again
        sleep(INTER_SIMULATION_TIME)
