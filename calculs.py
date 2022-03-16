from copy import deepcopy


def rgb_convert(rgb):
    return "#%02x%02x%02x" % rgb


def propagation(slot, search, team, distance):
    distance += 1
    search[slot[0]][slot[1]] = distance

    if slot[0] + 1 <= len(search) - 1:
        if search[slot[0] + 1][slot[1]] == team or search[slot[0] + 1][slot[1]] > distance:
            propagation((slot[0] + 1, slot[1]), search, team, distance)
    if slot[0] + 1 <= len(search) - 1 and slot[1] - 1 >= 0:
        if search[slot[0] + 1][slot[1] - 1] == team or search[slot[0] + 1][slot[1] - 1] > distance:
            propagation((slot[0] + 1, slot[1] - 1), search, team, distance)
    if slot[1] - 1 >= 0:
        if search[slot[0]][slot[1] - 1] == team or search[slot[0]][slot[1] - 1] > distance:
            propagation((slot[0], slot[1] - 1), search, team, distance)
    if slot[1] + 1 <= len(search) - 1:
        if search[slot[0]][slot[1] + 1] == team or search[slot[0]][slot[1] + 1] > distance:
            propagation((slot[0], slot[1] + 1), search, team, distance)
    if slot[0] - 1 >= 0 and slot[1] + 1 <= len(search) - 1:
        if search[slot[0] - 1][slot[1] + 1] == team or search[slot[0] - 1][slot[1] + 1] > distance:
            propagation((slot[0] - 1, slot[1] + 1), search, team, distance)
    if slot[0] - 1 >= 0:
        if search[slot[0] - 1][slot[1]] == team or search[slot[0] - 1][slot[1]] > distance:
            propagation((slot[0] - 1, slot[1]), search, team, distance)


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
            pass
        else:
            # print("verrou 2 ok")
            if plat[plat == team].size < size:  # verrou de minimum de pion joué pour une victoire
                pass
            else:
                # print("verrou 3 ok")
                search = deepcopy(plat)  # creation d'une matrice de travail copié d'un plateau

                propagation(slot, search, team, 9)  # fonction récursive de propagation sur le plateau de travail en fonction du dernier coup joué
                print(search)

                if True in [search[k[0]][k[1]] >= 10 for k in start]:  # si un des pions de la team touche un des bord et est relier au dernier coup
                    if True in [search[q[0]][q[1]] >= 10 for q in end]:  # si un des pions de la team touche l'autre bord et est relier au dernier coup
                        return search
    return False
