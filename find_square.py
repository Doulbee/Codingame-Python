#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys


# Vérifie que chaque caractère de fin du fichier soit '\n'
def fin_des_lignes_du_fichier_est_ok(map_name):
    fin_des_lignes_ok = True

    map_file = open(map_name, 'r')
    lines = map_file.readlines()
    map_file.close()

    # Pour chaque ligne du fichier
    for line in lines:
        # Si le caractère de fin de ligne n'est pas '\n'
        if line[-1] != '\n':
            fin_des_lignes_ok = False

    return fin_des_lignes_ok


class Plateau:
    def __init__(self, carte, plein, obstacle, vide, longueur):
        self.carte = carte
        self.len_x = len(carte[0])
        self.len_y = len(carte)
        self.pos_largest_x = None
        self.pos_largest_y = None
        self.size_largest = 0
        self.size_largest_to_found = 1
        self.plein = plein
        self.obstacle = obstacle
        self.vide = vide
        self.longueur = longueur

    # Retourne un booléen : True si le fichier est une map valide, False sinon
    def toutes_les_lignes_meme_longueur(self):
        # Vérifie si toutes les lignes font la même longueur
        len_ligne = len(self.carte[0])
        for i in range(self.len_y):
            if len_ligne != len(self.carte[i]):
                return False

        return True

    # Retourne un booléen : True si tous les caractères sont ceux présents en début de fichier, False sinon
    def carte_composee_de_caractere_valide(self):
        # Vérifie toute la carte à la recherche de caractère inconu
        for i in range(self.len_y):
            for j in range(self.len_x):
                if (self.carte[i][j] != self.vide and
                        self.carte[i][j] != self.obstacle):
                    return False

        return True

    # Trouve le carré le plus grand à une position donnée
    def find_square(self, current_y, current_x):
        # Si le nouveau carré le plus long à trouver est hors des limites
        if (current_x + self.size_largest_to_found - 1 >= self.len_x or
                current_y + self.size_largest_to_found - 1 >= self.len_y):
            pass
        # Sinon
        else:
            new_largest_square_found = True
            # Pour chaque élément du plateau pouvant faire parti du nouveau carré le plus grand
            for m in range(self.size_largest_to_found):
                for n in range(self.size_largest_to_found):
                    # Nous vérifions que les éléments ne soient pas des obstacles
                    if self.carte[current_y + m][current_x + n] == self.vide:
                        pass
                    else:
                        new_largest_square_found = False

            # Si un nouveau plus grand carré a été trouvé
            if new_largest_square_found:
                # La taille du plus grand carré augmente
                self.size_largest_to_found = self.size_largest_to_found + 1
                # La taille du plus grand carré à trouver augmente
                self.size_largest = self.size_largest + 1
                # Les positions du carré le plus grand du moment sont mises à jour
                self.pos_largest_x = current_x
                self.pos_largest_y = current_y

                # On relance la fonction sur ces positions pour vérifier si un carré encore plus grand est présent ici
                self.find_square(current_y, current_x)

    # Affiche le plus grand carré
    def print_largest_square(self):
        # Remplace les caractères vides du plus grand carré trouvé par des pleins
        if self.pos_largest_x is not None and self.pos_largest_y is not None:
            for m in range(self.size_largest):
                for n in range(self.size_largest):
                    self.carte[self.pos_largest_y + m][self.pos_largest_x + n] = self.plein

        # Affiche le nouveau plateau
        for i in range(self.len_y):
            for j in range(self.len_x):
                print(self.carte[i][j], end='')
            print('', end='\n')


if __name__ == '__main__':
    # Si aucun fichier n'est passé en paramètre
    if len(sys.argv) < 2:
        print('Missing parameters.')
        exit()

    # Pour chaque fichier passé en paramètre
    for map_name in sys.argv[1:]:
        # Si le caractère de fin de chaque ligne est '\n'
        if fin_des_lignes_du_fichier_est_ok(map_name):
            # Lecture du fichier et modélisation sous forme d'une liste de str
            map_file = open(map_name, 'r')
            contenu = map_file.read()
            c = contenu.split('\n')
            map_file.close()

            # Récupération des informations de la première ligne
            plein = c[0][-1]
            obstacle = c[0][-2]
            vide = c[0][-3]
            longueur = c[0][0:-3]

            # Suppression de la première et la dernière ligne du fichier
            del(c[0])
            del(c[-1])

            # Modélisation sous forme d'un tableau à 2 dimensions
            carte = []
            for ligne in c:
                carte.append(list(ligne))

            # Si la carte est vide, on affiche Map Error
            if len(carte) == 0:
                print("Map error : carte vide")

            # Si la carte n'est pas vide : on continu
            else:
                # Création d'un objet Plateau
                plateau = Plateau(carte, plein, obstacle, vide, longueur)

                # Si le plateau est valide
                if plateau.toutes_les_lignes_meme_longueur():
                    # Si tous les caractères sont ceux de la première ligne du fichier
                    if plateau.carte_composee_de_caractere_valide():
                        # Trouve le plus grand carré dans le plateau
                        for i in range(plateau.len_y):
                            for j in range(plateau.len_x):
                                plateau.find_square(i, j)

                        # Affiche le plateau
                        plateau.print_largest_square()

                    # Sinon la carte est compose de caractere inconu
                    else:
                        print('Map error : caractere inconu dans le fichier')

                # Sinon les lignes ne font pas la meme longeur
                else:
                    print('Map error : toutes les lignes ne font pas la meme longueur')
        # Sinon le caractère '\n' n'est pas à la fin de chaque ligne
        else:
            print('Map error : il n y a pas de retour a la ligne a la fin de chaque ligne')

        # Affiche un délimiteur annonçant la fin du traitement d'une carte
        print('-' * 30)
        print('')
        print('-' * 30)
