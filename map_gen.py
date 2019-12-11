#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import random


# Fonction qui créée un fichier contenant un plateau conforme
def map_gen(x, y, density):
    map_a_creer = open("map_non_valide_4", "w")
    map_a_creer.write('{}.ox'.format(y))
    map_a_creer.write('\n')
    for i in range(int(y)):
        for j in range(int(x)):
            if (random.randint(0, int(y)) * 2) < int(density):
                map_a_creer.write('o')
            else:
                map_a_creer.write('.')
        map_a_creer.write('\n')
    map_a_creer.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Missing parameters.')
        exit()
    map_gen(*sys.argv[1:4])
