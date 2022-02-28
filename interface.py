import tkinter as tk
import tkinter.font as tkFont
from string import ascii_letters
from calculs import Rgb_convert,Propagation,Reset_Value
from numpy import zeros


def Plein_ecran(event):
    if fe.attributes()[7] == 0:
        fe.attributes('-fullscreen', True)

    else:
        fe.attributes('-fullscreen', False)


def Affichage_plateau(plat, size, scale):
    for i in range(size):
        for j in range(size):
            x = (width - (scale * ((size - 1) * 3 + 2))) / 2 + (j * scale * 1.5) + (i * scale * 1.5)
            y = (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (0.866 * scale * size) - (
                        j * scale * 0.866) + (i * scale * 0.866)

            if plat[i][j] == 0:
                partie1.create_polygon(x + (0.5 * scale), y, x + (1.5 * scale), y, x + (2 * scale), y + (scale * 0.866),
                                       x + (scale * 1.5), y + (scale * 2 * 0.866),
                                       x + (scale * 0.5), y + (scale * 2 * 0.866), x, y + (scale * 0.866),
                                       fill=Rgb_convert((160, 160, 160)), activefill=Rgb_convert((180, 180, 180)),
                                       outline='black', width=3, tags=(str(i) + "," + str(j), "cellule"))

            if i == 0:
                partie1.create_text(x, y + 0.2 * scale, font=Police, fill='black', text=ascii_letters[j])

            if j == 0:
                partie1.create_text(x, y + 1.5 * scale, font=Police, fill='black', text=i + 1)


def Clear_plateau():
    if len(ordre) != 0:
        partie1.itemconfig(str(ordre[len(ordre) - 1][0]) + "," + str(ordre[len(ordre) - 1][1]), dash="",
                           outline='black', width=3)

    for i in range(len(plat)):
        for j in range(len(plat)):
            # if plat[i][j] != 0 :
            tag = str(i) + ',' + str(j)
            partie1.itemconfig(tag, fill=Rgb_convert((160, 160, 160)), activefill=Rgb_convert((180, 180, 180)))


def load_plateau(plat):
    for i in range(len(plat)):
        for j in range(len(plat)):

            if plat[i][j] == 0:
                pass

            elif plat[i][j] == 1:
                partie1.itemconfig(str(i) + "," + str(j), fill="red")

            elif plat[i][j] == 2:
                partie1.itemconfig(str(i) + "," + str(j), fill="blue")

def Show_distance(team, search):
    print(search)
    r = 220 / (max(search) - 10)
    for i in range(len(plat)):
        for j in range(len(plat)):
            if search[i][j] >= 10:
                tag = str(i) + ',' + str(j)
                if team == 1:
                    partie1.itemconfig(tag, fill=Rgb_convert((255 - int((search[i][j] - 10) * r), 0, 0)))
                else:
                    partie1.itemconfig(tag, fill=Rgb_convert((0, 0, 255 - int((search[i][j] - 10) * r))))


width = 900
size = 5
player1, player2 = False, False  # Si Tru

begin = False  # soit blanc commence, soit noir, soit random
timed = False  # active ou non le minuteur pour les joueurs
Game_status = True

height = round(width * 0.618)
scale = (width - 250) / ((size - 1) * 3 + 2)

tour = 0
ordre = []

plat = zeros((size, size))  # Crée une matrice carré de taille size remplie de 0

fe = tk.Tk()

fe.title('HexGame')
fe.config(bg=Rgb_convert((50, 50, 50)))
xu = width + (width * (0.618 ** 3))
yu = height + (width * (0.618 ** 5))

window = str(round(width + (width * (0.618 ** 3)))) + 'x' + str(round(height + (width * (0.618 ** 5)))) + '+' + str(
    10) + '+' + str(100)

fe.geometry(window)

frame = tk.Frame(fe, width=round(width + (width * (0.618 ** 3))), height=round(height + (width * (0.618 ** 5))),
                 bg='blue')
frame.place(relx=0.5, rely=0.5, anchor="center")

frame.configure(bg=Rgb_convert((100, 80, 70)))

partie1 = tk.Canvas(frame, width=width, height=height, bg=Rgb_convert((200, 160, 150)), highlightbackground='red',
                    highlightthickness=0)
partie1.grid(row=0, column=0, rowspan=3, columnspan=3)

enregi1 = tk.Button(frame, text="Enregistrement 1", command=fe.destroy, borderwidth=5, relief='groove', bg='pink')
enregi1.grid(row=0, column=4, padx=10, pady=10)

enregi2 = tk.Button(frame, text="Enregistrement 2", command=fe.destroy, borderwidth=5, relief='ridge', bg='blue')
enregi2.grid(row=1, column=4, padx=10, pady=10)

enregi3 = tk.Button(frame, text="Enregistrement 3", command=fe.destroy)
enregi3.grid(row=2, column=4, padx=10, pady=10)

des = tk.Button(frame, text='Menu principal', command=fe.destroy)
des.grid(row=4, column=0, padx=10, pady=10)

des1 = tk.Button(frame, text='Reset')
des1.grid(row=4, column=1, padx=10, pady=10)

des2 = tk.Button(frame, text='Distance Rouge', command=Show_distance)
des2.grid(row=4, column=2, padx=10, pady=10)

partie4 = tk.Frame(frame, width=(width * (0.618 ** 3)), height=(width * (0.618 ** 5)), bg='pink')
partie4.grid(row=4, column=4)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=0, extent=180, fill="red", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=180, extent=180, fill="blue", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 + 0.75),
                   start=90, extent=180, fill="red", outline="black", width=3)

partie1.create_arc((width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 - 0.75),
                   (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 - 0.75),
                   (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + scale * (0.866 + 0.75),
                   start=270, extent=180, fill="blue", outline="black", width=3)

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
                   start=90, extent=180, fill="blue", outline="black", width=3)

partie1.create_arc(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 1.25 * scale - scale * 0.5 + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 - 0.5 * scale + 1.25 * scale + scale * ((size - 1) * 3 + 2),
    (height - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
    start=0, extent=180, fill="blue", outline="black", width=3)

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
    fill="blue", outline="black", width=3)

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
                       fill="blue", outline="black", width=3)

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
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.3746),
    (height - (scale * size * 2 * 0.866)) / 2 - 0.5 * scale + (2 * 0.866 * scale * size),
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) + 2,
    (height - (scale * size * 2 * 0.866)) / 2 - (0.866 * scale) + (2 * 0.866 * scale * size) + scale * (
                0.6494 + 0.866) - 3,
    fill='blue', outline='blue', width=6)

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
    fill='blue', outline='blue', width=6)

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
                       fill='blue', outline='blue', width=6)

partie1.create_polygon(
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.5 + 0.3746) - 10,
    (height - (scale * size * 2 * 0.866)) / 2 + scale,
    (width - (scale * ((size - 1) * 3 + 2))) / 2 + (size * scale * 1.5) - scale * (0.3746),
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
                       fill='blue', outline='blue', width=6)

Police = tkFont.Font(weight="bold", size=-(int(scale / 2)))