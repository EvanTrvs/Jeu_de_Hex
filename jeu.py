from interface import *
from calculs import *
import sqlite3
from copy import deepcopy
from sys import setrecursionlimit
from random import choice

conn = sqlite3.connect('Jeu_HEX')
cur = conn.cursor()


class HEX():
    def __init__(self, width):
        self.fe = tk.Tk()
        self.width = width
        self.height = round(width * 0.618)
        self.size = 5
        self.scale = (self.width - 250) / ((self.size - 1) * 3 + 2)
        self.plat = np.zeros((self.size, self.size), dtype=int)
        self.player1 = False
        self.player2 = True
        self.tour = 0
        self.ordre = []
        self.Game_status = True

        self.str_time = tk.StringVar()  # Variable de temps
        self.str_time1 = tk.StringVar()  # Variable de temps
        self.str_time2 = tk.StringVar()  # Variable de temps
        self.tempsT = [default_timer(), 0, 0, 0, 0]

        self.fe.bind("<f>", self.Plein_ecran)
        self.fe.bind("<KeyPress-F11>", self.Plein_ecran)
        self.fe.bind("<Button-1>", self.Clic_gauche_joueur)

    def graphiques(self):
        #fe
        #frame
        #button
        pass

    def detection_victoire(self, plat, slot):
        team = plat[slot[0]][
            slot[1]]  # team = 1, le joueur blanc viens de jouer, team = 2 le joueur noir viens de jouer

        start = []  # liste des coordonnees de depart

        if team == 1:
            for i in range(self.size):  # verrou de pion jouer sur un bord
                if plat[0][i] == team:
                    start.append((0, i))

        elif team == 2:
            for i in range(self.size):  # verrou de pion jouer sur un bord
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
                for i in range(self.size):  # verrou de pion jouer sur l'autre bord
                    if plat[self.size - 1][i] == team:
                        end.append((self.size - 1, i))

            elif team == 2:
                for i in range(self.size):  # verrou de pion jouer sur l'autre bord
                    if plat[i][self.size - 1] == team:
                        end.append((i, self.size - 1))

            if len(end) == 0:
                # if bot == True:
                # move = Ask_bot(plat)
                # plat[ move[0] ][ move[1] ] =
                pass

            else:
                print("verrou 2 ok")
                if plat[plat == team].size < self.size:  # verrou de minimum de pion joue pour une victoire
                    # if bot == True:
                    # Ask_bot(plat)
                    pass

                else:
                    print("verrou 3 ok")
                    search = deepcopy(plat)  # creation d'une matrice de travail copie d'un plateau
                    distance = 9

                    self.Propagation(slot, search, team,
                                     distance)  # fonction recursive de propagation sur le plateau de travail en fonction du dernier coup joue

                    if True in [search[k[0]][k[1]] >= 10 for k in
                                start]:  # si un des pions de la team touche un des bord et est relier au dernier coup

                        if True in [search[q[0]][q[1]] >= 10 for q in
                                    end]:  # si un des pions de la team touche l'autre bord et est relier au dernier coup
                            self.stop = True
                            if team == 2:
                                # Show_distance(team, search)
                                print("victoire noir")
                                # Fin_Partie(team, search)

                            elif team == 1:
                                # Show_distance(team, search)
                                print("victoire blanc")
                                # Fin_Partie(team, search)




    def Reset_Value(self, New_plat, New_ordre):

        self.tour = len(New_ordre)
        self.ordre = New_ordre
        self.plat = New_plat


    def Reset(self):
        self.Clear_plateau()
        self.Reset_Value(np.zeros((self.size, self.size), dtype=int), [])


    def chargement(self, numero):
        self.Reset()

        num = "'" + str(numero) + "'"

        cur.execute("""SELECT Plateau, Taille, Ordre FROM Enregistrement WHERE Numero = """ + num + """ """)
        conn.commit()
        sauvegarde = cur.fetchall()

        sauvegardes = list(sauvegarde[0][0])
        taille_plat = int(sauvegarde[0][1])
        ordres = list(sauvegarde[0][2])

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
        plateau = np.zeros((taille_plat, taille_plat), dtype=int)
        for i in plato:
            if y == taille_plat:
                x += 1
                y = 0

            plateau[x][y] = i

            y += 1

        self.Reset_Value(plateau, ordre)
        self.load_plateau(plateau)

        if numero == 1:
            self.enregi1.configure(text='Enregistrement 1', command=lambda: self.enregistrement(1))
            self.Affichage_plateau(plateau, taille_plat, self.scale)

        elif numero == 2:
            self.enregi2.configure(text='Enregistrement 2', command=lambda: self.enregistrement(2))
            self.Affichage_plateau(plateau, taille_plat, self.scale)

        elif numero == 3:
            self.enregi3.configure(text='Enregistrement 3', command=lambda: self.enregistrement(3))
            self.Affichage_plateau(plateau, taille_plat, self.scale)

    def enregistrement(self, numeros):
        save = '"' + str(self.plat) + '"'
        taille = '"' + str(self.size) + '"'
        ordres = "'" + str(self.ordre) + "'"
        nb = "'" + str(numeros) + "'"

        cur.execute("""UPDATE Enregistrement SET Plateau = """ + save + """,
                Taille = """ + taille + """,
                Ordre = """ + ordres + """
                WHERE Numero = """ + nb + """ """)
        conn.commit()

        self.Reset()

        if numeros == 1:
            self.enregi1.configure(text='Chargement 1', command=lambda: self.chargement(1))

        elif numeros == 2:
            self.enregi2.configure(text='Chargement 2', command=lambda: self.chargement(2))

        elif numeros == 3:
            self.enregi3.configure(text='Chargement 3', command=lambda: self.chargement(3))

    def reset_enregistrement(self):
        for i in range(1, 4):
            i = "'" + str(i) + "'"

            cur.execute("""UPDATE Enregistrement SET Plateau = "", Taille = "", Ordre = "" WHERE Numero = """ + str(
                i) + """ """)
            conn.commit()

            self.Reset()

            self.enregi1.configure(text='Enregistrement 1', command=lambda: self.enregistrement(1))
            self.enregi2.configure(text='Enregistrement 2', command=lambda: self.enregistrement(2))
            self.enregi3.configure(text='Enregistrement 3', command=lambda: self.enregistrement(3))


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

                propagation(slot, search, team, distance)  # fonction récursive de propagation sur le plateau de travail en fonction du dernier coup joué
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

    if len(tags) == 3 and Game_status is True:

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
                partie1.itemconfig(player1tk, fill='white')
                partie1.itemconfig(player2tk, fill='blue')
                tempsT[1] = tempsT[3]


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
                partie1.itemconfig(player1tk, fill='red')
                partie1.itemconfig(player2tk, fill='white')
                tempsT[2] = tempsT[4]

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


"""
def Reset():
    global plat, ordre, tour, Game_status
    Clear_plateau()
    plat, ordre, tour = Reset_Value(zeros((size, size), dtype=int), [])
    Game_status = True
"""

setrecursionlimit(1500)

chrono = tk.Button(frame, text='lancer chrono', command=lancementchrono)
chrono.place(x=100, y=450)


# des1.config(command = Reset)

affichage_plateau(plat, size, scale)

fe.bind("<Button-1>", clic_gauche)
fe.bind("<KeyPress-F11>", plein_ecran)
fe.bind("<f>", plein_ecran)

fe.mainloop()
