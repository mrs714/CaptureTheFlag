# Get the closest drop id of type "type"
closest_drop_id = game.functions.nearest_object("drops_points")
game.functions.print("Closest drop id: " + str(closest_drop_id))

if closest_drop_id != None:
  # Get the drop info
  x = game.functions.get_attribute(closest_drop_id, "drops_points", "x")
  y = game.functions.get_attribute(closest_drop_id, "drops_points", "y")
  game.functions.print("Drop position: " + str(x) + ", " + str(y))

  # Get the vector to there:
  vector = game.functions.vector_to(x, y)   
  game.functions.print("Direction vector: " + str(vector))

  # Move towards it
  game.actions.move(vector[0], vector[1])