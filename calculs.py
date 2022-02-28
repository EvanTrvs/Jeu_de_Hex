def Rgb_convert(rgb):
    return "#%02x%02x%02x" % rgb


def Reset_Value(New_plat, New_ordre):
    tour = len(New_ordre)
    ordre = New_ordre
    plat = New_plat

    return (plat, ordre, tour)


def Propagation(slot, search, team, distance):
    distance += 1
    search[slot[0]][slot[1]] = distance

    if slot[0] + 1 <= len(search) - 1:
        if search[slot[0] + 1][slot[1]] == team or search[slot[0] + 1][slot[1]] > distance:
            Propagation((slot[0] + 1, slot[1]), search, team, distance)

    if slot[0] + 1 <= len(search) - 1 and slot[1] - 1 >= 0:
        if search[slot[0] + 1][slot[1] - 1] == team or search[slot[0] + 1][slot[1] - 1] > distance:
            Propagation((slot[0] + 1, slot[1] - 1), search, team, distance)

    if slot[1] - 1 >= 0:
        if search[slot[0]][slot[1] - 1] == team or search[slot[0]][slot[1] - 1] > distance:
            Propagation((slot[0], slot[1] - 1), search, team, distance)

    if slot[1] + 1 <= len(search) - 1:
        if search[slot[0]][slot[1] + 1] == team or search[slot[0]][slot[1] + 1] > distance:
            Propagation((slot[0], slot[1] + 1), search, team, distance)

    if slot[0] - 1 >= 0 and slot[1] + 1 <= len(search) - 1:
        if search[slot[0] - 1][slot[1] + 1] == team or search[slot[0] - 1][slot[1] + 1] > distance:
            Propagation((slot[0] - 1, slot[1] + 1), search, team, distance)

    if slot[0] - 1 >= 0:
        if search[slot[0] - 1][slot[1]] == team or search[slot[0] - 1][slot[1]] > distance:
            Propagation((slot[0] - 1, slot[1]), search, team, distance)