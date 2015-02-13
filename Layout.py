# python
# -*- coding: utf8 -*-

import codecs

class Layout:
    
    # Initialisiert Werte.
    def __init__(self):
        # Lies die Bigrammhäufigkeiten aus Datei ein
        self.freq = {}
        with codecs.open('2gramme_de1.csv', 'r', 'utf-8') as csvfile:
            for line in csvfile:
                row = line.split(';')
                self.freq[row[2].strip('"')] = int(row[3].strip('"'))
    
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

    # Gibt eine Tastenbelegung als einigermaßen leserlichen String aus.
    def pretty(self, tasten):
        pretty = u''
        for taste in tasten:
            pretty += u'('
            for stabe in taste:
                pretty += stabe
            pretty += u') '
        return pretty[:-1]
    
    # Normiert die Schreibweise einer Tastenbelegung, indem die Buchstaben auf jeder Taste jeweils
    # alphabetisch geordnet werden, und die Tasten untereinander alphabetisch sortiert werden.
    def alphabetical(self, tasten):
        for taste in tasten:
            taste.sort()
        tasten.sort()
