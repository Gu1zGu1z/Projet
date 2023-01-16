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






# =========================================================
# == UPDATE
# =========================================================
def update():
  pass()


# =========================================================
# == DRAW
# =========================================================


def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.jeux
    
pyxel.run(update, draw)
