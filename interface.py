from calculs import *
import tkinter as tk
import tkinter.font as tkf
from string import ascii_letters
import numpy as np
from webbrowser import open

#blue : (0,110,255)
#blanc/jaune : (255,255,180)
#rouge : 255 0 0


def affichage_plateau(partie1, plat, size, scale, width, height):
    police = tkf.Font(weight="bold", size=-int(scale / 2))

    for i in range(size):
        for j in range(size):
            x = (width - (scale * ((size - 1) * 3 + 2))) / 2 + (j * scale * 1.5) + (i * scale * 1.5)
            y = (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (0.866 * scale * size) - (
                        j * scale * 0.866) + (i * scale * 0.866)

            if plat[i][j] == 0:
                partie1.create_polygon(x + (0.5 * scale), y, x + (1.5 * scale), y, x + (2 * scale), y + (scale * 0.866),
                                       x + (scale * 1.5), y + (scale * 2 * 0.866), x + (scale * 0.5), y + (scale * 2 * 0.866), x, y + (scale * 0.866),
                                       fill=rgb_convert((160, 160, 160)), outline='black', width=3, tags=(str(i) + "," + str(j), "cellule"))
            if i == 0:
                partie1.create_text(x, y + 0.2 * scale, font=police, fill=rgb_convert((255,255,180)), text=ascii_letters[j])
            if j == 0:
                partie1.create_text(x, y + 1.5 * scale, font=police, fill=rgb_convert((255,255,180)), text=i + 1)


def refresh_plateau(partie1, frame1, frame2, plat, ordre):

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


def fin_partie(team, search):
    chemin = []
    size = len(search)

    if team == 1:
        depart = min(filter(lambda i: i > 10, search[0]))
        debut = list(np.where((search[0] == depart))[0])
        arrive = min(filter(lambda i: i > 10, search[size-1]))
        fin = list(np.where((search[size-1] == depart))[size-1])

        for i in debut:
            chemin.append((0, i))
        for j in fin:
            chemin.append((size-1,i))
            
    print(chemin)

def show_distance(team, search):
    print(search)
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

    [widget.destroy() for widget in frame.winfo_children()]
    partie1 = tk.Canvas(frame, width=width, height=height, bg=rgb_convert((200, 160, 150)), highlightbackground='red', highlightthickness=0)
    partie1.grid(row=1, column=0, rowspan=15, columnspan=10)

    partie4 = tk.Canvas(frame, width=(width * (0.618 ** 3)), height=(width * (0.618 ** 6)), bg='pink')
    partie4.grid(row=0, column=11)

    partie4.create_text(60, 30, fill='black', text='HexGame.logo')

    frame1 = tk.Frame(partie1, bg='black')
    frame1.place(relx=0.05, rely=0.02, anchor='nw')
    player1 = tk.Label(frame1, bg='red', text="Joueur 1", font=("Arial", int(width*0.03), "bold"), fg=rgb_convert((255,255,180)))
    player1.pack(padx=4, pady=4)
    
    frame2 = tk.Frame(partie1, bg='black')
    frame2.place(relx=0.95, rely=0.02, anchor='ne')
    player2 = tk.Label(frame2, bg=rgb_convert((0,110,255)), text="Joueur 2", font=("Arial", int(width*0.03), "bold"), fg=rgb_convert((255,255,180)))
    player2.pack(padx=4, pady=4)

    str_time = tk.StringVar()
    chron = tk.Label(frame, textvariable=str_time, font=("Arial", int(width*0.05)))
    chron.place(relx=0.01, rely=0.98, anchor=tk.SW)

    if timed is True:
        str_time1 = tk.StringVar()  # Variable de temps
        chron1 = tk.Label(frame, textvariable=str_time1)
        chron1.place(x=50, y=90)

        str_time2 = tk.StringVar()  # Variable de temps
        chron2 = tk.Label(frame, textvariable=str_time2)
        chron2.place(x=850, y=90)
    else:
        str_time1 = False
        str_time2 = False

    return partie1, str_time, str_time1, str_time2, frame1, frame2, chron

def boutons_creations(frame, width):
    restart = tk.Button(frame, text='Nouvelle partie', font=("Arial", int(width*0.02), "bold"))
    restart.grid(row=15, column=11, padx=0, pady=0)

    playbutton = tk.Button(frame, text='Commencer', width=10, bg=rgb_convert((200,255,120)), font=("Arial", int(width*0.02), "bold"))
    playbutton.grid(row=14, column=11, padx=0, pady=0)

    tomenu = tk.Button(frame, text='Menu Principal', font=("Arial", int(width*0.018), "bold"))
    tomenu.grid(row=0, column=0, padx=0, pady=0)

    A = tk.Menubutton(frame, text="Sauvegarde A", font=("Arial", int(width*0.015)))
    B = tk.Menubutton(frame, text="Sauvegarde B", font=("Arial", int(width*0.015)))
    C = tk.Menubutton(frame, text="Sauvegarde C", font=("Arial", int(width*0.015)))

    OA = tk.Menu(A)
    OA.add_command(label="Enregistrer sur A")
    OA.add_command(label="Charger A")
    OA.entryconfig('Charger A', state='disabled')

    OB = tk.Menu(B)
    OB.add_command(label="Enregistrer sur B")
    OB.add_command(label="Charger B")
    OB.entryconfig('Charger B', state='disabled')

    OC = tk.Menu(C)
    OC.add_command(label="Enregistrer sur C")
    OC.add_command(label="Charger C")
    OC.entryconfig('Charger C', state='disabled')

    A["menu"] = OA
    B["menu"] = OB
    C["menu"] = OC

    A.grid(row=0, column=4, padx=0, pady=0)
    B.grid(row=0, column=6, padx=0, pady=0)
    C.grid(row=0, column=8, padx=0, pady=0)

    return (A, OA), (B, OB), (C, OC), restart, playbutton, tomenu

def affichage_accueil(fe, frame, width):
    [widget.destroy() for widget in frame.winfo_children()]
    
    HEXlogo = tk.Label (frame)
    HEXlogo.place(relx = 0.5, rely = 0.2, anchor ='center')
    
    play = tk.Button(frame, text='Jouer', font=("Arial", int(width*0.03), "bold"))
    play.place(width=width*0.5, relx = 0.5, rely = 0.35, anchor ='center')
    
    shortcut = tk.Button(frame, text='Shortcut')
    shortcut.place(relx = 0.5, rely = 0.9, anchor ='center')
        
    parties = tk.Button(frame, text='Charger une Partie ?', font=("Arial", int(width*0.03), "bold"), command = lambda: [Save1.place(relx = 0.37, rely = 0.61, anchor ='center'),
                                                                                             Save2.place (relx = 0.5, rely = 0.61, anchor ='center'),
                                                                                             Save3.place (relx = 0.63, rely = 0.61, anchor ='center'),
                                                                                             Regle.place (rely = 0.73)])
    parties.place(width=width*0.5, relx = 0.5, rely = 0.5, anchor ='center')
    
    Save1 = tk.Button(frame, text='Sauvegarde A', font=("Arial", int(width*0.015)))
    Save1.place_forget()
    Save2 = tk.Button(frame, text='Sauvegarde B', font=("Arial", int(width*0.015)))
    Save2.place_forget()
    Save3 = tk.Button(frame, text='Sauvegarde C', font=("Arial", int(width*0.015)))
    Save3.place_forget()
        
    #Ajout Base de donnée et rendre inactif les boutons n'ayant pas d'enregistrement
    Regle = tk.Button(frame, text='Règles', font=("Arial", int(width*0.03), "bold"), command=lambda: open('https://github.com/EvanTrvs/Jeu_de_Hex/blob/main/Regles.md'))
    Regle.place(width=width*0.5, relx = 0.5, rely = 0.65, anchor ='center')
    note = tk.Label(frame, bg='gray', text='Jeu de Hex  -  Projet PeiP 2022  -  Evan & Thibaud', font=("",int(width*0.01), "italic"))
    note.place(width=round(width + (width * (0.618 ** 3))), relx=0, rely=1, anchor="sw")
    
    return shortcut, play
    
def affichage_parametres(fe, frame, width):
    [widget.destroy() for widget in frame.winfo_children()]
    #frame.grid_propagate (False)
    
    choix1 = tk.BooleanVar ()
    choix2 = tk.BooleanVar ()
    
    #bg = rgb_convert((100, 80, 70))
    option = tk.Frame (frame, bg = 'red')
    option.place(relx = 0.5, rely = 0.5, width = 500, height = 500, anchor = 'center')
    
    menuprincipal = tk.Button(frame, text='Menu Principal', font=("Arial", int(width*0.018), "bold"))
    menuprincipal.place (relx = 0.018, rely = 0.003, anchor = 'nw')
    
    
    titre = tk.Label (option, text = 'Paramètres', borderwidth  = 3)
    titre.place (relx = 0.5, rely = 0.1, width = 100, height = 50, anchor = 'center')

    J1 = tk.Label (option, text = "Joueur 1")
    J1.place (relx = 0.2, rely = 0.3, width = 100, height = 20, anchor = 'center')
    
    R = tk.Label (option, text = "Rouge").place (relx = 0.2, rely = 0.35, width = 50, height = 20, anchor = 'center')
    
    Joueur1 = tk.Radiobutton (option, text = 'Joueur 1', variable = choix1, value = False, command = lambda: [bot1.place_forget (), botA1.place_forget (), botB1.place_forget (), cd1.place_forget ()])
    BOT1 = tk.Radiobutton (option, text = 'BOT 1', variable = choix1, value = True, command = lambda: [bot1.place (relx = 0.2, rely = 0.8, width = 60, height = 20, anchor = 'center'),
                                                                                                        botA1.place (relx = 0.05, rely = 0.85, anchor = 'w'),
                                                                                                        botB1.place (relx = 0.25, rely = 0.85, anchor = 'w'),
                                                                                                        cd1.place (relx = 0.20, rely = 0.90, anchor = 'center')])
    Joueur1.place (relx = 0.15, rely = 0.4, anchor = 'w')
    BOT1.place (relx = 0.15, rely = 0.47, anchor = 'w')
    
    J2 = tk.Label (option, text = "Joueur 2")
    J2.place (relx = 0.8, rely = 0.3, width = 100, height = 20, anchor = 'center')
    
    B = tk.Label (option, text="Bleu").place (relx = 0.8, rely = 0.35, width = 50, height = 20, anchor = 'center')
    
    Joueur2 = tk.Radiobutton (option, text = 'Joueur 2', variable = choix2, value = False, command = lambda: [bot2.place_forget (), botA2.place_forget (), botB2.place_forget (), cd2.place_forget ()])
    BOT2 = tk.Radiobutton (option, text = 'BOT 2', variable = choix2, value = True, command = lambda: [bot2.place (relx = 0.8, rely = 0.8, width = 60, height = 20, anchor = 'center'),
                                                                                                        botA2.place (relx = 0.65, rely = 0.85, anchor = 'w'),
                                                                                                        botB2.place (relx = 0.85, rely = 0.85, anchor = 'w'),
                                                                                                        cd2.place (relx = 0.80, rely = 0.90, anchor = 'center')])
    Joueur2.place (relx = 0.75, rely = 0.4, anchor = 'w')
    BOT2.place (relx = 0.75, rely = 0.47, anchor = 'w')
    
    taille = tk.Scale(option, orient ='horizontal', from_= 7, to = 13, resolution = 1, tickinterval = 1, length=250)
    taille.set (11)
    taille.place (relx = 0.5, rely = 0.6, anchor = 'center')
    
    taillem = tk.Button (option, text = '-', command = lambda: [taille.config (from_ = 4, to = 11, tickinterval = 1, resolution = 1), taille.set (7),
                                                                taillem.place_forget (), taillep.place_forget (), taillemoyenp.place (relx = 0.8, rely = 0.6, anchor = 'center')])
    taillem.place (relx = 0.2, rely = 0.6, anchor = 'center')
    
    taillemoyenp = tk.Button (option, text = '+', command = lambda: [taille.config (from_ = 7, to = 13, tickinterval = 1, resolution = 1), taille.set (11), taillemoyenp.place_forget (),
                                                                     taillem.place (relx = 0.2, rely = 0.6, anchor = 'center'), taillep.place (relx = 0.8, rely = 0.6, anchor = 'center')])
    
    taillemoyenm = tk.Button (option, text = '-', command = lambda: [taille.config (from_ = 7, to = 13, tickinterval = 1, resolution = 1), taille.set (11), taillemoyenm.place_forget (),
                                                                     taillem.place (relx = 0.2, rely = 0.6, anchor = 'center'), taillep.place (relx = 0.8, rely = 0.6, anchor = 'center')])
    
    taillep = tk.Button (option, text = '+', command = lambda: [taille.config (from_ = 11, to = 52, tickinterval = 5, resolution = 1), taille.set (22), 
                                                                taillep.place_forget (), taillem.place_forget (), taillemoyenm.place (relx = 0.2, rely = 0.6, anchor = 'center')])
    taillep.place (relx = 0.8, rely = 0.6, anchor = 'center')
    
    timevar = tk.BooleanVar()
    
    time = tk.Checkbutton (option, text = 'Chrono ?', variable = timevar)
    time.place (relx = 0.5, rely = 0.7, anchor = 'center')
    
    choixb1 = tk.BooleanVar ()
    choixb2 = tk.BooleanVar ()

    bot1 = tk.Label (option, text = 'Quel BOT ?')
    botA1 = tk.Radiobutton (option, text = 'BOT 1', variable = choixb1, value = True)
    botB1 = tk.Radiobutton (option, text = 'BOT 2', variable = choixb1, value = False)
    
    
    bot2 = tk.Label (option, text = 'Quel BOT ?')
    botA2 = tk.Radiobutton (option, text = 'BOT 1', variable = choixb2, value = True)
    botB2 = tk.Radiobutton (option, text = 'BOT 2', variable = choixb2, value = False)
    
    cd1 = tk.Spinbox (option, from_= 0, to= 5, increment=0.1,  width = 10)
    
    cd2 = tk.Spinbox (option, from_= 0, to= 5, increment=0.1,  width = 10)
    
    ready = tk.Button (option, text = 'Ready', command = lambda: [print (choix1.get (), choix2.get (), timevar.get (), cd1.get (), cd2.get (), taille.get ())])
    ready.place (relx = 0.5, rely = 0.9, anchor = 'center')
    
    return menuprincipal


def background(partie1, scale, width, height, size):
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
