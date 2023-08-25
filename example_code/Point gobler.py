# Get the closest drop id of type "type"
closest_drop_id = game.functions.nearest_object(type)
game.functions.print("Closest drop id: " + str(closest_drop_id))

if closest_drop_id != None:
  # Get the drop info
  x = game.functions.get_attribute(closest_drop_id, type, "x")
  y = game.functions.get_attribute(closest_drop_id, type, "y")
  game.functions.print("Drop position: " + str(x) + ", " + str(y) + ", " + str(type))

  # Get the vector to there:
  vector = game.functions.vector_to(x, y)   
  game.functions.print("Direction vector: " + str(vector))

  # Move towards it
  game.actions.move(vector[0], vector[1])