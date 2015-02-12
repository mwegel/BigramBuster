# python
# -*- coding: utf8 -*-

import codecs
import copy

# Nimmt eine Start-Tastenbelegung und findet iterativ durch Tauschen einzelner Buchstaben zwischen
# den Tasten eine Tastenbelegung, die die Häufigkeit von Konflikten lokal minimiert. Ein Konflikt
# besteht, wenn zur Eingabe eines Bigramms zweimal dieselbe Taste betätigt werden muss.
class LocalMinimizer:

    # Initialisiert Werte.
    def __init__(self, starttasten, log = False):
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
        # Speichere, ob der Suchvorgang geloggt werden soll
        self.log = log
        self.logstring = u''
        # Gehe davon aus, dass noch kein lokales Minimum erreicht
        self.found_min = False
    
    # Wechselt von der aktuellen Belegung solange zur konfliktminimierenden Nachbarbelegung
    # bis lokales Minimum erreicht, und gibt dieses aus.
    def run(self):
        if self.log:
            # Solange lokales Minimum nicht erreicht
            while self.found_min == False:
                # Logge die aktuelle Belegung und ihre Konflikthäufigkeit
                self.log_layout()
                # Wechsle zur Nachbarbelegung mit der kleinsten Konflikthäufigkeit
                self.min_neighbour()
                # Logge, ob lokales Minimum erreicht
                self.log_min()
        else:
            # Solange lokales Minimum nicht erreicht
            while self.found_min == False:
                # Wechsle zur Nachbarbelegung mit der kleinsten Konflikthäufigkeit
                self.min_neighbour()
        # Lokales Minimum erreicht, gib Belegung und Konflikthäufigkeit aus
        print 'Lokales Minimum gefunden'
        print self.pretty_layout(self.tasten)
        print 'Konflikte:', self.conflicts
        # Schreibe das Log in CSV-Datei
        with codecs.open('handylog.csv', 'a', 'utf-8') as logfile:
            logfile.write(self.logstring)

    # Berechnet die Konflikthäufigkeit einer Tastenbelegung.
    def calc_conflicts(self, tasten):
        conflicts = 0
        # Gehe alle Tasten durch
        for taste in tasten:
            # Gehe jedes Buchstabenpaar der Taste durch
            for i in range(0,len(taste)):
                for j in range(i+1,len(taste)):
                    # Betrachte Bigramme "ab", "ba", "Ab", "Ba", "AB", "BA"
                    bigrams = [taste[i] + taste[j], taste[j] + taste[i],
                               taste[i].upper() + taste[j], taste[j].upper() + taste[i],
                               taste[i].upper() + taste[j].upper(), taste[j].upper() + taste[i].upper()]
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
    
    # Gibt eine Tastenbelegung als einigermaßen leserlichen String aus.
    def pretty_layout(self, tasten):
        pretty = u''
        for taste in tasten:
            pretty += u'('
            for stabe in taste:
                pretty += stabe
            pretty += u') '
        return pretty[:-1]
    
    # Schreibe die aktuelle Tastenbelegung mit ihrer Konflikthäufigkeit ins Log.
    def log_layout(self):
        self.logstring += (u'"'+self.pretty_layout(self.tasten)+u'";')
        self.logstring += (u'"'+str(self.conflicts)+u'";')
    
    # Schreibe zum letzten Logeintrag 1 hinzu, wenn lokales Minimum gefunden, sonst 0.
    def log_min(self):
        self.logstring += (u'"'+str(int(self.found_min))+u'"\n')

if __name__ == "__main__":
    belegung = [[u'e',u'b',u'f'], [u'n',u'm',u'w'], [u'i',u'g',u'k',u'q'], [u'r',u'o',u'z',u'x'], [u't',u'c',u'v',u'j'], [u's',u'l',u'p',u'ß'], [u'a',u'u',u'ü',u'y'], [u'd',u'h',u'ä',u'ö']]
    minimizer = LocalMinimizer(belegung,True)
    minimizer.run()
