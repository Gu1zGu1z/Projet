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
class Balle:
    def __init__(self, x, y, gravite):
        self.x = x
        self.y = y
        self.gravite = gravite

    def update(self):
        self.y += self.gravite

class Jeu:
    def __init__(self):
        self.balle = Balle(57, 100, 1)
        self.gravite = config['gravite_puissance']

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravite = -(config['gravite_puissance'])
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravite = config['gravite_puissance']

        self.balle.gravite = self.gravite
        self.balle.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.balle.x, self.balle.y, config['rayon_balle'], 2)
        
jeu = Jeu()

def update():
    jeu.update()


def draw():
    jeu.draw()
    
    
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.jeux
    
pyxel.run(update, draw)
