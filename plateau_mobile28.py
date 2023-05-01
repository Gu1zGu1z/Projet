import pyxel
import random

# constantes
# taille de la fenetre TAILLE_FENETRE_W x TAILLE_FENETRE_H pixels
TAILLE_FENETRE_W = 160
TAILLE_FENETRE_H = 160
HAUTEUR_BANDE = 8

ETAT_EN_JEU = 0
ETAT_PAUSE = 1
ETAT_FIN = 2

# définit les différentes variables
config = { 
    'taille_x' : TAILLE_FENETRE_W, \
    'taille_y' : TAILLE_FENETRE_H, \
    'taille_ennemi' : 2, \
    'titre' : 'Flip flop', \
    'rayon_balle': 4, \
    'niveau_max' : 3, \
    'score' : 0, \
    'balle_max' : TAILLE_FENETRE_H, \
    'balle_min' : 37, \
    'gravite' : 2, \
    'bande1_y' : 50, \
    'bande2_y' : 105, \
    'vitesse_ennemis' : 2, \
    'etat' : ETAT_EN_JEU, \
    'frequence_obstacle' : 22, \
    'frequence_ennemi' : 50, \
    'frequence_niveau' : 500
}

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
        #print(f'Chrono: {self.time}')

    def draw(self):
        minutes, seconds = divmod(self.time, 60)
        pyxel.text(90, 5, f"Score: {minutes:02}{seconds:02}", 7)

class Niveau:
    def __init__(self, chrono, bande1, bande2):
        self.niveau = 1
        self.chrono = chrono
        self.chrono_precedent = 0
        self.bande1 = bande1
        self.bande2 = bande2

    def update(self):
        if self.chrono.time > self.chrono_precedent and (self.chrono.time % config['frequence_niveau']) == 0:
            self.niveau += 1
            # noter chrono_precedent est utile sinon on n'arrive jamais à sortir du pause level up
            # parce qu'on retombe direct dedans
            self.chrono_precedent = self.chrono.time
            pyxel.text(50, 20, f'Level up!', 7)
            config['etat'] = ETAT_PAUSE
            # soit on accélère les balles ennemies
            # soit on accélère les bandes
            if self.niveau % 2 == 0:
                config['vitesse_ennemis'] += 1
            else:
                self.bande1.vitesse += 1
                self.bande2.vitesse += 1

    def draw(self):
        # affichage du numéro du niveau sur la meme ligne que le score (chrono)
        pyxel.text(40, 5, f"Niveau: {self.niveau:02}", 7)
        
class Balle: 
    def __init__(self, x, y, min_y, max_y, gravite):
        # création de l'objet de la balle contrôlée par le joueur
        # position initial de la balle
        self.x = x
        self.y = y

        # coordonnées y acceptables pour la balle (entre les deux bandes)
        self.min_y = min_y
        self.max_y = max_y

        # gravité initiale de la balle
        self.gravite = gravite

    def update(self):
        # cette fonction permet de mettre en mouvement la balle en fonction de la gravité.
        if (self.gravite + self.y + config['rayon_balle']<= self.max_y) and (self.gravite + self.y - config['rayon_balle'] - HAUTEUR_BANDE >= self.min_y):
          self.y = self.gravite + self.y  # on ajoute l'influence de la gravité à la position verticale de la balle

        '''Pour faire rebondir la balle sur les bords
        if (self.y + config['rayon_balle'] +1 >= self.max_y) or (self.y - config['rayon_balle'] -1 - HAUTEUR_BANDE<= self.min_y):
            print('ici')
            self.gravite = - (self.gravite)
        '''
        #print(f"Balle y={self.y} + {config['rayon_balle']} gravite={self.gravite} min={self.min_y} max={self.max_y}")


    def draw(self):
        # option possible: affichage d'une ressource pour la balle
        pyxel.circ(self.x, self.y, config['rayon_balle'], 15)

class TirEnnemi:
    def __init__(self, min_y, max_y, vitesse):
        self.x = config['taille_x'] - 1
        self.y = random.randint(min_y + config['taille_ennemi'], max_y - config['taille_ennemi'])  # zone d'apparition de l'ennemi
        self.vitesse = vitesse

    def update(self):
        # l'ennemi se déplace horizontalement
        self.x = (self.x - self.vitesse)
        if self.x < 0:
            self.x = 0

    def draw(self):
        pyxel.circ(self.x, self.y, config['taille_ennemi'], 2)

class Bande:
    def __init__(self, x=0, y=50, modif_obstacle=HAUTEUR_BANDE):
        # il s'agit des plateaux défilants (soit celui du haut, soit celui du bas)
        self.vitesse = 1  # vitesse de défilement du plateau
        # coordonnées du plateau - origine = coin haut gauche
        self.x = x  
        self.y = y  
        self.obstacles = []  # liste des obstacles sur la bande
        # pour créer des obstacles au dessus de la bande, on utilise une valeur positive de la hauteur de la bande
        # pour créer l'obstacle en dessous, modif negatif
        self.modif_obstacle = modif_obstacle
        
    def deplacement_bande(self):
        self.x = self.x - self.vitesse
        if self.x < 0:
            self.x = self.x + TAILLE_FENETRE_W

    def creation_obstacle(self):
        y = self.y + self.modif_obstacle
        self.obstacles.append([TAILLE_FENETRE_W, y])
        # print(f'creation_obstacle ({TAILLE_FENETRE_W}, {y})')

    def deplacement_obstacle(self):
        # déplacer les obstacles en meme temps que la bande
        for obstacle in self.obstacles:
            obstacle[0] -= self.vitesse

        # netttoyer la bande des obstacles qui ne sont plus visibles
        for obstacle in self.obstacles:
            if obstacle[0] < 0:
                self.obstacles.remove(obstacle)

    def update(self):
        self.deplacement_bande()
        self.deplacement_obstacle()

    def draw_bande(self):
        #print(f'draw_bande(): ({self.x}, {self.y})')
        pyxel.blt(self.x % TAILLE_FENETRE_W, self.y, 0, 0, 16, TAILLE_FENETRE_W, HAUTEUR_BANDE)
        pyxel.blt((self.x % TAILLE_FENETRE_W) - TAILLE_FENETRE_W, self.y, 0, 0, 16, TAILLE_FENETRE_W, HAUTEUR_BANDE)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            if self.modif_obstacle > 0 :
                pyxel.blt(obstacle[0],obstacle[1],0,16,0,8,8)
            else :
                pyxel.blt(obstacle[0],obstacle[1],0,16,8,8,8)

    def draw(self):
        self.draw_bande()
        self.draw_obstacles()


class Jeu:
    def __init__(self):
        # définit la taille de la fenêtre et son titre
        pyxel.init(config['taille_x'], config['taille_y'], title=config['titre'])
        pyxel.load("flipflop1.pyxres")
        # plateaux du haut et du bas
        self.bande1 = Bande(0, config['bande1_y'], HAUTEUR_BANDE)
        self.bande2 = Bande(0, config['bande2_y'], -HAUTEUR_BANDE)
        # balle du joueur
        self.balle = Balle(60, 60, min_y=config['bande1_y'], max_y=config['bande2_y'], gravite=config['gravite'])
        # tableau des boules ennemies en jeu
        self.ennemis = []
        # création du chronomètre
        self.chrono = Chronometre()
        # niveau
        self.niveau = Niveau(self.chrono, self.bande1, self.bande2)
        # démarrage
        self.chrono.start()
        pyxel.run(self.update, self.draw)
        
    def toggle_pause(self):
        # on passe dans le mode pause si on n'y était pas
        # on le quitte si on y était
        if config['etat'] == ETAT_EN_JEU:
            config['etat'] = ETAT_PAUSE
        elif config['etat'] == ETAT_PAUSE:
            config['etat'] = ETAT_EN_JEU
           
    def update(self):
        """ cette fonction définit le changement de gravité ( attraction vers le haut ou vers le bas ) en fonction des touches de directions haut et bas"""
        if pyxel.btnp(pyxel.KEY_UP):
            self.balle.gravite = - config['gravite']
            # lorsque la touche de direction "haut" est pressée, la gravité prend une valeur négative.
            # la balle est donc attirée vers le haut puisque self.y tend vers 0
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.balle.gravite = config['gravite']
            # lorsque la touche de direction "bas" est pressée, la gravité prend une valeur positive.
            # la balle est donc attirée vers le bas puisque self.y tend vers +∞
        elif pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.KEY_A):
            # lorsque le bouton P est appuyé: entrer/quitter le mode pause
            self.toggle_pause()
        elif pyxel.btnp(pyxel.KEY_Q) or (pyxel.btnp(pyxel.KEY_RETURN) and config['etat'] == ETAT_FIN):
            # fin du jeu
            pyxel.quit()
            
        self.niveau.update()

        if config['etat'] == ETAT_PAUSE:
            return
        
        self.test_collision()
        if config['etat'] == ETAT_FIN:
            return

        # generation d'un nouvel ennemi tous les x "frames"
        if pyxel.frame_count % config['frequence_ennemi'] == 0:
            self.ennemis.append(TirEnnemi(min_y=config['bande1_y'] + HAUTEUR_BANDE, 
                                             max_y=config['bande2_y'] - HAUTEUR_BANDE,
                                             vitesse=config['vitesse_ennemis']))

        for ennemi in self.ennemis:
            ennemi.update()
            # si l'ennemi a parcouru toute la largeur, on l'efface
            if ennemi.x <= 0:
                self.ennemis.remove(ennemi)

        # generation d'un obstacle tous les xx, au hasard sur une des deux bandes
        if (pyxel.frame_count % config['frequence_obstacle'] == 0):
            bande = random.choice([self.bande1, self.bande2])  # hasard
            bande.creation_obstacle()

        #print(f'balle=({self.balle.x, self.balle.y})')
        self.balle.update()
        self.bande1.update()
        self.bande2.update()
        self.chrono.update()

    def test_collision(self):
        '''
        A FAIRE : Clara
        collision avec un obstacle: utiliser self.bande1.obstacles et self.bande2.obstacles 
        par rapport à la balle (self.balle.x, self.balle.y)
        collision avec un tir: utiliser self.ennemis par rapport à self.balle.x, self.balle y

        Si collision, passer config['etat'] = ETAT_FIN
        '''
        # Pour l'instant, on ne fait rien
        pass
    
            
    def display_gameover(self):
        pyxel.text(50, 40, "Game Over", 7)
        pyxel.text(30, 100, "Appuyez sur ENTRER", 7)

    def display_pause(self):
        pyxel.text(50, 40, 'En Pause', 7)
        pyxel.text(20, 80, 'Appuyez sur P pour reprendre', 7)
          

    def draw(self):
        if config['etat'] == ETAT_FIN:
            return self.display_gameover()
        if config['etat'] == ETAT_PAUSE:
            return self.display_pause()
        pyxel.cls(0)
        self.bande1.draw()
        self.bande2.draw()
        self.balle.draw()
        self.chrono.draw()
        self.niveau.draw()
        
        for ennemi in self.ennemis:
            ennemi.draw()

Jeu()
# https://kitao.github.io/pyxel/wasm/launcher/?run=Gu1zGu1z.Projet.plateau_mobile
