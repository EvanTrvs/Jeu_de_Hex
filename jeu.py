from interface import *
from calculs import *
from database import *
from strat_hub import ask_bot1
from sys import setrecursionlimit
from time import sleep
from timeit import default_timer
        


class HEX:
    def __init__(self):
        
        
        self.width = 1000 #en fonction de la taille de l'écran, optimal : 1000, maximal : 1500
        
        
        self.height = round(self.width * 0.618)
        self.size = 5
        self.tour = 0
        self.ordre = []
        self.scale = round((self.width - ((self.width/4.8) - (self.size*5))) / ((self.size - 1) * 3 + 2))
        self.plat = np.zeros((self.size, self.size), dtype=int)
        self.bot = [ask_bot1, ask_bot1]
        self.game_status = False
        self.players = False, False
        self.begin = False
        self.timed = False
        self.temps = [0, 0, 0, 0, 0, 30000, 30000]
        self.botcooldown = 1
        self.fe, self.frame = structure_tkinter(self.width, self.height)
        self.fe.bind("<f>", self.plein_ecran)
        self.fe.bind("<KeyPress-F11>", self.plein_ecran)
        
    def ecran_accueil(self, *event):
        self.plat, self.ordre, self.tour, self.game_status, self.temps[0] = np.zeros((self.size, self.size), dtype=int), [], 0, False, round(default_timer() * 100)
        game_status = False
        shortcut, play, Save1, Save2, Save3 = affichage_accueil(self.fe, self.frame, self.width)
        self.ecran_sauvegarde(Save1, Save2, Save3)
        shortcut.config(command = self.ecran_jeu)
        play.config(command = self.ecran_parametres)
        self.fe.bind("<Escape>", lambda x: self.fe.destroy())
        self.fe.unbind("<Button-1>")
        self.fe.unbind("<space>")
        
    def ecran_parametres(self):
        menuprincipal, HEXlogo, ready, choix1, choix2, taille, timevar, choixb1, choixb2, assis1, assis2, cd1 = affichage_parametres(self.fe, self.frame, self.width)
        menuprincipal.config(command = self.ecran_accueil)
        HEXlogo.config(command = self.ecran_accueil)
        ready.config(command = lambda: [self.charge(4, taille.get(), (choix1.get(), choix2.get()), timevar.get(), (choixb1.get(), choixb2.get()), (assis1.get(), assis2.get()), float(cd1.get()[:3]))])                                         
        self.fe.bind("<Escape>", self.ecran_accueil)
        
    def ecran_sauvegarde (self, save1, save2, save3):
        verif = verif_enregistrement ()
        
        if type(save1)!=tuple:
            save1.config (state = verif [0], command = lambda: [self.charge (1)])
            save2.config (state = verif [1], command = lambda: [self.charge (2)])
            save3.config (state = verif [2], command = lambda: [self.charge (3)])
        else:        
            save1 [0].config (save1 [1].entryconfig ("Charger A", state = verif [0], command = lambda: [self.charge (1)]))
            save2 [0].config (save2 [1].entryconfig ("Charger B", state = verif [1], command = lambda: [self.charge (2)]))
            save3 [0].config (save3 [1].entryconfig ("Charger C", state = verif [2], command = lambda: [self.charge (3)]))

    def ecran_jeu(self):
        self.partie1, self.temps[2], self.temps[3], self.temps[4], self.frame1, self.frame2, self.chron = fenetre_jeu(self.fe, self.frame, self.width, self.height, self.timed)

        self.temps[2].set("%02d:%02d" % (0, 0))

        if self.timed is True:
            self.temps[3].set("%02d:%02d" % (5, 0))
            self.temps[4].set("%02d:%02d" % (5, 0))

        background(self.partie1, self.scale, self.width, self.height, self.size)

        affichage_plateau(self.partie1, self.plat, self.size, self.scale, self.width, self.height)

        save1, save2, save3, restart, self.playbutton, tomenu = boutons_creations(self.frame, self.width)
        self.button_config(save1, save2, save3, restart, tomenu)

        self.fe.bind("<Button-1>", self.clic_gauche)
        self.fe.bind("<Escape>", self.ecran_accueil)
        self.fe.bind("<space>", self.pausef)
        
        #print(self.plat, self.ordre, self.tour, self.game_status, self.temps[1], self.size, self.players, self.timed, self.bot, self.assis, self.botcooldown)

    def reset(self):
        self.plat, self.ordre, self.tour, self.game_status, self.temps[0] = np.zeros((self.size, self.size), dtype=int), [], 0, True, round(default_timer() * 100)
        refresh_plateau(self.partie1, self.frame1, self.frame2, self.plat, self.ordre)
        self.temps[2].set("%02d:%02d" % (0, 0))
        if self.timed is True:
            self.temps[3].set("%02d:%02d" % (5, 0))
            self.temps[4].set("%02d:%02d" % (5, 0))

        self.pausef()
        self.playbutton.config(text="Commencer", state='normal', bg=rgb_convert((200,255,120)))
        self.playbutton.grid(row=14, column=11, padx=0, pady=0)
        self.chron.config(bg='white')
        self.fe.bind("<space>", self.pausef)

    def pausef(self, *event):
        if self.game_status is True:
            self.game_status = False
            self.temps[1] = round(default_timer() * 100) - self.temps[0]
            if self.temps[1]<10:
                self.temps[5] = 30000
                self.temps[6] = 30000
            self.partie1.itemconfig("cellule", activefill='')
            self.playbutton.config(bg=rgb_convert((255,80,80)), text='Reprendre', state="normal")
            self.chron.config(bg=rgb_convert((255,80,80)))
            print("pause on")
        else:
            self.game_status = True
            self.temps[0] = round(default_timer() * 100) - self.temps[1]
            
            if self.temps[1] < 10:
                self.temps[0] = round(default_timer() * 100)
                self.frame1.config(bg=rgb_convert((255,255,0)))
                self.update_time()

            for i in range(self.size):
                for j in range(self.size):
                    tag = str(i) + ',' + str(j)

                    if self.plat[i][j] == 0:
                        self.partie1.itemconfig(tag, activefill=rgb_convert((180, 180, 180)))
            self.playbutton.config(bg='white', text="Pause")
            self.chron.config(bg='white')
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

    def plein_ecran(self, event):
        if self.fe.attributes()[7] == 0:
            self.fe.attributes('-fullscreen', True)
        else:
            self.fe.attributes('-fullscreen', False)
            
    def button_config(self, save1, save2, save3, restart, tomenu):
        
        save1 [0].config (save1 [1].entryconfig ("Enregistrer sur A", command = lambda: [enregistrement (self.plat, self.ordre, self.players, self.timed, 1),self.ecran_sauvegarde(save1, save2, save3)]))
        save2 [0].config (save2 [1].entryconfig ("Enregistrer sur B", command = lambda: [enregistrement (self.plat, self.ordre, self.players, self.timed, 2),self.ecran_sauvegarde(save1, save2, save3)]))
        save3 [0].config (save3 [1].entryconfig ("Enregistrer sur C", command = lambda: [enregistrement (self.plat, self.ordre, self.players, self.timed, 3),self.ecran_sauvegarde(save1, save2, save3)]))
        
        verif = verif_enregistrement()
        
        save1 [0].config (save1 [1].entryconfig ("Charger A", state = verif [0], command = lambda: [self.charge (1)]))
        save2 [0].config (save2 [1].entryconfig ("Charger B", state = verif [1], command = lambda: [self.charge (2)]))
        save3 [0].config (save3 [1].entryconfig ("Charger C", state = verif [2], command = lambda: [self.charge (3)]))

        restart.config(command=self.reset)
        tomenu.config(command=self.ecran_accueil)
        self.playbutton.config(command=self.pausef)
        
    def charge(self, nb, *args):
        
        if nb != 4:
            self.plat, self.ordre, self.players, self.time = chargement(nb)
            self.tour, self.size = len(self.ordre), len(self.plat)
            self.scale = round((self.width - ((self.width/4.8) - (self.size*5))) / ((self.size - 1) * 3 + 2))
            
            if len(self.frame.winfo_children())==9:
                self.partie1.delete('all')
                background(self.partie1, self.scale, self.width, self.height, self.size)
                affichage_plateau(self.partie1, np.zeros((self.size, self.size), dtype=int), self.size, self.scale, self.width, self.height)
            else:
                self.ecran_jeu()
                
            refresh_plateau(self.partie1, self.frame1, self.frame2, self.plat, self.ordre)
            if len(self.ordre) != 0:
                self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash=(3, 3, 3, 3), outline=rgb_convert((255,255,180)), width=2)
                self.partie1.tag_raise(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]))
                self.game_status = True
                self.playbutton.grid(row=14, column=11, padx=0, pady=0)
                self.pausef() 
        else:
            self.size, self.players, self.timed, self.assis, self.botcooldown = args[0], args[1], args[2], args[4], args[5]
            self.plat, self.ordre, self.tour, self.game_status, self.temps[0], self.temps[1] = np.zeros((self.size, self.size), dtype=int), [], 0, False, round(default_timer() * 100), 0
            self.scale = round((self.width - ((self.width/4.8) - (self.size*5))) / ((self.size - 1) * 3 + 2))
            
            for i in range (2):
                if args[3][i] == 1:
                    self.bot[i]=ask_bot1
                elif args[3][i] == 2:
                    self.bot[i]=ask_bot2
                    
            self.ecran_jeu() 

    def test_victoire(self, slot):
        team = self.plat[slot[0]][slot[1]]
        search = False
        start, end = verrous(self.plat, team)

        if start is not False:
            search = detection_victoire(self.plat, slot, team, start, end)

            if search is not False: #victoire
                self.pausef()
                self.fe.unbind("<space>")

                self.frame1.config(bg="black")
                self.frame2.config(bg="black")

                if len(self.ordre) > 1:
                    self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="",outline='black', width=3)

                self.playbutton.config(state="disabled")
                self.playbutton.grid_forget()
                    
                fin_partie(team, search, self.partie1)
                # show_distance(team, search)

    def game_action(self, tag, slot):

        if len(self.ordre) != 0:
            self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="", outline='black', width=3)

        team = ((self.tour) % 2) + 1

        self.partie1.tag_raise(tag)
        self.ordre.append((slot[0], slot[1]))

        if team == 1:
            self.partie1.itemconfig(tag, fill='red', dash=(3, 3, 3, 3), outline=rgb_convert((255,255,180)), activefill="", width=2)
            print("Tour", self.tour, ': Rouge (1)')
            self.frame2.config(bg=rgb_convert((255,230,0)))
            self.frame1.config(bg="black")
            # tempsT[1] = tempsT[3]
        else:
            self.partie1.itemconfig(tag, fill=rgb_convert((0,110,255)), dash=(3, 3, 3, 3),outline=rgb_convert((255,255,180)), activefill="", width=2)
            self.plat[slot[0]][slot[1]] = 2
            print("Tour", self.tour, ": Bleu (2)")
            self.frame1.config(bg=rgb_convert((255,230,0)))
            self.frame2.config(bg="black")
            # tempsT[2] = tempsT[4]

        self.plat[slot[0]][slot[1]] = team
        print(self.plat)
        self.tour += 1

    def nexts(self):

        team = ((self.tour) % 2) + 1

        if self.players[self.tour % 2] is True and self.game_status is True:
            slot = self.bot[self.tour % 2](self.plat, team)
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
                if self.tour % 2 == 0:
                    a, n = 5, 6
                else:
                    a, n = 6, 5
                
                self.temps[a] = 60000 - self.temps[1] - self.temps[n]
                
                arrondi = round(self.temps[a]*0.01)*100
                minutes = int(arrondi / 6000)  # Calcul des minutes
                secondes = int(arrondi/100 - minutes * 60)  # Calcul des secondes
                csecondes = int(arrondi - minutes * 6000 - secondes * 100 )  # Calcul des milli-secondes
                
                self.temps[a-2].set("%02d:%02d" % (minutes, secondes))
                
                """
                else:
                    self.temps[6] = 60000 - self.temps[1] - self.temps[5]
                    
                    arrondi = round(self.temps[6]*0.01)*100
                    minutes = int(arrondi / 6000)  # Calcul des minutes
                    secondes = int(arrondi/100 - minutes * 60)  # Calcul des secondes
                    csecondes = int(arrondi - minutes * 6000 - secondes * 100 )  # Calcul des milli-secondes
                    
                    self.temps[4].set("%02d:%02d" % (minutes, secondes))
                
                
                m_csecondes = 100 - csecondes
                m_secondes = 59 - secondes
                m_minutes = 4 - minutes
                
                if tour%2 == 0:
                    self.temps[5] = (m_csecondes + m_secondes * 100 + m_minutes * 6000) - self.temps[6]
                    tid = 3
                    
                else:
                    self.temps[6]= (m_csecondes + m_secondes * 100 + m_minutes * 6000) - self.temps[5]
                    tid = 4

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
                    """

        self.fe.after(sleep_time, self.update_time)


setrecursionlimit(2000)

hex = HEX()

hex.ecran_accueil()

hex.fe.mainloop()