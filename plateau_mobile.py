import pyxel

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(160, 120, title="Nuit du c0de")
pyxel.load("res.pyxres")
# position initiale du vaisseau
# (origine des positions : coin haut gauche)
vaisseau_x = 60
vaisseau_y = 60
ennemis_x = 100
ennemis_y = 60
bande1_x = 0
bande1_y = 30
bande2_x =0
bande2_y = 90

VITESSE_BANDE_1 = 10
VITESSE_BANDE_2 = 5

def vaisseau_deplacement(x, y):
    """déplacement avec les touches de directions"""

    if pyxel.btn(pyxel.KEY_RIGHT):
        if (x < 152) :
            x = x + 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if (x > 0) :
            x = x - 1
    if pyxel.btn(pyxel.KEY_DOWN):
        if (y < 82) :
            y = y + 1
    if pyxel.btn(pyxel.KEY_UP):
        if (y > 38) :
            y = y - 1
    return x, y


def bande_deplacement(x, y):
    """déplacement de la bande"""
    x = x-VITESSE_BANDE_1
    return x, y

class Chronometer:
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


# Create an instance of the chronometer
chronometer = Chronometer()

# Start the chronometer
chronometer.start()

# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global vaisseau_x, vaisseau_y

    # mise à jour de la position du vaisseau
    vaisseau_x, vaisseau_y = vaisseau_deplacement(vaisseau_x, vaisseau_y)
    bande1_x, bande1_y = bande_deplacement(bande1_x, bande1_y)
    chronometer.update()

# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(0)
    #pyxel.blt(vaisseau_x, vaisseau_y,0,32,0,8,8)

    """ (a,b,c,d,e,f,g) 
    a= x 
    b= y
    c= quelle fenetre( de l'outil de creation de pyxel)
    d= position du dessin(x)
    e= position du dessin(y)
    f= longeur du dessin
    g= hauteur du dessin
    
    """
    chronometer.draw()
    
    """pyxel.blt( 78,300,32,0,8,8)"""
    # vaisseau (carre 8x8)
    
   # pyxel.blt(ennemis_x, ennemis_y,0,24,9,7,7)
    
    pyxel.blt(bande1_x, bande1_y,0,0,16,160,8)
    pyxel.blt(bande2_x, bande2_y,0,0,16,160,8)
  
pyxel.run(update, draw)
