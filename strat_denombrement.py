from random import choice


def pre_pascal(mat, team, side):
    mats = deepcopy(mat)

    if side == 'd':
        for i in range(len(mat)):
            if mat[i][0] == 0:
                mats[i][0] = 1
            elif mat[i][0] == team:
                mats[i][0] = 2
            else:
                mats[i][0] = 0
    else:
        for i in range(len(mat)):
            if mat[i][len(mat) - 1] == 0:
                mats[i][len(mat) - 1] = 1
            elif mat[i][len(mat) - 1] == team:
                mats[i][len(mat) - 1] = 2
            else:
                mats[i][len(mat) - 1] = 0
    return mats


def meilleur_coup(res, mat):
    flat = res.flatten()
    flat.sort()

    coup = np.where(mat != 0)

    libre = []
    occupe = []
    dic = {}

    for i in range(len(coup[0])):
        occupe.append((coup[0][i], coup[1][i]))

    n = 0

    while len(libre) == 0:
        n += 1
        li = np.where(res == flat[-n])
        libre = []

        for i in range(len(li[0])):
            libre.append((li[0][i], li[1][i]))

        for i in occupe:
            if i in libre:
                libre.remove(i)

        if len(occupe) == 0 and (int(len(mat) / 2), int(len(mat) / 2)) in libre:
            libre.remove((int(len(mat) / 2), int(len(mat) / 2)))

    for i in libre:
        sum_voisin = 0

        if i[0] + 1 <= len(res) - 1:
            sum_voisin += res[i[0] + 1][i[1]]
        if i[0] + 1 <= len(plat) - 1 and i[1] - 1 >= 0:
            sum_voisin += res[i[0] + 1][i[1] - 1]
        if i[1] - 1 >= 0:
            sum_voisin += res[i[0]][i[1] - 1]
        if i[1] + 1 <= len(plat) - 1:
            sum_voisin += res[i[0]][i[1] + 1]
        if i[0] - 1 >= 0 and i[1] + 1 <= len(plat) - 1:
            sum_voisin += res[i[0] - 1][i[1] + 1]
        if i[0] - 1 >= 0:
            sum_voisin += res[i[0] - 1][i[1]]

        # doit etre un ratio entre la plus grosse valeur et ses voisins

        if sum_voisin not in dic:
            dic[sum_voisin] = [i]
        else:
            dic[sum_voisin].append(i)

    return choice(dic[max(dic.keys())])


def pascald(mat, slot, team):
    matx = deepcopy(mat)

    for i in range(1, len(matx) - (slot[1])):
        for j in range(slot[0] + 1):

            if matx[slot[0] - j][slot[1] + i] != team and matx[slot[0] - j][slot[1] + i] != 0:
                matx[slot[0] - j][slot[1] + i] = 0

            elif slot[0] - j + 1 < len(matx):
                if matx[slot[0] - j][slot[1] + i] == 0:
                    matx[slot[0] - j][slot[1] + i] = matx[slot[0] - j][slot[1] + i - 1] + matx[slot[0] - j + 1][
                        slot[1] + i - 1]
                elif matx[slot[0] - j][slot[1] + i] == team:
                    matx[slot[0] - j][slot[1] + i] = 2 * (
                                matx[slot[0] - j][slot[1] + i - 1] + matx[slot[0] - j + 1][slot[1] + i - 1])
            else:
                if matx[slot[0] - j][slot[1] + i] == 0:
                    matx[slot[0] - j][slot[1] + i] = matx[slot[0] - j][slot[1] + i - 1]
                elif matx[slot[0] - j][slot[1] + i] == team:
                    matx[slot[0] - j][slot[1] + i] = 2 * matx[slot[0] - j][slot[1] + i - 1]

    return matx


def pascalg(mat, slot, team):
    matx = deepcopy(mat)

    for i in range(1, (slot[1]) + 1):
        for j in range(len(matx) - slot[0]):

            if matx[slot[0] + j][slot[1] - i] != team and matx[slot[0] + j][slot[1] - i] != 0:
                matx[slot[0] + j][slot[1] - i] = 0

            elif slot[0] + j - 1 >= 0:
                if matx[slot[0] + j][slot[1] - i] == 0:
                    matx[slot[0] + j][slot[1] - i] = matx[slot[0] + j][slot[1] - i + 1] + matx[slot[0] + j - 1][
                        slot[1] - i + 1]
                elif matx[slot[0] + j][slot[1] - i] == team:
                    matx[slot[0] + j][slot[1] - i] = 2 * (
                                matx[slot[0] + j][slot[1] - i + 1] + matx[slot[0] + j - 1][slot[1] - i + 1])
            else:
                if matx[slot[0] + j][slot[1] - i] == 0:
                    matx[slot[0] + j][slot[1] - i] = matx[slot[0] + j][slot[1] - i + 1]
                elif matx[slot[0] + j][slot[1] - i] == team:
                    matx[slot[0] + j][slot[1] - i] = 2 * matx[slot[0] + j][slot[1] - i + 1]

    return matx
