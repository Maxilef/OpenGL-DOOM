#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 10:27:09 2023

@author: L. SEGURA, M. ROUSSEL
"""
import tkinter as tk
import MAP as m
import MAP_IHM as ihm
import PLAYER as p
import myglob as g
import OPENGL.myopengl as myop
import IHM as wintk

import time


#########################
def main_tk(root) :
    ###########
    # TKINTER #
    ###########

    #Initialisation d'un canvas dans root
    canvas = tk.Canvas(root,bg = "white",height = g.TAILLE_FENETRE_X, width = g.TAILLE_FENETRE_Y)

    # affiche carte
    ihm.afficher_carte(g.carte,root,canvas)

    # place le joeur dans la map/ matrice
    g.joueur.place_joueur_map(g.carte)
    #print(g.carte._matrice)

    # place le joeur dans la carte
    ihm.dessiner_joueur(g.carte,g.joueur,canvas)

    #print(joueur.coordonnees_angle_vision())
    ihm.dessiner_angle_vision(g.carte,g.joueur, canvas)

    def reinit():
        #afficher tkinter 2.5d
        wintk.window(g.canvastk,g.liste_distance)


    def afficher_opgl():
        g.x_floatg = g.joueur.x_float
        g.z_floatg = g.joueur.y_float

        g.direction = g.joueur._direction

        #afficher opengl
        g.app.display()


    # BIND
    def on_z_press(event):
        g.joueur = ihm.move_up(event, g.joueur, g.carte)
        # appeler affichage opengl
        afficher_opgl()
        reinit()


    def on_q_press(event):
        g.joueur = ihm.move_left(event,g.joueur,g.carte)
        afficher_opgl()
        reinit()

    def on_s_press(event):
        g.joueur = ihm.move_down(event,g.joueur,g.carte)
        afficher_opgl()
        reinit()

    def on_d_press(event):
        g.joueur = ihm.move_right(event,g.joueur,g.carte)
        afficher_opgl()
        reinit()

    # Mettre le focus sur le canvas pour recevoir les événements clavier
    canvas.bind("<z>", lambda event : on_z_press(event))
    canvas.bind("<q>", lambda event : on_q_press(event))
    canvas.bind("<s>", lambda event : on_s_press(event))
    canvas.bind("<d>", lambda event : on_d_press(event))

    def turn_cam_gauche(event):
        g.joueur = ihm.tourner_FOV_gauche(event,g.joueur,g.carte)
        afficher_opgl()
        reinit()

    def turn_cam_droite(event):
        g.joueur = ihm.tourner_FOV_droite(event,g.joueur,g.carte)
        afficher_opgl()
        reinit()



    canvas.bind("<t>", lambda event : turn_cam_gauche(event))
    canvas.bind("<y>", lambda event : turn_cam_droite(event))
    canvas.focus_set()


def main():
    # fenetre principal
    root = tk.Tk()
    root.geometry()

    main_tk(root)

    root.mainloop()
