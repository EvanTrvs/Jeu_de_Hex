from interface import *
from calculs import *
from database import *
from strat_hub import ask_bot1
from sys import setrecursionlimit
from time import sleep
from timeit import default_timer


class HEX:
    def __init__(self):
        self.width = 1400
        self.height = round(self.width * 0.618)
        self.size = 5
        self.tour = 0
        self.ordre = []
        self.scale = round((self.width - 250) / ((self.size - 1) * 3 + 2))
        self.plat = np.zeros((self.size, self.size), dtype=int)
        self.bot = ask_bot1
        self.game_status = False
        self.players = False, False
        self.begin = False
        self.timed = False
        self.temps = [0, 0, 0, 0, 0, 0]
        self.botcooldown = 1
        self.fe, self.frame = structure_tkinter(self.width, self.height)
        
    def ecran_accueil(self, *event):
        game_status = False
        shortcut, play = affichage_accueil(self.fe, self.frame, self.scale)
        shortcut.config(command = self.ecran_jeu)
        play.config(command = self.ecran_parametres)
        self.fe.bind("<Escape>", lambda x: self.fe.destroy())
        self.fe.unbind("<Button-1>")
        self.fe.unbind("<space>")
        
    def ecran_parametres(self):
        menuprincipal = affichage_parametres(self.fe, self.frame, self.scale)
        menuprincipal.config(command = self.ecran_accueil)
        self.fe.bind("<Escape>", self.ecran_accueil)

    def ecran_jeu(self):
        self.partie1, self.temps[2], self.temps[3], self.temps[4] = fenetre_jeu(self.fe, self.frame, self.width, self.height, self.timed, self.scale)

        self.temps[2].set("%02d:%02d" % (0, 0))

        if self.timed is True:
            self.temps[3].set("%02d:%02d" % (5, 0))
            self.temps[4].set("%02d:%02d" % (5, 0))

        background(self.partie1, self.scale, self.width, self.height, self.size)

        affichage_plateau(self.partie1, self.plat, self.size, self.scale, self.width, self.height)

        save1, save2, save3, restart, self.playbutton, tomenu = button_create(self.frame, self.scale)
        self.button_config(save1, save2, save3, restart, tomenu)

        self.fe.bind("<Button-1>", self.clic_gauche)
        self.fe.bind("<Escape>", self.ecran_accueil)
        self.fe.bind("<space>", self.pausef)

    def reset(self):
        self.plat, self.ordre, self.tour, self.game_status = np.zeros((self.size, self.size), dtype=int), [], 0, True
        refresh_plateau(self.partie1, self.plat, self.ordre)
        self.temps[0] = round(default_timer() * 100)
        self.temps[2].set("%02d:%02d" % (0, 0))
        if self.timed is True:
            self.temps[3].set("%02d:%02d" % (5, 0))
            self.temps[4].set("%02d:%02d" % (5, 0))

        self.pausef()
        self.playbutton.config(text="Commencer", state='normal')

    def pausef(self, *event):
        if self.game_status is True:
            self.game_status = False
            self.temps[1] = round(default_timer() * 100) - self.temps[0]
            self.partie1.itemconfig("cellule", activefill='')
            self.playbutton.config(bg='red')
            print("pause on")
        else:
            self.game_status = True
            self.temps[0] = round(default_timer() * 100) - self.temps[1]
            
            if self.temps[1] == 0:
                self.temps[0] = round(default_timer() * 100)
                self.update_time()
                self.playbutton.config(text='Pause')

            for i in range(self.size):
                for j in range(self.size):
                    tag = str(i) + ',' + str(j)

                    if self.plat[i][j] == 0:
                        self.partie1.itemconfig(tag, activefill=rgb_convert((180, 180, 180)))
            self.playbutton.config(bg='white')
            print("pause off")
            self.nexts()


    def clic_gauche(self, event):
        tags = self.partie1.gettags('current')

        if len(tags) == 3 and self.game_status is True:
            tag = tags[0].split(",")
            slot = (int(tag[0]), int(tag[1]))

            if self.tour == 0 and slot[0] == self.size - (self.size + 1) / 2 and slot[1] == self.size - (self.size + 1) / 2:  # condition de l'interdiction de jouer le premier coup sur le centre
                pass

            elif self.plat[slot[0]][slot[1]] == 0:
                self.game_action(tags[0], slot)
                self.test_victoire(slot)
        self.nexts()

    def button_config(self, save1, save2, save3, restart, tomenu):
        restart.config(command=self.reset)
        tomenu.config(command=self.ecran_accueil)
        self.playbutton.config(command=self.pausef)

    def plein_ecran(self, event):
        if self.fe.attributes()[7] == 0:
            self.fe.attributes('-fullscreen', True)

        else:
            self.fe.attributes('-fullscreen', False)

    def test_victoire(self, slot):
        team = self.plat[slot[0]][slot[1]]
        search = False
        start, end = verrous(self.plat, team)

        if start is not False:
            search = detection_victoire(self.plat, slot, team, start, end)

        if search is not False: #victoire
            self.pausef()
            self.fe.unbind("<space>")

            self.partie1.itemconfig("player1tk", fill='')
            self.partie1.itemconfig("player2tk", fill='')

            if len(self.ordre) > 1:
                self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="",outline='black', width=3)

            if team == 2:
                print("victoire bleu")
            else:
                print("victoire rouge")

            self.playbutton.config(state="disabled")
            fin_partie(team, search)
            # show_distance(team, search)

    def game_action(self, tag, slot):

        if len(self.ordre) != 0:
            self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="", outline='black', width=3)

        team = ((self.tour) % 2) + 1

        self.partie1.tag_raise(tag)
        self.ordre.append((slot[0], slot[1]))

        if team == 1:
            self.partie1.itemconfig(tag, fill='red', dash=(3, 3, 3, 3), outline=rgb_convert((230, 230, 230)), activefill="", width=2)
            print("Tour", self.tour, ': Rouge (1)')
            self.partie1.itemconfig("player1tk", fill='')
            self.partie1.itemconfig("player2tk", fill='blue')
            # tempsT[1] = tempsT[3]
        else:
            self.partie1.itemconfig(tag, fill=rgb_convert((0, 0, 255)), dash=(3, 3, 3, 3),outline=rgb_convert((230, 230, 230)), activefill="", width=2)
            self.plat[slot[0]][slot[1]] = 2
            print("Tour", self.tour, ": Bleu (2)")
            self.partie1.itemconfig("player1tk", fill='red')
            self.partie1.itemconfig("player2tk", fill='')
            # tempsT[2] = tempsT[4]

        self.plat[slot[0]][slot[1]] = team
        print(self.plat)
        self.tour += 1

    def nexts(self):

        team = ((self.tour) % 2) + 1

        if self.players[self.tour % 2] is True and self.game_status is True:
            slot = self.bot(self.plat, team)
            tag = str(slot[0]) + ',' + str(slot[1])
            self.game_action(tag, slot)
            self.test_victoire(slot)

            if self.players[self.tour % 2] is True:
                self.fe.update()
                sleep(self.botcooldown)
                self.nexts()

    def update_time(self):
        sleep_time = 997

        if self.game_status is True:
            self.temps[1] = round(default_timer()*100) - self.temps[0]

            minutes = int(self.temps[1] / 6000)  # Calcul des minutes
            secondes = int(self.temps[1]/100 - minutes * 60)  # Calcul des secondes
            csecondes = int(self.temps[1] - minutes * 6000 - secondes * 100 )  # Calcul des milli-secondes

            self.temps[2].set("%02d:%02d" % (minutes, secondes))

            if self.timed is True:
                m_csecondes = 100 - csecondes
                m_secondes = 59 - secondes
                m_minutes = 4 - minutes

                if m_secondes <= 0 and m_csecondes <= 90:
                    self.pausef()

                    self.partie1.itemconfig("player1tk", fill='')
                    self.partie1.itemconfig("player2tk", fill='')

                    if len(self.ordre) > 1:
                        self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="",
                                                outline='black', width=3)

                    if team == 2:
                        print("victoire bleu")
                    else:
                        print("victoire rouge")

                    self.playbutton.config(state="disabled")
                else:
                    if csecondes == 0:
                        m_csecondes = 0
                        m_secondes += 1
                        if m_secondes == 60:
                            m_secondes = 0
                            m_minutes += 1

                    if m_minutes == 0 and m_secondes <= 30:
                        self.temps[3].set("%02d:%02d:%02d" % (m_minutes, m_secondes, m_csecondes))
                        self.temps[4].set("%02d:%02d:%02d" % (m_minutes, m_secondes, m_csecondes))
                        sleep_time = 80
                    else:
                        if m_csecondes > 0:
                            m_secondes += 1
                            if m_secondes > 59:
                                m_secondes = 0
                                m_minutes += 1

                        self.temps[3].set("%02d:%02d" % (m_minutes, m_secondes))
                        self.temps[4].set("%02d:%02d" % (m_minutes, m_secondes))

        self.fe.after(sleep_time, self.update_time)


setrecursionlimit(2000)

hex = HEX()

hex.ecran_accueil()

hex.fe.bind("<f>", hex.plein_ecran)
hex.fe.bind("<KeyPress-F11>", hex.plein_ecran)

hex.fe.mainloop()