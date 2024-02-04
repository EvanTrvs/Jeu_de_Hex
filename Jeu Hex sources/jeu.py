from interface import *
from calculs import *
from database import *
from strat_hub import *
from sys import setrecursionlimit
from time import sleep
from timeit import default_timer
        


class HEX:
    def __init__(self):
        
        self.width = 1300 #en fonction de la taille de l'écran, optimal : 1000, maximal : 1500
        
        #Initialisation des paramètres de la Class
        self.height = round(self.width * 0.618)
        self.size = 5 #Nombre de cases d'un côter
        self.tour = 0 #Numéro du tour actuel 
        self.ordre = [] #Ordre des coups jouer
        self.scale = round((self.width - ((self.width/4.8) - (self.size*5))) / ((self.size - 1) * 3 + 2))
        self.plat = np.zeros((self.size, self.size), dtype=int) #Création de la matrice du plateau (vide)
        self.bot = [ask_bot1, ask_bot1]
        self.game_status = False #Pause ou non
        self.players = [False, False] #Joueurs
        self.begin = False
        self.timed = False
        self.temps = [0, 30000, 30000, 0, 0, 0, 0] #Chronomètre Global et Individuel
        self.botcooldown = 1 #Temps entre chaque coups (dans une partie BOT contre BOT)
        self.fe, self.frame = structure_tkinter(self.width, self.height) #Fenêtre principale et Cadre principal
        self.fe.bind("<f>", self.plein_ecran) #Intéraction sur la touche F, lançant le plein écran de la fenêtre
        self.fe.bind("<KeyPress-F11>", self.plein_ecran) #Intéraction sur la touche F11, lançant le plein écran de la fenêtre
        self.sleep_time = 997
        
    def ecran_accueil(self, *event): #Focntion créatrice de l'écran d'accueil
        self.plat, self.ordre, self.tour, self.game_status, self.temps[3] = np.zeros((self.size, self.size), dtype=int), [], 0, False, round(default_timer() * 100) #Initialisation des paramètres (plateau, ordre, tours, Pause et temps global)
        game_status = False #Sert réellement ?
        shortcut, play, Save1, Save2, Save3, boutonp, boutonm, fulls = affichage_accueil(self.fe, self.frame, self.width) #Création du bouton Jouer et des boutons de sauvegardes
        #self.ecran_sauvegarde(Save1, Save2, Save3) #Configuration des boutons de sauvegardes
        Save1.config(command = lambda: [self.charge(4, 8, [False, True], False, [0, 1], [False, False], 0.2)]) #Configuration du bouton de lancement de jeu
        Save2.config(command = lambda: [self.charge(4, 8, [True, True], False, [1, 2], [False, False], 0.1)]) #Configuration du bouton de lancement de jeu
        shortcut.config(command = self.ecran_jeu) #sert ?
        play.config(command = lambda: [self.charge(4, 8, [False, False], False, [0, 0], [False, False], 0.2)]) #Configuration du bouton de lancement de jeu
        boutonm.config (command = lambda: [self.taille_fenetre (True)]) #Rétrécissement de la fenêtre
        boutonp.config (command = lambda: [self.taille_fenetre (False)]) #Agrandissement de la fenêtre
        fulls.config (command = self.plein_ecran)
        if self.width <= 500: #Désactivation du bouton en dessous de 500
            boutonm.config (state = 'disabled')
        elif self.width >= 1500: #Désactivation du bouton au dessus de 1500
            boutonp.config (state = 'disabled')
        self.fe.bind("<Escape>", lambda x: self.fe.destroy()) #Intéraction sur la touche Echape, destruisant la fenêtre principale
        self.fe.unbind("<Button-1>") #Empêchement de l'intéraction du clique gauche 
        self.fe.unbind("<space>") #Empêchement de l'intéraction de la barre espace
        
    def ecran_parametres(self): #Fonction créatrice de la fenêtre des paramètres
        menuprincipal, HEXlogo, ready, choix1, choix2, taille, timevar, choixb1, choixb2, assis1, assis2, cd1 = affichage_parametres(self.fe, self.frame, self.width) #Création des boutons à partir de la fenêtre principale, du cadre principal et de la taille de la fenêtre
        menuprincipal.config(command = self.ecran_accueil) #Configuration du bouton permettant le retour à l'écran d'accueil
        HEXlogo.config(command = self.ecran_accueil)#Configuration du bouton image permettant le retour à l'écran d'accueil
        ready.config(command = lambda: [self.charge(4, taille.get(), [choix1.get(), choix2.get()], timevar.get(), [choixb1.get(), choixb2.get()], [assis1.get(), assis2.get()], float(cd1.get()[:3]))]) #Configuration du bouton permettant la récupération et l'envoye des données de paramétrage                                       
        self.fe.bind("<Escape>", self.ecran_accueil) #Intéraction sur la touche Echape
        
    def ecran_sauvegarde (self, save1, save2, save3): #Fonction configurant les boutons d'enregistrements
        verif = verif_enregistrement () #Fonction renvoyant une liste des enregistrements pleins
        
        if type(save1)!=tuple: #Vérification du type de bouton de chargement des sauvegarde (ici, celui du plateau de jeu)
            save1.config (state = verif [0], command = lambda: [self.charge (1)]) #Configuration du bouton de chargement de la sauvegarde A, affiché si l'enregistrement n'est pas vide
            save2.config (state = verif [1], command = lambda: [self.charge (2)]) #Configuration du bouton de chargement de la sauvegarde B, affiché si l'enregistrement n'est pas vide
            save3.config (state = verif [2], command = lambda: [self.charge (3)]) #Configuration du bouton de chargement de la sauvegarde C, affiché si l'enregistrement n'est pas vide
        else: #Vérification du type de bouton de chargement des sauvegarde (ici, celui de l'écran d'accueil)
            save1 [0].config (save1 [1].entryconfig ("Charger A", state = verif [0], command = lambda: [self.charge (1)])) #Configuration du bouton de chargement de la sauvegarde A, affiché si l'enregistrement n'est pas vide
            save2 [0].config (save2 [1].entryconfig ("Charger B", state = verif [1], command = lambda: [self.charge (2)])) #Configuration du bouton de chargement de la sauvegarde B, affiché si l'enregistrement n'est pas vide
            save3 [0].config (save3 [1].entryconfig ("Charger C", state = verif [2], command = lambda: [self.charge (3)])) #Configuration du bouton de chargement de la sauvegarde C, affiché si l'enregistrement n'est pas vide

    def ecran_jeu(self): #Fonction créatrice du plateau de jeu
        self.partie1, self.temps[4], self.temps[5], self.temps[6], self.frame1, self.frame2, self.chron = fenetre_jeu(self.fe, self.frame, self.width, self.height, self.timed)

        self.temps[4].set("%02d:%02d" % (0, 0)) #Création de l'emplacement du Chronomètre global

        if self.timed is True: #Vérification de la demande ou non des chronomètres individuels
            self.temps[5].set("%02d:%02d" % (5, 0)) #Création de l'emplacement du Chronomètre du Joueur 1
            self.temps[6].set("%02d:%02d" % (5, 0)) #Création de l'emplacement du Chronomètre du Joueur 2

        background(self.partie1, self.scale, self.width, self.height, self.size) #Création du fond 

        affichage_plateau(self.partie1, self.plat, self.size, self.scale, self.width, self.height) #Création du plateau de jeu à partir de la matrice du plateau, de la taille du plateau et de la taille de la fenêtre principale

        self.save1, self.save2, self.save3, restart, self.playbutton, tomenu = boutons_creations(self.frame, self.width) #Création des boutons de sauvegardes, de lancement du jeu et de la nouvelle partie
        self.button_config(self.save1, self.save2, self.save3, restart, tomenu) #Configuration des boutons précédents

        self.fe.bind("<Button-1>", self.clic_gauche) #Intéraction sur le clique gauche, lançant la fonction ...
        self.fe.bind("<Escape>", self.ecran_accueil) #Intéraction sur la touche Echape, lançant la fonction de l'écran d'accueil
        self.fe.bind("<space>", self.pausef) #Intéraction sur la barre espace lançant la fonction ...
        
    def reset(self): #Fonction restaurant le plateau à neuf
        self.plat, self.ordre, self.tour, self.game_status, self.temps[3] = np.zeros((self.size, self.size), dtype=int), [], 0, True, round(default_timer() * 100)-1 #Reset du plateau, numéro de tours, ordre et chronomètre
        refresh_plateau(self.partie1, self.frame1, self.frame2, self.plat, self.ordre) #Actualisation du plateau
        self.temps[4].set("%02d:%02d" % (0, 0)) #Actualisation du temps initialisé
        if self.timed is True: #Vérification des chronomètres individuels
            self.temps[5].set("%02d:%02d" % (5, 0)) #Actualisation du temps initialisé
            self.temps[6].set("%02d:%02d" % (5, 0)) #Actualisation du temps initialisé

        self.pausef() #Lancement de la fonction ... (actualisation du temps)
        self.playbutton.config(text="Commencer", state='normal', bg=rgb_convert((200,255,120))) #Configuration du bouton de lancement de jeu
        self.playbutton.grid(row=14, column=11, padx=0, pady=0) #Positionnement du bouton de lancement du jeu
        self.chron.config(bg=rgb_convert((200, 160, 150))) #Configuration du fond du chronomètre
        self.sleep_time = 997
        self.partie1.itemconfigure("vict", text="")
        self.fe.bind("<space>", self.pausef) #Intéraction sur la barre espace, lançant la fonction ...

    def pausef(self, *event):
        if self.game_status is True: #Vérification la pause (désactivée)
            self.game_status = False #Activation de la pause
            self.temps[0] = round(default_timer() * 100) - self.temps[3] #Initialisation du temps pour le chronomètre global
            if self.temps[0]<10:
                self.temps[1] = 30000 #initialisation du temps du chrono du joueur 1
                self.temps[2] = 30000 #initialisation du temps du chrono du joueur 2
            self.partie1.itemconfig("cellule", activefill='')
            self.playbutton.config(bg=rgb_convert((255,80,80)), text='Reprendre', state="normal")
            self.chron.config(bg=rgb_convert((255,80,80)))
            print("pause on")
        else: #Si la pause est active
            self.game_status = True #Désactivation de la pause
            self.temps[3] = round(default_timer() * 100) - self.temps[0] #Initialisation du temps pour le chronomètre global
            
            if self.temps[0] < 10:
                self.temps[3] = round(default_timer() * 100)
                self.frame1.config(bg=rgb_convert((255,255,0)))
                if self.begin==False:
                    self.update_time()
                    self.begin=True

            for i in range(self.size):
                for j in range(self.size):
                    tag = str(i) + ',' + str(j)

                    if self.plat[i][j] == 0:
                        self.partie1.itemconfig(tag, activefill=rgb_convert((180, 180, 180)))
            self.playbutton.config(bg='white', text="Pause")
            self.chron.config(bg=rgb_convert((200, 160, 150)))
            print("pause off")
            self.nexts()


    def clic_gauche(self, event): #Fonction d'événement lors du clique gauche
        tags = self.partie1.gettags('current') 

        if len(tags) == 3 and self.game_status is True:
            tag = tags[0].split(",")
            slot = (int(tag[0]), int(tag[1]))

            if self.tour == 0 and slot[0] == self.size - (self.size + 1) / 2 and slot[1] == self.size - (self.size + 1) / 2:  # condition de l'interdiction de jouer le premier coup sur le centre
                pass

            elif self.plat[slot[0]][slot[1]] == 0:
                self.game_action(tags[0], slot)
                self.test_victoire(slot) #Vérification d'une victoire 
        self.nexts()

    def plein_ecran(self, *event): #Fonction permettant le passage en plein écran
        if self.fe.attributes()[7] == 0: #Vérfication de l'état de la fenêtre actuelle (ici, écran fenêtré)
            self.fe.attributes('-fullscreen', True) #Passage en plein écran
        else: #écran déjà en plein écran
            self.fe.attributes('-fullscreen', False) #Passage en écran fenêtré
            
    def button_config(self, save1, save2, save3, restart, tomenu): #Fonction de configuration des sauvegardes
        
        save1 [0].config( bg=rgb_convert((100, 80, 70)), fg=rgb_convert((100, 80, 70)))
        save2 [0].config( bg=rgb_convert((100, 80, 70)), fg=rgb_convert((100, 80, 70)))
        save3 [0].config( bg=rgb_convert((100, 80, 70)), fg=rgb_convert((100, 80, 70)))
        tomenu.config(bg=rgb_convert((100, 80, 70)), fg='white' ,text="Projet PeiP : Interface pour le Jeu de HEX", highlightthickness = 0, bd = 0)

        restart.config(command=self.reset)
        self.playbutton.config(command=self.pausef)
        
    def charge(self, nb, *args): #Fonction de chargement des sauvegardes
        
        if nb != 4: #Type de c
            self.plat, self.ordre, self.players, self.bot, self.temps = chargement(nb) #Récupération des données de la sauvegarde
            self.temps[3] = round(default_timer() * 100) - self.temps[0] #Iinitialisation du temps
            self.tour, self.size = len(self.ordre), len(self.plat) #Récupération des dernières données
            self.scale = round((self.width - ((self.width/4.8) - (self.size*5))) / ((self.size - 1) * 3 + 2))
            
            if self.temps[6]==' False': #Vérification des chronos individuels (ici, sans chronomètre)
                self.timed = False #Pas d'affichage de Chronomètre
            else:
                self.timed = True #Affichage de Chronomètre
                
            self.ecran_jeu() #Affichage de la fenêtre de jeu
            
            self.temps[4].set("%02d:%02d" % ((int(self.temps[0] / 6000), int(self.temps[0]/100 - 60*int(self.temps[0]/6000))))) #Affichage du Chronomètre global
            
            if self.timed is True: #Vérification de la demande des chronos individuels
                self.temps[5].set("%02d:%02d" % (int((round(self.temps[1]*0.01)*100)/6000), int(round(self.temps[1]*0.01) - 60*int((round(self.temps[1]*0.01)*100)/6000)))) #Affichage du Chronomètre Joueur 1
                self.temps[6].set("%02d:%02d" % (int((round(self.temps[2]*0.01)*100)/6000), int(round(self.temps[2]*0.01) - 60*int((round(self.temps[2]*0.01)*100)/6000)))) #Affichage du Chronomètre Joueur 2
            
            if self.begin == False:
                self.update_time()
                self.begin = True
                
            refresh_plateau(self.partie1, self.frame1, self.frame2, self.plat, self.ordre) #Actualisation du plateau
            if len(self.ordre) != 0: #Si le plateau n'est pas vide
                self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash=(3, 3, 3, 3), outline=rgb_convert((255,255,180)), width=2)
                self.partie1.tag_raise(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]))
                self.game_status = True
                self.playbutton.grid(row=14, column=11, padx=0, pady=0)
                self.pausef() 
        else:
            self.size, self.players, self.timed, self.assis, self.botcooldown = args[0], args[1], args[2], args[4], args[5]
            self.plat, self.ordre, self.tour, self.game_status, self.temps[3], self.temps[0] = np.zeros((self.size, self.size), dtype=int), [], 0, False, round(default_timer() * 100), 0
            self.scale = round((self.width - ((self.width/4.8) - (self.size*5))) / ((self.size - 1) * 3 + 2))
            self.temps[0], self.temps[1], self.temps[2] = 1, 30000, 30000
            self.temps[3] = round(default_timer() * 100) - self.temps[0]
            
            for i in range (2):
                if args[3][i] == 1:
                    self.bot[i]=ask_bot1
                elif args[3][i] == 2:
                    self.bot[i]=ask_bot2
                    
            self.ecran_jeu() 

    def test_victoire(self, slot): #Détection victoire
        team = self.plat[slot[0]][slot[1]] #Récupération du chiffre des pions à analyser (1 ou 2)
        search = False
        start, end = verrous(self.plat, team) #Détection de certaines conditions (nombre de pion nécessaire et bords atteints)

        if start is not False: #Vérification des conditions nécessaires
            search = detection_victoire(self.plat, slot, team, start, end) #Fonction de propagation à travers les pions d'une même couleur détectant une victoire
            
            if search is not False: #Si victoire détectée
                self.victoire() #Lancement de la procédure de victoire
                fin_partie(team, search, self.partie1, self.width) #Lancement de la fin de partie

    def victoire(self): #fonction arrêtant la partie
        self.pausef()
        self.fe.unbind("<space>") #Empêchement de l'intéraction de la barre espace
        
        self.frame1.config(bg="black")
        self.frame2.config(bg="black")
        
        #self.save1 [0].config (self.save1 [1].entryconfig ("Enregistrer sur A", state = "disabled"))
        #self.save2 [0].config (self.save2 [1].entryconfig ("Enregistrer sur B", state = "disabled"))
        #self.save3 [0].config (self.save3 [1].entryconfig ("Enregistrer sur C", state = "disabled"))

        if len(self.ordre) > 1:
            self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="",outline='black', width=3)

        self.playbutton.config(state="disabled")
        self.playbutton.grid_forget()
        
        if self.tour % 2 == 0: #Victoire Bleu
            print("Victoire Bleu") 
            self.partie1.itemconfigure("vict", text="Victoire Bleu") #Affichage de la victoire Bleu
        else:
            print("Victoire Rouge")
            self.partie1.itemconfigure("vict", text="Victoire Rouge") #Affichage de la victoire Rouge

        # show_distance(team, search)

    def game_action(self, tag, slot): #Fonction d'affichage de la pose des pions

        if len(self.ordre) != 0:
            self.partie1.itemconfig(str(self.ordre[-1][0]) + "," + str(self.ordre[-1][1]), dash="", outline='black', width=3)

        team = ((self.tour) % 2) + 1 #Récupération du joueur

        self.partie1.tag_raise(tag)
        self.ordre.append((slot[0], slot[1])) #Apprentissage du nouveau pion posé

        if team == 1: #Tour du joueur 1 
            self.partie1.itemconfig(tag, fill='red', dash=(3, 3, 3, 3), outline=rgb_convert((255,255,180)), activefill="", width=2) #Coloration de la case en rouge (avec bordure pour montrer le dernier coups)
            print("Tour", self.tour, ': Rouge (1)')
            self.frame2.config(bg=rgb_convert((255,230,0)))
            self.frame1.config(bg="black")
            self.temps[1] = 60000 - self.temps[0] - self.temps[2] #Reprise du temps pour le joueur 2
        else:
            self.partie1.itemconfig(tag, fill=rgb_convert((0,110,255)), dash=(3, 3, 3, 3),outline=rgb_convert((255,255,180)), activefill="", width=2) #Coloration de la case en bleu (avec bordure pour montrer le dernier coups)
            print("Tour", self.tour, ": Bleu (2)")
            self.frame1.config(bg=rgb_convert((255,230,0)))
            self.frame2.config(bg="black")
            self.temps[2] = 60000 - self.temps[0] - self.temps[1] #Reprise du temps pour le joueur 1

        self.plat[slot[0]][slot[1]] = team #Actualisation de la matrice
        print(self.plat)
        self.tour += 1 #Tour suivant

    def nexts(self):

        team = ((self.tour) % 2) + 1 #Récupération du Joueur

        if self.players[self.tour % 2] is True and self.game_status is True:
            slot = self.bot[self.tour % 2](self.plat, team, self.assis[self.tour % 2])
            tag = str(slot[0]) + ',' + str(slot[1])
            self.game_action(tag, slot)
            self.test_victoire(slot)

            if self.players[self.tour % 2] is True:
                if self.timed is True: #Si les chronomètres individuels sont demandés
                    if self.botcooldown < 1:
                        self.sleep_time = int((1000* self.botcooldown)-50)
                self.fe.update()
                sleep(self.botcooldown)
                self.nexts()
                
    def taille_fenetre (self, choix): #Fonction pour augmenter ou réduire la taille de la fenêtre
        if choix == True: #Type du bouton (ici, réduction)
            self.width -= 100 #Modification de variable
        else:
            self.width += 100 #Modification de variable
                              
        self.height = round(self.width * 0.618) #Modification de variable
        self.fe.destroy () #Destruction de l'ancienne fenêtre
        self.fe, self.frame = structure_tkinter(self.width, self.height) #Recréation  avec les nouvelles valeurs
        self.fe.bind("<f>", self.plein_ecran) #Intéraction sur la touche F, lançant le plein écran de la fenêtre
        self.fe.bind("<KeyPress-F11>", self.plein_ecran) #Intéraction sur la touche F11, lançant le plein écran de la fenêtre
        self.ecran_accueil() #Affichage des boutons de l'écran d'accueil

    def actual_time(self): #
        temps=[round(default_timer()*100) - self.temps[3], self.temps[1], self.temps[2], self.temps[3], self.temps[4], self.temps[5], self.temps[6]] #Initialisation du temps pour tous les chronos
        if self.timed is True: #Chronomètres individuels
            if self.tour % 2 == 0: #Tour du joueur 1
                a, n = 1, 2 #initialisation de variable pour les chronos
            else: #Tour du joueur 2
                a, n = 2, 1 #initialisation de variable pour les chronos
                
            self.temps[a] = 60000 - self.temps[0] - self.temps[n] #Temps du joueur jouant, détecté avec le temps total de la partie (ici 2x5 min = 60000 ms) - le temps global passé - le temps de l'adversaire
        return temps
                

    def update_time(self): #Actualisation du temps
        if self.game_status is True: #Si le jeu n'est pas en pause
            self.temps[0] = round(default_timer()*100) - self.temps[3] #Initialisation du temps actuel

            minutes = int(self.temps[0] / 6000)  # Calcul des minutes
            secondes = int(self.temps[0]/100 - minutes * 60)  # Calcul des secondes
            csecondes = int(self.temps[0] - minutes * 6000 - secondes * 100 )  # Calcul des milli-secondes

            self.temps[4].set("%02d:%02d" % (minutes, secondes)) #Affichage du Chronomètre global

            if self.timed is True: #Si les chronomètres individuels sont demandés
                if self.tour % 2 == 0: #Pour le joueur 1
                    a, n = 1, 2 #initialisation de variable
                else: #Pour le joueur 2
                    a, n = 2, 1 #initialisation de variable
                    
                self.temps[a] = 60000 - self.temps[0] - self.temps[n] #Temps du joueur jouant, détecté avec le temps total de la partie (ici 2x5 min = 60000 ms) - le temps global passé - le temps de l'adversaire
                
                if self.temps[a] <= 0: #Détection de la fin de chronomètre d'un joueur = défaite
                    self.temps[a+4].set("%02d:%02d:%02d" % (0, 0, 0)) #Affichage du temps pour le joueur 
                    self.victoire() #affichage de la victoire
                else:
                    if self.temps[a] > 3000: #Si le temps au-dessous de 30 secondes
                        arrondi = round(self.temps[a]*0.01)*100 #Arrondit pour faciliter les calculs
                    else:
                        arrondi = self.temps[a] #Temps complet pour calculer les milli-secondes
                        self.sleep_time = 80
                        
                    minutes = int(arrondi / 6000)  # Calcul des minutes
                    secondes = int(arrondi/100 - minutes * 60)  # Calcul des secondes
                    csecondes = int(arrondi - minutes * 6000 - secondes * 100 )  # Calcul des milli-secondes
                    
                    if self.temps[a] > 3000: #Si le temps est au-dessous de 30 secondes
                        self.temps[a+4].set("%02d:%02d" % (minutes, secondes)) #Affichage des minutes et des secondes
                    else:
                        self.temps[a+4].set("%02d:%02d:%02d" % (minutes, secondes, csecondes)) #Affichage des minutes / secondes / milli-secondes
                        
        self.fe.after(self.sleep_time, self.update_time) #Relancement de la fonction "update_time" après un temps d'attente


setrecursionlimit(2000)

hex = HEX()

hex.ecran_accueil() #Appel la première fonction, l'affichage de l'accueil

hex.fe.mainloop() #Permet de garder ouvert la fenetre et de la rafraichir