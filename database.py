import sqlite3
import numpy as np


conn = sqlite3.connect('Jeu_HEX')
cur = conn.cursor()

def chargement(numero):

    num = "'" + str(numero) + "'"

    cur.execute("""SELECT Plateau, Taille, Ordre, Players, Temps FROM Enregistrement WHERE Numero = """ + num + """ """)
    conn.commit()
    sauvegarde = cur.fetchall()

    sauvegardes = list(sauvegarde[0][0])
    taille_plat = int(sauvegarde[0][1])
    ordres = list(sauvegarde[0][2])
    players = str (sauvegarde [0][3])
    temps = str (sauvegarde [0][4])
    
    print (sauvegarde)
    print (type (sauvegardes), type (taille_plat), type (ordres), type (players), type (temps))
    print (temps)
    plato = []
    for i in sauvegardes:
        if i != "[" and i != "]" and i != "." and i != " " and i != "\n" and i != ",":
            plato.append(int(i))

    ordre = []
    for i in range(len(ordres)):
        if ordres[i] == '(':
            ordre.append((int(ordres[i + 1]), int(ordres[i + 4])))

    x = 0
    y = 0
    plat = np.zeros((taille_plat, taille_plat), dtype=int)
    for i in plato:
        if y == taille_plat:
            x += 1
            y = 0

        plat[x][y] = i
        y += 1
    

    for i in range (len (players)):
        if players [i] == '(':
            player1 = str ((str (players [i+1]) + str (players [i+2]) + str (players [i+3]) + str (players [i+4]) + str (players [i+5])))
        
        elif players [i] == ',':
            player2 = str ((str (players [i+2]) + str (players [i+3]) + str (players [i+4]) + str (players [i+5]) + str (players [i+6])))
    
    if player1 == 'False':
        player1 = False
        
    if player2 == 'False':
        player2 = False
    
    print(plat, ordre, (player1, player2), temps)
    return plat, ordre, (player1, player2), temps

def enregistrement(plat, ordre, player, time, numeros):
    print (plat, ordre, player, time, numeros)
    save = '"' + str(plat) + '"'
    taille = '"' + str(len (plat)) + '"'
    ordres = "'" + str(ordre) + "'"
    players = "'" + str(player) + "'"
    temps = "'" + str (time) + "'"
    nb = "'" + str(numeros) + "'"
    
    cur.execute("""UPDATE Enregistrement SET Plateau = """ + save + """,
            Taille = """ + taille + """,
            Ordre = """ + ordres + """,
            Players = """ + players + """,
            Temps = """ + temps + """
            WHERE Numero = """ + nb + """ """)
    conn.commit()


def reset_enregistrement():
    for i in range(1, 4):
        i = "'" + str(i) + "'"

        cur.execute("""UPDATE Enregistrement SET Plateau = "", Taille = "", Ordre = "", Players = "", Temps = "" WHERE Numero = """ + str(
            i) + """ """)
        conn.commit()

def verif_enregistrement ():
    verif = ['disabled', 'disabled', 'disabled']
    for nb in range (1, 4):
        cur.execute ("""SELECT Plateau, Taille, Ordre FROM Enregistrement WHERE Numero = """ + str (nb) + """ """)
        conn.commit ()
        demarrage = cur.fetchall ()
            
        if demarrage [0][0] != '' and demarrage [0][2] != "[]":
            if nb == 1:
                verif [0] = 'normal'
        
            elif nb == 2:
                verif [1] = 'normal'
        
            elif nb == 3:
                verif [2] = 'normal'
                
    return verif
