from simulation.simulation_consts import *

class Constants:
    def __init__(self):
        for key, value in globals().items():
            if key.isupper():
                setattr(self, key, value)