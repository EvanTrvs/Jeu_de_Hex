from interface import *
from calculs import *
from database import *
from strat_denombrement import *
import sqlite3
from copy import deepcopy
from sys import setrecursionlimit
from random import choice



class HEX:
    def __init__(self):
        self.width = 1000
        self.height = round(self.width * 0.618)
        self.size = 5
        self.tour = 0
        self.ordre = []
        self.scale = (self.width - 250) / ((self.size - 1) * 3 + 2)
        self.plat = np.zeros((self.size, self.size), dtype=int)
        self.fe = tk.Tk()
        self.game_status = True
        self.player1 = False
        self.player2 = False
        self.begin = False
        self.timed = False

        self.str_time = tk.StringVar()  # Variable de temps
        self.str_time1 = tk.StringVar()  # Variable de temps
        self.str_time2 = tk.StringVar()  # Variable de temps
        self.tempsT = [default_timer(), 0, 0, 0, 0]

    def graphiques(self):
        self.frame, self.partie1 = fenetre_jeu(self.fe, self.width, self.height)
        save1, save2, save3, restart, pause, tomenu = button_create(self.frame)
        background(self.partie1, self.scale, self.width, self.height, self.size)
        affichage_plateau(self.partie1, self.plat, self.size, self.scale, self.width, self.height)
        self.button_config(save1, save2, save3, restart, pause, tomenu)
        if self.timed is True:
            minuteur()

    def reset(self):
        self.plat, self.ordre, self.tour, self.game_status = np.zeros((self.size, self.size), dtype=int), [], 0, True
        refresh_plateau(self.partie1, self.plat, self.ordre)

    def clic_gauche(self, event):
        tags = self.partie1.gettags('current')

        if len(tags) == 3 and self.game_status is True:
            tag = tags[0].split(",")
            slot = (int(tag[0]), int(tag[1]))

            if self.tour == 0 and slot[0] == self.size - (self.size + 1) / 2 and slot[1] == self.size - (self.size + 1) / 2:  # condition de l'interdiction de jouer le premier coup sur le centre
                pass

            elif self.plat[slot[0]][slot[1]] == 0:
                self.partie1.tag_raise(tags[0])
                self.ordre.append((slot[0], slot[1]))

                if len(self.ordre) > 1:
                    self.partie1.itemconfig(str(self.ordre[-2][0]) + "," + str(self.ordre[-2][1]), dash="", outline='black', width=3)

                if self.tour % 2 == 0:
                    self.partie1.itemconfig(tags[0], fill='red', dash=(3, 3, 3, 3), outline=rgb_convert((230, 230, 230)), activefill="", width=2)
                    self.plat[slot[0]][slot[1]] = 1
                    print("Tour", self.tour, ': Rouge (1)')
                    self.partie1.itemconfig("player1tk", fill='')
                    self.partie1.itemconfig("player2tk", fill='blue')
                    #tempsT[1] = tempsT[3]
                else:
                    self.partie1.itemconfig(tags[0], fill='blue', dash=(3, 3, 3, 3), outline=rgb_convert((230, 230, 230)), activefill="", width=2)
                    self.plat[slot[0]][slot[1]] = 2
                    print("Tour", self.tour, ": Bleu (2)")
                    self.partie1.itemconfig("player1tk", fill='red')
                    self.partie1.itemconfig("player2tk", fill='')
                    #tempsT[2] = tempsT[4]

                print(self.plat)
                self.tour += 1
                self.test_victoire(slot)

    def button_config(self, save1, save2, save3, restart, pause, tomenu):
        restart.config(command=self.reset)
        tomenu.config(command=self.fe.destroy)

    def plein_ecran(self, event):
        if self.fe.attributes()[7] == 0:
            self.fe.attributes('-fullscreen', True)

        else:
            self.fe.attributes('-fullscreen', False)

    def test_victoire(self, slot):
        search = detection_victoire(self.plat, slot)

        if search is not False:
            self.game_status = False
            team = self.plat[slot[0]][slot[1]]

            if team == 2:
                print("victoire bleu")
            else:
                print("victoire rouge")

            #fin_partie(team, search)
            # show_distance(team, search)


"""
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
"""
setrecursionlimit(1500)

hex = HEX()
hex.graphiques()

hex.fe.bind("<f>", hex.plein_ecran)
hex.fe.bind("<KeyPress-F11>", hex.plein_ecran)
hex.fe.bind("<Button-1>", hex.clic_gauche)

hex.fe.mainloop()