if game.entities["me"].x < 100: 
  game.actions.move(1,0)
game.actions.dash(-1,0)

x = 0
y = 0
  
info = []

if game.entities["bots"] != {}:
  for id, bot_info in game.entities["bots"]:
    info.append(bot_info)
 
if info != []:
  x = info[0].x
  y = info[0].y
else:
  x = rnd.randint(-100000, 100000)
  y = rnd.randint(-100000, 100000)
  
game.actions.shoot(x, y)
game.actions.super_shot(x, y)
game.actions.melee()
game.actions.super_melee()