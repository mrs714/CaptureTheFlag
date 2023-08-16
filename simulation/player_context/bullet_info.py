class BulletInfo():
    def __init__(self, sim_id, x, y, dx, dy, damage, owner_id):
        self.id = sim_id
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.owner_id = owner_id