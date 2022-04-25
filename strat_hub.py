from strat_denombrement import *
import random
import math


def ask_bot1(mat, team, assis):
    mat2 = deepcopy(np.transpose(mat))

    if team == 2:
        res = pascald(pre_pascal(mat, 2, "d"), (len(mat) - 1, 0), 2) * pascalg(pre_pascal(mat, 2, "g"), (0, len(mat) - 1), 2)
        res2 = np.transpose(pascald(pre_pascal(mat2, 1, "d"), (len(mat2) - 1, 0), 1) * pascalg(pre_pascal(mat2, 1, "g"), (0, len(mat2) - 1), 1))
    else:
        res = np.transpose(pascald(pre_pascal(mat2, 1, "d"), (len(mat2) - 1, 0), 1) * pascalg(pre_pascal(mat2, 1, "g"), (0, len(mat2) - 1), 1))
        res2 = pascald(pre_pascal(mat, 2, "d"), (len(mat) - 1, 0), 2) * pascalg(pre_pascal(mat, 2, "g"), (0, len(mat) - 1), 2)

    s = np.where(mat != 0)

    for i in range(len(s[0])):
        res[s[0][i]][s[1][i]] = 0
        res2[s[0][i]][s[1][i]] = 0

    coup = meilleur_coup(res + res2, mat)
    
    if assis==True:
        
        platposee = deepcopy (mat)
        poseeB = []
        for i in range (len (mat2)):        
            if platposee[:,i] [platposee [:,i] == team].size != 0:
                for y in range (platposee[:,i] [platposee [:,i] == team].size):
                    poseeB.append ((platposee [:,i].tolist().index(team), i))
                    platposee [platposee [:,i].tolist().index(team)][i] = 0
                    
        possibilites, pos = aide (mat, poseeB, team)
        if len (pos) != 0:
            coup = max(possibilites, key = possibilites.get)
        
    return (coup)

def calcul (search, distance, plat, pelement, team):
    elements = [pelement]
    zm = True
    search [pelement [0]][pelement [1]] = distance
    while len (elements) != 0:
        elements1 = deepcopy (elements)
        search1 = deepcopy (search)
        distance += 1
        
        for z in elements1:
            if pelement [1] == 0:
                if z [1] == len (plat) - 1:
                    zm = False
                    
            if pelement [1] == len (plat) - 1:
                if z [1] == 0:
                    zm = False
            
        up = []
        for slot in elements1:
            elements.remove (slot)
            if slot[0]+1 <= len(plat)-1:
                if plat [ slot[0]+1][ slot[1] ] == team and search1 [ slot[0]+1][ slot[1] ] == 0:
                    elements.append ((slot[0]+1, slot[1]))

                    search [slot[0]+1 ][ slot[1] ] = search [slot [0]][slot [1]]
                    up.append (((slot[0]+1, slot[1]), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0]+1][ slot[1] ] == 0:
                    elements.append ((slot[0]+1, slot[1]))

                    search[ slot[0]+1 ][ slot[1] ] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]+1, slot[1]), search [slot [0]][slot [1]] + 1))
            
            
            if slot[0]+1 <= len(plat)-1 and slot[1]-1 >= 0:
                if plat [ slot[0]+1][ slot[1]-1 ] == team and search1 [ slot[0]+1 ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0]+1, slot[1]-1))

                    search[ slot[0]+1][ slot[1]-1] = search [slot [0]][slot [1]]
                    up.append (((slot[0]+1, slot[1]-1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0]+1 ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0]+1, slot[1]-1))

                    search[ slot[0]+1 ][ slot[1]-1] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]+1, slot[1]-1), search [slot [0]][slot [1]] + 1))
                
                
                
            if slot[1]-1 >= 0:
                if plat [ slot[0]][ slot[1]-1 ] == team and search1 [ slot[0] ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0], slot[1]-1)) 
             
                    search[ slot[0] ][ slot[1]-1] = search [slot [0]][slot [1]]
                    up.append (((slot[0], slot[1]-1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0] ][ slot[1]-1 ] == 0:
                    elements.append ((slot[0], slot[1]-1))

                    search[ slot[0] ][ slot[1]-1] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0], slot[1]-1), search [slot [0]][slot [1]] + 1))
                
                
                
            if slot[1]+1 <= len(plat)-1:
                if plat [ slot[0]][ slot[1]+1 ] == team and search1 [ slot[0] ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0], slot[1]+1))
 
                    search[ slot[0]][ slot[1]+1] = search [slot [0]][slot [1]]
                    up.append (((slot[0], slot[1]+1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0] ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0], slot[1]+1))

                    search[ slot[0] ][ slot[1]+1 ] = search [slot [0]][slot [1]] + 1 
                    up.append (((slot[0], slot[1]+1), search [slot [0]][slot [1]] + 1))
                
                
                
            if slot[0]-1 >= 0 and slot[1]+1 <= len(plat)-1: 
                if plat [ slot[0]-1 ][ slot[1]+1 ] == team and search1 [ slot[0]-1 ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0]-1, slot[1]+1))

                    search[ slot[0]-1 ][ slot[1]+1] = search [slot [0]][slot [1]]
                    up.append (((slot[0]-1, slot[1]+1), search [slot [0]][slot [1]]))
                    
                elif search1 [ slot[0]-1 ][ slot[1]+1 ] == 0:
                    elements.append ((slot[0]-1, slot[1]+1))

                    search[ slot[0]-1 ][ slot[1]+1] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]-1, slot[1]+1), search [slot [0]][slot [1]] + 1))

                
            if slot[0]-1 >= 0:
                if plat [ slot[0]-1 ][ slot[1]] == team and search1 [ slot[0]-1 ][ slot[1] ] == 0:
                    elements.append ((slot[0]-1, slot[1]))
                
                    search[ slot[0]-1 ][ slot[1]] = search [slot [0]][slot [1]]
                    up.append (((slot[0]-1, slot[1]), search [slot [0]][slot [1]]))
                elif search1 [ slot[0]-1 ][ slot[1] ] == 0:
                    elements.append ((slot[0]-1, slot[1]))

                    search[ slot[0]-1 ][ slot[1] ] = search [slot [0]][slot [1]] + 1
                    up.append (((slot[0]-1, slot[1]), search [slot [0]][slot [1]] + 1))
        
        for i in up:
            if search [i [0][0]][i [0][1]] > i [1]:
                search [i [0][0]][i [0][1]] = i [1]
        
        
    return zm

def ask_bot2 (plat, team, assis):
    platposee = deepcopy (plat)
    if team == 2:
        autre = 1
        
    else:
        autre = 2
        plat = plat.transpose ()
    
    posee = []
    poseeB = []

    for i in range (len (plat)):        
        if platposee[:,i] [platposee [:,i] == team].size != 0:
            for y in range (platposee[:,i] [platposee [:,i] == team].size):
                poseeB.append ((platposee [:,i].tolist().index(team), i))
                platposee [platposee [:,i].tolist().index(team)][i] = 0
            
        if platposee[:,i] [platposee [:,i] == autre].size != 0:
            for y in range (platposee[:,i] [platposee [:,i] == autre].size):
                posee.append ((platposee [:,i].tolist().index(autre), i))
                platposee [platposee [:,i].tolist().index(autre)][i] = 0
    
    poss = [posee, poseeB]
    copy = deepcopy (plat)
    copy = np.where (copy == team, 0, copy)
    copy = np.where (copy == autre, 20, copy)

    posee = []
    for p in range (len (plat)):
        if plat [p][0] == autre:
            if p == 0:
                if plat [p+1][0] != autre:
                    posee.append ((p+1, 0))
            
            elif p == len (plat) - 1:
                if plat [p-1][0] != autre:
                    posee.append ((p-1, 0))
            else:
                if plat [p-1][0] != autre:
                    posee.append ((p-1, 0))
                if plat [p+1][0] != autre:
                    posee.append ((p+1, 0))
        else:
            posee.append ((p, 0))
        
        
        if plat [p][len (plat) - 1] == autre:
            if p == 0:
                if plat [p+1][len (plat) - 1] != autre:
                    posee.append ((p+1, len (plat) - 1))
            elif p == len (plat) - 1:
                if plat [p-1][len (plat) - 1] != 1:
                    posee.append ((p-1, len (plat) - 1))
            else:
                if plat [p-1][len (plat) - 1] != autre:
                    posee.append ((p-1, len (plat) - 1))
                if plat [p+1][len (plat) - 1] != autre:
                    posee.append ((p+1, len (plat) - 1))
        else:
            posee.append ((p, len (plat) - 1))
            
    zonem = []
    matriceprop = 0
    for slots in posee:
        zm = calcul (copy, 1, plat, slots, team)
        
        if zm == True:
            zonem.append (slots)
        
        matriceprop += copy
            
        copy = deepcopy (plat)
        copy = np.where (copy == team, 0, copy)
        copy = np.where (copy == autre, 20, copy)
        
    if team == 1:
        matriceprop = matriceprop.transpose () 
        platposee = platposee.transpose ()
        plat = plat.transpose ()

    for p in poss [0]:
        matriceprop [p [0]][p [1]] = 500
    
    for p2 in poss [1]:
        matriceprop [p2 [0]][p2 [1]] = 350
    
    for p3 in zonem:
        matriceprop [p3 [0]][p3 [1]] = 300
        

    possible = []
    for i in range (len (plat)):
        for y in range (len (plat)):
            if matriceprop [i][y] == np.min (matriceprop):
                possible.append ((i, y))  
    coup = random.choice (possible)
    
    
    if assis==True:

        possibilites, pos = aide (plat, poss [1], team)
        if len (pos) != 0:
            coup = max(possibilites, key = possibilites.get)
    
    return coup


def aide (plat, pos, team):
    if team == 2:
        autre = 1
    else:
        autre = 2
        
    possibilite = []
    for p in pos:
        y = p [0]
        x = p [1]
            
        v = False # y-2 et x+1
        if (y-2) > 0 and (x+1) < len (plat):
            if plat [y-2][x+1] == team:
                v = True
                
        if (y-2) == -1 and (x+1) <= len (plat) -1 and team == 1:
            v = True
                
        if v == True:
            n = 0
            if plat [y-1][x+1] == autre:
                n += 1
            elif plat [y-1][x] == autre:
                n -= 1
                    
            if n == -1:
                if plat [y-1][x+1] == 0:
                    possibilite.append ((y-1, x+1))
            
            elif n == 1:
                if plat [y-1][x] == 0:
                    possibilite.append ((y-1,x))
                    
        v = False #y-1 et x+2
        
        if (y-1) > 0 and (x+2) < len (plat):
            if plat [y-1][x+2] == team:
                v = True
                    
        if (x+2) == len (plat) and (y-1) >= 0 and team == 2:
            v = True
            
        if v == True:
            n = 0
            if plat [y-1][x+1] == autre:
                n += 1
            elif plat [y][x+1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y-1][x+1] == 0:
                    possibilite.append ((y-1, x+1))
                
            elif n == 1:
                if plat [y][x+1] == 0:
                    possibilite.append ((y, x+1))
                    
            

        v = False #y-1 et x-1
        if (y-1) > 0 and (x-1) > 0:
            if plat [y-1][x-1] == team:
                v = True
            
        if v == True:
            n = 0
            if plat [y-1][x] == autre:
                n += 1
            elif plat [y][x-1] == autre:
                n -= 1
                    
            if n == -1:
                if plat [y-1][x] == 0:
                    possibilite.append ((y-1, x))
            
            elif n == 1:
                if plat [y][x-1] == 0:
                    possibilite.append ((y, x-1))
                    
            
            
        v = False #y+1 et x+1
        if (y+1) < len (plat) and (x+1) < len (plat):
            if plat [y+1][x+1] == team:
                v = True
                
        if v == True:
            n = 0
            if plat [y+1][x] == autre:
                n += 1
            elif plat [y][x+1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y+1][x] == 0:
                    possibilite.append ((y+1, x))
            
            elif n == 1:
                if plat [y][x+1] == 0:
                    possibilite.append ((y, x+1))
                
            
        
            
        v = False #y+1 et x-2
        if ((y+1) < len (plat) and (x-2) > 0):
            if plat [y+1][x-2] == team:
                v = True
                
        if (y+1) <= len (plat) -1 and (x-2) == -1 and team == 2:
            v = True
            
        if v == True:
            n = 0
            if plat [y+1][x-1] == autre :
                n += 1
            elif plat [y][x-1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y+1][x-1] == 0:
                    possibilite.append ((y+1, x-1))
            
            elif n == 1:
                if plat [y][x-1] == 0:
                    possibilite.append ((y, x-1))

        v = False #y+2 et x-1
        if (y+2) < len (plat) and (x-1) > 0:
            if plat [y+2][x-1] == team:
                v = True
                
        if (y+2) == len (plat) and (x-1) >= 1 and team == 1:
            v = True
                
        if v == True:
        
            n = 0
            if plat [y+1][x] == autre:
                n += 1
            elif plat [y+1][x-1] == autre:
                n -= 1
                
            if n == -1:
                if plat [y+1][x] == 0:
                    possibilite.append ((y+1, x))
            
            elif n == 1:
                if plat [y+1][x-1] == 0:
                    possibilite.append ((y+1, x-1))
    
        
    possi = {}
    for i in possibilite:
        possi [i] = possibilite.count (i)   
    
    return possi, possibilite