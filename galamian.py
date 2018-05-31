#!/usr/bin/python3

# TODO: calculate the note names in a different function

import re

class rhythmic_pattern:
    def __init__(self, string, time_signature="4/4"):
        self.time_signature=time_signature
        regex=r'((?<![/r])\d+(?!/)\.*|(?<= )\.)'
        (s, n) = re.subn(regex, '#\g<0>%', string)
        ties = s.count('~')
        self.string = s.replace('#.%', '#%')
        self.l = n - ties

class melodic_pattern:
    def __init__(self, string, key_signature=0):
        note_names=['c','d','e','f','g','a','b']
        key_names=['c', 'g', 'd', 'a', 'e', 'b', 'fis', 'cis',
                'ces', 'ges', 'des', 'aes', 'ees', 'bes', 'f']
        nkeys=len(key_names)
        self.key_signature=key_names[key_signature % nkeys]
        tokens=string.split()
        l=len(tokens)
        grades=[0]*l
        accidentals=[0]*l
        self.notes=['']*l
        for i in range(l):
            item=tokens[i]
            r=re.match('([1-7])([+-=]*)', item)
            (g, a) = (r.group(1), r.group(2))
            grades[i]=int(g)
            accidentals[i]=a.count('+') - a.count('-')
            index=(int(g)-1+key_signature*4)%7
            if (2*index+1) % 7 +1 <= key_signature:
                accidentals[i]+=1
            if (5-2*index) % 7 +1 <= -key_signature:
                accidentals[i]-=1
            s=note_names[index]
            if accidentals[i]>0:
                s+='is'*accidentals[i]
            elif accidentals[i]<0:
                s+='es'*(-accidentals[i])
            if tokens[i][-1]=='=':
                s+='!'
            self.notes[i]=s
        self.l=len(self.notes)
        self.grades=grades
        self.accidentals=accidentals
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
        s=string.replace(' ','')
        fingers=list(s)
        l=len(fingers)
        for i in range(l):
            if fingers[i]=='.':
                fingers[i]=''
            else:
                fingers[i]='-' + fingers[i]
        self.fingers=fingers
        self.l=l
        return

class repeat_pattern:
    def __init__(self, string):
        pass
        return

class escala:
    def __init__(self, melody, fingering, bowing, rhythm):
        self.key_signature=melody.key_signature
        self.time_signature=rhythm.time_signature
        m=melody.l
        b=bowing.l
        ritmo=rhythm.string
        r=len(ritmo)
        s=''
        i=0
        n=0
        while i < r:
            c=ritmo[i]
            if c=='#':
                s+=melody.notes[n]
            elif c=='%':
                s+=bowing.bowings[n%b]
                s+=fingering.fingers[n]
                n+=1
            else:
                s+=c
            if c=='~':
                n-=1
            i+=1
            if i==r and n<m:
                i=0
                s+='\n    '
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
        s+='    \\bar "||"\n'
        s+="  }\n}\n"
        print(s)



ritmo=rhythmic_pattern(r"16","6/8")
melodia=melodic_pattern(
"1 3 2 1 2 3 4 5 6 7 1 2 3 4 5 6 7 1 2 3 4 5 6 7 1 7 6 5 4 3 2 1 7 6 5 4 3 2 1 7 6 5 4 3 2 1 3 2", -2)
#melodia=melodic_pattern("bes d c bes c d ees f g a bes c d ees f g a bes c d ees f g a bes a g f ees d c bes a g f ees d c bes a g f ees d c bes d c", "bes")
digitacion=fingering_pattern("1....... .....1.. ....1... 44...3.. 2....... ........")
arcos=bowing_pattern(r"( . ) ( . )")

a=escala(melodia, digitacion, arcos, ritmo)

print ('\\version "2.18.0"')
a.export()

