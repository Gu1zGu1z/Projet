import pyxel

class Ball:
    def __init__(self, x, y, gravity):
        self.x = x
        self.y = y
        self.gravity = gravity

    def update(self):
        self.y += self.gravity

class Game:
    def __init__(self):
        self.ball = Ball(80, 60, 1)
        self.gravity = 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravity = -1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravity = 1

        self.ball.gravity = self.gravity
        self.ball.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.ball.x, self.ball.y, 5, 9)

# Initialize Pyxel
pyxel.init(160, 120)

# Create an instance of the game
game = Game()

# Update function for Pyxel
def update():
    game.update()

# Draw function for Pyxel
def draw():
    game.draw()

# Run Pyxel
pyxel.run(update, draw)
