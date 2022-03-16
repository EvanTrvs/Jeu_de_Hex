def chargement(numero):
    Reset()

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


def enregistrement(numeros):
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
        enregi1.configure(text='Chargement 1', command=lambda: chargement(1))

    elif numeros == 2:
        enregi2.configure(text='Chargement 2', command=lambda: chargement(2))

    elif numeros == 3:
        enregi3.configure(text='Chargement 3', command=lambda: chargement(3))


def reset_enregistrement():
    for i in range(1, 4):
        i = "'" + str(i) + "'"

        cur.execute("""UPDATE Enregistrement SET Plateau = "", Taille = "", Ordre = "" WHERE Numero = """ + str(
            i) + """ """)
        conn.commit()

        self.Reset()

        enregi1.configure(text='Enregistrement 1', command=lambda: enregistrement(1))
        enregi2.configure(text='Enregistrement 2', command=lambda: enregistrement(2))
        enregi3.configure(text='Enregistrement 3', command=lambda: enregistrement(3))
