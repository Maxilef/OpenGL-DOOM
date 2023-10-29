import sys
import os

# Obtenez le chemin absolu du répertoire parent
parent_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(parent_dir)

# Ajoutez le chemin du répertoire parent au sys.path
sys.path.append(project_dir)


from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

from math import pi, cos, sin, radians,ceil
from PIL import Image
import numpy as np

import MAP as mp


"""
A FAIRE :
colision
sprite + deplacement
cursor

'fonction de tir'
"""

######################
# variables globales #
######################
zoom = -1 -0.5
x = -1 -0.5

y = 0
u, i, o = 0,0,0

quadric = None

# GENERATION DE LA MAP
PATH_MAP = "../maps/"
carte = mp.Map(16,16)
carte = carte.file_to_map(16,16,PATH_MAP+"map1.txt","test") # recupe matrice

ouverture_sol = Image.open("sol2.jpg")
ouverture_mur = Image.open("mur1.jpg")

DICO_TEXTURES = {"sol" : ouverture_sol,
                "mur" : ouverture_mur}

frame_count = 0
start_time = 0

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
        print("FPS:", round(fps, 2))
        frame_count = 0
        start_time = time.time()

def update_fps(value):
    """
    pour un écran 144hz
    """
    glutTimerFunc(1000 // 60, update_fps, 0)  # Mettre à jour toutes les 1/60e de seconde
    calculate_fps()


#################################################################
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

###############################################################
# fonction de DESSIN opengl

# dessine un cube
def draw_cube():
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
    glNormal3f(0.0, 1.0, 0.0)


    #glDisable(GL_LIGHTING)
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
    #glEnable(GL_LIGHTING)

# dessine grille
def drawGrid():
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
def drawSol(carte):
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
def drawMap(carte):
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
                draw_cube()

            # on se deplace pour le prochain
            glTranslatef(1, 0.0,0)

            if j+1 == nb_colonne :
                glTranslatef(-nb_ligne*1,0.0,1)


    glPopMatrix()


###############################################################
# CALCULES
def transfo_rad(degre) :
    """
    permet de tranformer un angle en degrès en un angle en radiant
    """
    res = radians(degre)
    return res

def calcule_deplacement(rota_map_degre) :
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
    map_rota_deg = transfo_rad(rota_map_degre)

    # récupe des valeurs pour compenser cette rotation
    move_x = float(cos(map_rota_deg))
    move_z = float(sin(map_rota_deg))

    return move_x, move_z

###############################################################
# fonction rendue OPENGL

def luminous():
    """
    active la lumiére v1
    """
    # LUMIERE
    # Activer l'éclairage
    glEnable(GL_LIGHTING)

    # Définir la position et la couleur de la source lumineuse

    glPushMatrix()

    glEnable(GL_LIGHT0) # Activer la source lumineuse 0
    glLightfv(GL_LIGHT0, GL_POSITION, [0, 10, 10, 1.0]) # Position de la source lumineuse
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, 0.0,0.0, -1.0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 0, 0, 1.0]) # Couleur de la source lumineuse
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0, 0, 0, 1.0]) # Couleur de la réflexion spéculaire
    glPopMatrix()

def lumiere():
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


def init():
    """
    init fenetre d'affichage et parametre
    """
    global quadric
    # définir la couleur de fond de la fenêtre
    glClearColor(0.5, 0.8, 1.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)

    # objet quadrique, qui est une forme géométrique utilisée
    quadric = gluNewQuadric()

    # configure le style de dessin pour l'objet quadrique
    glEnable(GL_DEPTH_TEST) #buffer
    glPolygonMode(GL_FRONT, GL_FILL)
    # définir le modèle de rendu
    glShadeModel(GL_SMOOTH)

    #luminous()


######
def ecrire_map(fichier,map):
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


def init_pos_cam(carte,x,z):
    """
    place un int dans le fichier de la map pour représenté la caméra
    """

    taille_x = carte.ligne
    taille_z = carte.colonne

    if carte._matrice[-int(z)] [-int(x)] != "#" :
        carte._matrice[-int(z)] [-int(x)] = 0

    ecrire_map("testmap.txt",carte)


def display():
    global x, zoom


    """
    appelée à chaque fois que la fenêtre de rendu doit être mise à jour.
    Elle efface l'écran avec la couleur de fond
    Elle termine en échangeant les buffers de la fenêtre de rendu pour afficher l'image.
    """


    #print("Z  X")
    #print(-int(zoom),-int(x))

    # efface le tampon de couleur (couleur de fond)
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Appliquer les transformations à la source lumineuse
    glPushMatrix()


    lumiere()
    glLoadIdentity()

    # POSITION CAM

    glRotatef(u,1 ,0 ,0)
    glRotatef(i,0 ,1 ,0)
    glRotatef(o,0 ,0 ,1)

    # POSITIONNE LA CAMERA
    glTranslatef(x ,y,zoom)

    #place la caméra dans la matrice
    init_pos_cam(carte,x,zoom)


    # EFFECTUE LES TRANSFORMATIONS DE LA SCENE
    # DESSINE LA GRILLE
    glPushMatrix()

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

    glTranslatef(carte.ligne//2 , -0.51, carte.colonne//2)
    #drawGrid()
    tex_id = load_texture(DICO_TEXTURES["sol"])
    drawSol(carte)
    glPopMatrix()

    # DESSINE MAP
    glPushMatrix()
    tex_id = load_texture(DICO_TEXTURES["mur"])
    drawMap(carte)

    glPopMatrix()


    # échange les buffers de la fenêtre de rendu pour afficher l'image
    glPopMatrix()

    glutSwapBuffers()
    calculate_fps()

def reshape(width, height):
    """
    appelée lorsque la taille de la fenêtre de rendu est modifiée.
    Elle ajuste la projection pour s'adapter à la nouvelle taille de la fenêtre.
    """
    global zoom, x, y
    global t, y, u
    fov = 60



    glViewport(0, 0, width, height) #définiton de la view port. 0, 0 en bas à gauche

    glMatrixMode(GL_PROJECTION) # mode d'affichage
    glLoadIdentity()
    gluPerspective(fov, width/height, 0.00001, 150)


    glMatrixMode(GL_MODELVIEW) # matrice spécifique d'affichage
    glLoadIdentity()

def keyboard(key, droite, gauche):
    """
    appelée lorsque l'utilisateur appuie sur une touche du clavier
    """
    global zoom, x, y, carte
    global u,i,o
    key = key.decode('utf-8')

    res = calcule_deplacement(90+i)

    global val_x,val_z



    ################
    #deplacement

    vit_move = 0.2

    # EFFECTUE LES TRANSFORMATIONS DE LA SCENE
    if key == 's':
        x -= vit_move*res[0]
        zoom -= vit_move*res[1]

        if carte._matrice[-int(zoom)][-int(x)] == '#' :
            # on avance pas retour arriére
            x += vit_move*res[0]
            zoom += vit_move*res[1]


    elif key == 'z':
        x += vit_move*res[0]
        zoom += vit_move*res[1]

        if carte._matrice[-int(zoom)][-int(x)] == '#' :
            # on avance pas retour arriére
            x -= vit_move*res[0]
            zoom -= vit_move*res[1]




    elif key == 'q':
        x += vit_move*res[1]
        zoom -= vit_move*res[0]

        if carte._matrice[-int(zoom)][-int(x)] == '#' :
            # on avance pas retour arriére
            x -= vit_move*res[1]
            zoom += vit_move*res[0]


    elif key == 'd':
        x -= vit_move*res[1]
        zoom += vit_move*res[0]

        if carte._matrice[-int(zoom)][-int(x)] == '#' :
            # on avance pas retour arriére
            x += vit_move*res[1]
            zoom -= vit_move*res[0]


    # hauteur de la map
    elif key == '8':
        y += 0.3

    elif key == '2':
        y -= 0.3

    ################
    #rotation camera haut bas
    elif key == 'u':
        u += 0.5

    elif key == 'j':
        u -= 0.5


    # rotation caméra  gauche droite
    elif key == '6':
        i += 2

    elif key == '4':
        i -= 2


    # rotation caméra bascule gauche droite
    elif key == 'o':
        o += 0.5

    elif key == 'l':
        o -= 0.5

    # quiter fenetre echap
    elif key == '\033':
        # sys.exit( )  # Exception ignored
        glutLeaveMainLoop()



    #reshape(800, 800)
    glLightfv(GL_LIGHT0, GL_POSITION, [x, 0, zoom, 1.0])
    glutPostRedisplay()  # indispensable en Python


################
# MAIN opengl  #
################

# initialise la bibliothèque GLUT.
glutInit()

# définit les paramètres d'affichage pour la fenêtre de rendu.
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

# crée une nouvelle fenêtre de rendu.et
# définit la taille initiale de la fenêtre de rendu.
glutCreateWindow('OPENGL')
glutReshapeWindow(800,800)

# définit la fonction de rappel pour le redimensionnement de la fenêtre.
glutReshapeFunc(reshape)

# définit la fonction de rappel pour l'affichage de la fenêtre.
glutDisplayFunc(display)

# définit la fonction de rappel pour les événements de clavier.
glutKeyboardFunc(keyboard)

# appelée pour initialiser les paramètres de rendu.
init()

glutTimerFunc(0, update_fps, 0)
# lance la BOUCLE principale de GLUT pour gérer les événements.
glutMainLoop()
