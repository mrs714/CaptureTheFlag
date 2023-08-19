from simulation.simulation_consts import *

class CollisionAlgorithm():
    
    # The map is divided in a grid of cells.
    class Cell():
        def __init__(self, row, column):
            self.__row = row
            self.__column = column
            self.__grid_position = (row, column)
            
            # Each cell has a dictionary for the bots, bullets and drops it contains, and their id's.
            # Those lists will be updated at each tick/frame.
            self.__bots = {}
            self.__bullets = {}
            self.__drops = {}

    def __init__(self):
        
        self.__cells = []
        pass