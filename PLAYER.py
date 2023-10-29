 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:39:23 2023

@author: L. SEGURA, M. ROUSSEL
"""

import MAP
import math as m
import os


class Player:
    """
    classe du joeur permet d'initialise un joeur dans une map
    """
    # constructeur par default
    def __init__(self,symbole,x,y,angle,direction,TAILLE_FENETRE_X,TAILLE_FENETRE_Y):

        #taille
        self.TAILLE_FENETRE_X = TAILLE_FENETRE_X
        self.TAILLE_FENETRE_Y = TAILLE_FENETRE_Y

        #symbole qui reprentera le joueur dans la matrice
        self._symbole = symbole

        #Coordonnées ou le joeur est placer
        self._x = x
        self._y = y

        #Coordonnées en float la ou le joeur et placé
        self.x_float = x
        self.y_float = y

        #Coordonnées du joueur dans le canvas
        self._x_canv = 0
        self._y_canv = 0

        #Angle de vision du joueur
        self._FOV = angle
        self._direction = direction

    def place_joueur_map(self,map):
        """
        Permet de placé un joueur sur une map donné
        """

        x = self._x
        y = self._y

        # si pas de mur on place le player
        if map._matrice[x][y] != '#' :
            map._matrice[x][y] = self._symbole

    def deplacement_j(self, carte,direction):
        """
        permet de deplacer le joeur dans la map en fonction de la ou il regarde
        (une direction)
        touche :
                                    z
                                q   s  d
        """

        deplacement = False

        # la ou on est dans la matrice
        x = self._x
        y = self._y

        # la ou on est dans le canvas apres avoir bouger
        x_canv = int(self._y_canv)/(self.TAILLE_FENETRE_X/16)
        y_canv = int(self._x_canv)/(self.TAILLE_FENETRE_Y/16)

        # canvas in to matrice
        x_canv = int(x_canv)
        y_canv = int(y_canv)

        #print(x_canv)
        #print(y_canv)

        if direction == 'z' or direction == 's' or direction == 'q' or direction == 'd':
            # deplacement en haut
            if carte.verifier_mur(x_canv,y_canv):
                # la ou je suis je sup le joueur
                carte._matrice[x][y] = '_'

                # recup new position
                self._x = int(x_canv)
                self._y = int(y_canv)

                self.x_float = (self._y_canv)/(self.TAILLE_FENETRE_X/16)
                self.y_float = (self._x_canv)/(self.TAILLE_FENETRE_Y/16)
                #print("ici",self.x_float,self.y_float)

                # la ou je vais je met le joueur
                carte._matrice[x_canv][y_canv] = self._symbole
                deplacement = True

        return deplacement

    def coordonnees_angle_vision(self):
        """
        Permet de de calculer le Y a aditionner et soustraire pour langle de vision du joueur
        """

        # separe le champ de vision en 2
        new_angle = self._FOV // 2

        angle_point1 = self._direction - new_angle
        angle_point2 = self._direction + new_angle

        #On calcul les radians des nouveau angle obtenu
        r1 = m.radians(angle_point1)
        r2 = m.radians(angle_point2)

        coef_taille = 3
        #Coordonnées des deux points de notre FOV
        coord_point1 = [m.cos(r1)*coef_taille,m.sin(r1)*coef_taille]
        coord_point2 = [m.cos(r2)*coef_taille,m.sin(r2)*coef_taille]

        return [coord_point1,coord_point2]
