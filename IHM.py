import sys
import os

# Obtenez le chemin absolu de la racine du projet
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# Ajoutez le chemin de la racine du projet à sys.path
sys.path.append(root_path)

import time
import tkinter as tk
import myglob as g
from math import cos,sin,radians, degrees, tan

def window(canvastk, liste_distance):
    """
    affiche les murs pour le rendu 2.5d de Tkinter
    """

    # Supprimer tous les objets du canvas avec le tag "mur"
    canvastk.delete('mur')

    # Pour chaque rayon
    for i in range(len(liste_distance)):

        dp = (liste_distance[i] * tan(g.angle_hauteur))

        ratio = g.h_mur / dp

        taille_mur = (g.TAILLE_FENETRE_Y / 2) * ratio

        # Les points haut et bas du segment pour le mur
        x0 = i * g.largeur_bande
        y0 = (g.TAILLE_FENETRE_Y / 2) - taille_mur

        x1 = x0 + g.largeur_bande
        y1 = (g.TAILLE_FENETRE_Y / 2) + taille_mur

        canvastk.create_rectangle(x0, y0, x1, y1, width=0, fill="#963a15", tags="mur")



def main():
    canvastk = None

    liste_distance = []

    window(canvastk,liste_distance)
