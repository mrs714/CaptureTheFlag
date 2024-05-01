# Constants
MAP_SIZE = game.constants.MAP_SIZE
ENEMY_CLOSE_RANGE = 100
LOW_HEALTH = 75

# Functions
def search_drop(type): # Get vector to closest drop of type "type"
  closest_drop_id = game.functions.nearest_object(type)
  if closest_drop_id != None:
    # Get the drop info
    x = game.functions.get_attribute(closest_drop_id, type, "x")
    y = game.functions.get_attribute(closest_drop_id, type, "y")
    vector = game.functions.vector_to(x, y)
    return vector
  return None

def get_vector_to_closest_enemy(): # Get vector to closest enemy
  closest_enemy_id = game.functions.nearest_object() # Default: type = "bot"
  if closest_enemy_id is not None:
    x = game.functions.get_attribute(closest_enemy_id, "bots", "x")
    y = game.functions.get_attribute(closest_enemy_id, "bots", "y")
    vector = game.functions.vector_to(x, y)   
    return vector
  return None

def get_vector_flag(): # Get vector to closest flag
  closest_flag_id = game.functions.nearest_object("flags")
  if closest_flag_id is not None:
    x = game.functions.get_attribute(closest_flag_id, "flags", "x")
    y = game.functions.get_attribute(closest_flag_id, "flags", "y")
    vector = game.functions.vector_to(x, y)
    return vector
  return None

def get_vector_my_zone():
    zones_ids = game.functions.get_objects_in_range("zones", 1000)
    
    # Check if zone bot_id is the same as my bot_id
    if zones_ids is not None:
        my_id = game.functions.get_attribute(None, "me", "id")
        for zone_id in zones_ids:
            zone_owner = game.functions.get_attribute(zone_id, "zones", "owner_id")
            if zone_owner == my_id:
                x = game.functions.get_attribute(zone_id, "zones", "x")
                y = game.functions.get_attribute(zone_id, "zones", "y")
                vector = game.functions.vector_to(x, y)
                return vector
    return None

def flag_in_my_zone():
    my_id = game.functions.get_attribute(None, "me", "id")

    # Get flag
    flag_id = game.functions.get_objects_in_range("flags", 1000)
    
    # Check if the flag is in a zone
    if flag_id is not None:
        flag_zone = game.functions.get_attribute(flag_id, "flags", "in_zone")
        if flag_zone is not None:
            zone_owner = game.functions.get_attribute(flag_zone, "zones", "owner_id")
            if zone_owner == my_id:
                return True
    return False

           
# Check the state of the bot - shield and health
if game.functions.get_attribute(None, "me", "health") < LOW_HEALTH:
    vector = search_drop("drops_health")
    if vector is not None:
        game.actions.move(vector[0], vector[1])

elif game.functions.get_attribute(None, "me", "shield") == 0:
    vector = search_drop("drops_shield")
    if vector is not None:
        game.actions.move(vector[0], vector[1])

# Go put the flag in my base
if not flag_in_my_zone():
    carrying_flag = game.functions.get_attribute(None, "me", "carrying_flag_id") is not None
    if not carrying_flag:
        vector = get_vector_flag()
        if vector is not None:
            game.actions.move(vector[0], vector[1])
    else:
        game.functions.print("Carrying flag")
        vector = get_vector_my_zone()
        if vector is not None:
            game.actions.move(vector[0], vector[1])
        else:
            game.functions.print("No vector to my zone")
    
# If the flag is in my zone, go kill the enemies
# Check for any enemy too close, and shoot at the closest either way
close_enemies = game.functions.get_objects_in_range("bots", ENEMY_CLOSE_RANGE) # Default range
vector = get_vector_to_closest_enemy()

if close_enemies != []:
    # If the enemy is too far, move towards it
    if game.functions.vector_length(vector) > 50:
        game.actions.move(vector[0], vector[1])
    # But don't get too close
    else:
        game.actions.move(-vector[0], -vector[1])

else: # If no enemy is too close, move towards the nearest drop
    vector = search_drop("drops_points")
    if vector is not None: # There might not always be a points drop
        game.actions.move(vector[0], vector[1])

# Regardless of the above, shoot at the closest enemy
vector = get_vector_to_closest_enemy()
if vector is not None:
    game.actions.shoot(vector[0], vector[1])
    game.actions.super_shot(vector[0], vector[1])
    
# And if the enemy is too close, use melee
if game.functions.get_bots_in_range_melee()[0]:
    game.actions.melee()
    game.actions.super_melee()