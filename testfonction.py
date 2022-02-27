from numpy import zeros
import tkinter as tk
from srac import hgh

def matrice_taille(n):
    print(zeros((n, n), dtype=int))
    return zeros((n, n), dtype=int)

scale = 10
size = 3

fe = tk.Tk()

fe.title('HexGame')

fe.geometry("500x500")

frame = tk.Frame(fe, width=100, height=100,
                 bg='blue')
frame.place(relx=0.5, rely=0.5, anchor="center")


partie1 = tk.Canvas(frame, width=200, height=200, bg="red")
partie1.grid(row=0, column=0, rowspan=3, columnspan=3)

enregi1 = tk.Button(frame, text="Enregistrement 1", command=fe.destroy, borderwidth=5, relief='groove', bg='pink')
enregi1.grid(row=0, column=4, padx=10, pady=10)

enregi2 = tk.Button(frame, text="Enregistrement 2", command=fe.destroy, borderwidth=5, relief='ridge', bg='blue')
enregi2.grid(row=1, column=4, padx=10, pady=10)

enregi3 = tk.Button(frame, text="Enregistrement 3", command=lambda: hgh() )
enregi3.grid(row=2, column=4, padx=10, pady=10)

des = tk.Button(frame, text='Menu principal', command=lambda: matrice_taille(2))
des.grid(row=4, column=0, padx=10, pady=10)

des1 = tk.Button(frame, text='Reset')
des1.grid(row=4, column=1, padx=10, pady=10)

des2 = tk.Button(frame, text='Distance Rouge')
des2.grid(row=4, column=2, padx=10, pady=10)

partie4 = tk.Frame(frame, width=50, height=30, bg='pink')
partie4.grid(row=4, column=4)

partie1.create_arc((30 - (scale * ((size - 1) * 3 + 2))) / 2 - scale + scale * 0.25,
                   (50 - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) - 1.25 * scale,
                   (40 - (scale * ((size - 1) * 3 + 2))) / 2 + 1.75 * scale,
                   (40 - (scale * size * 2 * 0.866)) / 2 + (0.866 * scale * size) + 1.25 * scale,
                   start=0, extent=180, fill="red", outline="black", width=3)

