import pyxel
import random

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
    'gravite_puissance' : 2
}

ETAT_EN_JEU = 0
ETAT_PAUSE = 1
ETAT_FIN = 2

# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------

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
        self.y = self.gravite + self.y  # on ajoute l'influence de la gravité à la position verticale de la balle

    def draw(self):
        pyxel.circ(self.x, self.y, config['rayon_balle'], 2)

class Ennemi:
    def __init__(self):
        self.x = config['taille_x'] - 1
        self.y = int(config['taille_y'] * 0.50)  # zone d'apparition de l'ennemi  # zone d'apparition de l'ennemi

    def update(self):
        # l'ennemi se déplace horizontalement
        self.x = (self.x - 1)
        if self.x < 0:
            self.x = 0

    def draw(self):
        # charger la boule rouge: (32,0) dans les ressources
        # sa taille est (8,8)
        pyxel.blt(self.x, self.y, img=0, u=32, v=0, w=8, h=8)


class Jeu:
    def __init__(self):
        # définit la taille de la fenêtre et son titre
        pyxel.init(config['taille_x'], config['taille_y'], title=config['titre'])
        pyxel.load("flipflop1.pyxres")
        self.balle = Balle(57, 10, 1)
        self.gravite = config['gravite_puissance']
        # état du jeu (en jeu, pause, fin)
        self.etat = ETAT_EN_JEU
        # tableau des ennemis en jeu
        self.ennemis = []
        self.prochain_spawn = 50
        # init du chronomètre
        self.chrono = Chronometre()
        self.chrono.start()
        # attention rien n'est executé après pyxel.run !   
        pyxel.run(self.update, self.draw)
                

    def toggle_pause(self):
        # on passe dans le mode pause si on n'y était pas
        # on le quitte si on y était
        if self.etat == ETAT_EN_JEU:
            self.etat = ETAT_PAUSE
        elif self.etat == ETAT_PAUSE:
            self.etat = ETAT_EN_JEU
   
    def update(self):
        """ cette fonction définit le changement de gravité ( attraction vers le haut ou vers le bas ) en fonction des touches de directions haut et bas"""
        if pyxel.btnp(pyxel.KEY_UP):
            self.gravite = -(config['gravite_puissance']) # lorsque la touche de direction "haut" est pressée, la gravité prend une valeur négative.
            # la balle est donc attirée vers le haut puisque self.y tend vers 0
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.gravite = config['gravite_puissance'] # lorsque la touche de direction "bas" est pressée, la gravité prend une valeur positive.
            # la balle est donc attirée vers le bas puisque self.y tend vers +∞
        elif pyxel.btnp(pyxel.KEY_P):
            # lorsque le bouton P est appuyé: entrer/quitter le mode pause
            self.toggle_pause()
        elif pyxel.btnp(pyxel.KEY_Q) or (pyxel.btnp(pyxel.KEY_RETURN) and self.etat == ETAT_FIN):
            # fin du jeu
            pyxel.quit()

        # on n'update pas inutilement si on est en pause ou fin
        if self.etat == ETAT_PAUSE:
            return
        
        self.test_borders()
        if self.etat == ETAT_FIN:
            return
        
        # nous sommes dans l'etat "en jeu"
        # generation d'un nouvel ennemi 
        if pyxel.frame_count == self.prochain_spawn:
            self.ennemis.append(Ennemi())
            self.prochain_spawn = self.prochain_spawn + random.randint(30, 100)
            #print(f'Prochain spawn={self.prochain_spawn}')

        for ennemi in self.ennemis:
            ennemi.update()
            # si l'ennemi a parcouru toute la largeur, on l'efface
            if ennemi.x <= 0:
                self.ennemis.remove(ennemi)

        #print(f'balle=({self.balle.x, self.balle.y})')        
        self.balle.gravite = self.gravite
        self.balle.update()
        self.chrono.update()
 
    def test_borders(self):
        if self.balle.y < 0 or self.balle.y >= config['taille_y']:
            # la balle a dépassé les bords
            self.etat = ETAT_FIN
    
    def display_gameover(self):
        pyxel.text(50, 80, "Game Over", 7)
        pyxel.text(30, 100, "Appuyez sur ENTRER", 7)

    def display_pause(self):
        pyxel.text(50, 80, 'En Pause', 7)
        pyxel.text(20, 100, 'Appuyez sur P pour reprendre', 7)

    def draw(self):
        if self.etat == ETAT_FIN:
            return self.display_gameover()
        if self.etat == ETAT_PAUSE:
            return self.display_pause()
        
        pyxel.cls(0)
        self.balle.draw()
        self.chrono.draw()
        for ennemi in self.ennemis:
            ennemi.draw()

    
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.jeux
    
Jeu()
