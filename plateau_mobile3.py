import pyxel
import random

# taille de la fenetre 160x120 pixels
# ne pas modifier
pyxel.init(160, 120, title="flipflop")
pyxel.load("flipflop.pyxres")

ennemis_liste = []

# (origine des positions : coin haut gauche)
bande1_x = 0
bande1_y = 30
bande2_x =0
bande2_y = 90

VITESSE_BANDE_1 = 1
VITESSE_BANDE_2 = 1

def bande_deplacement(x, y, vitesse):
    """déplacement de la bande"""
    x = x-vitesse
    return x, y

class Chronometre:
    def __init__(self):
        self.time = 0
        self.running = False

    def start(self):
        self.time = 0
        self.running = True

    def stop(self):
        self.running = False

    def update(self):
        if self.running:
            self.time += 1

    def draw(self):
        minutes, seconds = divmod(self.time, 60)
        pyxel.text(135, 5, f"{minutes:02}{seconds:02}", 7)


# crée une instance pour le chronomètre
chronometre = Chronometre()

# enclenche le chronomètre
chronometre.start()

  
def ennemis_creation(ennemis_liste):
    """création aléatoire des ennemis"""

    # un ennemi par seconde
    if (pyxel.frame_count % 30 == 0):
        ennemis_liste.append([random.randint(0, 120), 0])
    return ennemis_liste


def ennemis_deplacement(ennemis_liste):
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for ennemi in ennemis_liste:
        ennemi[1] += 1
        if  ennemi[1]>128:
            ennemis_liste.remove(ennemi)
    return ennemis_liste

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global bande1_x, bande1_y
    global bande2_x, bande2_y


    # mise à jour de la position du vaisseau
    bande1_x, bande1_y = bande_deplacement(bande1_x, bande1_y, VITESSE_BANDE_1)
    bande2_x, bande2_y = bande_deplacement(bande2_x, bande2_y, VITESSE_BANDE_2)

    chronometre.update()
  
 # creation des ennemis
    ennemis_liste = ennemis_creation(ennemis_liste)

    # mise a jour des positions des ennemis
    ennemis_liste = ennemis_deplacement(ennemis_liste) 
    
# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    
    """pyxel.blt(a,b,c,d,e,f,g) 
    a= x 
    b= y
    c= quelle fenetre( de l'outil de creation de pyxel)
    d= position du dessin(x)
    e= position du dessin(y)
    f= longeur du dessin
    g= hauteur du dessin
    
    """
    chronometre.draw()
    
    """pyxel.blt( 78,300,32,0,8,8)"""
    # vaisseau (carre 8x8)
    
   # pyxel.blt(ennemis_x, ennemis_y,0,24,9,7,7)
    pyxel.blt(bande1_x % 160, bande1_y,0,0,16,160,8)
    pyxel.blt((bande1_x % 160) - 160, bande1_y,0,0,16,160,8)

    pyxel.blt(bande2_x % 160, bande2_y,0,0,16,160,8)
    pyxel.blt((bande2_x % 160) - 160, bande2_y,0,0,16,160,8)
    
    for ennemi in ennemis_liste:
        pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)

  
pyxel.run(update, draw)

# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.plateau_mobile
