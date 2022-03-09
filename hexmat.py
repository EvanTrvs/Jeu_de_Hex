import sqlite3
import tkinter as tk
import tkinter.font as tkFont
import numpy as np
from string import ascii_letters
from copy import deepcopy
import random
# import math
import time
from timeit import default_timer

conn = sqlite3.connect('Jeu_HEX')
cur = conn.cursor()


def Rgb_convert(rgb):
    return "#%02x%02x%02x" % rgb


def Plein_ecran(event):
    if fe.attributes()[7] == 0:
        fe.attributes('-fullscreen', True)

    else:
        fe.attributes('-fullscreen', False)


def Affichage_plateau(plat, size, scale):
    for i in range(size):
        for j in range(size):
            x = (width - (scale * ((size - 1) * 3 + 2))) / 2 + (j * scale * 1.5) + (i * scale * 1.5)
            y = (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (0.866 * scale * size) - (
                        j * scale * 0.866) + (i * scale * 0.866)

            if plat[i][j] == 0:
                partie1.create_polygon(x + (0.5 * scale), y, x + (1.5 * scale), y, x + (2 * scale), y + (scale * 0.866),
                                       x + (scale * 1.5), y + (scale * 2 * 0.866),
                                       x + (scale * 0.5), y + (scale * 2 * 0.866), x, y + (scale * 0.866),
                                       fill=Rgb_convert((160, 160, 160)), activefill=Rgb_convert((170, 170, 170)),
                                       outline='black', width=3, tags=(str(i) + "," + str(j), "cellule"))

            elif plat[i][j] == 1:
                partie1.create_polygon(x + (0.5 * scale), y, x + (1.5 * scale), y, x + (2 * scale), y + (scale * 0.866),
                                       x + (scale * 1.5), y + (scale * 2 * 0.866),
                                       x + (scale * 0.5), y + (scale * 2 * 0.866), x, y + (scale * 0.866), fill="red",
                                       outline='black', width=3, tag=str(i) + "," + str(j))

            elif plat[i][j] == 2:
                partie1.create_polygon(x + (0.5 * scale), y, x + (1.5 * scale), y, x + (2 * scale), y + (scale * 0.866),
                                       x + (scale * 1.5), y + (scale * 2 * 0.866),
                                       x + (scale * 0.5), y + (scale * 2 * 0.866), x, y + (scale * 0.866), fill="blue",
                                       outline='black', width=3, tag=str(i) + "," + str(j))

            if i == 0:
                partie1.create_text(x, y + 0.2 * scale, font=Police, fill='black', text=ascii_letters[j])

            if j == 0:
                partie1.create_text(x, (y + 1.5 * scale), font=Police, fill='black', text=i + 1)


def Detection_victoire(plat, slot):
    global stop
    size = len(plat)
    team = plat[slot[0]][slot[1]]  # team = 1, le joueur blanc viens de jouer, team = 2 le joueur noir viens de jouer

    start = []  # liste des coordonnees de depart

    if team == 1:
        for i in range(size):  # verrou de pion jouer sur un bord
            if plat[0][i] == team:
                start.append((0, i))
    elif team == 2:
        for i in range(size):  # verrou de pion jouer sur un bord
            if plat[i][0] == team:
                start.append((i, 0))

    if len(start) == 0:
        # if bot == True:
        # Ask_bot(plat)
        pass

    else:
        end = []  # liste des coordonnees d'arrivee
        print("verrou 1 ok")

        if team == 1:
            for i in range(size):  # verrou de pion jouer sur l'autre bord
                if plat[size - 1][i] == team:
                    end.append((size - 1, i))
        elif team == 2:
            for i in range(size):  # verrou de pion jouer sur l'autre bord
                if plat[i][size - 1] == team:
                    end.append((i, size - 1))

        if len(end) == 0:
            # if bot == True:
            # move = Ask_bot(plat)
            # plat[ move[0] ][ move[1] ] =
            pass

        else:
            print("verrou 2 ok")
            if plat[plat == team].size < size:  # verrou de minimum de pion joue pour une victoire
                # if bot == True:
                # Ask_bot(plat)
                pass

            else:
                print("verrou 3 ok")
                search = deepcopy(plat)  # creation d'une matrice de travail copie d'un plateau
                distance = 9

                Propagation(slot, search, team,
                            distance)  # fonction recursive de propagation sur le plateau de travail en fonction du dernier coup joue

                if True in [search[k[0]][k[1]] >= 10 for k in
                            start]:  # si un des pions de la team touche un des bord et est relier au dernier coup

                    if True in [search[q[0]][q[1]] >= 10 for q in
                                end]:  # si un des pions de la team touche l'autre bord et est relier au dernier coup
                        stop = True
                        if team == 2:
                            # Show_distance(team, search)
                            print("victoire noir")
                            # Fin_Partie(team, search)

                        elif team == 1:
                            # Show_distance(team, search)
                            print("victoire blanc")
                            # Fin_Partie(team, search)


def Propagation(slot, search, team, distance):
    distance += 1
    search[slot[0]][slot[1]] = distance

    if slot[0] + 1 <= len(plat) - 1:
        if search[slot[0] + 1][slot[1]] == team or search[slot[0] + 1][slot[1]] > distance:
            Propagation((slot[0] + 1, slot[1]), search, team, distance)

    if slot[0] + 1 <= len(plat) - 1 and slot[1] - 1 >= 0:
        if search[slot[0] + 1][slot[1] - 1] == team or search[slot[0] + 1][slot[1] - 1] > distance:
            Propagation((slot[0] + 1, slot[1] - 1), search, team, distance)

    if slot[1] - 1 >= 0:
        if search[slot[0]][slot[1] - 1] == team or search[slot[0]][slot[1] - 1] > distance:
            Propagation((slot[0], slot[1] - 1), search, team, distance)

    if slot[1] + 1 <= len(plat) - 1:
        if search[slot[0]][slot[1] + 1] == team or search[slot[0]][slot[1] + 1] > distance:
            Propagation((slot[0], slot[1] + 1), search, team, distance)

    if slot[0] - 1 >= 0 and slot[1] + 1 <= len(plat) - 1:
        if search[slot[0] - 1][slot[1] + 1] == team or search[slot[0] - 1][slot[1] + 1] > distance:
            Propagation((slot[0] - 1, slot[1] + 1), search, team, distance)

    if slot[0] - 1 >= 0:
        if search[slot[0] - 1][slot[1]] == team or search[slot[0] - 1][slot[1]] > distance:
            Propagation((slot[0] - 1, slot[1]), search, team, distance)


def Fin_Partie(team, search):
    pass


def Show_distance(team, search):
    print("test", search)
    print((np.max(search) - 10))
    r = 220 / (np.max(search) - 10)
    for i in range(len(plat)):
        for j in range(len(plat)):
            if search[i][j] >= 10:
                tag = str(i) + ',' + str(j)
                if team == 1:
                    partie1.itemconfig(tag, fill=Rgb_convert((255 - int((search[i][j] - 10) * r), 0, 0)))
                else:
                    partie1.itemconfig(tag, fill=Rgb_convert((0, 0, 255 - int((search[i][j] - 10) * r))))


def Clic_gauche_joueur(event):
    global mode, tour, stop
    tags = partie1.gettags('current')

    if len(tags) == 3 and stop == False:
        if mode == "J":
            Joueur(tags)

        else:
            Joueur(tags)
            Bot()

            tour += 1


def Joueur(tags):
    global tour

    tag = tags[0].split(",")
    slot = (int(tag[0]), int(tag[1]))

    if tour == 0 and slot[0] == size - (size + 1) / 2 and slot[1] == size - (
            size + 1) / 2:  # condition de l'interdiction de jouer le premier coup sur le centre
        pass

    elif plat[slot[0]][slot[1]] == 0:

        if len(ordre) != 0:
            partie1.itemconfig(str(ordre[len(ordre) - 1][0]) + "," + str(ordre[len(ordre) - 1][1]), dash="",
                               outline='black')

        if tour % 2 == 0:
            partie1.tag_raise(tags[0])
            partie1.itemconfig(tags[0], fill='red', dash=(3, 3, 3, 3), outline='yellow', activefill="")
            tour += 1
            plat[slot[0]][slot[1]] = 1
            ordre.append((slot[0], slot[1]))
            print("Tour", tour, ': Blanc')
            print(plat)
            Detection_victoire(plat, slot)
            partie1.itemconfig(player1, fill='white')
            partie1.itemconfig(player2, fill='blue')
            tempsT[1] = tempsT[3]
            print(tempsT)

        else:
            partie1.tag_raise(tags[0])
            partie1.itemconfig(tags[0], fill='blue', dash=(3, 3, 3, 3), outline='yellow', activefill="")
            tour += 1
            plat[slot[0]][slot[1]] = 2
            ordre.append((slot[0], slot[1]))
            print("Tour", tour, ": Noir")
            print(plat)
            Detection_victoire(plat, slot)
            partie1.itemconfig(player1, fill='red')
            partie1.itemconfig(player2, fill='white')
            tempsT[2] = tempsT[4]
            print(tempsT)


def PascalD(pascal, plat, cell, team):
    for y in range(size - cell[1]):
        yy = cell[1] + y
        i = cell[0]

        if y <= i:
            nb = y + 1
        else:
            nb = i + 1

        for n in range(nb):

            if plat[i - n][yy] != team and plat[i - n][yy] != 0:
                pascal[i - n][yy] = 0

            elif yy == 0:
                pascal[i - n][yy] = 1

            elif i - n == 4:
                pascal[i - n][yy] = 1

            else:
                a = int(pascal[i - n][yy - 1])
                b = int(pascal[(i - n) + 1][yy - 1])

                if plat[i - n][yy] == team:
                    pascal[i - n][yy] = (a + b) * 2
                else:
                    pascal[i - n][yy] = (a + b)

                pascal[cell[0]][cell[1]] = 1

    return pascal


def PascalG(pascal, plat, cell, team):
    if cell[1] == 0:
        cell = (cell[0], size - 1)

    for y in range(cell[1] + 1):
        yy = cell[1] - y
        i = cell[0]

        if y <= abs(i - 4):
            nb = y + 1
        else:
            nb = abs(i - 4) + 1

        for n in range(nb):
            if plat[i + n][yy] != team and plat[i + n][yy] != 0:
                pascal[i + n][yy] = 0

            elif yy == 4:
                pascal[i + n][yy] = 1

            elif i + n == 0:
                pascal[i + n][yy] = 1

            else:
                a = int(pascal[i + n][yy + 1])
                b = int(pascal[(i + n) - 1][yy + 1])

                if plat[i + n][yy] == team:
                    pascal[i + n][yy] = (a + b) * 2
                else:
                    pascal[i + n][yy] = (a + b)

                pascal[cell[0]][cell[1]] = 1

    return pascal


def Bot():
    global plat

    platposee = deepcopy(plat)
    posee = []
    possible, possibleADV = [], []
    for i in range(size):
        possible.append((i, 0))
        possibleADV.append((i, 0))

        if platposee[:, i][platposee[:, i] == 2].size != 0:
            for y in range(platposee[:, i][platposee[:, i] == 2].size):
                possible.append((platposee[:, i].tolist().index(2), i))
                posee.append((platposee[:, i].tolist().index(2), i))
                platposee[platposee[:, i].tolist().index(2)][i] = 0

        if platposee[:, i][platposee[:, i] == 1].size != 0:
            for y in range(platposee[:, i][platposee[:, i] == 1].size):
                possibleADV.append((platposee[:, i].tolist().index(1), i))
                posee.append((platposee[:, i].tolist().index(1), i))
                platposee[platposee[:, i].tolist().index(1)][i] = 0

    pdroite, pgauche, agauche, adroite = 0, 0, 0, 0

    for i in set(possible):
        pascal = np.zeros((size, size), dtype=int)

        pascal = PascalD(pascal, plat, i, 2)

        print(pascal)
        print("===== pascal", i)
        pdroite += pascal

        pascal2 = np.zeros((size, size), dtype=int)

        pascal2 = PascalG(pascal2, plat, i, 2)

        print(pascal2)
        print("===== pascal2", i)
        pgauche += pascal2

    for i in set(possibleADV):
        pascal3 = np.zeros((size, size), dtype=int)

        pascal3 = PascalD(pascal3, plat.transpose(), i, 1)

        print(pascal3.transpose())
        print("===== pascal3", i)
        adroite += pascal3.transpose()

        pascal4 = np.zeros((size, size), dtype=int)

        pascal4 = PascalG(pascal4, plat.transpose(), i, 1)

        print(pascal4.transpose())
        print("===== pascal4", i)
        agauche += pascal4.transpose()

    print(agauche)
    print(adroite)
    print(pdroite)
    print(pgauche)
    pGD = pdroite * pgauche
    pGDADV = agauche * adroite

    Bp = pGDADV + pGD

    print(posee)
    for p in posee:
        Bp[p[0]][p[1]] = 0
        pGD[p[0]][p[1]] = 0
        pGDADV[p[0]][p[1]] = 0

    print(Bp, np.max(Bp))
    print(pGD, np.max(pGD))
    print(pGDADV, np.max(pGDADV))

    choix = {}
    for i in range(size):
        if Bp[:, i][Bp[:, i] == np.max(Bp)].size != 0:
            pos = Bp[:, i].tolist().index(np.max(Bp))
            print(i, pos)
            choix[(pos, i)] = Bp[pos, :].sum()

    print("choix", choix)
    choix = max(choix, key=choix.get)
    print(choix)

    """
    chemin = {}

    copy = deepcopy (plat)
    pascal = deepcopy (plat)
    posee = []
    for i in range (len (copy)):
        posee.append ((i, 0))
        n = copy[:,i] [copy [:,i] == 2].size
        for y in range (n):
            pion = (copy [:,i].tolist().index(2), i)
            copy [pion [0]][pion [1]] = 0

            pionpla = deepcopy (plat)
            pionpla = np.where (pionpla == 0, 2, pionpla)

            Propagation (pion, pionpla, 2, 9)

            for p in range (len (copy)):
                for o in range (pionpla[:,p] [pionpla [:,p] == 11].size):
                    posee.append ((pionpla [:,p].tolist().index(11), p))
                    pionpla [:,p][pionpla [:,p].tolist().index(11)] = 2




    copy = np.where (copy == 1, -1, copy)
    copy = np.where (copy == 0, 2, copy)
    #copy [:,0] = 1

    for slot in posee:
        Propagation(slot, copy, 2, 9)

        chemin [slot] = np.min (np.where (copy [:,size-1] == -1, 132, copy [:,size-1]))
        copy = deepcopy (plat)
        copy = np.where (copy == 1, -1, copy)
        copy = np.where (copy == 0, 2, copy)

    for key, value in chemin.items ():
        if value == min (chemin.values ()):
            depart = key

    Propagation(slot, copy, 2, 9) 
    """

    """
    chemin = {}


    for i in range (size):
        departs = (i, 0)
        for y in range (size):

            if  y <= i:
                nb = y + 1
            else:
                nb = i+1

            for n in range (nb):
                if pascal [i-n][y] < 0:
                        pascal [i-n][y] = 0

                elif y == 0:
                    pascal [i-n][y] = 1

                elif i-n == 4:
                    pascal [i-n][y] = 1

                else: 
                    a = int (pascal [i-n][y-1])
                    b = int (pascal [(i-n)+1][y-1])

                    if a < 0:
                        a = 0
                    if b < 0:
                        b = 0

                    pascal [i-n][y] = a + b

        #pascal = np.where (pascal == -5, 0, pascal)
        print (pascal)
        print ("=====")

        chemin [(i, 0)] = pascal [:,4].sum ()
        """
    """
    for i in range (size):
        departs = (i, 0)
        pascal2 = deepcopy(plat)
        pascal2 = np.where (pascal2 == 1, -5, pascal2)

        for y in range (size):
            if  y <= i:
                nb = y + 1
            else:
                nb = i+1

            for n in range (nb):
                posi = (i-n, y)
                possible = [posi]
                possibler = [posi]
                p = 0
                pr = 0


                if posi [1] != 4:
                    while len (possible) != 0:
                        posis = possible [0]
                        if posis [1] + 1 == 4:
                            p += 1
                            if posis [0] != 0:
                                p += 1

                            possible.remove (possible [0])

                        elif posis [0] == 0:
                            possible.append ((posis [0], posis [1]+1))
                            possible.remove (possible [0])

                        else:
                            possible.append ((posis [0], posis [1]+1))
                            possible.append ((posis [0]-1, posis [1]+1))
                            possible.remove (possible [0])

                    if posi [1] > 1:
                        while len (possibler) != 0:
                            posis = possibler [0]

                            if (posis [0], posis [1]-1) == departs:
                                pr += 1
                                possibler.remove (possibler [0])

                            elif (posis [0]+1, posis [1]-1) == departs:
                                pr += 1
                                possibler.remove (possibler [0])

                            elif posis [1] == 0:
                                possibler.remove (possibler [0])

                            elif posis [0] == i:
                                possibler.append ((posis [0], posis [1]-1))
                                possibler.remove (possibler [0])

                            else:
                                possibler.append ((posis [0], posis [1]-1))
                                possibler.append ((posis [0]+1, posis [1]-1))
                                possibler.remove (possibler [0])

                    else:
                        pr = 1




                    pascal2 [posi [0]][posi [1]] = p*pr

                else:
                    pascal2 [posi [0]][posi [1]] = pascal [posi [0]][posi [1]]  

          """

    """
    num = 0
    arrive = ((np.where (copy [:,size-1] == -1, 132, copy [:,size-1]).argmin()), 6)
    parcours = [arrive]
    while num != 10:

        num = copy [arrive [0]][arrive [1]]
        print (num)

        print (arrive)        
        print (chemin)

        posi = []
        for i in range (len (copy)):
            if ((num -1) in copy [:,i]) == True:
                print (copy [:,i])
                for y in range (copy[:,i] [copy [:,i] == num-1].size):

                    print(np.where (copy [:,i] == -1, 132, copy [:,i]).tolist().index(num-1))
                    posi.append ((np.where (copy [:,i] == -1, 132, copy [:,i]).tolist().index(num-1), i))
                    copy [:,i][np.where (copy [:,i] == -1, 132, copy [:,i]).tolist().index(num-1)] = 0

        print (posi)
        copy = np.where (copy == 0, num-1, copy)

        for i in posi:
            if (i [0]+1, i [1]-1) == arrive:
                print (i)
                arrive = i
            if (i [0], i [1]+1) == arrive:
                print (i)
                arrive = i
            if (i [0], i [1]-1) == arrive:
                print (i)
                arrive = i
            if (i [0]+1, i [1]) == arrive:
                print (i)
                arrive = i
            if (i [0]+1, i [1]) == arrive:
                print (i)
                arrive = i
            if (i [0]-1, i [1]+1) == arrive:
                print (i)
                arrive = i

        parcours.append (arrive)
        print (arrive)
        print (copy)
    """
    plat[choix[0]][choix[1]] = 2

    # Show_distance(2, copy)
    Affichage_plateau(plat, size, scale)
    # Detection_victoire (plat, depart)


def Clear_plateau():
    global plat, ordre, tour

    if len(ordre) != 0:
        partie1.itemconfig(str(ordre[len(ordre) - 1][0]) + "," + str(ordre[len(ordre) - 1][1]), dash="",
                           outline='black')

    for i in range(len(plat)):
        for j in range(len(plat)):
            if plat[i][j] != 0:
                tag = str(i) + ',' + str(j)
                partie1.itemconfig(tag, fill=Rgb_convert((160, 160, 160)))

    tour = 0
    ordre = []
    plat = np.zeros((size, size))

    return (plat, ordre, tour)


def load_plateau(plats, tours):
    global plat, tour

    for i in range(len(plats)):
        for j in range(len(plats)):

            if plats[i][j] == 0:
                pass

            elif plats[i][j] == 1:
                partie1.itemconfig(str(i) + "," + str(j), fill="red")
                plat[i][j] = 1


            elif plats[i][j] == 2:
                partie1.itemconfig(str(i) + "," + str(j), fill="blue")
                plat[i][j] = 2

    tour = tours
    return plat, tour


def chargement(numero):
    Clear_plateau()
    num = "'" + str(numero) + "'"

    cur.execute("""SELECT Plateau, Joueur, Taille, Tour FROM Enregistrement WHERE Numero = """ + num + """ """)
    conn.commit()
    sauvegarde = cur.fetchall()

    sauvegardes = list(sauvegarde[0][0])
    taille_plat = int(sauvegarde[0][2])
    tour = int(sauvegarde[0][3])

    plato = []

    for i in sauvegardes:
        if i != "[" and i != "]" and i != "." and i != " " and i != "\n":
            plato.append(int(i))

    nb = 0
    plateau = []
    ligne = []
    for i in plato:
        if nb == taille_plat:
            plateau.append(ligne)
            ligne = [i]
            nb = 0

        else:
            ligne.append(i)

        nb += 1

    plateau.append(ligne)

    load_plateau(plateau, tour)

    if numero == 1:
        enregi1.configure(text='Enregistrement 1', command=lambda: enregistrement(1))
        Affichage_plateau(plateau, size, scale)

    elif numero == 2:
        enregi2.configure(text='Enregistrement 2', command=lambda: enregistrement(2))
        Affichage_plateau(plateau, size, scale)

    elif numero == 3:
        enregi3.configure(text='Enregistrement 3', command=lambda: enregistrement(3))
        Affichage_plateau(plateau, size, scale)


def enregistrement(numeros):
    global plat

    save = '"' + str(plat) + '"'
    taille = '"' + str(size) + '"'
    tours = '"' + str(tour) + '"'
    nb = "'" + str(numeros) + "'"

    cur.execute("""UPDATE Enregistrement SET Plateau = """ + save + """,
                Taille = """ + taille + """,
                Tour = """ + tours + """,
                Joueur = "test" WHERE Numero = """ + nb + """ """)
    conn.commit()

    Clear_plateau()

    if numeros == 1:
        enregi1.configure(text='Chargement 1', command=lambda: chargement(1))

    elif numeros == 2:
        enregi2.configure(text='Chargement 2', command=lambda: chargement(2))

    elif numeros == 3:
        enregi3.configure(text='Chargement 3', command=lambda: chargement(3))


def reset_enregistrement():
    for i in range(1, 4):
        i = "'" + str(i) + "'"
        cur.execute("""UPDATE Enregistrement SET Plateau = "" WHERE Numero = """ + str(i) + """ """)
        conn.commit()

        Clear_plateau()

        enregi1.configure(text='Enregistrement 1', command=lambda: enregistrement(1))
        enregi2.configure(text='Enregistrement 2', command=lambda: enregistrement(2))
        enregi3.configure(text='Enregistrement 3', command=lambda: enregistrement(3))


"""
def Enregistrement (plat, ordre, numero):
    pass

def Fin_Partie (team, search):
    pass

def Parametrage():
    pass

def Ask_bot (plat):
    pass

"""

width = 1000
size = 5
player1 = False  # active ou non le bot en tant que player 2
player2 = False
begin = False  # soit blanc commence, soit noir, soit random
timed = False  # active ou non le minuteur pour les joueurs

height = round(width * 0.618)
scale = (width - 250) / ((size - 1) * 3 + 2)

tour = 0
stop = False
ordre = []
mode = "J"

plat = np.zeros((size, size), dtype=int)  # Cree une matrice carre de taille size remplie de 0

fe = tk.Tk()

fe.title('HexGame')
fe.config(bg=Rgb_convert((50, 50, 50)))
xu = width + (width * (0.618 ** 3))
yu = height + (width * (0.618 ** 5))

window = str(round(width + (width * (0.618 ** 3)))) + 'x' + str(round(height + (width * (0.618 ** 5)))) + '+' + str(
    10) + '+' + str(100)

fe.geometry(window)

frame = tk.Frame(fe, width=round(width + (width * (0.618 ** 3))), height=round(height + (width * (0.618 ** 5))),
                 bg='blue')
frame.place(relx=0.5, rely=0.5, anchor="center")

partie1 = tk.Canvas(frame, width=width, height=height, bg=Rgb_convert((180, 160, 150)), highlightbackground='pink',
                    highlightthickness=0)
partie1.grid(row=0, column=0, rowspan=3, columnspan=3)

tplayer1 = partie1.create_text(75, 30, text='player 1')
player1 = partie1.create_rectangle(50, 50, 100, 70, fill='red')

tplayer2 = partie1.create_text(875, 30, text='player 2')
player2 = partie1.create_rectangle(850, 50, 900, 70, fill='white')

str_time = tk.StringVar()  # Variable de temps
chron = tk.Label(frame, textvariable=str_time)
chron.place(x=100, y=500)

str_time1 = tk.StringVar()  # Variable de temps
chron1 = tk.Label(frame, textvariable=str_time1)
chron1.place(x=50, y=90)

str_time2 = tk.StringVar()  # Variable de temps
chron2 = tk.Label(frame, textvariable=str_time2)
chron2.place(x=850, y=90)

str_time.set("%02d:%02d:%02d" % (0, 0, 0))
str_time1.set("%02d:%02d:%02d" % (10, 0, 0))
str_time2.set("%02d:%02d:%02d" % (10, 0, 0))

tempsT = [default_timer(), 0, 0, 0, 0]


def lancementchrono():
    tempsT[0] = default_timer()
    updateTime()


def updateTime():
    global tour
    if tour % 2 == 0:
        now = default_timer() - tempsT[2] - tempsT[0]
        tempsT[3] = now + tempsT[0]

    else:
        now = default_timer() - tempsT[1]
        tempsT[4] = now

    now = 600 - now
    minutes1 = int(now / 60)  # Calcul des minutes
    seconds1 = int(now - minutes1 * 60.0)  # Calcul des secondes
    hseconds1 = int((now - minutes1 * 60.0 - seconds1) * 100)  # Calcul des milli-secondes

    if tour % 2 == 0:
        str_time1.set("%02d:%02d:%02d" % (minutes1, seconds1, hseconds1))  # Affichage
    else:
        str_time2.set("%02d:%02d:%02d" % (minutes1, seconds1, hseconds1))  # Affichage

    now = default_timer() - tempsT[0]
    minutes = int(now / 60)  # Calcul des minutes
    seconds = int(now - minutes * 60.0)  # Calcul des secondes
    hseconds = int((now - minutes * 60.0 - seconds) * 100)  # Calcul des milli-secondes
    str_time.set("%02d:%02d:%02d" % (minutes, seconds, hseconds))  # Affichage
    fe.after(50, updateTime)  # Actualisation toutes les 50 milli-secondes


chrono = tk.Button(frame, text='lancer chrono', command=lancementchrono)
chrono.place(x=100, y=450)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=0, extent=180, fill="red", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=180, extent=180, fill="blue", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 + 0.75),
                   start=90, extent=180, fill="red", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 + 0.75),
                   start=270, extent=180, fill="blue", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (2 * size * 0.866 * scale) - (0.866 * scale) + scale * (
                               0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * size * 2 * scale) - (0.866 * scale) + scale * (
                               0.866 + 0.75),
                   start=270, extent=180, fill="red", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (2 * size * 0.866 * scale) - (0.866 * scale) + scale * (
                               0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * size * 2 * scale) - (0.866 * scale) + scale * (
                               0.866 + 0.75),
                   start=90, extent=180, fill="blue", outline="black", width=3)

partie1.create_arc(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 1.25 * scale - scale * 0.5 + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 0.5 * scale + 1.25 * scale + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
    start=0, extent=180, fill="blue", outline="black", width=3)

partie1.create_arc(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 1.25 * scale - scale * 0.5 + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 0.5 * scale + 1.25 * scale + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
    start=180, extent=180, fill="red", outline="black", width=3)

partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 2 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 + 1.25 * scale * 0.866,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * 0.866 - scale * 0.6494,
                       fill="red", outline="black", width=3)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + scale * 0.625,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 + 1.25 * scale * 0.866,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * 0.866 - scale * 0.6494,
    fill="blue", outline="black", width=3)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + 0.625 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size) + scale * (0.6494 + 0.866),
    fill="red", outline="black", width=3)

partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - scale * 0.866 + 1.948 * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 2 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - 0.866 * scale + 1.948 * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (
                                   2 * 0.866 * scale * size) + scale * (0.6494 + 0.866),
                       fill="blue", outline="black", width=3)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + 0.625 * scale - 4,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale - 2,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale + 10,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
    fill='red', outline='red', width=6)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) - 80,
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - 0.5 * scale + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) + 3,
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size) + scale * (
                0.6494 + 0.866) - 2,
    fill='blue', outline='blue', width=6)

partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (
                                   -0.5 + 0.3746) + 20,
                       (height - (scale * size * 2 * 0.866)) / 2 - 0.5 * scale + (2 * 0.866 * scale * size),
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (
                                   2 * 0.866 * scale * size) + scale * (0.6494 + 0.866) - 4,
                       fill='red', outline='red', width=6)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + 0.625 * scale - 4,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale + 2,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale - 10,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
    fill='blue', outline='blue', width=6)

partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625 + 4,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale + 2,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale + 1.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (
                                   1.948 - 0.866) * scale - 10,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
                       fill='red', outline='red', width=6)

partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625 + 4,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - 0.866 * scale + 1.948 * scale - 2,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale + 1.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - 0.866 * scale + 1.948 * scale + 10,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
                       fill='blue', outline='blue', width=6)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) - 80,
    (height - (scale * size * 2 * 0.866)) / 2 + scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 + scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) + 1,
    (height - (scale * size * 2 * 0.866)) / 2 - scale * 0.6494 + 4,
    fill='red', outline='red', width=6)

partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5),
                       (height - (scale * size * 2 * 0.866)) / 2 + scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (
                                   -0.5 + 0.3746) + 20, (height - (scale * size * 2 * 0.866)) / 2 + scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - scale * 0.6494 + 4,
                       fill='blue', outline='blue', width=6)

Police = tkFont.Font(weight="bold", size=-(int(scale / 2)))

Affichage_plateau(plat, size, scale)

enregi1 = tk.Button(frame, text="Enregistrement 1", command=lambda: enregistrement(1))
enregi1.grid(row=0, column=4, padx=10, pady=10)
enregi2 = tk.Button(frame, text="Enregistrement 2", command=lambda: enregistrement(2))
enregi2.grid(row=1, column=4, padx=10, pady=10)
enregi3 = tk.Button(frame, text="Enregistrement 3", command=lambda: enregistrement(3))
enregi3.grid(row=2, column=4, padx=10, pady=10)

for nb in range(1, 4):
    cur.execute("""SELECT Plateau, Joueur, Taille, Tour FROM Enregistrement WHERE Numero = """ + str(nb) + """ """)
    conn.commit()
    demarrage = cur.fetchall()

    if demarrage[0][0] != '':
        if nb == 1:
            enregi1.configure(text='Chargement 1', command=lambda: chargement(1))

        elif nb == 2:
            enregi2.configure(text='Chargement 2', command=lambda: chargement(2))

        elif nb == 3:
            enregi3.configure(text='Chargement 3', command=lambda: chargement(3))

des = tk.Button(frame, text='Menu principal', command=fe.destroy)
des.grid(row=4, column=0, padx=10, pady=10)

des1 = tk.Button(frame, text='Abandon', command=Clear_plateau)
des1.grid(row=4, column=1, padx=10, pady=10)

reset = tk.Button(frame, text='RESET', command=reset_enregistrement)
reset.grid(row=4, column=2, padx=10, pady=10)

partie4 = tk.Frame(frame, width=(width * (0.618 ** 3)), height=(width * (0.618 ** 5)), bg='pink')
partie4.grid(row=4, column=4)

frame.configure(bg='gray')

fe.bind("<Button-1>", Clic_gauche_joueur)
fe.bind("<KeyPress-F11>", Plein_ecran)

fe.mainloop()