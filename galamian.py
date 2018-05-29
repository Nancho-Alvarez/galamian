#!/usr/bin/python3

import re

class rithmic_pattern:
    def __init__(self, string, time_signature="4/4"):
        self.time_signature=time_signature
        string=string.replace('~', ' ~ ')
        string=re.sub('times\s*', 'times', string)
        string=re.sub('\s*{\s*', '{', string)
        string=re.sub('\s*}', '}', string)
        tokens=string.split()
        l=len(tokens)
        i=0
        n=0
        self.values=[]
        self.pre=[]
        self.post=[]
        while i<l:
            self.values.append(tokens[i])
            i=i+1
            n=n+1
        self.l=n

        return

class melodic_pattern:
    def __init__(self, string, key_signature='c'):
        self.key_signature=key_signature
        self.notas=string.split()
        self.l=len(self.notas)
        return

class bowing_pattern:
    def __init__(self, string):
        self.bowings=string.split()
        self.l=len(self.bowings)
        for i in range(self.l):
            if self.bowings[i][0]=='.':
                self.bowings[i]=self.bowings[i][1:]
        return

class fingering_pattern:
    def __init__(self, string):
        pass
        return

class repeat_pattern:
    def __init__(self, string):
        pass
        return

class escala:
    def __init__(self, melody, fingering, bowing, rithm):
        self.key_signature=melody.key_signature
        self.time_signature=rithm.time_signature
        m=melody.l
        r=rithm.l
        b=bowing.l
        s=''
        for i in range(m):
            s+=melody.notas[i]
            s+=rithm.values[i%r]
            s+=bowing.bowings[i%b]
            s+=' '
        self.lilypond_string=s

        return

    def __str__(self):
        return self.lilypond_string

    def export(self):
        s ='\\score{\n'
        s+="  \\new Staff \\relative c'{\n"
        s+="    \\key " + self.key_signature + " \\major\n"
        s+="    \\time " + self.time_signature + "\n"
        s+="    " + self.lilypond_string + "\n"
        s+="  }\n}\n"
        print(s)



ritmo=rithmic_pattern(r"\times 2/3 { 8 8 8 }")
melodia=melodic_pattern("c d e f g a b c")
arcos=bowing_pattern(r"(\(\downbow . \) -.)")
digitacion=fingering_pattern("1.......")

a=escala(melodia, digitacion, arcos, ritmo)

print ('\\version "2.18.0"')
a.export()

