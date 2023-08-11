from simulation import Simulation
from time import sleep
from simulation_consts import *

if __name__ == '__main__':

    while True:
        # Create an empty simulation
        sim = Simulation()

        # Run the simulation
        sim.run()

        # Save the animation
        sim.save_replay()

        # Wait 5 minutes before running the simulation again
        sleep(INTER_SIMULATION_TIME)
