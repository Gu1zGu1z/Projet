import pyxel

# définit les différentes variables
config = { 
    'taille_x' : 152, \
    'taille_y' : 152, \
    'titre' : 'flip flop', \
    'rayon_balle': 2, \
    'vitesse_max' : 15, \
    'niveau_max' : 3,
    'score' : 0
}
# définit la taille de la fenêtre et son titre
pyxel.init(config['taille_x'], config['taille_y'], title=config['titre'])



# ----------- Balle --------------------------
# position initiale de la balle
# (origine des positions : milieu du tiers inférieur)
balle_x = 35
balle_y = 100


def balle_deplacement(x, y):
    """déplacement avec les touches de directions verticales"""
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 120) :
            y = y + 20
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 0) :
            y = y - 20
    return x, y






# =========================================================
# == UPDATE
# =========================================================
def update():
   """mise à jour des variables (30 fois par seconde)"""

   global balle_x, balle_y
   # mise à jour de la position du plateau
   balle_x, balle_y = balle_deplacement(balle_x, balle_y)


# =========================================================
# == DRAW
# =========================================================


def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    
    # balle (cercle)
        pyxel.circ(balle_x, balle_y, config['rayon_balle'], 2)
    
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.jeux
    
pyxel.run(update, draw)
