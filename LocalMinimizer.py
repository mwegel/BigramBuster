# python
# -*- coding: utf8 -*-

import codecs
import copy

# Nimmt eine Start-Tastenbelegung und findet iterativ durch Tauschen einzelner Buchstaben zwischen
# den Tasten eine Tastenbelegung, die die Häufigkeit von Konflikten lokal minimiert. Ein Konflikt
# besteht, wenn zur Eingabe eines Bigramms zweimal dieselbe Taste betätigt werden muss.
class LocalMinimizer:

    # Initialisiert Werte.
    def __init__(self, starttasten):
        # Lies die Bigrammhäufigkeiten aus Datei ein
        self.freq = {}
        with codecs.open('2gramme_de1.csv', 'r', 'utf-8') as csvfile:
            for line in csvfile:
                row = line.split(';')
                self.freq[row[2].strip('"')] = int(row[3].strip('"'))
        
        # Speichere die Start-Tastenbelegung
        self.tasten = starttasten
        # Berechne und speichere ihre Konflikthäufigkeit
        self.conflicts = self.calc_conflicts(self.tasten)
        # Gehe davon aus, dass noch kein lokales Minimum erreicht
        self.found_min = False
    
    # Wechselt von der aktuellen Belegung solange zur konfliktminimierenden Nachbarbelegung
    # bis lokales Minimum erreicht, und gibt dieses aus.
    def run(self):
        # Solange lokales Minimum nicht erreicht
        while self.found_min == False:
            # Wechsle zur Nachbarbelegung mit der kleinsten Konflikthäufigkeit
            self.min_neighbour()
        # Lokales Minimum erreicht, gib Belegung und Konflikthäufigkeit aus
        print 'Lokales Minimum gefunden'
        print self.tasten
        print 'Konflikte:', self.conflicts

    # Berechnet die Konflikthäufigkeit der aktuellen Tastenbelegung.
    def calc_conflicts(self, tasten):
        conflicts = 0
        # Gehe alle Tasten durch
        for taste in tasten:
            # Gehe jedes Buchstabenpaar der Taste durch
            for i in range(0,len(taste)):
                for j in range(i+1,len(taste)):
                    # Betrachte Bigramme "ab" und "ba"
                    bigrams = [taste[i] + taste[j], taste[j] + taste[i]]
                    for bigram in bigrams:
                        if bigram in self.freq:
                            # Schlage Bigrammhäufigkeit nach
                            bigramfreq = self.freq[bigram]
                            # Summiere auf
                            conflicts += bigramfreq
        # Gib summierte Bigrammhäufigkeiten als Konflikthäufigkeit aus
        return conflicts

    # Wechselt zur benachbarten Tastenbelegung mit der kleinsten Konflikthäufigkeit.
    # Eine Tastenbelegung ist benachbart, wenn der Unterschied zur aktuellen Belegung
    # genau eine Vertauschung zweier Buchstaben (auf unterschiedlichen Tasten) ist.
    # Wenn keine Nachbarbelegung besser als die aktuelle ist, wird bei der aktuellen
    # verblieben und found_min auf True gesetzt.
    def min_neighbour(self):
        tastenzahl = len(self.tasten)
        # Gehe davon aus, dass lokales Minimum erreicht - wird überschrieben, falls nicht
        found_min = True
        # Gehe davon aus, dass aktuelle Belegung = beste Belegung
        besttasten = copy.deepcopy(self.tasten)
        # Gehe alle möglichen Tastenpaare durch
        for i in range(0,tastenzahl):
            taste1 = self.tasten[i]
            for j in range(i+1,tastenzahl):
                taste2 = self.tasten[j]
                # Gehe jedes Paar <Buchstabe auf Taste 1, Buchstabe auf Taste 2> durch
                for k in range(0,len(taste1)):
                    for l in range(0,len(taste2)):
                        neutasten = copy.deepcopy(self.tasten)
                        # Vertausche die beiden Buchstaben (sodass sie die Tasten wechseln)
                        neutasten[i][k] = taste2[l]
                        neutasten[j][l] = taste1[k]
                        # Berechne die Konflikthäufigkeit dieser neuen Belegung
                        conflicts = self.calc_conflicts(neutasten)
                        if conflicts < self.conflicts:
                            # Verbesserung erzielt, also war das noch kein lokales Minimum
                            found_min = False
                            # Die neue Belegung ist jetzt die beste Belegung
                            besttasten = copy.deepcopy(neutasten)
                            # Speichere Konflikthäufigkeit
                            self.conflicts = conflicts
        # Speichere die beste Belegung
        self.tasten = besttasten
        # Speichere, ob lokales Minimum gefunden
        self.found_min = found_min

if __name__ == "__main__":
    belegung = [[u'e',u'b',u'f'], [u'n',u'm',u'w'], [u'i',u'g',u'k',u'q'], [u'r',u'o',u'z',u'x'], [u't',u'c',u'v',u'j'], [u's',u'l',u'p',u'ß'], [u'a',u'u',u'ü',u'y'], [u'd',u'h',u'ä',u'ö']]
    minimizer = OverlapMinimizer(belegung)
    minimizer.run()
