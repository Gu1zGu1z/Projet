import pyxel


# définit les différentes variables
config = { 
    'taille_x' : 152, \
    'taille_y' : 152, \
    'titre' : 'flip flop', \
    'rayon_balle': 2, \
    'vitesse_max' : 15, \
    'niveau_max' : 3,
    'score' : 0, \
    'balle_max' : 120, \
    'balle_min' : 37
}


class Ball:
    def __init__(self, x, y, gravite):
        self.x = x
        self.y = y
        self.gravite = gravite

    def update(self):
        self.y += self.gravite

class Game:
    def __init__(self):
        self.ball = Ball(80, 60, 1)
        self.gravite = 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravite = -3
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravite = 3

        self.ball.gravite = self.gravite
        self.ball.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.ball.x, self.ball.y, config['rayon_balle'], 2, 9)

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
