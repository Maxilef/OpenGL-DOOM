# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 16:13:19 2023

@author: L. SEGURA, M. ROUSSEL
"""

''' FICHIER POUR STOCKER LES VARIABLES GLOBALES'''
import sys
import os

# Obtenez le chemin absolu de la racine du projet
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# Ajoutez le chemin de la racine du projet à sys.path
sys.path.append(root_path)

import tkinter as tk
import MAP as m
import MAP_IHM as ihm
import PLAYER as p

#APLLICATION OPGL
app = None

#APLLICATION TK 3D
canvastk = None


#VARIABLE POUR TAILLE DE FENETRE tkinter 2d
TAILLE_FENETRE_X = 400
TAILLE_FENETRE_Y = TAILLE_FENETRE_X

#stockage list des distance pour tk 2.5d
liste_distance = []
angle_hauteur = 45
h_mur = 35

# vitesse de deplacement du joueur
move_speed = 7
# Nombre de segments à afficher
nb_segments = TAILLE_FENETRE_X -1  #+1
segment_length = 200

#larguer d'une bande pour 2.5d
largeur_bande = TAILLE_FENETRE_X / nb_segments

#######
# MAP #
#######
#Nombre de ligne et de colonne (taille map)
nb_ligne = 16
nb_colonne = 16

#Teste file_to_map
carte = m.Map(0,0)
carte = carte.file_to_map(nb_ligne,nb_colonne,"../maps/carte_test.txt","carte_test")

##########
# PLAYER #
##########
x = 7
z = 7

# position
x_floatg = x
z_floatg = z

y = 0
u, i, o = 0,0,0

fov = 60
direction = -90
symbole = 'o'
vitesse_cam = 7 #vitesse de rotation de la cam

joueur = p.Player(symbole,x,z,fov,direction,TAILLE_FENETRE_X,TAILLE_FENETRE_Y)

#fps
fps_tkinter = 0
fps_opengl = 0
