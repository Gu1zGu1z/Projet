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
    'balle_min' : 37, \
    'gravite_puissance' : 5
}
# définit la taille de la fenêtre et son titre
pyxel.init(config['taille_x'], config['taille_y'], title=config['titre'])

# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
class Ball:
    def __init__(self, x, y, gravite):
        self.x = x
        self.y = y
        self.gravite = gravite

    def update(self):
        self.y += self.gravite

class Game:
    def __init__(self):
        self.ball = Ball(57, 100, 1)
        self.gravite = config['gravite_puissance']

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravite = -(config['gravite_puissance'])
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravite = config['gravite_puissance']

        self.ball.gravite = self.gravite
        self.ball.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.ball.x, self.ball.y, config['rayon_balle'], 2)
        
game = Game()

def update():
    game.update()


def draw():
    game.draw()
    
    
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.jeux
    
pyxel.run(update, draw)
