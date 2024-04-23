# Constants
MAP_SIZE = 500 # Check the files, we'll give CONSTS in the future
ENEMY_CLOSE_RANGE = 100
LOW_HEALTH = 75

# Functions
def search_drop(type):
  # Get the closest drop id of type "type"
  closest_drop_id = game.functions.nearest_object(type)
  #game.functions.print("Closest drop id: " + str(closest_drop_id))

  if closest_drop_id != None:
    # Get the drop info
    x = game.functions.get_attribute(closest_drop_id, type, "x")
    y = game.functions.get_attribute(closest_drop_id, type, "y")
    #game.functions.print("Drop position: " + str(x) + ", " + str(y) + ", " + str(type))

    # Get the vector to there:
    vector = game.functions.vector_to(x, y)   
    #game.functions.print("Direction vector: " + str(vector))

    # Return info
    return vector
  return None

def get_vector_to_closest_enemy():
  # Get the closest bot id
  closest_enemy_id = game.functions.nearest_object() # Default: type = "bot"
  #game.functions.print("Closest enemy id: " + str(closest_enemy_id))
	
  if closest_enemy_id is not None:
    # Get the bot info
    x = game.functions.get_attribute(closest_enemy_id, "bots", "x")
    y = game.functions.get_attribute(closest_enemy_id, "bots", "y")
    #game.functions.print("Enemy position: " + str(x) + ", " + str(y))

    # Get the vector to there:
    vector = game.functions.vector_to(x, y)   
    #game.functions.print("Direction vector: " + str(vector))
    return vector
  return None
  
# Check the state of the bot - shield and health
low_health = False
no_shield = False
#game.functions.print("Health: " + str(game.functions.get_attribute(0, "me", "health")))
#game.functions.print("Shield: " + str(game.functions.get_attribute(0, "me", "shield")))

if game.functions.get_attribute(None, "me", "health") < LOW_HEALTH:
  low_health = True
  # Search for the nearest health drop:
  vector = search_drop("drops_health")
  
  # Move towards it
  if vector is not None:
  	game.actions.move(vector[0], vector[1])

elif game.functions.get_attribute(None, "me", "shield") == 0:
  vector = search_drop("drops_shield")
  
  if vector is not None:
    game.actions.move(vector[0], vector[1])
    
    
# Check for any enemy too close, and shoot at the closest either way
close_enemies = game.functions.get_objects_in_range("bots", ENEMY_CLOSE_RANGE) # Default range
#game.functions.print("Close enemies: " + str(close_enemies))
vector = get_vector_to_closest_enemy()

if close_enemies != []:
  # If the enemy is too far.. 
  if game.functions.vector_length(vector) > 50:
    game.actions.move(vector[0], vector[1])
  # But if it's too close....
  else:
    game.actions.move(-vector[0], -vector[1])
  
else: 
  # Get vector to nearest drop of points 
  vector = search_drop("drops_points")
  
  if vector is not None: # There might not always be a points drop
    # Move towards it
    game.actions.move(vector[0], vector[1])
  
# Shoot to the closest enemy:
vector = get_vector_to_closest_enemy()
if vector is not None:
  # Shoot in the given direction
  game.actions.shoot(vector[0], vector[1])
  game.actions.super_shot(vector[0], vector[1])
  
# If an enemy is within melee range:
if game.functions.get_bots_in_range_melee()[0]:
  game.actions.melee()
  game.actions.super_melee()