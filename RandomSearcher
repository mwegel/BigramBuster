# python
# -*- coding: utf8 -*-

import random
from Layout import Layout
from LocalMinimizer import LocalMinimizer

# Buchstaben, die auf der Tastatur verteilt werden sollen
buchstaben = [u'a',u'b',u'c',u'd',u'e',u'f',u'g',u'h',u'i',u'j',u'k',u'l',u'm',u'n',u'o',u'p',u'q',u'r',u's',u't',u'u',u'v',u'w',u'x',u'y',u'z',u'ä',u'ö',u'ü',u'ß']
# Stellen, die auf der Tastatur belegt werden sollen; z.B. drei Stellen auf Taste 0
stellen = [0,0,0, 1,1,1, 2,2,2,2, 3,3,3,3, 4,4,4,4, 5,5,5,5, 6,6,6,6, 7,7,7,7]
# Anzahl der Stellen (= Anzahl der Buchstaben)
stellenzahl = len(stellen)

besttasten = [[],[],[],[],[],[],[],[]]
bestconflicts = 100000000 # 100 Mio.
layout = Layout()

# Probiere 10 zufällige Startbelegungen
for ii in range(10):
    # Mische die Liste der Stellen zufällig
    random.shuffle(stellen)
    # Nimm eine leere Tastatur
    belegung = [[],[],[],[],[],[],[],[]]
    # Iteriere über die gemischte Liste der Stellen
    for jj in range(stellenzahl):
        stelle = stellen[jj]
        # Füge zur Taste, die die Stelle benennt, den Buchstaben hinzu, der an der Position jj im Alphabet steht
        belegung[stelle].append(buchstaben[jj])
    
    # Finde lokales Minimum mit dieser zufälligen Startbelegung
    minimizer = LocalMinimizer(belegung,True)
    (tasten,conflicts) = minimizer.run()
    # Vergleiche lokales Minimum mit bisherigem Stand
    if conflicts < bestconflicts:
        besttasten = tasten
        bestconflicts = conflicts
        print ':',
    else:
        print '.',

print '\nBeste gefundene Belegung:'
print layout.pretty(besttasten)
print 'Konflikte:', bestconflicts
