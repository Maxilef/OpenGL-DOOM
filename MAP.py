 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 09:39:23 2023

@author: L. SEGURA, M. ROUSSEL
"""

class Map:
    """ classe pour représenté une carte(map) """
    # constructeur par default
    def __init__(self,nb_ligne,nb_colonne):

        # On initialise une carte vide
        self._nom = ""

        #Atribut permetant de connaitre le nombre de colonne et de ligne
        self._l = nb_ligne
        self._c = nb_colonne

        #Attribut permettant de stocker le nombre de mur
        self._wall = 0

        #Matrice représentant la carte dans le terminal
        self._matrice = [0] * nb_ligne

        for i in range(nb_ligne):
            self._matrice[i] = ['_'] * nb_colonne

        #Ajouter plus tard limite de 16x16

    @property
    def nom(self):
        return self._nom

    @property
    def ligne(self):
        return self._l

    @property
    def colonne(self):
        return self._c

    @property
    def matrice(self):
        return self._matrice

    @classmethod
    def file_to_map(cls,nb_ligne,nb_colonne, nom_fichier, nom_carte):
        """
        Lecture d'un fichier pour le convertir en Map:
                # : Mur avec collision
                _ : Espace libr eou le joueur peut se déplacer
        """


        #Ouverture du fichier
        try :
            fichier = open(nom_fichier, "r")
        except:
            print("Erreur lors de l'ouverture du fichier")
            return None

        carte = cls(nb_ligne,nb_colonne)

        carte._nom = str(nom_carte)
        i = 0
        for ligne in fichier:

            # On regarde s'il y a le bon nombre de symbôles sur la ligne -> self.c + 1
            # car on compte '\n'
            if len(ligne) != carte._c+1:
                print(ligne)
                print(f"Erreur sur la ligne, doit contenir {nb_colonne} symbôles, en contient {len(ligne)-1}" )
                raise ValueError

            # Ici on regarde s'il y a le bon nombre de lignes dans le fichier
            elif i >= carte._l:
                print(f"Erreur dans le fichier, doit contenir {nb_ligne} lignes, en contient {i+1}" )
                raise ValueError

            # On regarde chacun des caractères de la ligne
            for j in range(len(ligne)):

                # On traite les position on le joueur peut se déplacer
                if (ligne[j] == '_'):
                    carte._matrice[i][j] = '_'

                # on traite les murs et on incrémente l'attribut
                elif (ligne[j] == '#'):
                    carte._matrice[i][j] = '#'
                    carte._wall += 1


                # on traite le reste avec une erreur
                elif (ligne[j] != '\n'):
                    print(f"Erreur lexique, symbole '{ligne[j]}' inconnu dans le fichier")
                    raise ValueError

            i +=1
        return carte

    def verifier_mur(self,x,y) :
        """
        verifie si mur en x y
        """
        # pas de mur
        res = True

        if self._matrice[int(x)][int(y)] == '#' :
            # mur
            res = False

        return res
