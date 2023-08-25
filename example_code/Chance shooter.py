# Get two random vectors
x = rnd.randint(-10000, 10000)
y = rnd.randint(-10000, 10000)

# Shoot at it
game.actions.shoot(x, y)
game.actions.super_shot(x, y)

# Just in case someone gets too close... 
game.actions.melee()
game.actions.super_melee()