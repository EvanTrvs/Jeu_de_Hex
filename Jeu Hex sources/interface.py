from calculs import *
import tkinter as tk
import tkinter.font as tkf
from string import ascii_letters
import numpy as np
from webbrowser import open
from PIL import Image, ImageTk
from tkinter import ttk

#bleu : (0,110,255)
#blanc/jaune : (255,255,180)
#rouge : (255,0,0)


def affichage_plateau(partie1, plat, size, scale, width, height):
    #Permet d'afficher le plateau vide (taille et proportion des cases du plateau)
    
    police = tkf.Font(weight="bold", size=-int(scale / 2))

    for i in range(size):
        for j in range(size):
            x = (width - (scale * ((size - 1) * 3 + 2))) / 2 + (j * scale * 1.5) + (i * scale * 1.5)
            y = (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (0.866 * scale * size) - (j * scale * 0.866) + (i * scale * 0.866)

            partie1.create_polygon(x + (0.5 * scale), y, x + (1.5 * scale), y, x + (2 * scale), y + (scale * 0.866),
                                   x + (scale * 1.5), y + (scale * 2 * 0.866), x + (scale * 0.5), y + (scale * 2 * 0.866), x, y + (scale * 0.866),
                                   fill=rgb_convert((160, 160, 160)), outline='black', width=3, tags=(str(i) + "," + str(j), "cellule"))
            if i == 0:
                partie1.create_text(x, y + 0.2 * scale, font=police, fill=rgb_convert((255,255,180)), text=ascii_letters[j])
            if j == 0:
                partie1.create_text(x, y + 1.5 * scale, font=police, fill=rgb_convert((255,255,180)), text=i + 1)


def refresh_plateau(partie1, frame1, frame2, plat, ordre):
    #Permet d'afficher les pions sur le plateau ainsi que la distinction pour le joueur devant jouer

    if len(ordre) == 0:
        frame1.config(bg="black")
        frame2.config(bg="black")
        
    elif len(ordre) % 2 == 0:
        frame1.config(bg=rgb_convert((255,230,0)))
        frame2.config(bg="black")
    else:
        frame2.config(bg=rgb_convert((255,230,0)))
        frame1.config(bg="black")

    for i in range(len(plat)):
        for j in range(len(plat)):
            tag = str(i) + ',' + str(j)

            if plat[i][j] == 0:
                partie1.itemconfig(tag, fill=rgb_convert((160, 160, 160)), activefill=rgb_convert((180, 180, 180)), dash="", outline='black', width=3)
            elif plat[i][j] == 1:
                partie1.itemconfig(tag, fill="red", activefill='', dash="", outline='black', width=3)
            elif plat[i][j] == 2:
                partie1.itemconfig(tag, fill=rgb_convert((0,110,255)), activefill='', dash="", outline='black', width=3)


def fin_partie(team, search, partie1, width):
    #Permet de détecter une victoire d'un des 2 joueurs
    
    chemin = []
    size = len(search)

    if team == 1:
        minup = min(filter(lambda i: i >= 10, search[0])) 
        start = [(0, k) for k, i in enumerate(search[0]) if i == minup]
        
        mindown = min(filter(lambda i: i >= 10, search[size-1])) 
        end = [(size-1, k) for k, i in enumerate(search[size - 1]) if i == mindown]
    else:
        minup = min(filter(lambda i: i >= 10, search[:, 0])) 
        start = [(k, 0) for k, i in enumerate(search[:, 0]) if i == minup]
        
        mindown = min(filter(lambda i: i >= 10, search[:, size - 1])) 
        end = [(k, size-1) for k, i in enumerate(search[:, size - 1]) if i == mindown]
        
    for slot in start+end:
        chemin.append(slot)
        
        while search[slot[0]][slot[1]] != 10:
            slot = chemin[-1]
            distance = search[slot[0]][slot[1]]-1

            if slot[0] + 1 <= len(search) - 1:
                if search[slot[0] + 1][slot[1]] == distance:
                    chemin.append((slot[0] + 1,slot[1]))
            if slot[0] + 1 <= len(search) - 1 and slot[1] - 1 >= 0:
                if search[slot[0] + 1][slot[1] - 1] == distance:
                    chemin.append((slot[0] + 1,slot[1] - 1))
            if slot[1] - 1 >= 0:
                if search[slot[0]][slot[1] - 1] == distance:
                    chemin.append((slot[0],slot[1] - 1))
            if slot[1] + 1 <= len(search) - 1:
                if search[slot[0]][slot[1] + 1] == distance:
                    chemin.append((slot[0],slot[1] + 1))
            if slot[0] - 1 >= 0 and slot[1] + 1 <= len(search) - 1:
                if search[slot[0] - 1][slot[1] + 1] == distance:
                    chemin.append((slot[0] - 1,slot[1] + 1))
            if slot[0] - 1 >= 0:
                if search[slot[0] - 1][slot[1]] == distance:
                    chemin.append((slot[0] - 1,slot[1]))
   
    for i in list(set(chemin)):
        tag = str(i[0]) + ',' + str(i[1])
        partie1.itemconfig(tag, fill=rgb_convert((100,255,100)), activefill='', dash="", outline='black', width=3)

def show_distance(team, search):
    #Dégrader de couleurs sur un chemin
    r = 220 / (max(search) - 10)

    for i in range(len(plat)):
        for j in range(len(plat)):

            if search[i][j] >= 10:
                tag = str(i) + ',' + str(j)
                if team == 1:
                    partie1.itemconfig(tag, fill=rgb_convert((255 - int((search[i][j] - 10) * r), 0, 0)))
                else:
                    partie1.itemconfig(tag, fill=rgb_convert((0, 0, 255 - int((search[i][j] - 10) * r))))

def structure_tkinter(width, height):
    #Pemet de structurer la fenêtre Tkinter (Fenêtre principale et Cadre principal)
    
    fe = tk.Tk()
    fe.title('HexGame')
    fe.config(bg=rgb_convert((50, 50, 50)))
    
    xu = round(width + (width * (0.618 ** 3)))
    yu = round(height + (width * (0.618 ** 6)))

    fe.geometry(str(xu) + 'x' + str(yu) + '+' + str(10) + '+' + str(20))

    frame = tk.Frame(fe, width=xu, height=yu, bg=rgb_convert((100, 80, 70)))
    frame.place(relx=0.5, rely=0.5, anchor="center")
    return fe, frame

def fenetre_jeu(fe, frame, width, height, timed):
    #Permet de structurer et d'afficher l'écran de jeu (plateau, chronomètre, logo)

    [widget.destroy() for widget in frame.winfo_children()]
    partie1 = tk.Canvas(frame, width=width, height=height, bg=rgb_convert((200, 160, 150)), highlightbackground='red', highlightthickness=0)
    partie1.grid(row=1, column=0, rowspan=15, columnspan=10)

    partie4 = tk.Canvas(frame, width=(width * (0.618 ** 3))-6, height=(width * (0.618 ** 6))-3, highlightthickness=3, bg=rgb_convert((180,180,255)), highlightbackground='black')
    partie4.grid(row=0, column=11)
    
    img = np.array([80,100,125,150,175,200,225,250,300,400,500,600])
    res = np.absolute(img-round(width*0.225))
    index=res.argmin()
    
    image = Image.open ("graphismes\\lpx\\" + str(img[index]) + "lpx.png")
    photo = ImageTk.PhotoImage (image, fe)

    HEXlogo = tk.Button (partie4, image = photo, bg=rgb_convert((180,180,255)), borderwidth = 0)
    HEXlogo.image = photo 
    HEXlogo.place(relx = 0.5, rely = 0.5, anchor ='center')
    
    if timed is True:
        str_time1 = tk.StringVar()  # Variable de temps
        chron1 = tk.Label(partie1, textvariable=str_time1, font=("Arial", int(width*0.02)), bg='red', fg=rgb_convert((255,255,180)), relief="solid")
        chron1.place(relx=0.05, rely=0.126)

        str_time2 = tk.StringVar()  # Variable de temps
        chron2 = tk.Label(partie1, textvariable=str_time2, font=("Arial", int(width*0.02)), bg=rgb_convert((0,110,255)), fg=rgb_convert((255,255,180)), relief="solid")
        chron2.place(relx=0.95, rely=0.126, anchor="ne")
    else:
        str_time1 = False
        str_time2 = False

    frame1 = tk.Frame(partie1, bg='black')
    frame1.place(relx=0.05, rely=0.13, anchor='sw')
    player1 = tk.Label(frame1, bg='red', text="Joueur 1", highlightthickness=int(width*0.001), font=("Arial", int(width*0.03), "bold"), fg=rgb_convert((255,255,180)))
    player1.pack(padx=4, pady=4)
    
    frame2 = tk.Frame(partie1, bg='black')
    frame2.place(relx=0.95, rely=0.13, anchor='se')
    player2 = tk.Label(frame2, bg=rgb_convert((0,110,255)), highlightthickness=int(width*0.001), text="Joueur 2", font=("Arial", int(width*0.03), "bold"), fg=rgb_convert((255,255,180)))
    player2.pack(padx=4, pady=4)

    str_time = tk.StringVar()
    chron = tk.Label(frame, bg=rgb_convert((200, 160, 150)), textvariable=str_time, font=("Arial", int(width*0.05)))
    chron.place(relx=0, rely=1, anchor=tk.SW)
    
    partie1.create_text(width, width*0.618, anchor="se", fill="black" , font=("Arial", int(width*0.04)), tag="vict")

    return partie1, str_time, str_time1, str_time2, frame1, frame2, chron

def boutons_creations(frame, width):
    #Permet la création des Menu déroulant pour les enregistrements à côter du plateau de jeu
    
    restart = tk.Button(frame, text='Nouvelle partie', font=("Arial", int(width*0.02), "bold"))
    restart.grid(row=15, column=11, padx=0, pady=0)

    playbutton = tk.Button(frame, text='Commencer', width=10, bg=rgb_convert((200,255,120)), font=("Arial", int(width*0.02), "bold"))
    playbutton.grid(row=14, column=11, padx=0, pady=0)

    tomenu = tk.Button(frame, text='', font=("Arial", int(width*0.022)))
    tomenu.grid(row=0, column=0, padx=0, pady=0)

    A = tk.Menubutton(frame, text="                               Evan & Thibaud 2021/22", font=("Arial", int(width*0.015)), state='disabled')
    B = tk.Menubutton(frame, text="", font=("Arial", int(width*0.015)), state='disabled')
    C = tk.Menubutton(frame, text="", font=("Arial", int(width*0.015)), state='disabled')

    OA = tk.Menu(A, tearoff=0)
    OA.add_command(label="", font=("Arial", int(width*0.01)))
    OA.add_command(label="", font=("Arial", int(width*0.01)))
    OA.entryconfig('', state='disabled')

    OB = tk.Menu(B, tearoff=0)
    OB.add_command(label="", font=("Arial", int(width*0.01)))
    OB.add_command(label="", font=("Arial", int(width*0.01)))
    OB.entryconfig('', state='disabled')

    OC = tk.Menu(C, tearoff=0)
    OC.add_command(label="",font=("Arial", int(width*0.01)))
    OC.add_command(label="", font=("Arial", int(width*0.01)))
    OC.entryconfig('', state='disabled')

    A["menu"] = OA
    B["menu"] = OB
    C["menu"] = OC

    A.grid(row=0, column=4, padx=0, pady=0)
    B.grid(row=0, column=6, padx=0, pady=0)
    C.grid(row=0, column=8, padx=0, pady=0)

    return (A, OA), (B, OB), (C, OC), restart, playbutton, tomenu

def affichage_accueil(fe, frame, width):
    #Permet l'organisation et l'affichage de l'écran d'accueil (logo, boutons d'enregistrements, boutons de jeu)
    
    [widget.destroy() for widget in frame.winfo_children()]
    
    truc = tk.Label(frame, text="10")
    truc.place(relx = 0.5, rely = 0.2, anchor ='center')
    
    img = np.array([150,200,250,275,300,320,350,400,450,500,600])
    res = np.absolute(img-round(width*0.32))
    index=res.argmin()
    
    image = Image.open ("graphismes\\px\\" + str(img[index]) + "px.png")
    photo = ImageTk.PhotoImage (image, fe)

    HEXlogo = tk.Label(frame, borderwidth = 3, highlightthickness=int(width*0.01), relief="solid", bg=rgb_convert((180,180,255)), image = photo)
    HEXlogo.image = photo 
    HEXlogo.place(relx = 0.5, rely = 0.17, anchor ='center')
    HEXlogo.config(padx=500)
    
    play = tk.Button(frame, text='Joueur vs Joueur', font=("Arial", int(width*0.03), "bold"))
    play.place(width=width*0.5, relx = 0.5, rely = 0.4, anchor ='center')
        
    parties = tk.Button(frame, text='Joueur vs Ordinateur', font=("Arial", int(width*0.03), "bold"))
    parties.place(width=width*0.5, relx = 0.5, rely = 0.55, anchor ='center')
    
    Save1 = tk.Button(frame, text='Sauvegarde A', font=("Arial", int(width*0.015)))
    Save1.place_forget()
    Save2 = tk.Button(frame, text='Sauvegarde B', font=("Arial", int(width*0.015)))
    Save2.place_forget()
    Save3 = tk.Button(frame, text='Sauvegarde C', font=("Arial", int(width*0.015)))
    Save3.place_forget()
        
    #Ajout Base de donnée et rendre inactif les boutons n'ayant pas d'enregistrement
    Regle = tk.Button(frame, text='Ordinateur vs Ordinateur', font=("Arial", int(width*0.03), "bold"))
    Regle.place(width=width*0.5, relx = 0.5, rely = 0.7, anchor ='center')
    note = tk.Label(frame, bg='gray', text='Interface pour le Jeu de Hex    -    Projet PeiP 2022    -    Evan & Thibaud', font=("",int(width*0.01), "italic"))
    note.place(width=round(width + (width * (0.618 ** 3))), relx=0, rely=1, anchor="sw")
    
    shortcut = tk.Button(frame, text='default', borderwidth=0, bg=rgb_convert((100, 80, 70)), fg=rgb_convert((90,70,60)))
    shortcut.place(relx = 1, rely = 0.96, anchor ='se')
    
    def bas ():
        Save1.place(relx = 0.37, rely = 0.66, anchor ='center')
        Save2.place (relx = 0.5, rely = 0.66, anchor ='center')
        Save3.place (relx = 0.63, rely = 0.66, anchor ='center')
        Regle.place (rely = 0.78),
        parties.config (command = haut)

    def haut ():
        Save1.place_forget ()
        Save2.place_forget ()
        Save3.place_forget ()
        Regle.place(width=width*0.5, relx = 0.5, rely = 0.7, anchor ='center')
        parties.config (command = bas)
    
    boutonp = tk.Button (frame, text = "+", font=("Arial", int(width*0.03)), bg=rgb_convert((50, 30, 20)), fg=rgb_convert((200,200,200)))
    boutonp.place (relx = 1, rely = 0.038, anchor ='se', width=int(width*0.025), height=int(width*0.025))

    boutonm = tk.Button (frame, text = "-", font=("Arial", int(width*0.03)), bg=rgb_convert((50, 30, 20)), fg=rgb_convert((200,200,200)))
    boutonm.place (relx = 1, rely = 0.038, anchor ='ne', width=int(width*0.025), height=int(width*0.025))
    
    fulls = tk.Button (frame, text = "↔", font=("Arial", int(width*0.02)), bg=rgb_convert((50, 30, 20)), fg=rgb_convert((200,200,200)))
    fulls.place (relx = 1, rely = 0.075, anchor ='ne', width=int(width*0.025), height=int(width*0.025))
    
    return shortcut, play, parties, Regle, Save3, boutonp, boutonm, fulls

def affichage_parametres(fe, frame, width):
    #Permet l'organisation et l'affichage des paramètres de jeu avant le lancement d'une partie
    
    [widget.destroy() for widget in frame.winfo_children()]
    
    def cooldown_test():
        if choix2.get()==True and choix1.get()==True:
            cd1.place(relx=0.35, rely=0.84, anchor="n")
            cd2.place(relx=0.35, rely=0.84, anchor="s")
            
    partie4 = tk.Canvas(frame, width=(width * (0.618 ** 3))-6, height=(width * (0.618 ** 6))-3, highlightthickness=3, bg=rgb_convert((180,180,255)), highlightbackground='black')
    partie4.place(relx=1, rely=0, anchor="ne")
    
    img = np.array([80,100,125,150,175,200,225,250,300,400,500,600])
    res = np.absolute(img-round(width*0.225))
    index=res.argmin()
    
    image = Image.open ("graphismes\\lpx\\" + str(img[index]) + "lpx.png")
    photo = ImageTk.PhotoImage (image, fe)

    HEXlogo = tk.Button (partie4, image = photo, bg=rgb_convert((180,180,255)), borderwidth = 0)
    HEXlogo.image = photo 
    HEXlogo.place(relx = 0.5, rely = 0.5, anchor ='center')
    
    choix1 = tk.BooleanVar ()
    choix2 = tk.BooleanVar ()
    
    option = tk.Frame (frame, bg ='gray')
    option.place(relx = 0.5, rely = 0.5, width = width, height = round(width * 0.618)*0.9, anchor = 'center')
    
    menuprincipal = tk.Button(frame, text='Menu Principal', font=("Arial", int(width*0.018), "bold"))
    menuprincipal.place (relx = 0.018, rely = 0.003, anchor = 'nw')
    
    titre = tk.Label (option, text = 'Paramètres', borderwidth = 3, bg=rgb_convert((200,200,200)) , font=("Arial", int(width*0.035), "bold"))
    titre.place (relx = 0.5, rely = 0.05, anchor = 'center')

    frame1 = tk.Frame(option, bg='black')
    frame1.place(relx=0.2, rely=0.2, anchor='center')
    player1 = tk.Label(frame1, bg='red', text="Joueur 1", font=("Arial", int(width*0.03), "bold"), fg=rgb_convert((255,255,180)))
    player1.pack(padx=4, pady=4)
    
    frame2 = tk.Frame(option, bg='black')
    frame2.place(relx=0.5, rely=0.2, anchor='center')
    player2 = tk.Label(frame2, bg=rgb_convert((0,110,255)), text="Joueur 2", font=("Arial", int(width*0.03), "bold"), fg=rgb_convert((255,255,180)))
    player2.pack(padx=4, pady=4)
    
    Joueur1 = tk.Radiobutton (option, text = 'Utilisateur', font=("Arial", int(width*0.015)), width=9, variable = choix1, value = False, command = lambda: [bot1.place_forget (), botA1.place_forget (), botB1.place_forget (), bota1.place_forget(), cd1.place_forget (), cd2.place_forget ()])
    BOT1 = tk.Radiobutton (option, text = 'Ordinateur', font=("Arial", int(width*0.015)), width=9, variable = choix1, value=True, command = lambda: [bot1.place (relx = 0.2, rely = 0.5, anchor = 'center'),
                                                                                                        botA1.place (relx = 0.08, rely = 0.57, anchor = 'w'),
                                                                                                        botB1.place (relx = 0.08, rely = 0.64, anchor = 'w'),botA1.select(),
                                                                                                        bota1.place(relx = 0.08, rely = 0.75, anchor = 'w'), cooldown_test()])
    Joueur1.place (relx = 0.2, rely = 0.32, anchor = 'center')
    BOT1.place (relx = 0.2, rely = 0.39, anchor = 'center')
    
    Joueur2 = tk.Radiobutton (option, text = 'Utilisateur', font=("Arial", int(width*0.015)), width=9, variable = choix2, value = False, command = lambda: [bot2.place_forget (), botA2.place_forget (), botB2.place_forget (), bota2.place_forget(), cd1.place_forget (), cd2.place_forget ()])
    BOT2 = tk.Radiobutton (option, text = 'Ordinateur', font=("Arial", int(width*0.015)), width=9, variable = choix2, value = True, command = lambda: [bot2.place (relx = 0.5, rely = 0.5, anchor = 'center'),
                                                                                                        botA2.place (relx = 0.38, rely = 0.57, anchor = 'w'), botA2.select(),
                                                                                                        botB2.place (relx = 0.38, rely = 0.64, anchor = 'w'),
                                                                                                        bota2.place(relx=0.38, rely=0.75, anchor = "w"), cooldown_test()])
    Joueur2.place (relx = 0.5, rely = 0.32, anchor = 'center')
    BOT2.place (relx = 0.5, rely = 0.39, anchor = 'center')
    
    def print_selection(v):
        strvar.set(taille.get())

    taille = tk.Scale(option, orient ='vertical', from_= 7, to = 13, resolution = 1, tickinterval = 1, length=width*0.22,  width=int(width*0.022), font=("Arial", int(width*0.015)), showvalue=0, relief="solid", command=print_selection)
    taille.set (11)
    taille.place (relx = 0.8, rely = 0.3, anchor = 'n')
    
    l1 = tk.Label(option, relief="solid", text = "Taille de plateau :", font =("Courier", int(width*0.02)))
    l1.place(relx = 0.8, rely = 0.2, anchor='center')
    
    strvar = tk.StringVar()
    strvar.set(11)
    taillev = tk.Label(option, textvariable=strvar, font=("Arial", int(width*0.02), "bold"))
    taillev.place(relx=0.72, rely=0.35, anchor="center")
    
    taillem = tk.Button (option, text="^", compound=tk.TOP, font=("Arial", int(width*0.02)), command = lambda: [taille.config (from_ = 4, to = 11, tickinterval = 1, resolution = 1), taille.set (11),
                                                                                                                                                         taillem.place_forget (), taillep.place_forget (), taillemoyenp.place (relx = 0.8, rely = 0.71, anchor = 'n', width=int(width*0.023), height=int(width*0.025))])
    taillem.place (relx = 0.8, rely = 0.3, anchor = 's', width=int(width*0.023), height=int(width*0.025))
    
    taillemoyenp = tk.Button (option, text="v", compound=tk.TOP, font=("Arial", int(width*0.017)), command = lambda: [taille.config (from_ = 7, to = 13, tickinterval = 1, resolution = 1), taille.set (11), taillemoyenp.place_forget (),
                                                                     taillem.place (relx = 0.8, rely = 0.3, anchor = 's', width=int(width*0.023), height=int(width*0.025)), taillep.place (relx = 0.8, rely = 0.71, anchor = 'n', width=int(width*0.023), height=int(width*0.025))])
    
    taillemoyenm = tk.Button (option, text="^", compound=tk.TOP, font=("Arial", int(width*0.02)), command = lambda: [taille.config (from_ = 7, to = 13, tickinterval = 1, resolution = 1), taille.set (11), taillemoyenm.place_forget (),
                                                                     taillem.place (relx = 0.8, rely = 0.3, anchor = 's', width=int(width*0.023), height=int(width*0.025)), taillep.place (relx = 0.8, rely = 0.71, anchor = 'n', width=int(width*0.023), height=int(width*0.025))])
    
    taillep = tk.Button (option, text="v", compound=tk.TOP, font=("Arial", int(width*0.017)), command = lambda: [taille.config (from_ = 11, to = 52, tickinterval = 5, resolution = 1), taille.set (11), 
                                                                taillep.place_forget (), taillem.place_forget (), taillemoyenm.place (relx = 0.8, rely = 0.3, anchor = 's', width=int(width*0.023), height=int(width*0.025))])
    taillep.place (relx = 0.8, rely = 0.71, anchor = 'n', width=int(width*0.023), height=int(width*0.025))
    
    timevar = tk.BooleanVar()
    
    time = tk.Checkbutton (option, text = "Temps limité", variable = timevar, font=("Arial", int(width*0.018)))
    time.place (relx = 0.8, rely = 0.82, anchor = 'center')
    
    choixb1 = tk.IntVar()
    choixb2 = tk.IntVar()

    bot1 = tk.Label (option, text = "Stratégie de l'Ordinateur 1", font=("Arial", int(width*0.018)))
    botA1 = tk.Radiobutton (option, text = 'Dénombrement', variable = choixb1, value = 1, font=("Arial", int(width*0.015)))
    botB1 = tk.Radiobutton (option, text = 'Pathfinding', variable = choixb1, value = 2, font=("Arial", int(width*0.015)), command= lambda: [taille.config (from_ = 7, to = 13, tickinterval = 1, resolution = 1), taille.set (7)])
    
    assis1 = tk.BooleanVar()
    
    bota1 = tk.Checkbutton(option, text = 'Assistance Logic', variable = assis1, font=("Arial", int(width*0.015)))
    
    
    bot2 = tk.Label (option, text = "Stratégie de l'Ordinateur 2", font=("Arial", int(width*0.018)))
    botA2 = tk.Radiobutton (option, text = 'Dénombrement', variable = choixb2, value = 1, font=("Arial", int(width*0.015)))
    botB2 = tk.Radiobutton (option, text = 'Pathfinding', variable = choixb2, value = 2, font=("Arial", int(width*0.015)), command= lambda: [taille.config (from_ = 7, to = 13, tickinterval = 1, resolution = 1), taille.set (7)])
    
    assis2 = tk.BooleanVar()
    
    bota2 = tk.Checkbutton(option, text = 'Assistance Logic', variable = assis2, font=("Arial", int(width*0.015)))
    
    cd1 = ttk.Spinbox (option, from_= 0.0, to= 5.0, increment=0.1,  width = 17, format="%.1f secondes", justify="center", wrap=True, font=("Arial", int(width*0.013)))
    cd1.insert(0,"0.5 secondes")
    cd2 = tk.Label (option, text = "Délai entre chaque coup", font=("Arial", int(width*0.012)))
    
    ready = tk.Button (option, text = 'Lancer la Partie', bg=rgb_convert((200,255,120)), font=("Arial", int(width*0.03), "bold"), width=width)
    ready.place (relx = 0.5, rely = 1, anchor = 's', height=int(width*0.045))
    
    return menuprincipal, HEXlogo, ready, choix1, choix2, taille, timevar, choixb1, choixb2, assis1, assis2, cd1


def background(partie1, scale, width, height, size):
    #Affichage des bords proportionnés du plateau
    
    partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=0, extent=180, fill="red", outline="black", width=3)

    partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=180, extent=180, fill=rgb_convert((0,110,255)), outline="black", width=3)

    partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 + 0.75),
                   start=90, extent=180, fill="red", outline="black", width=3)

    partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 + 0.75),
                   start=270, extent=180, fill=rgb_convert((0,110,255)), outline="black", width=3)

    partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (2 * size * 0.866 * scale) - (0.866 * scale) + scale * (
                               0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * size * 2 * scale) - (0.866 * scale) + scale * (
                               0.866 + 0.75),
                   start=270, extent=180, fill="red", outline="black", width=3)

    partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (2 * size * 0.866 * scale) - (0.866 * scale) + scale * (
                               0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * size * 2 * scale) - (0.866 * scale) + scale * (
                               0.866 + 0.75),
                   start=90, extent=180, fill=rgb_convert((0,110,255)), outline="black", width=3)

    partie1.create_arc(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 1.25 * scale - scale * 0.5 + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 0.5 * scale + 1.25 * scale + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
    start=0, extent=180, fill=rgb_convert((0,110,255)), outline="black", width=3)

    partie1.create_arc(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 1.25 * scale - scale * 0.5 + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 0.5 * scale + 1.25 * scale + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
    start=180, extent=180, fill="red", outline="black", width=3)

    partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 2 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 + 1.25 * scale * 0.866,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * 0.866 - scale * 0.6494,
                       fill="red", outline="black", width=3)

    partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + scale * 0.625,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 + 1.25 * scale * 0.866,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * 0.866 - scale * 0.6494,
    fill=rgb_convert((0,110,255)), outline="black", width=3)

    partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + 0.625 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size) + scale * (0.6494 + 0.866),
    fill="red", outline="black", width=3)

    partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - scale * 0.866 + 1.948 * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 2 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - 0.866 * scale + 1.948 * scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (
                                   2 * 0.866 * scale * size) + scale * (0.6494 + 0.866),
                       fill=rgb_convert((0,110,255)), outline="black", width=3)

    partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + 0.625 * scale - 4,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale - 2,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 0.866 * scale + 1.948 * scale + 10,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - scale,
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
    fill='red', outline='red', width=6)

    partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) - 30,
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * 0.3746,
    (height - (scale * size * 2 * 0.866)) / 2 - 0.5 * scale + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) + 2,
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size) + scale * (
                0.6494 + 0.866) - 3,
    fill=rgb_convert((0,110,255)), outline=rgb_convert((0,110,255)), width=6)

    partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size),
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (
                                   -0.5 + 0.3746) + 20,
                       (height - (scale * size * 2 * 0.866)) / 2 - 0.5 * scale + (2 * 0.866 * scale * size),
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (
                                   2 * 0.866 * scale * size) + scale * (0.6494 + 0.866) - 4,
                       fill='red', outline='red', width=6)

    partie1.create_polygon(
        (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 0.5 * scale + 0.625 * scale - 4,
        (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale + 2,
        (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - 2 * scale,
        (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale - 10,
        (width - (scale * ((size - 1) * 3 + 2))) / 2 + scale * ((size - 1) * 3 + 2) - scale,
        (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
        fill=rgb_convert((0,110,255)), outline=rgb_convert((0,110,255)), width=6)

    partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625 + 4,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (1.948 - 0.866) * scale + 2,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale + 1.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - (
                                   1.948 - 0.866) * scale - 10,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
                       fill='red', outline='red', width=6)

    partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale - scale * 0.625 + 4,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - 0.866 * scale + 1.948 * scale - 2,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale + 1.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (
                                   0.866 * scale * size) - 0.866 * scale + 1.948 * scale + 10,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + 0.5 * scale,
                       (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size),
                       fill=rgb_convert((0,110,255)), outline=rgb_convert((0,110,255)), width=6)

    partie1.create_polygon(
        (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) - 10,
        (height - (scale * size * 2 * 0.866)) / 2 + scale,
        (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * 0.3746,
        (height - (scale * size * 2 * 0.866)) / 2 + scale,
        (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) + 1,
        (height - (scale * size * 2 * 0.866)) / 2 - scale * 0.6494 + 4,
        fill='red', outline='red', width=6)

    partie1.create_polygon((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5),
                       (height - (scale * size * 2 * 0.866)) / 2 + scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (
                                   -0.5 + 0.3746) + 20, (height - (scale * size * 2 * 0.866)) / 2 + scale,
                       (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) + scale * (-0.5 + 0.3746),
                       (height - (scale * size * 2 * 0.866)) / 2 - scale * 0.6494 + 4,
                       fill=rgb_convert((0,110,255)), outline=rgb_convert((0,110,255)), width=6)
