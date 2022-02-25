import tkinter as tk
import tkinter.font as tkFont
from numpy import zeros
from numpy import where
from numpy import max
from string import ascii_letters
from copy import deepcopy
#from tkinter.tix import *
#import math
#import time
#test
#test


def Rgb_convert(rgb):
    return "#%02x%02x%02x" % rgb 


def Plein_ecran (event):
    if fe.attributes ()[7] == 0:
        fe.attributes('-fullscreen', True)
        
    else:
        fe.attributes('-fullscreen', False)


def Affichage_plateau (plat, size, scale):
    
    for i in range (size):
        for j in range (size):
            x = (width-(scale*((size-1)*3+2)))/2 + (j*scale*1.5) + (i*scale*1.5)
            y = (height-(scale*size*2*0.866))/2 - (0.866*scale) + (0.866*scale*size) - (j*scale*0.866) + (i*scale*0.866)
            
            if plat[i][j]==0:
                partie1.create_polygon (x+(0.5*scale), y, x+(1.5*scale), y, x+(2*scale), y+(scale*0.866), x+(scale*1.5), y+(scale*2*0.866),
                                      x+(scale*0.5), y+(scale*2*0.866), x, y+(scale*0.866), fill = Rgb_convert((160,160,160)), activefill = Rgb_convert((180,180,180)), outline = 'black', width=3, tags = (str(i) + "," + str(j) , "cellule") )
                
            if i == 0:
                partie1.create_text( x, y + 0.2*scale, font = Police, fil = 'black', text = ascii_letters[j] )
            
            if j == 0:
                partie1.create_text( x, (y+1.5*scale), font = Police, fil = 'black', text = i+1)


def Reset_Value (New_plat, New_ordre):
    
    tour = len( New_ordre )
    ordre = New_ordre
    plat = New_plat
    
    return (plat, ordre, tour)


def Clear_plateau ():
    
    if len (ordre) != 0:
        partie1.itemconfig ( str( ordre[ len(ordre)-1 ][0] ) + "," + str( ordre[ len(ordre)-1 ][1] ),  dash = ""  , outline = 'black', width= 3)
    
    for i in range (len(plat)):
        for j in range (len(plat)):
            #if plat[i][j] != 0 :
            tag = str(i ) + ',' + str( j )   
            partie1.itemconfig (tag, fill = Rgb_convert((160,160,160)), activefill = Rgb_convert((180,180,180)) )
    
def load_plateau (plat):
    
    for i in range (len(plat)):
        for j in range(len(plat)):
            
            if plat [i][j] == 0:
                pass
            
            elif plat [i][j] == 1:
                partie1.itemconfig (str(i) + "," + str(j), fill = "red" )
                
            elif plat [i][j] == 2:
                partie1.itemconfig (str(i) + "," + str(j), fill = "blue" )
                


def Reset ():
    
    global plat,ordre,tour,Game_status
    Clear_plateau()
    plat,ordre,tour = Reset_Value(zeros((size, size)),[])
    Game_status = True


def Show_distance (team,search):
    
    print(search)
    r = 220/(max(search)-10)
    for i in range (len(plat)):
        for j in range(len(plat)):
            if search[i][j] >= 10 :
                tag = str(i ) + ',' + str( j )
                if team == 1 :
                    partie1.itemconfig (tag, fill = Rgb_convert((255-int((search[i][j]-10)*r),0,0)) )
                else :
                    partie1.itemconfig (tag, fill = Rgb_convert((0,0,255-int((search[i][j]-10)*r))) )
                    
                    
def Detection_victoire (plat, slot):
    
    size = len(plat)
    team = plat[slot[0]][slot[1]] #team = 1, le joueur blanc viens de jouer, team = 2 le joueur noir viens de jouer
    
    start = [] #liste des coordonnées de départ
    

    if team == 1:
        for i in range(size): #verrou de pion jouer sur un bord
            if plat[0][i] == team :
                start.append( ( 0, i) )
    else:
        for i in range(size): #verrou de pion jouer sur un bord
            if plat[i][0] == team :
                start.append( ( i, 0) )
            
    if len(start) == 0 :
        #if bot == True:
            #Ask_bot(plat)
            pass
    
    else:
        end = [] #liste des coordonnées d'arrivée
        #print("verrou 1 ok")
        
        if team == 1:
            for i in range(size):  #verrou de pion jouer sur l'autre bord
                if plat[size-1][i] == team :
                    end.append( ( size-1, i) )
        else:
            for i in range(size):  #verrou de pion jouer sur l'autre bord
                if plat[i][size-1] == team :
                    end.append( ( i, size-1) )
            
        if len(end) == 0 :
            #if bot == True:
                #move = Ask_bot(plat)
                #plat[ move[0] ][ move[1] ] = 
                pass
        
        else:
            #print("verrou 2 ok")
            if plat[plat==team].size < size: #verrou de minimum de pion joué pour une victoire
                #if bot == True:
                    #Ask_bot(plat)
                    pass
            
            else:
                #print("verrou 3 ok")
                search = deepcopy(plat) #creation d'une matrice de travail copié d'un plateau
                distance = 9
                
                Propagation( slot, search, team, distance) #fonction récursive de propagation sur le plateau de travail en fonction du dernier coup joué
                print (search)
                
                
                if True in [search[ k[0] ][ k[1] ] >= 10 for k in start]: #si un des pions de la team touche un des bord et est relier au dernier coup
                    
                    if True in [search[ q[0] ][ q[1] ] >= 10 for q in end]: #si un des pions de la team touche l'autre bord et est relier au dernier coup
                        
                        if team == 2:
                            print("victoire bleu")
                            Fin_Partie(team, search)
                                
                        else:
                            print("victoire rouge")
                            Fin_Partie(team, search)
                Show_distance(team,search)
            
            
def Propagation (slot, search, team, distance):

    distance += 1
    search[ slot[0] ][ slot[1] ] = distance

    if slot[0]+1 <= len(plat)-1:
        if search[ slot[0]+1 ][ slot[1] ] == team or search[ slot[0]+1 ][ slot[1] ] > distance:
            Propagation( ( slot[0]+1, slot[1]), search, team, distance)
            
    if slot[0]+1 <= len(plat)-1 and slot[1]-1 >= 0:
        if search[ slot[0]+1 ][ slot[1]-1 ] == team  or search[ slot[0]+1 ][ slot[1]-1 ] > distance:
            Propagation( ( slot[0]+1, slot[1]-1), search, team, distance)
            
    if slot[1]-1 >= 0:
        if search[ slot[0] ][ slot[1]-1 ] == team or search[ slot[0] ][ slot[1]-1 ] > distance:
            Propagation( ( slot[0], slot[1]-1), search, team, distance)
            
    if slot[1]+1 <= len(plat)-1:
        if search[ slot[0] ][ slot[1]+1 ] == team or search[ slot[0] ][ slot[1]+1 ] > distance:
            Propagation( ( slot[0], slot[1]+1), search, team, distance)
            
    if slot[0]-1 >= 0 and slot[1]+1 <= len(plat)-1:
        if search[ slot[0]-1 ][ slot[1]+1 ] == team or search[ slot[0]-1 ][ slot[1]+1 ] > distance:
            Propagation( ( slot[0]-1, slot[1]+1), search, team, distance)
            
    if slot[0]-1 >= 0:
        if search[ slot[0]-1 ][ slot[1] ] == team or search[ slot[0]-1 ][ slot[1] ] > distance:
            Propagation( ( slot[0]-1, slot[1]), search, team, distance)
    
    
def Fin_Partie (team, search):
    
    
    global Game_status
    Game_status = False
    
    if len (ordre) != 0:
        partie1.itemconfig ( str( ordre[ len(ordre)-1 ][0] ) + "," + str( ordre[ len(ordre)-1 ][1] ),  dash = ""  , outline = 'black', width = 3)
        
    partie1.itemconfig("cellule", activefill = '')
    
    chemin = []
    
    if team == 1:
        
        depart = min(filter(lambda i : i > 10 , search[0]))
        debut = list(where((search[0] == depart))[0])
        for i in debut:
            chemin.append( (0, i) )
        
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

                
    

def Clic_gauche (event):
    
    global tour, Game_status
    
    tags = partie1.gettags( 'current')

    if len (tags) == 3 and Game_status == True :
        
        tag = tags[0].split(",")
        slot = (int(tag[0]),int(tag[1]))
        
        if tour == 0 and slot[0] == size - (size+1)/2 and slot[1] == size - (size+1)/2 : #condition de l'interdiction de jouer le premier coup sur le centre
            pass
        
        elif plat [ slot[0] ] [ slot[1] ] == 0 :
            
            if len (ordre) != 0:
                partie1.itemconfig ( str( ordre[ len(ordre)-1 ][0] ) + "," + str( ordre[ len(ordre)-1 ][1] ),  dash = ""  , outline = 'black', width = 3)       
            
            if tour%2 == 0:
                partie1.tag_raise(tags[0])
                partie1.itemconfig (tags[0], fill = 'red', dash = (3,3,3,3), outline = Rgb_convert((230,230,230)), activefill = "", width = 2 )
                tour += 1
                plat[slot[0]][slot[1]] = 1
                ordre.append((slot[0],slot[1]))
                print("Tour", tour, ': Rouge (1)')
                print(plat)
                Detection_victoire( plat, slot)                    

            else:
                partie1.tag_raise(tags[0])
                partie1.itemconfig (tags[0], fill = 'blue', dash = (3,3,3,3), outline = Rgb_convert((230,230,230)), activefill = "", width = 2 )
                tour += 1
                plat[ slot[0] ][ slot[1] ] = 2
                ordre.append((slot[0],slot[1]))
                print("Tour", tour, ": Bleu (2)")
                print(plat)
                Detection_victoire(plat, slot)
                
                

    
"""
def Enregistrement (plat, ordre, numero):
    pass


def Parametrage():
    pass

def Ask_bot (plat):
    pass

"""

width = 1300
size = 5
player1 = False #active ou non le bot en tant que player 2
player2 = False
begin = False #soit blanc commence, soit noir, soit random
timed = False #active ou non le minuteur pour les joueurs
Game_status = True

height = round(width*0.618)
scale = (width-250)/((size-1)*3+2)

tour = 0
ordre = []


plat = zeros((size, size)) #Crée une matrice carré de taille size remplie de 0


fe = tk.Tk ()


fe.title('HexGame')
fe.config(bg= Rgb_convert((50,50,50)))
xu=width+(width*(0.618**3))
yu=height+(width*(0.618**5))


window = str(round(width+(width*(0.618**3)))) + 'x' + str(round(height+(width*(0.618**5)))) + '+' + str(10) + '+' + str( 100 )

fe.geometry(window)


frame = tk.Frame (fe, width = round(width+(width*(0.618**3))), height = round(height+(width*(0.618**5))), bg ='blue')
frame.place (relx = 0.5, rely = 0.5, anchor = "center")
    
frame.configure(bg = Rgb_convert((100,80,70)))


partie1 = tk.Canvas (frame, width = width, height = height, bg = Rgb_convert((200,160,150)), highlightbackground = 'red', highlightthickness = 0)
partie1.grid (row = 0, column = 0, rowspan = 3, columnspan = 3)

enregi1 = tk.Button (frame, text = "Enregistrement 1", command = fe.destroy, borderwidth = 5, relief = 'groove', bg = 'pink')
enregi1.grid (row = 0, column = 4, padx = 10, pady = 10)

enregi2 = tk.Button (frame, text = "Enregistrement 2", command = fe.destroy, borderwidth = 5, relief = 'ridge', bg = 'blue')
enregi2.grid (row = 1, column = 4, padx = 10, pady = 10)

enregi3 = tk.Button (frame, text = "Enregistrement 3", command = fe.destroy)
enregi3.grid (row = 2, column = 4, padx = 10, pady = 10)

des = tk.Button (frame, text = 'Menu principal', command = fe.destroy)
des.grid (row = 4, column = 0, padx = 10, pady = 10)

des1 = tk.Button (frame, text = 'Reset', command = Reset )
des1.grid (row = 4, column = 1, padx = 10, pady = 10)

des2 = tk.Button (frame, text = 'Distance Rouge', command = Show_distance)
des2.grid (row = 4, column = 2, padx = 10, pady = 10)

partie4 = tk.Frame (frame, width = (width*(0.618**3)), height = (width*(0.618**5)), bg = 'pink')
partie4.grid (row = 4, column = 4)

   

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 - scale + scale*0.25, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 1.25*scale,
                   (width-(scale*((size-1)*3+2)))/2 + 1.75*scale, (height-(scale*size*2*0.866)  )/2 + (0.866*scale*size) + 1.25*scale,
                   start = 0, extent = 180, fill = "red", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 - scale + scale*0.25, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 1.25*scale,
                   (width-(scale*((size-1)*3+2)))/2 + 1.75*scale, (height-(scale*size*2*0.866)  )/2 + (0.866*scale*size) + 1.25*scale,
                   start = 180, extent = 180, fill = "blue", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5+0.75), (height-(scale*size*2*0.866))/2 - (0.866*scale) + scale*(0.866-0.75),
                   (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5-0.75), (height-(scale*size*2*0.866))/2 - (0.866*scale) + scale*(0.866+0.75),
                   start = 90, extent = 180, fill = "red", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5+0.75), (height-(scale*size*2*0.866))/2 - (0.866*scale) + scale*(0.866-0.75),
                   (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5-0.75), (height-(scale*size*2*0.866))/2 - (0.866*scale) + scale*(0.866+0.75),
                   start = 270, extent = 180, fill = "blue", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5+0.75), (height-(scale*size*2*0.866))/2 + (2*size*0.866*scale) - (0.866*scale) + scale*(0.866-0.75),
                   (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5-0.75), (height-(scale*size*2*0.866))/2 + (0.866*size*2*scale) - (0.866*scale) + scale*(0.866+0.75),
                   start = 270, extent = 180, fill = "red", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5+0.75), (height-(scale*size*2*0.866))/2 + (2*size*0.866*scale) - (0.866*scale) + scale*(0.866-0.75),
                   (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5-0.75), (height-(scale*size*2*0.866))/2 + (0.866*size*2*scale) - (0.866*scale) + scale*(0.866+0.75),
                   start = 90, extent = 180, fill = "blue", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 - 1.25*scale - scale*0.5 + scale*((size-1)*3+2), (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 1.25*scale,
                   (width-(scale*((size-1)*3+2)))/2 - 0.5*scale + 1.25*scale + scale*((size-1)*3+2), (height-(scale*size*2*0.866))/2 + (0.866*scale*size) + 1.25*scale,
                   start = 0, extent = 180, fill = "blue", outline = "black", width = 3 )

partie1.create_arc( (width-(scale*((size-1)*3+2)))/2 - 1.25*scale - scale*0.5 + scale*((size-1)*3+2), (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 1.25*scale,
                   (width-(scale*((size-1)*3+2)))/2 - 0.5*scale + 1.25*scale + scale*((size-1)*3+2), (height-(scale*size*2*0.866))/2 + (0.866*scale*size) + 1.25*scale,
                   start = 180, extent = 180, fill = "red", outline = "black", width = 3 )

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + 0.5*scale - scale*0.625, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale,
                       (width-(scale*((size-1)*3+2)))/2 + 2*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746), (height-(scale*size*2*0.866))/2 + 1.25*scale*0.866,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + scale*0.866 - scale*0.6494,
                       fill = "red", outline = "black", width = 3 )

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 0.5*scale + scale*0.625, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale,
                       (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 2*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746), (height-(scale*size*2*0.866))/2 + 1.25*scale*0.866,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + scale*0.866 - scale*0.6494,
                       fill = "blue", outline = "black", width = 3 )

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 0.5*scale + 0.625*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale,
                       (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 2*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale ,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size),
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size) + scale*(0.6494+ 0.866),
                       fill = "red", outline = "black", width = 3 )

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + 0.5*scale - scale*0.625, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - scale*0.866 + 1.948*scale,
                       (width-(scale*((size-1)*3+2)))/2 + 2*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size),
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size) + scale*(0.6494+ 0.866),
                       fill = "blue", outline = "black", width = 3 )



partie1.create_polygon(  (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 0.5*scale + 0.625*scale - 4, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale - 2,
                       (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 2*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale + 10 ,
                       (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size),
                       fill = 'red', outline = 'red', width = 6)

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746) - 30, (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size),
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.3746), (height-(scale*size*2*0.866))/2 - 0.5*scale + (2*0.866*scale*size),
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746) + 2, (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size) + scale*(0.6494+ 0.866) - 3,    
                       fill = 'blue', outline = 'blue', width = 6)

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5), (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size),
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746) + 20, (height-(scale*size*2*0.866))/2 - 0.5*scale + (2*0.866*scale*size),
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - (0.866*scale) + (2*0.866*scale*size) + scale*(0.6494+ 0.866) -4,    
                       fill = 'red', outline = 'red', width = 6)

partie1.create_polygon(  (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 0.5*scale + 0.625*scale - 4, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale + 2,
                       (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - 2*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale - 10 ,
                       (width-(scale*((size-1)*3+2)))/2 + scale*((size-1)*3+2) - scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size),
                       fill = 'blue', outline = 'blue', width = 6)

partie1.create_polygon(  (width-(scale*((size-1)*3+2)))/2 + 0.5*scale - scale*0.625 + 4, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale + 2,
                       (width-(scale*((size-1)*3+2)))/2 + 0.5*scale + 1.5*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - (1.948 - 0.866)*scale - 10 ,
                       (width-(scale*((size-1)*3+2)))/2 + 0.5*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size),
                       fill = 'red', outline = 'red', width = 6)

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + 0.5*scale - scale*0.625 + 4, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale - 2,
                       (width-(scale*((size-1)*3+2)))/2 + 0.5*scale + 1.5*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size) - 0.866*scale + 1.948*scale + 10 ,
                       (width-(scale*((size-1)*3+2)))/2 + 0.5*scale, (height-(scale*size*2*0.866))/2 + (0.866*scale*size),
                       fill = 'blue', outline = 'blue', width = 6)

partie1.create_polygon( (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746) - 10, (height-(scale*size*2*0.866))/2 + scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.3746), (height-(scale*size*2*0.866))/2 + scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) - scale*(0.5 + 0.3746) + 1, (height-(scale*size*2*0.866))/2 - scale*0.6494 + 4,    
                       fill = 'red', outline = 'red', width = 6)

partie1.create_polygon(  (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5), (height-(scale*size*2*0.866))/2 + scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746) + 20, (height-(scale*size*2*0.866))/2 + scale,
                       (width-(scale*((size-1)*3+2)))/2 + (size*scale*1.5) + scale*(-0.5 + 0.3746), (height-(scale*size*2*0.866))/2 - scale*0.6494 + 4,    
                       fill = 'blue', outline = 'blue', width = 6)


Police = tkFont.Font ( weight = "bold", size = -(int(scale/2)) )

Affichage_plateau (plat, size, scale)


fe.bind ("<Button-1>", Clic_gauche)
fe.bind ("<KeyPress-F11>", Plein_ecran)
fe.bind ("<f>", Plein_ecran)


fe.mainloop ()