from interface import *
from calculs import rgb_convert, propagation, reset_value
from numpy import where
from copy import deepcopy


def detection_victoire(plat, slot):

    size = len(plat)
    team = plat[slot[0]][slot[1]]  # team = 1, le joueur blanc viens de jouer, team = 2 le joueur noir viens de jouer

    start = []  # liste des coordonnées de départ

    if team == 1:
        for i in range(size):  # verrou de pion jouer sur un bord
            if plat[0][i] == team:
                start.append((0, i))
    else:
        for i in range(size):  # verrou de pion jouer sur un bord
            if plat[i][0] == team:
                start.append((i, 0))

    if len(start) == 0:
        # if bot == True:
        # Ask_bot(plat)
        pass

    else:
        end = []  # liste des coordonnées d'arrivée
        # print("verrou 1 ok")

        if team == 1:
            for i in range(size):  # verrou de pion jouer sur l'autre bord
                if plat[size - 1][i] == team:
                    end.append((size - 1, i))
        else:
            for i in range(size):  # verrou de pion jouer sur l'autre bord
                if plat[i][size - 1] == team:
                    end.append((i, size - 1))

        if len(end) == 0:
            # if bot == True:
            # move = Ask_bot(plat)
            # plat[ move[0] ][ move[1] ] =
            pass

        else:
            # print("verrou 2 ok")
            if plat[plat == team].size < size:  # verrou de minimum de pion joué pour une victoire
                # if bot == True:
                # Ask_bot(plat)
                pass

            else:
                # print("verrou 3 ok")
                search = deepcopy(plat)  # creation d'une matrice de travail copié d'un plateau
                distance = 9

                propagation(slot, search, team,
                            distance)  # fonction récursive de propagation sur le plateau de travail en fonction du dernier coup joué
                print(search)

                if True in [search[k[0]][k[1]] >= 10 for k in
                            start]:  # si un des pions de la team touche un des bord et est relier au dernier coup

                    if True in [search[q[0]][q[1]] >= 10 for q in
                                end]:  # si un des pions de la team touche l'autre bord et est relier au dernier coup

                        if team == 2:
                            print("victoire bleu")
                            fin_partie(team, search)

                        else:
                            print("victoire rouge")
                            fin_partie(team, search)
                show_distance(team, search)


def fin_partie(team, search):
    global Game_status
    Game_status = False

    if len(ordre) != 0:
        partie1.itemconfig(str(ordre[len(ordre) - 1][0]) + "," + str(ordre[len(ordre) - 1][1]), dash="",
                           outline='black', width=3)

    partie1.itemconfig("cellule", activefill='')

    chemin = []

    if team == 1:

        depart = min(filter(lambda i: i > 10, search[0]))
        debut = list(where((search[0] == depart))[0])
        for i in debut:
            chemin.append((0, i))

        """
        for i in range (int(depart)-10):

            if slot[0]+1 <= len(plat)-1:
                if search[ slot[0]+1 ][ slot[1] ] == team or search[ slot[0]+1 ][ slot[1] ] > distance:
                    Propagation( ( slot[0]+1, slot[1]), search, team, distance)

            elif slot[0]+1 <= len(plat)-1 and slot[1]-1 >= 0:
                if search[ slot[0]+1 ][ slot[1]-1 ] == team  or search[ slot[0]+1 ][ slot[1]-1 ] > distance:
                    Propagation( ( slot[0]+1, slot[1]-1), search, team, distance)

            elif slot[1]-1 >= 0:
                if search[ slot[0] ][ slot[1]-1 ] == team or search[ slot[0] ][ slot[1]-1 ] > distance:
                    Propagation( ( slot[0], slot[1]-1), search, team, distance)

            elif slot[1]+1 <= len(plat)-1:
                if search[ slot[0] ][ slot[1]+1 ] == team or search[ slot[0] ][ slot[1]+1 ] > distance:
                    Propagation( ( slot[0], slot[1]+1), search, team, distance)

            elif slot[0]-1 >= 0 and slot[1]+1 <= len(plat)-1:
                if search[ slot[0]-1 ][ slot[1]+1 ] == team or search[ slot[0]-1 ][ slot[1]+1 ] > distance:
                    Propagation( ( slot[0]-1, slot[1]+1), search, team, distance)

            elif slot[0]-1 >= 0:
                if search[ slot[0]-1 ][ slot[1] ] == team or search[ slot[0]-1 ][ slot[1] ] > distance:
                    Propagation( ( slot[0]-1, slot[1]), search, team, distance)

        """


def clic_gauche(event):
    global tour, Game_status

    tags = partie1.gettags('current')

    if len(tags) == 3 and Game_status == True:

        tag = tags[0].split(",")
        slot = (int(tag[0]), int(tag[1]))

        if tour == 0 and slot[0] == size - (size + 1) / 2 and slot[1] == size - (
                size + 1) / 2:  # condition de l'interdiction de jouer le premier coup sur le centre
            pass

        elif plat[slot[0]][slot[1]] == 0:

            if len(ordre) != 0:
                partie1.itemconfig(str(ordre[len(ordre) - 1][0]) + "," + str(ordre[len(ordre) - 1][1]), dash="",
                                   outline='black', width=3)

            if tour % 2 == 0:
                partie1.tag_raise(tags[0])
                partie1.itemconfig(tags[0], fill='red', dash=(3, 3, 3, 3), outline=rgb_convert((230, 230, 230)),
                                   activefill="", width=2)
                tour += 1
                plat[slot[0]][slot[1]] = 1
                ordre.append((slot[0], slot[1]))
                print("Tour", tour, ': Rouge (1)')
                print(plat)
                detection_victoire(plat, slot)

            else:
                partie1.tag_raise(tags[0])
                partie1.itemconfig(tags[0], fill='blue', dash=(3, 3, 3, 3), outline=rgb_convert((230, 230, 230)),
                                   activefill="", width=2)
                tour += 1
                plat[slot[0]][slot[1]] = 2
                ordre.append((slot[0], slot[1]))
                print("Tour", tour, ": Bleu (2)")
                print(plat)
                detection_victoire(plat, slot)


"""
def Reset():
    global plat, ordre, tour, Game_status
    Clear_plateau()
    plat, ordre, tour = Reset_Value(zeros((size, size)), [])
    Game_status = True
"""

# des1.config(command = Reset)

affichage_plateau(plat, size, scale)

fe.bind("<Button-1>", clic_gauche)
fe.bind("<KeyPress-F11>", plein_ecran)
fe.bind("<f>", plein_ecran)

fe.mainloop()
