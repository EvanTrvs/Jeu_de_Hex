def rgb_convert(rgb):
    return "#%02x%02x%02x" % rgb


def reset_value(new_plat, new_ordre):
    tour = len(new_ordre)
    ordre = new_ordre
    plat = new_plat

    return plat, ordre, tour


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