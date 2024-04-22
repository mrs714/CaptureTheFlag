# Constants
MAP_SIZE = 500 # Check the files, we'll give CONSTS in the future
ENEMY_CLOSE_RANGE = 100
LOW_HEALTH = 75

# Setup game access
nearest_object = game.functions.nearest_object
get_attribute = game.functions.get_attribute
vector_to = game.functions.vector_to
vector_length = game.functions.vector_length
get_objects_in_range = game.functions.get_objects_in_range
get_bots_in_range_melee = game.functions.get_bots_in_range_melee
print_info = game.functions.print
move = game.actions.move
shoot = game.actions.shoot
super_shot = game.actions.super_shot
melee = game.actions.melee
super_melee = game.actions.super_melee

# Functions
def search_drop(type): # Get vector to closest drop of type "type"
  closest_drop_id = nearest_object(type)
  if closest_drop_id != None:
    # Get the drop info
    x = get_attribute(closest_drop_id, type, "x")
    y = get_attribute(closest_drop_id, type, "y")
    vector = vector_to(x, y)
    return vector
  return None

def get_vector_to_closest_enemy(): # Get vector to closest enemy
  closest_enemy_id = nearest_object() # Default: type = "bot"
  if closest_enemy_id is not None:
    x = get_attribute(closest_enemy_id, "bots", "x")
    y = get_attribute(closest_enemy_id, "bots", "y")
    vector = vector_to(x, y)   
    return vector
  return None

def get_vector_flag(): # Get vector to closest flag
  closest_flag_id = nearest_object("flags")
  if closest_flag_id is not None:
    x = get_attribute(closest_flag_id, "flags", "x")
    y = get_attribute(closest_flag_id, "flags", "y")
    vector = vector_to(x, y)
    return vector
  return None

def get_vector_my_zone():
    zones_ids = get_objects_in_range("zones", MAP_SIZE)
    
    # Check if zone bot_id is the same as my bot_id
    if zones_ids is not None:
        my_id = get_attribute(None, "me", "id")
        for zone_id in zones_ids:
            if get_attribute(zone_id, "zones", "owner") == my_id:
                x = get_attribute(zone_id, "zones", "x")
                y = get_attribute(zone_id, "zones", "y")
                vector = vector_to(x, y)
                return vector
    return None

def flag_in_my_zone():
    # Get all the zones
    zones_ids = get_objects_in_range("zones", 1000) # Default: type = "bot", MAP_SIZE / 10
    #game.functions.print("Closest zone id: " + str(closest_zone_id))

    # Check if zone bot_id is the same as my bot_id
    if zones_ids is not None:
        my_id = get_attribute(None, "me", "id")
        for zone_id in zones_ids:
            if get_attribute(zone_id, "zones", "owner") == my_id:

                # Check if there is a flag in the zone
                if get_attribute(zone_id, "zones", "contains_flag") is not None:
                    return True
           
# Check the state of the bot - shield and health
low_health = False
no_shield = False

if get_attribute(None, "me", "health") < LOW_HEALTH:
    low_health = True
    # Search for the nearest health drop:
    vector = search_drop("drops_health")

    # Move towards it
    if vector is not None:
        move(vector[0], vector[1])

elif get_attribute(None, "me", "shield") == 0:
    vector = search_drop("drops_shield")

    if vector is not None:
        move(vector[0], vector[1])

# Go put the flag in my base
if not flag_in_my_zone():
    carrying_flag = get_attribute(None, "me", "carrying_flag_id") is not None
    if not carrying_flag:
        vector = get_vector_flag()
        if vector is not None:
            move(vector[0], vector[1])
    else:
        print_info("Carrying flag")
        vector = get_vector_my_zone()
        if vector is not None:
            move(vector[0], vector[1])
        else:
            print_info("No vector to my zone")
    
else: # If the flag is in my zone, go kill the enemies
    # Check for any enemy too close, and shoot at the closest either way
    close_enemies = get_objects_in_range("bots", ENEMY_CLOSE_RANGE) # Default range
    vector = get_vector_to_closest_enemy()

    if close_enemies != []:
        # If the enemy is too far, move towards it
        if vector_length(vector) > 50:
            move(vector[0], vector[1])
        # But don't get too close
        else:
            move(-vector[0], -vector[1])
  
    else: # If no enemy is too close, move towards the nearest drop
        vector = search_drop("drops_points")
        if vector is not None: # There might not always be a points drop
            move(vector[0], vector[1])
  
    # Regardless of the above, shoot at the closest enemy
    vector = get_vector_to_closest_enemy()
    if vector is not None:
        shoot(vector[0], vector[1])
        super_shot(vector[0], vector[1])
        
    # And if the enemy is too close, use melee
    if get_bots_in_range_melee()[0]:
        melee()
        super_melee()