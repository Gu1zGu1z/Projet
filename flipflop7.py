import pyxel
import random

# taille de la fenetre TAILLE_FENETRE_XxTAILLE_FENETRE_Y pixels
# ne pas modifier
TAILLE_FENETRE_X = 160
TAILLE_FENETRE_Y = 120
HAUTEUR_BANDE = 8

#pyxel.init(TAILLE_FENETRE_X, TAILLE_FENETRE_Y, title="flipflop")
#pyxel.load("flipflop1.pyxres")


# définit les différentes variables
config = { 
    'taille_x' : TAILLE_FENETRE_X, \
    'taille_y' : TAILLE_FENETRE_Y, \
    'taille_ennemi' : 2, \
    'titre' : 'flip flop', \
    'rayon_balle': 4, \
    'niveau_max' : 3, \
    'score' : 0, \
    'balle_max' : TAILLE_FENETRE_Y, \
    'balle_min' : 37, \
    'gravite_puissance' : 2
}


# (origine des positions : coin haut gauche)
bande1_x = 0
bande1_y = 30
bande2_x = 0
bande2_y = 90

VITESSE_BANDE_1 = 2
VITESSE_BANDE_2 = 2

ennemis = [38,82]
# initialisation des ennemis
ennemis_liste = []

def bande_deplacement(x, y, vitesse):
    """déplacement de la bande"""
    x = x-vitesse
    if x<0:
        x = x+TAILLE_FENETRE_X
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
        
class Balle: # création de l'objet de la balle
    def __init__(self, x, y, gravite):
        # position initial de la balle
        self.x = x
        self.y = y

        # gravité initiale de la balle
        self.gravite = gravite

    def update(self):
        """ cette fonction permet de mettre en mouvement la balle en fonction de la gravité. """
        if (self.gravite + self.y + config['rayon_balle']<= bande2_y) and (self.gravite + self.y - config['rayon_balle'] - HAUTEUR_BANDE >= bande1_y):
          self.y = self.gravite + self.y  # on ajoute l'influence de la gravité à la position verticale de la balle

    def draw(self):
        pyxel.circ(self.x, self.y, config['rayon_balle'], 15
    )

class Ennemi:
    def __init__(self):
        self.x = config['taille_x'] - 1
        self.y = int(config['taille_y'] * 0.75)  # zone d'apparition de l'ennemi

    def update(self):
        # l'ennemi se déplace horizontalement
        self.x = (self.x - 1)
        if self.x < 0:
            self.x = 0

    def draw(self):
        # charger la boule rouge des ressources
        pyxel.circ(self.x, self.y, config['taille_ennemi'], 2)


class Jeu:
    def __init__(self):
        # définit la taille de la fenêtre et son titre
        pyxel.init(config['taille_x'], config['taille_y'], title=config['titre'])
        pyxel.load("flipflop1.pyxres")
        self.balle = Balle(60, 60, 1)
        self.gravite = config['gravite_puissance']
        # tableau des ennemis en jeu
        self.ennemis = []
        # création du chronomètre
        self.chrono = Chronometre()
        pyxel.run(self.update, self.draw)
        self.chrono.start()
   
    def update(self):
        update_plateau()
        update_ennemis()
        """ cette fonction définit le changement de gravité ( attraction vers le haut ou vers le bas ) en fonction des touches de directions haut et bas"""
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravite = -(config['gravite_puissance']) # lorsque la touche de direction "haut" est pressée, la gravité prend une valeur négative.
            # la balle est donc attirée vers le haut puisque self.y tend vers 0
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravite = config['gravite_puissance'] # lorsque la touche de direction "bas" est pressée, la gravité prend une valeur positive.
            # la balle est donc attirée vers le bas puisque self.y tend vers +∞

        # generation d'un nouvel ennemi tous les 50 "frames"
        if pyxel.frame_count % 50 == 0:
            self.ennemis.append(Ennemi())

        for ennemi in self.ennemis:
            ennemi.update()
            # si l'ennemi a parcouru toute la largeur, on l'efface
            if ennemi.x <= 0:
                self.ennemis.remove(ennemi)

        #print(f'balle=({self.balle.x, self.balle.y})')
        
        if not self.game_over():
            self.balle.gravite = self.gravite
            self.balle.update()
            self.chrono.update()

    def game_over(self):
        if self.balle.y < 0 or self.balle.y >= config['taille_y']:
            # la balle a dépassé les bords
            return True
        
        return False

    def draw(self):
        pyxel.cls(0)
        if self.game_over():
            pyxel.text(50, 80, "Game Over", 7)
            pyxel.text(30, 100, "Appuyez sur ENTRER", 7)
            if pyxel.btn(pyxel.KEY_RETURN):
                pyxel.quit()
        else:
            draw_plateau()
            draw_ennemis()
            chronometre.draw()
            self.balle.draw()
            #self.chrono.draw()
            
            #for ennemi in self.ennemis:
            #    ennemi.draw()

# crée une instance pour le chronomètre
chronometre = Chronometre()

# enclenche le chronomètre
chronometre.start()

def ennemis_creation(ennemis_list):
    """création aléatoire des ennemis"""

    # un ennemi par seconde
    if (pyxel.frame_count % 35 == 0):
        ennemis_list.append([TAILLE_FENETRE_X, (random.choice(ennemis))])
    return ennemis_list


def ennemis_deplacement(ennemis_list,vitesse):
    """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

    for ennemi in ennemis_list:
        ennemi[0] -= vitesse
        if  ennemi[0]<-8:
            ennemis_list.remove(ennemi)
    return ennemis_list

  

# =========================================================
# == UPDATE
# =========================================================
def update_plateau():
    """mise à jour des variables (30 fois par seconde)"""
    global bande1_x, bande1_y
    global bande2_x, bande2_y
    # mise à jour de la position du vaisseau
    bande1_x, bande1_y = bande_deplacement(bande1_x, bande1_y, VITESSE_BANDE_1)
    bande2_x, bande2_y = bande_deplacement(bande2_x, bande2_y, VITESSE_BANDE_2)
    #
    chronometre.update()
 
def update_ennemis():
    global ennemis_liste
    # creation des ennemis
    ennemis_liste = ennemis_creation(ennemis_liste)
    # mise a jour des positions des ennemis
    ennemis_liste = ennemis_deplacement(ennemis_liste,VITESSE_BANDE_1)  

    
# =========================================================
# == DRAW
# =========================================================
def draw_plateau():
    """création des objets (30 fois par seconde)"""
    global bande1_x, bande1_y
    global bande2_x, bande2_y
    global ennemis_liste
    
    # vide la fenetre
    #pyxel.cls(0)
    
    #pyxel.blt(a,b,c,d,e,f,g) 
    #a= x 
    #b= y
    #c= quelle fenetre( de l'outil de creation de pyxel)
    #d= position du dessin(x)
    #e= position du dessin(y)
    #f= longeur du dessin
    #g= hauteur du dessin
    
    
    chronometre.draw()
    #######pyxel.blt(128,91,1,0,3,32,29)
    #pyxel.blt( 78,300,32,0,8,8)
    # vaisseau (carre 8x8)
    
   # pyxel.blt(ennemis_x, ennemis_y,0,24,9,7,7)
    pyxel.blt(bande1_x % TAILLE_FENETRE_X, bande1_y,0,0,16,TAILLE_FENETRE_X,HAUTEUR_BANDE)
    pyxel.blt((bande1_x % TAILLE_FENETRE_X) - TAILLE_FENETRE_X, bande1_y,0,0,16,TAILLE_FENETRE_X,HAUTEUR_BANDE)

    pyxel.blt(bande2_x % TAILLE_FENETRE_X, bande2_y,0,0,16,TAILLE_FENETRE_X,-HAUTEUR_BANDE)
    pyxel.blt((bande2_x % TAILLE_FENETRE_X) - TAILLE_FENETRE_X, bande2_y,0,0,16,TAILLE_FENETRE_X,-HAUTEUR_BANDE)
  

def draw_ennemis():
# ennemis
    for ennemi in ennemis_liste:
        #pyxel.rect(ennemi[0], ennemi[1], 8, 8, 12)  
        if ennemi[1]== 38 :
            pyxel.blt(ennemi[0],ennemi[1],0,16,0,8,8)
        else :
            pyxel.blt(ennemi[0],ennemi[1],0,16,8,8,8)


  
#pyxel.run(update, draw)
Jeu()
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.flipflop
