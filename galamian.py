#!/usr/bin/python3

# TODO: re-think the rhythm patterns (string with placeholders) DONE!
# TODO: re-implement escala using the new class rhythm_pattern

import re

class rythmic_pattern:
    def __init__(self, string, time_signature="4/4"):
        self.time_signature=time_signature
        def placeholder(value):
            return '#' + value.group(0) +'#'
        regex=r'((?<![/r])\d+(?!/)\.*|(?<= )\.)'
        (s, n) = re.subn(regex, placeholder, string)
        ties = s.count('~')
        self.string = s.replace('#.#', '##')
        self.l = n - ties
        print (self.string)
        print(self.l)

    def a__init__(self, string, time_signature="4/4"):
        self.time_signature=time_signature
        string=string.replace('~', ' ~ ')
        string=re.sub('times\s*', 'times', string)
        string=re.sub('\s*{\s*', '{ ', string)
        string=re.sub('\s*}', '}', string)
        tokens=string.split()
        l=len(tokens)
        i=0
        n=0
        self.values=[]
        self.pre=[]
        self.post=[]
        self.tie=[]
        self.rest=[]
        tresillo=''
        while i<l:
            if tokens[i] == '~':
               self.tie[n-1]+='~' + tokens[i+1]
               i=i+1
            elif tokens[i][0] == 'r':
                if n==0:
                    tresillo+=tokens[i]+' '
                else:
                    self.rest[n-1]+= tokens[i]
            elif tokens[i][-1]=='{':
                tresillo+=tokens[i]
            else:
                r=re.match(r"(\d*\.*)(.*)", tokens[i])
                numero=r.group(1)
                if numero == '.':
                    numero=''
                scripts=r.group(2)
                self.pre.append(tresillo)
                self.values.append(numero)
                self.post.append(scripts)
                self.tie.append('')
                self.rest.append('')
                tresillo=''
                n=n+1
            i=i+1
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
    def __init__(self, melody, fingering, bowing, rythm):
        self.key_signature=melody.key_signature
        self.time_signature=rythm.time_signature
        m=melody.l
        r=rythm.l
        b=bowing.l
        s=''
        for i in range(m):
            if i%r==0:
                s+='\n    '
            s+=rythm.pre[i%r]
            s+=melody.notas[i]
            s+=rythm.values[i%r]
            s+=bowing.bowings[i%b]
            s+=rythm.post[i%r]
            s+=' '
            if rythm.tie[i%r]:
                ties=rythm.tie[i%r].split('~')
                ties=ties[1:]
                print (ties)
                for j in ties:
                    s+='~ '
                    s+=melody.notas[i]
                    s+=j
                s+=' '
            if rythm.rest[i%r]:
                s+=rythm.rest[i%r]
        self.lilypond_string=s

        return

    def __str__(self):
        return self.lilypond_string

    def export(self):
        s ='\\score{\n'
        s+="  \\new Staff \\relative c'{\n"
        s+="    \\key " + self.key_signature + " \\major\n"
        s+="    \\time " + self.time_signature
        s+="    " + self.lilypond_string + "\n"
        s+='    \\bar "||"'
        s+="  }\n}\n"
        print(s)



ritmo=rythmic_pattern(r"8 ~ 16 r r4 .->")
melodia=melodic_pattern("c d e f g a b c d e f g")
arcos=bowing_pattern(r".")
digitacion=fingering_pattern("1...........")

a=escala(melodia, digitacion, arcos, ritmo)

print ('\\version "2.18.0"')
a.export()

