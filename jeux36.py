import pyxel

# définit les différentes variables
config = { 
    'taille_x' : 152, \
    'taille_y' : 152, \
    'titre' : 'flip flop', \
    'rayon_balle': 2, \
    'niveau_max' : 3, \
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
class Balle: # création de l'objet de la balle
    def __init__(self, x, y, gravite):
        self.x = x
        self.y = y
        self.gravite = gravite

    def update(self):
        """ cette fonction permet de mettre en mouvement la balle en fonction de la gravité. """
        self.y = self.gravite + self.y  # on ajoute l'influence de la gravité à la position verticale de la balle

class Jeu:
    def __init__(self):
        self.balle = Balle(57, 100, 1)
        self.gravite = config['gravite_puissance']

    def update(self):
        """ cette fonction définit le changement de gravité ( attraction vers le haut ou vers le bas ) en fonction des touches de directions haut et bas"""
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravite = -(config['gravite_puissance']) # lorsque la touche de direction "haut" est pressée, la gravité prend une valeur négative.
            # la balle est donc attirée vers le haut puisque self.y tend vers 0
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravite = config['gravite_puissance'] # lorsque la touche de direction "bas" est pressée, la gravité prend une valeur positive.
            # la balle est donc attirée vers le bas puisque self.y tend vers +∞

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
