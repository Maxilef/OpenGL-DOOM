import sys
import os

# Obtenez le chemin absolu du répertoire parent
parent_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(parent_dir)

# Ajoutez le chemin du répertoire parent au sys.path
sys.path.append(project_dir)


import MAP as mp
import MAP_IHM as ihm
import PLAYER as p
import myglob as g

# Tkinter
import tkinter as tk
from pyopengltk import OpenGLFrame

#OPENGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL import GL, GLU

import time
from math import pi, cos, sin, radians,ceil
from PIL import Image
import numpy as np


class AppOgl(OpenGLFrame):
    width = None
    height = None
    # variables globales
    zoom = -g.x_floatg - 0.5
    x =  -g.z_floatg - 0.5

    y = g.y
    u, i, o = g.u, g.direction+90, g.o

    quadric = None


    ouverture_sol = Image.open("sol2.jpg")
    ouverture_mur = Image.open("mur1.jpg")

    DICO_TEXTURES = {"sol" : ouverture_sol,
                    "mur" : ouverture_mur}

    global frame_count, start_time
    frame_count = 0
    start_time = 0

    @staticmethod
    def load_texture(image):
        """
        charge la texture de l'image donné
        """
        texture_data = image.tobytes()
        width = image.width
        height = image.height

        glEnable(GL_TEXTURE_2D)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
        return tex_id

    @staticmethod
    def calculate_fps():
        """
        cette fonction permet de mesurer les performances de l'application en affichant
        le nombre de frames rendues par seconde.
        """
        global frame_count, start_time

        # Incrémenter le compteur de frames
        frame_count += 1

        # Obtenir le temps écoulé depuis le début du programme
        current_time = time.time() - start_time

        # Afficher les FPS toutes les secondes
        if current_time > 1.0:
            fps = frame_count / current_time
            os.system('clear')
            AppOgl.affiche_pos_j(g.joueur)
            print("\nFPS OPENGL:", round(fps, 2))
            frame_count = 0
            start_time = time.time()

    @staticmethod
    def affiche_pos_j(joueur):
        print("POSITION DU JOUEUR\nx :",joueur._x)
        print("y :",joueur._y)
        print("\nORINTATION DU JOUEUR\n-> ",-joueur._direction % 360)


    ###############################################################
    # fonction rendue paramètres OPENGL
    def setup(self):
        """
        Initialise la fenêtre d'affichage et les paramètres.
        """
        # Définir la couleur de fond de la fenêtre.
        glClearColor(0.5, 0.8, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)

        # Objet quadrique, qui est une forme géométrique utilisée.
        self.quadric = gluNewQuadric()

        # Configure le style de dessin pour l'objet quadrique.
        glEnable(GL_DEPTH_TEST)  # Buffer de profondeur.
        glPolygonMode(GL_FRONT, GL_FILL)
        # Définir le modèle de rendu.
        glShadeModel(GL_SMOOTH)

        #self.luminous()

    def luminous(self):
        """
        active la lumiére v1
        """
        # LUMIERE
        # Activer l'éclairage
        glEnable(GL_LIGHTING)

        # Définir la position et la couleur de la source lumineuse
        glLoadIdentity()
        glPushMatrix()

        glTranslatef(self.x ,self.y ,self.zoom)
        glRotatef(self.u, 1, 0.0, 0.0)
        glRotatef(self.i, 0.0, 1, 0.0)
        glRotatef(self.o, 0.0, 0.0, 1)

        glEnable(GL_LIGHT0) # Activer la source lumineuse 0
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 16, 1.0]) # Position de la source lumineuse
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0]) # Couleur de la source lumineuse
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0]) # Couleur de la réflexion spéculaire
        glPopMatrix()

    def lumiere(self):
        """
        active la lumiére v2
        """
        # Obtenir la position de la caméra
        camera_pos = glGetDoublev(GL_MODELVIEW_MATRIX)[3][:3]

        # Configurer une source de lumière
        light_ambient = [1.0,1.0,1.0, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]

        # Position de la lumiére sur la caméra
        light_position = [0,0,0, -2000]
        #draw_light_source(0.0,0.0,0.0)

        # Activation du matériau
        glMaterialfv(GL_BACK, GL_AMBIENT_AND_DIFFUSE, [1.00, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1 ,1, 0.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [50.0])

        #
        glShadeModel((GL_SMOOTH))
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

        glLightfv(GL_LIGHT0, GL_POSITION, light_position)
        #print(i)

        # Définir les paramètres d'atténuation
        attenuation_cst = 0.0  # Atténuation constante
        attenuation_lineaire = 0.99  # Atténuation linéaire

        glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, attenuation_cst)
        glLightfv(GL_LIGHT0, GL_LINEAR_ATTENUATION, attenuation_lineaire)

        # Activer l'éclairage
        glEnable(GL_LIGHTING)

        # Activer la source de lumière
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)


    ###############################################################
    # fonction game
    def reshape(self, width, height):
        """
        Appelée lorsque la taille de la fenêtre de rendu est modifiée.
        Elle ajuste la projection pour s'adapter à la nouvelle taille de la fenêtre.
        """

        glViewport(0, 0, width, height)  # Définition de la view port. (0, 0) en bas à gauche.

        glMatrixMode(GL_PROJECTION)  # Mode d'affichage.
        glLoadIdentity()
        gluPerspective(g.fov, width / height, 0.00001, 150)

        glMatrixMode(GL_MODELVIEW)  # Matrice spécifique d'affichage.
        glLoadIdentity()

    def ecrire_map(self,fichier,map):
        """
        ecrie la map dans un fichier txt
        """
        name = str(fichier)
        racine_du_fichier = "../maps/"+str(name) #print(racine_du_fichier)
        #verification si le fichier peut s'ouvrir
        try :
            fichier = open(str(racine_du_fichier), "w")
            for i in range(map.ligne):
                for j in range(map.colonne):
                    val = map._matrice[i][j]
                    if isinstance(val, tuple):
                        fichier.write(str(val[0]))
                    else :
                        fichier.write(str(val))
                    if j+1 == map.colonne :
                        fichier.write("\n")

            fichier.close()

        except FileNotFoundError:
            print("le fichier n'a pas pue etre ouvert ou n'existe pas ")

    def init_pos_cam(self,carte,x,z):
        """
        place un int dans le fichier de la map pour représenté la caméra
        """

        taille_x = carte.ligne
        taille_z = carte.colonne

        if carte._matrice[-int(z)] [-int(x)] != "#" :
            carte._matrice[-int(z)] [-int(x)] = 0

        self.ecrire_map("testmap.txt",g.carte)

    def display(self):
        self.zoom = -g.x_floatg
        self.x =  -g.z_floatg

        self.y = g.y
        self.u, self.i, self.o = g.u, g.direction+90, g.o

        # + 90 car opengl pas le meme repére trigo
        """
        appelée à chaque fois que la fenêtre de rendu doit être mise à jour.
        Elle efface l'écran avec la couleur de fond
        Elle termine en échangeant les buffers de la fenêtre de rendu pour afficher l'image.
        """

        # efface le tampon de couleur (couleur de fond)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Appliquer les transformations à la source lumineuse
        glPushMatrix()
        self.lumiere()
        # POSITION CAM

        glLoadIdentity()

        glRotatef(self.u,1 ,0 ,0)
        glRotatef(self.i,0 ,1 ,0)
        glRotatef(self.o,0 ,0 ,1)

        # POSITIONNE LA CAMERA / PLAYER
        glTranslatef(-g.z_floatg,self.y,-g.x_floatg)



        """
        # on translate la grille pour que le point 0,0 de OpenGL
        # corresponde a la matrice de la map
        ______
        |     |
        |  .  |
        |     |
        |_____|


        point 0.0 opengl au milleu d'une case
        """

        # EFFECTUE LES TRANSFORMATIONS DE LA SCENE
        # DESSINE LA GRILLE(SOL)
        glPushMatrix()
        glTranslatef(g.carte.ligne//2 , -0.51, g.carte.colonne//2)
        #drawGrid()
        tex_id = self.load_texture(self.DICO_TEXTURES["sol"])
        self.drawSol(g.carte)
        glPopMatrix()

        # DESSINE MAP
        glPushMatrix()
        tex_id = self.load_texture(self.DICO_TEXTURES["mur"])
        self.drawMap(g.carte)
        glPopMatrix()
        glPopMatrix()

        # échange les buffers de la fenêtre de rendu pour afficher l'image
        #glutSwapBuffers()

        AppOgl.calculate_fps()

    def keyboard(self,key, droite, gauche):
        """
        appelée lorsque l'utilisateur appuie sur une touche du clavier
        """

        key = key.decode('utf-8')

        res = self.calcule_deplacement(90+self.i)

        ################
        #deplacement

        vit_move = 0.2

        # EFFECTUE LES TRANSFORMATIONS DE LA SCENE
        if key == 's':
            self.x -= vit_move*res[0]
            self.zoom -= vit_move*res[1]

            if g.carte._matrice[-int(self.zoom)][-int(self.x)] == '#' :
                # on avance pas retour arriére
                self.x += vit_move*res[0]
                self.zoom += vit_move*res[1]


        elif key == 'z':
            self.x += vit_move*res[0]
            self.zoom += vit_move*res[1]

            if g.carte._matrice[-int(self.zoom)][-int(self.x)] == '#' :
                # on avance pas retour arriére
                self.x -= vit_move*res[0]
                self.zoom -= vit_move*res[1]




        elif key == 'q':
            self.x += vit_move*res[1]
            self.zoom -= vit_move*res[0]

            if g.carte._matrice[-int(self.zoom)][-int(self.x)] == '#' :
                # on avance pas retour arriére
                self.x -= vit_move*res[1]
                self.zoom += vit_move*res[0]


        elif key == 'd':
            self.x -= vit_move*res[1]
            self.zoom += vit_move*res[0]

            if g.carte._matrice[-int(self.zoom)][-int(self.x)] == '#' :
                # on avance pas retour arriére
                self.x += vit_move*res[1]
                self.zoom -= vit_move*res[0]


        # hauteur de la map
        elif key == '8':
            self.y += 0.3

        elif key == '2':
            self.y -= 0.3

        ################
        #rotation camera haut bas
        elif key == 'u':
            self.u += 0.5

        elif key == 'j':
            self.u -= 0.5


        # rotation caméra  gauche droite
        elif key == '6':
            self.i += 2

        elif key == '4':
            self.i -= 2


        # rotation caméra bascule gauche droite
        elif key == 'o':
            self.o += 0.5

        elif key == 'l':
            self.o -= 0.5

        # quiter fenetre echap
        elif key == '\033':
            # sys.exit( )  # Exception ignored
            glutLeaveMainLoop()



        #reshape(800, 800)
        glutPostRedisplay()

    def update_fps(self,value):
        """
        pour un écran 144hz
        """
        glutTimerFunc(1000 // 144, self.update_fps, 0)  # Mettre à jour toutes les 1/60e de seconde
        AppOgl.calculate_fps()

    ###############################################################
    # fonction de DESSIN opengl

    #dessine source lumiére
    def draw_light_source(x,y,z):
        """
        dessine la source de lumiere
        """
        # Définir la couleur de l'objet représentant la source lumineuse
        glColor3f(1.0, 1.0, 0.0)  # Jaune

        # Définir la position de la source lumineuse
        light_position = [x, y, z]

        # Dessiner une sphère à la position de la source lumineuse
        glPushMatrix()
        glTranslatef(*light_position)
        glutSolidSphere(0.5, 10, 10)  # Dessine une sphère de rayon 0.5
        glPopMatrix()

    # dessine un cube
    def draw_cube(self):
        """
        dessine cube de 1*1*1
        ___________
        |    |     |
        |    |     |
        |----|-----|
        |    |     |
        |____|_____|
        0.5   0.5

        """



        glDisable(GL_LIGHTING)
        glBegin(GL_QUADS)

        # face orange mat
        # glColor4f(0.8, 0.4, 0.0, 1.0)

        # face haut
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, 0.5, 0.5)

        #face bas
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, -0.5)

        # face devant 1
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, 0.5)

        # face arriére 4
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, 0.5, -0.5)

        # face gauche 2
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(-0.5, -0.5, -0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-0.5, -0.5, 0.5)

        # face droite 3
        glTexCoord2f(0.0, 0.0)
        glVertex3f(0.5, 0.5, -0.5)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(0.5, 0.5, 0.5)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(0.5, -0.5, 0.5)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(0.5, -0.5, -0.5)

        glEnd()
        glEnable(GL_LIGHTING)

    # dessine grille
    def drawGrid(self):
        """
        dessine une grille de 16 par 16
        """
        glDisable(GL_LIGHTING)
        glBegin(GL_LINES)
        glColor3f(0.5, 0.5, 0.5) # couleur des lignes

        size = 16 # nombre de lignes
        step = 1 # espace entre les lignes
        for i in range(-size, size+1, step):
            glVertex3f(i, 0, -size)
            glVertex3f(i, 0, size)
            glVertex3f(-size, 0, i)
            glVertex3f(size, 0, i)

        glEnd()
        glEnable(GL_LIGHTING)

    # dessine sol
    def drawSol(self,carte):
        """
        dessine un Sol de x par y en utilisant un seul carré
        """
        taille_x = carte.ligne //2
        taille_y = carte.colonne //2

        glPushMatrix()

        #glDisable(GL_LIGHTING)
        #glColor3f(0.5, 0.5, 0.5) # couleur de la grille

        glBegin(GL_QUADS)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(-taille_x, 0, -taille_y)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(-taille_x, 0, taille_y)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(taille_x, 0, taille_y)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(taille_x, 0, -taille_y)
        glEnd()

        glPopMatrix()


        #glEnable(GL_LIGHTING)

    # dessine la map
    def drawMap(self,carte):
        """
        lit la matrice de la carte et afficher les murs(cube)
        """
        glPushMatrix()

        nb_ligne = carte.ligne
        nb_colonne = carte.colonne

        matrice = carte.matrice

        #on se translate au debut de la grille
        glTranslatef(0.5, 0.0,0.5)

        for i in range(nb_ligne):
            for j in range(nb_colonne):
                # SI MUR
                if matrice[i][j] == "#" :
                    self.draw_cube()

                # on se deplace pour le prochain
                glTranslatef(1, 0.0,0)

                if j+1 == nb_colonne :
                    glTranslatef(-nb_ligne*1,0.0,1)

        glPopMatrix()

    ###############################################################
    # CALCULES
    def transfo_rad(self,degre) :
        """
        permet de tranformer un angle en degrès en un angle en radiant
        """
        res = radians(degre)
        return res

    def calcule_deplacement(self,rota_map_degre) :
        """
        calcule les deplacement necessaire pour compenser la rotaion de la scene



        90°  ->   80°
        ^^^^^
    z   |   /
        |  /
        | /
        |/____________

                    x
        """

        # calcule du l'angle en radiant de la rotaion de la map
        map_rota_deg = self.transfo_rad(rota_map_degre)

        # récupe des valeurs pour compenser cette rotation
        move_x = float(cos(map_rota_deg))
        move_z = float(sin(map_rota_deg))

        return move_x, move_z

    ###############################################################
    # POUR OpenGLFrame
    #setting
    def initgl(self):
        # Initialisation des paramètres de rendu.
        # Initialise la bibliothèque GLUT.
        glutInit()

        # Définit les paramètres d'affichage pour la fenêtre de rendu.
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

        # Appelée pour initialiser les paramètres de rendu.
        self.setup()

        # start cpt fps
        self.start = time.time()
        self.nframes = 0

        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        self.reshape(self.width,self.height)

    #affichage dynamique si animate activer
    def redraw(self):

        self.display()
        #GL.glFlush()
        self.nframes += 1
        tm = time.time() - self.start
        #print("fps", self.nframes / tm, end="\r")
