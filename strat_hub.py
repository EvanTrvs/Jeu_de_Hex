from strat_denombrement import *


def ask_bot1(mat, team):
    mat2 = deepcopy(np.transpose(mat))

    if team == 2:
        res = pascald(pre_pascal(mat, 2, "d"), (len(mat) - 1, 0), 2) * pascalg(pre_pascal(mat, 2, "g"), (0, len(mat) - 1), 2)
        res2 = np.transpose(pascald(pre_pascal(mat2, 1, "d"), (len(mat2) - 1, 0), 1) * pascalg(pre_pascal(mat2, 1, "g"), (0, len(mat2) - 1), 1))
    else:
        res = np.transpose(pascald(pre_pascal(mat2, 1, "d"), (len(mat2) - 1, 0), 1) * pascalg(pre_pascal(mat2, 1, "g"), (0, len(mat2) - 1), 1))
        res2 = pascald(pre_pascal(mat, 2, "d"), (len(mat) - 1, 0), 2) * pascalg(pre_pascal(mat, 2, "g"), (0, len(mat) - 1), 2)

    s = np.where(mat != 0)

    for i in range(len(s[0])):
        # res[s[0][i]][s[1][i]] = res[s[0][i]][s[1][i]]/2
        res[s[0][i]][s[1][i]] = 0
        res2[s[0][i]][s[1][i]] = 0

    print(res)
    print(res2)
    print(res + res2)

    coup = meilleur_coup(res + res2, mat)

    print(coup)
    return (coup)