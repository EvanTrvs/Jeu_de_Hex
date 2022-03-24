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


def verrous(plat, team):
    size = len(plat)

    if team == 1:
        start = [(0, k) for k, i in enumerate(plat[0]) if i == team]
        end = [(size-1, k) for k, i in enumerate(plat[size - 1]) if i == team]
    else:
        start = [(k, 0) for k, i in enumerate(plat[:, 0]) if i == team]
        end = [(k, size-1) for k, i in enumerate(plat[:, size - 1]) if i == team]

    if len(start) != 0:
        if len(end) != 0:
            if plat[plat == team].size >= size:  # verrou de minimum de pion joué pour une victoire
                return start, end  # print("verrou 3 ok")

    return False, False


def detection_victoire(plat, slot, start, end):
    team = plat[slot[0]][slot[1]]  # team = 1, le joueur blanc viens de jouer, team = 2 le joueur noir viens de jouer

    search = deepcopy(plat)  # creation d'une matrice de travail copié d'un plateau

    propagation(slot, search, team, 9)  # fonction récursive de propagation sur le plateau de travail en fonction du dernier coup joué
    print(search)

    print(start)
    print(end)
    if any(filter(lambda x: x >= 10, {search[i[0]][i[1]] for i in start})) is True:  # si un des pions de la team touche un des bord et est relier au dernier coup
        if any(filter(lambda x: x >= 10, {search[i[0]][i[1]] for i in end})) is True:  # si un des pions de la team touche l'autre bord et est relier au dernier coup
            return search

    return False