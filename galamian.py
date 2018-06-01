#!/usr/bin/python3

# TODO: phase en bowings
# TODO: each scale should have several fingerings
# TODO: fingerings should include string changes
# TODO: octave change inside scale

import re

class rhythmic_pattern:
    def __init__(self, r):
        self.time_signature=r[1]
        regex=r'((?<![/r])\d+(?!/)\.*|(?<= )\.)'
        (s, n) = re.subn(regex, '#\g<0>%', r[0])
        ties = s.count('~')
        self.string = s.replace('#.%', '#%')
        self.l = n - ties

class melodic_pattern:

    names=['c','d','e','f','g','a','b']
    key_names=['c', 'g', 'd', 'a', 'e', 'b', 'fis', 'cis',
            'ces', 'ges', 'des', 'aes', 'ees', 'bes', 'f']

    def __init__(self, string):
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
        self.l=len(tokens)
        self.grades=grades
        self.accidentals=accidentals
        self.tokens=tokens
        return

    def note_names(self, key_signature=0):
        nkeys=len(self.key_names)
        k=key_signature
        l=self.l
        grades=self.grades
        accidentals=self.accidentals[:]
        notes=['']*l
        for i in range(l):
            (g, a) = (grades[i], accidentals[i])
            index=(g-1+k*4)%7
            if (2*index+1) % 7 +1 <= k:
                accidentals[i]+=1
            if (5-2*index) % 7 +1 <= -k:
                accidentals[i]-=1
            s=self.names[index]
            if accidentals[i]>0:
                s+='is'*accidentals[i]
            elif accidentals[i]<0:
                s+='es'*(-accidentals[i])
            if self.tokens[i][-1]=='=':
                s+='!'
            notes[i]=s
        return notes

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
    def __init__(self, melody, fingering, bowing, rhythm, key_signature=0):
        self.key_signature=melodic_pattern.key_names[key_signature]
        self.time_signature=rhythm.time_signature
        note_names=melody.note_names(key_signature)
        b=bowing.l
        ritmo=rhythm.string
        r=len(ritmo)
        s=''
        i=0
        n=0
        while i < r:
            c=ritmo[i]
            if c=='#':
                s+=note_names[n]
            elif c=='%':
                s+=bowing.bowings[n%b]
                s+=fingering.fingers[n]
                n+=1
            else:
                s+=c
            if c=='~':
                n-=1
            i+=1
            if i==r and n<melody.l:
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

def parse (file_name):
    f=open(file_name)
    content=f.readlines()
    i=0
    scales=[]
    in_scales=1
    while in_scales:
        line=content[i].strip()
        i+=1
        if line=='RHYTHMS':
            in_scales=0
            break
        if line:
            scales.append(line)
    rhythms=[]
    in_rhythms=1
    while in_rhythms:
        line=content[i]
        i+=1
        r_line=line.split('#')
        time_signature="4/4"
        if len(r_line)==2:
            time_signature=r_line[1].strip()
        r=r_line[0].strip()
        if r=='BOWINGS':
            in_rhythms=1
            break
        if r:
            rhythms.append([r, time_signature])
    bowings=[]
    while i<len(content):
        line=content[i].strip()
        i+=1
        if line:
            bowings.append(line)
    return (scales, rhythms, bowings)


(s,r,b)=parse("galamian.txt")

ritmo=rhythmic_pattern(r[1])
melodia=melodic_pattern(s[0])
digitacion=fingering_pattern(s[1][1:])
arcos=bowing_pattern(b[1])

a=escala(melodia, digitacion, arcos, ritmo, -2)

print ('\\version "2.18.0"')
a.export()

