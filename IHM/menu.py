import sys
import os

# Obtenez le chemin absolu du répertoire parent
parent_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(parent_dir)

# Ajoutez le chemin du répertoire parent au sys.path
sys.path.append(project_dir)

# A nous
import MAP as mp
import MAP_IHM as ihm
import PLAYER as p
import OPENGL.myopengl as myop
import myglob as g
import MAIN as tkmain
import IHM as wintk

# Tkinter
import tkinter as tk
from pyopengltk import OpenGLFrame

#OPENGL
from OpenGL.GL import *  # exception car prefixe systematique
from OpenGL.GLU import *
from OpenGL.GLUT import *

import time
from math import pi, cos, sin, radians,ceil
from PIL import Image
import numpy as np


class RaycastingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Projet Raycasting")
        self.geometry("600x600")

        # Création des widget de la frame
        self.create_title_frame()
        self.create_button_frame()

    # crée la frame pour titre
    def create_title_frame(self):
        frame_titre = tk.Frame(self, bg=None)
        frame_titre.pack(side=tk.TOP, fill="x")

        label_frame = tk.Label(frame_titre, text="MENU \n RAYCASTING", font=("Courier", 30, "bold"))
        label_frame.pack(pady=10)

    # crée la frame pour les bouton
    def create_button_frame(self):
        frame_bouton = tk.Frame(self, bg=None)
        frame_bouton.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=20)

        self.add_buttons(frame_bouton)

    def add_buttons(self, frame_bouton):
        bouton_jouer = tk.Button(frame_bouton, text="Jouer",
                                 font=("Courier", 28),
                                 width=10, height=2,
                                 relief="solid",
                                 activebackground="cyan",
                                 activeforeground="white",
                                 command=self.open_new_window)
        bouton_jouer.pack(side=tk.TOP, padx=10, pady=10)

        bouton_option = tk.Button(frame_bouton, text="Option",
                                  font=("Courier", 28),
                                  width=10, height=2,
                                  relief="solid",
                                  activebackground="cyan",
                                  activeforeground="white")
        bouton_option.pack(side=tk.TOP, padx=10, pady=10)

        bouton_quitter = tk.Button(frame_bouton, text="Quitter",
                                   font=("Courier", 28),
                                   width=10, height=2,
                                   relief="solid",
                                   activebackground="cyan",
                                   activeforeground="white",
                                   command=self.quit)
        bouton_quitter.pack(side=tk.TOP, padx=10, pady=10)

    # affichage de play
    def open_new_window(self):

        self.destroy()  # Ferme la fenêtre principale
        root = tk.Tk()  # Crée une nouvelle fenêtre
        root.title("raycasting !!")



        # frame gauche et ses sous-frame:
        frame_gauche = tk.Frame(root, bg="grey")
        frame_gauche.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame_tk1 = tk.Frame(root)
        frame_tk1.pack(side=tk.LEFT, expand=True)

        frame_tk2 = tk.Frame(root)
        frame_tk2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


        #mettre tkinter dans frame gauche 2
        tkmain.main_tk(frame_tk2)

        # Création du canvas pour tkinter 2.5d
        g.canvastk = tk.Canvas(frame_tk1,bg="grey",width = g.TAILLE_FENETRE_X,height = g.TAILLE_FENETRE_Y)
        g.canvastk.pack()


        # Ajout du ciel et du sol
        g.canvastk.create_rectangle(0,0,g.TAILLE_FENETRE_X,g.TAILLE_FENETRE_Y/2, width = 0, fill = "#80C8FF", tags = "ciel")
        g.canvastk.create_rectangle(0,g.TAILLE_FENETRE_Y/2,g.TAILLE_FENETRE_X,g.TAILLE_FENETRE_Y, width = 0, fill = "black", tags = "sol")

        #fenetre 2.5d tk
        wintk.window(g.canvastk,g.liste_distance)


        # Frame droite
        frame_droite = tk.Frame(root, bg="blue",width=g.TAILLE_FENETRE_X, height=g.TAILLE_FENETRE_Y)
        frame_droite.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)


        #mettre opengl dans frame droite
        g.app = myop.AppOgl(frame_droite, width=g.TAILLE_FENETRE_X, height=g.TAILLE_FENETRE_Y )
        g.app.pack(side=tk.LEFT,fill=tk.BOTH, expand=False)
        g.app.animate = 1 # active l'animation en boucle de opengl


if __name__ == '__main__':
    g.app = RaycastingApp()
    g.app.mainloop()
