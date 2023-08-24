if game.tick > 10: # Give the game some time to warm up

  # If there are enemies close, shoot them, move towards them
  close_enemies = game.functions.get_objects_in_range("bot", 200)
  game.functions.print("Close enemies: " + str(close_enemies))
  
  if close_enemies != []:
    
    # Get the closest bot id
    closest_enemy_id = game.functions.nearest_object("bot")
    game.functions.print("Closest enemy id: " + str(closest_enemy_id))
    
    # Get the bot info
    x = get_attr(closest_enemy_id, "bot", "x")
    y = get_attr(closest_enemy_id, "bot", "y")
    game.functions.print("Enemy position: " + str(x) + ", " + str(y))

    # Get the vector to there:
    vector = game.functions.vector_to(x, y)   
    game.functions.print("Direction vector: " + str(vector))

    # Move and shoot
    game.actions.move(vector[0], vector[1])
    game.actions.shoot(vector[0], vector[1])
    game.actions.super_shot(vector[0], vector[1])
    
"""
  else: 
    closest_drop_id = game.functions.nearest_object("points")
    game.functions.print(closest_drop_id)
    # Get the drop info
    drop_info = game.entities["drops_points"].get(closest_drop_id, None)
    game.functions.print(drop_info)
    if drop_info != None:
      x = drop_info.x
      y = drop_info.y

      # Get the vector to there:
      vector = game.functions.vector_to(x, y)   
      game.functions.print(vector)

      # Move for the points
      game.actions.move(vector[0], vector[1])

  # If an enemy is within melee range:
  if game.functions.get_bots_in_range_melee()[0]:
    game.actions.melee()
    game.actions.super_melee()"""