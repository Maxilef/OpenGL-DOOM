#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 09:59:40 2023

@author: L. SEGURA, M. ROUSSEL
"""

import sys
import os

# Obtenez le chemin absolu de la racine du projet
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# Ajoutez le chemin de la racine du projet à sys.path
sys.path.append(root_path)

import MAP
import PLAYER
import tkinter as tk
import myglob as g
from math import cos,sin,atan2,pi,radians,ceil, degrees, tan, sqrt


#############
# AFFICHAGE #
#############

def afficher_carte(carte,root,canvas):
        """
        affiche la carte(matrice) dans un canvas sous forme de rectangle
        """

        #Pour chaque ligne de la matrice on dessine une carre de taille carre:
        taille_x = (g.TAILLE_FENETRE_X)/carte._c
        taille_y = (g.TAILLE_FENETRE_Y)/carte._l

        x,y=0,0

        #On parcours la matrie de la carte et on trace chaque case en fonction de l'élément dans la matrice
        for i in range(carte._l):
            for j in range(carte._c):

                if carte._matrice[i][j] == '_':
                    #print(carte._matrice[i][j])
                    canvas.create_rectangle(x,y,x+taille_x,y+taille_y, fill="white", tags = "libre")

                elif carte._matrice[i][j] == '#':
                    canvas.create_rectangle(x,y,x+taille_x,y+taille_y, fill="black", tags = "wall")
                x = x + taille_x
                #print("x=",x)
                if x == g.TAILLE_FENETRE_X:
                    x = 0
                    y = y + taille_y

        canvas.pack()
        return canvas

def dessiner_joueur(carte,joueur,canvas):
    """
    dessine le joueur sur la carte au bonne coordonnées
    le joeur et représenté par un carré
    """
    ratio1_x = g.TAILLE_FENETRE_X * 20 / 800
    ratio1_y = g.TAILLE_FENETRE_Y * 20 / 800

    ratio2_x = g.TAILLE_FENETRE_X * 30 / 800
    ratio2_y = g.TAILLE_FENETRE_Y * 30 / 800

    canvas.create_rectangle(joueur._y*(g.TAILLE_FENETRE_X/16)+ratio1_x, joueur._x*(g.TAILLE_FENETRE_Y/16)+ratio1_y, joueur._y*(g.TAILLE_FENETRE_X/16)+ratio2_x, joueur._x*(g.TAILLE_FENETRE_Y/16)+ratio2_y,fill = "red",tag = "joueur")

    rectangle_id = canvas.find_withtag("joueur")
    coordonne = canvas.coords(rectangle_id)

    joueur._x_canv = coordonne[0]
    joueur._y_canv = coordonne[1]



###########################
# FONCTION DE DEPLACEMENT #
###########################
# calcule pour deplacement
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

#deplacement
def move_up(event,joueur,carte):
    """
    Calback qui gere l'evenement de faire bouger le joueur vers le haut
    """
    # VERIFIER SI ON PEUT BOUGER

    # on fait bouger le carré du joueur
    canvas = event.widget
    rectangle_id = canvas.find_withtag("joueur")

    #print(- joueur._direction)

    #calcule direction
    coef_dir = calcule_deplacement(-joueur._direction)

    #print(coef_dir[0],coef_dir[1])

    # recup coordonnées avant qu'on bouge
    old_x_canv = joueur._x_canv
    old_y_canv = joueur._y_canv

    #deplacer carré joueur
    deplacement_x = ( g.move_speed * -(coef_dir[0]) )
    deplacement_y = ( g.move_speed * -(coef_dir[1]) )

    canvas.move(rectangle_id, -deplacement_x, deplacement_y)
    t=event.keysym

    coordonne = canvas.coords(rectangle_id)

    #convertir pour correspondre a la matrice
    colonne = coordonne[0]/(g.TAILLE_FENETRE_X//16)
    ligne = coordonne[1]/(g.TAILLE_FENETRE_X//16)

    #coordonnées canvas
    joueur._x_canv = coordonne[0]
    joueur._y_canv = coordonne[1]

    # a remetre si o veut voir matrice avec perso qui bouge
    #if (int(ligne) != int(joueur._x)) or (int(colonne) != int(joueur._y)):

    #vérifier si la on ou se deplace mur ou pas
    deplacement = joueur.deplacement_j(g.carte,t)
    if not deplacement :
        canvas.move(rectangle_id, +deplacement_x, -deplacement_y)

        joueur._x_canv = old_x_canv
        joueur._y_canv = old_y_canv


    canvas.delete("FOV")
    dessiner_angle_vision(carte,joueur,canvas)
    return joueur

def move_left(event, joueur, carte):
    """
    Callback qui gère l'événement de déplacement du joueur vers la gauche
    """

    # VÉRIFIER SI ON PEUT BOUGER

    # On fait bouger le carré du joueur
    canvas = event.widget
    rectangle_id = canvas.find_withtag("joueur")

    # Calcule de la direction
    coef_dir = calcule_deplacement(joueur._direction +90)

    # Récupération des coordonnées avant le déplacement
    old_x_canv = joueur._x_canv
    old_y_canv = joueur._y_canv

    deplacement_x = g.move_speed * coef_dir[0]
    deplacement_y = g.move_speed * coef_dir[1]

    canvas.move(rectangle_id, -deplacement_x, -deplacement_y)
    t = event.keysym

    coordonne = canvas.coords(rectangle_id)

    # Convertir pour correspondre à la matrice
    colonne = coordonne[0] / (g.TAILLE_FENETRE_X // 16)
    ligne = coordonne[1] / (g.TAILLE_FENETRE_X // 16)

    # Coordonnées canvas
    joueur._x_canv = coordonne[0]
    joueur._y_canv = coordonne[1]

    # a remetre si o veut voir matrice avec perso qui bouge
    #if (int(ligne) != int(joueur._x)) or (int(colonne) != int(joueur._y)):

    # Vérifier si la case où l'on se déplace est un mur ou pas
    deplacement = joueur.deplacement_j(g.carte, t)
    if not deplacement:
        canvas.move(rectangle_id, deplacement_x, deplacement_y)

        joueur._x_canv = old_x_canv
        joueur._y_canv = old_y_canv

    canvas.delete("FOV")
    dessiner_angle_vision(carte,joueur, canvas)
    return joueur

def move_down(event,joueur,carte):
    """
    Calback qui gere l'evenement de faire bouger le joueur vars le bas
    """

    # VERIFIER SI ON PEUT BOUGER

    # on fait bouger le carré du joueur
    canvas = event.widget
    rectangle_id = canvas.find_withtag("joueur")

    #calcule direction
    coef_dir = calcule_deplacement(-joueur._direction)

    # recup coordonnées avant qu'on bouge
    old_x_canv = joueur._x_canv
    old_y_canv = joueur._y_canv

    deplacement_x = -( g.move_speed * (coef_dir[0]) )
    deplacement_y = -( g.move_speed * (coef_dir[1]) )

    canvas.move(rectangle_id, +deplacement_x, -deplacement_y)
    t=event.keysym

    coordonne = canvas.coords(rectangle_id)

    #convertir pour correspondre a la matrice
    colonne = coordonne[0]/(g.TAILLE_FENETRE_X//16)
    ligne = coordonne[1]/(g.TAILLE_FENETRE_X//16)

    #coordonnées canvas
    joueur._x_canv = coordonne[0]
    joueur._y_canv = coordonne[1]

    # a remetre si o veut voir matrice avec perso qui bouge
    #if (int(ligne) != int(joueur._x)) or (int(colonne) != int(joueur._y)):

    #vérifier si la on ou se deplace mur ou pas
    deplacement = joueur.deplacement_j(g.carte,t)
    if not deplacement :
        canvas.move(rectangle_id, -deplacement_x, +deplacement_y)

        joueur._x_canv = old_x_canv
        joueur._y_canv = old_y_canv


    canvas.delete("FOV")
    dessiner_angle_vision(carte,joueur,canvas)
    return joueur

def move_right(event, joueur, carte):
    """
    Callback qui gère l'événement de déplacement du joueur vers la gauche
    """

    # VÉRIFIER SI ON PEUT BOUGER

    # On fait bouger le carré du joueur
    canvas = event.widget
    rectangle_id = canvas.find_withtag("joueur")

    # Calcule de la direction
    coef_dir = calcule_deplacement(joueur._direction - 90)

    # Récupération des coordonnées avant le déplacement
    old_x_canv = joueur._x_canv
    old_y_canv = joueur._y_canv

    deplacement_x = g.move_speed * coef_dir[0]
    deplacement_y = g.move_speed * coef_dir[1]

    canvas.move(rectangle_id, -deplacement_x, -deplacement_y)
    t = event.keysym

    coordonne = canvas.coords(rectangle_id)

    # Convertir pour correspondre à la matrice
    colonne = coordonne[0] / (g.TAILLE_FENETRE_X // 16)
    ligne = coordonne[1] / (g.TAILLE_FENETRE_X // 16)

    # Coordonnées canvas
    joueur._x_canv = coordonne[0]
    joueur._y_canv = coordonne[1]

    # a remetre si o veut voir matrice avec perso qui bouge
    #if (int(ligne) != int(joueur._x)) or (int(colonne) != int(joueur._y)):

    # Vérifier si la case où l'on se déplace est un mur ou pas
    deplacement = joueur.deplacement_j(g.carte, t)
    if not deplacement:
        canvas.move(rectangle_id, deplacement_x, deplacement_y)

        joueur._x_canv = old_x_canv
        joueur._y_canv = old_y_canv

    canvas.delete("FOV")
    dessiner_angle_vision(carte,joueur, canvas)
    return joueur

##################
# CAMERA / RAYON #
##################
def distance(point1, point2):
    """Calcul la distance entre deux point"""
    deltaX = point2[0] - point1[0]
    deltaY = point2[1] - point1[1]
    distance = sqrt(deltaX**2 + deltaY**2)
    return distance

def plus_proche(point, point1, point2):
    """Renvoie le point le plus proche"""
    distance1 = distance(point, point1)
    distance2 = distance(point, point2)

    if distance1 < distance2:
        #print("horizontale")
        return point1
    else:
        #print("verticale")
        return point2

def get_rectangle_tag(canvas,x, y):
    """Recupere le tag d'un rectangle a l aide de ccoordonnées"""

    overlapping = canvas.find_overlapping(x, y, x, y)
    if overlapping:
        tag = canvas.gettags(overlapping[0])[0]
        return tag

def interesection_vertical_mur(point,canvas,angle):
    """
    Fonction permettant de trouvé le point d'intersection touchant un mur a
    partir du premier point d'intersection vertical
    """
    x = point[0]
    y = point[1]

    taille_cote = (g.TAILLE_FENETRE_Y / 16)

    tag_verticale = get_rectangle_tag(canvas, x, y)
    #print("Tag vertical du rectangle :", tag_verticale)
    #Imposible pour p0 degre ou 270 degre
    if angle != 90 and angle != 270:
        #Si l'intersection touche un  mur ou sort du canvas alors on sort de la boucle
        while tag_verticale != "wall" and tag_verticale != None:
            #Calcul prochaine inntersection premier quadrant
            if(0 <= angle % 360 and angle % 360 < 90 ):
                y += taille_cote * tan(radians(angle))
                x += taille_cote

            #Calcul prochaine inntersection deuxieme quadrant
            elif (90 < angle % 360 and angle % 360 < 180):
                y += taille_cote * -tan(radians(angle))
                x -= taille_cote

            #Calcul prochaine inntersection troisieme quadrant
            elif (180 <= angle % 360 and angle % 360 < 270):
                y -= taille_cote * tan(radians(angle))
                x -= taille_cote

            #Calcul prochaine inntersection quatrieme quadrant
            else:
                y -= taille_cote * -tan(radians(angle))
                x += taille_cote

            #On recupere le tag de la nouvelle intersection
            tag_verticale = get_rectangle_tag(canvas, x, y)
            #print("Tag vertical du rectangle :", tag_verticale)
            #print(tag_verticale)

        #Si le tag est == None alors on dit qu'il n'y pas de point d'intersection mur vertical
        if tag_verticale==None:
            return None

        #Sinon on renvoie le point d'intersection verticale mur
        else:
            #canvas.create_oval(x-2, y-2, x+ 2, y + 2, tags="FOV", fill="red")
            return x,y

def interesection_horizontale_mur(point,canvas,angle):
    """
    Fonction permettant de trouvé le point d'intersection touchant un mur a partir
    du premier point d'intersection vertical
    """
    x = point[0]
    y = point[1]

    taille_cote = (g.TAILLE_FENETRE_Y / 16)
    if angle%360 != 0 and angle%360 != 180:
        tag_horizontale = get_rectangle_tag(canvas, x, y)
        #print("Tag horizontale du rectangle :", tag_horizontale)
        while tag_horizontale != "wall" and tag_horizontale != None:
            #Calcul prochaine inntersection premier quadrant
            if(0 <= angle % 360 and angle % 360 < 90 ):
                x += taille_cote / tan(radians(angle))
                y += taille_cote

             #Calcul prochaine inntersection deuxieme quadrant
            elif (90 <= angle % 360 and angle % 360 < 180):
                #print("yo")
                x += taille_cote / tan(radians(angle))
                y += taille_cote

             #Calcul prochaine inntersection troisieme quadrant
            elif (180 < angle % 360 and angle % 360 < 270):
                x -= taille_cote /tan(radians(angle))
                y -= taille_cote

             #Calcul prochaine inntersection quatrieme quadrant
            elif (270 <= angle % 360 and angle % 360 < 360):
                x -= taille_cote /tan(radians(angle))
                y -= taille_cote

            tag_horizontale = get_rectangle_tag(canvas, x, y)
            #print("Tag horizontale du rectangle :", tag_horizontale)
            #print(angle)
            #print(tag_horizontale)

        #Si le tag est == None alors on dit qu'il n'y pas de point d'intersection mur horizontal
        if tag_horizontale==None:
            return None
        #Sinon on renvoie le point d'intersection horizontale mur
        else:
            #canvas.create_oval(x-2, y-2, x+ 2, y + 2, tags="FOV", fill="green")
            return x,y
    else:
       #print("segment horizontal intracable")
       return None


def dessiner_angle_vision(carte, joueur, canvas):
    """
    Dessiner l'angle vision et les rayon du fov joueur.
    Il y aura autant de rayon que la largeur de l'ecran
    """
    coef = joueur.coordonnees_angle_vision()

    # Nombre de segments à afficher
    nb_segments = g.nb_segments
    segment_length = g.segment_length
    ratio = g.TAILLE_FENETRE_X * 5 / 800
    g.liste_distance = []

    # donne le point du joueur et le point du rayon sur cercle trigo
    x1, y1 = coef[0][0], coef[0][1]
    x2, y2 = coef[1][0], coef[1][1]
    angle1 = atan2(y1, x1)
    angle2 = atan2(y2, x2)
    angle_degrees_list = []

    if angle2 < angle1:
        angle2 += 2 * pi

    angle_segment = (angle2 - angle1) / nb_segments

    # Pour tous les rayons envoyés
    i = 0
    while i <= nb_segments:

        # On calcule l'angle du rayon
        angle_segment_i = angle1 + angle_segment * i
        angle_degrees = degrees(angle_segment_i)%360

        taille_cote = (g.TAILLE_FENETRE_Y / 16)

        # Init des points d'intersection à None
        point_verticale=None
        point_horizontale = None
        # On calcule les coordonnées de la première intersection verticale
        # selon formule de cours (fonctions des quadrant)
        if int(angle_degrees)%360 != 90 and int(angle_degrees)%360 != 270:
            x_verticale = int(joueur._x_canv // taille_cote) * taille_cote
            if ( (angle_degrees %360 >= 0) and (angle_degrees % 360 < 90) ) or ( (270< angle_degrees % 360) and (angle_degrees % 360 >= 0 ) ) :

                    x_verticale += taille_cote+1


            #Premier Quadrant
            if (0 <= angle_degrees % 360 and angle_degrees % 360 < 90 ):
                y_verticale = joueur._y_canv + (abs(joueur._x_canv - x_verticale)) * tan(radians(angle_degrees))

            #Quatrieme quadrant
            elif  (270 <= angle_degrees % 360 and angle_degrees % 360 < 360 ):
                y_verticale = joueur._y_canv + (abs(joueur._x_canv - x_verticale)) * tan(radians(angle_degrees))

            #Deuxieme quadrant et troisieme quadrant
            else:
                y_verticale = joueur._y_canv + (abs(joueur._x_canv - x_verticale)) * -tan(radians(angle_degrees))

            # on essaye de trouver le point d'intersection vertical qui touche un mur
            point_verticale = interesection_vertical_mur([x_verticale,y_verticale], canvas, angle_degrees)
            #canvas.create_oval(x_verticale-2, y_verticale-2, x_verticale + 2, y_verticale + 2, tags="FOV", fill="blue")


        # On calcule la première intersection horizontale
        # tj en fonction des quadrant
        if int(angle_degrees) != 0 and int(angle_degrees) != 180:
            y_horizontale = joueur._y_canv // taille_cote * taille_cote
            if 180 > int(angle_degrees) %360 and int(angle_degrees) %360 > 0:
                    y_horizontale += taille_cote+2

            #Premier Quadrant et Deuxieme
            if 180 >= angle_degrees %360 and angle_degrees %360 >= 0:
                x_horizontale = joueur._x_canv + abs(joueur._y_canv - y_horizontale) / tan(radians(angle_degrees))

            #Troisieme Quadrant
            elif angle_degrees %360 > 180 and angle_degrees %360<=270:
                x_horizontale = joueur._x_canv - abs(joueur._y_canv - y_horizontale) / tan(radians(angle_degrees))

            #Quatrieme Quadrant
            else :
                x_horizontale = joueur._x_canv + abs(joueur._y_canv - y_horizontale) / -tan(radians(angle_degrees))

            # on essaye de trouver le point d'intersection horizontal qui touche un mur
            point_horizontale = interesection_horizontale_mur([x_horizontale,y_horizontale],canvas,angle_degrees)
            #canvas.create_oval(x_horizontale-2, y_horizontale-2, x_horizontale+ 2, y_horizontale + 2, tags="FOV", fill="green")

        #print("\n RAYON N",i,"_______________________________________")

        #print("angle == ",angle_degrees)
        #point_horizontale = interesection_horizontale_mur([x_horizontale,y_horizontale],canvas,angle_degrees)
        #point_verticale = interesection_vertical_mur([x_verticale,y_verticale], canvas, angle_degrees)

        #Si il y'a pas d'intersection vertical , il y a forcement un intersection horizontal
        if point_verticale == None:
            #print("point horizontal")
            #print(point_horizontale)
            canvas.create_line(joueur._x_canv + ratio, joueur._y_canv + ratio,
                               point_horizontale[0], point_horizontale[1],
                               tags="FOV", fill="blue")

            #On calcul la distance par rapport au joueur
            d = distance((joueur._x_canv, joueur._y_canv),point_horizontale)

            # Rajout dans liste distance global
            g.liste_distance += [d]

        #Si il y'a pas d'intersection horizontal , il y a forcement un intersection vertical
        elif point_horizontale == None:
            #print("point verticale")
            #print(point_verticale)
            canvas.create_line(joueur._x_canv + ratio, joueur._y_canv + ratio,
                               point_verticale[0], point_verticale[1],
                               tags="FOV", fill="blue")

            d = distance((joueur._x_canv, joueur._y_canv),point_verticale)
            g.liste_distance += [d]

        #Si il y a deux point d'interstion touchant un mur on calcul le plus proche du joueur
        else:
            point_plus_proche = plus_proche([joueur._x_canv,joueur._y_canv], point_horizontale,point_verticale)
            #print(point_plus_proche)
            canvas.create_line(joueur._x_canv + ratio, joueur._y_canv + ratio,
                               point_plus_proche[0], point_plus_proche[1],
                               tags="FOV", fill="blue")

            d = distance((joueur._x_canv, joueur._y_canv),point_plus_proche)
            g.liste_distance += [d]

        i+= 1
    #print(g.liste_distance)

def tourner_FOV_gauche(event,joueur,carte):
    """Permet de tourner le FOV du joueur"""

    canvas = event.widget
    canvas.delete("FOV")

    joueur._direction = (joueur._direction-g.vitesse_cam) %360
    #print(joueur._direction)
    dessiner_angle_vision(carte,joueur,canvas)
    return joueur

def tourner_FOV_droite(event,joueur,carte):
    """Permet de tourner le FOV du joueur"""

    canvas = event.widget
    canvas.delete("FOV")

    joueur._direction = (joueur._direction+g.vitesse_cam) %360
    #print(joueur._direction)
    dessiner_angle_vision(carte,joueur,canvas)
    return joueur
