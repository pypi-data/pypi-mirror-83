# -*- coding: utf-8 -*-
"""
Created on Sat Aug 10 09:24:24 2019

@author: Dror
"""

import numpy as np
from gensound.utils import isnumber

midA = 440
octave = 2

semitone = np.power(octave, 1/12)
cent = np.power(semitone, 1/100)

logSemitone = lambda k: np.log(k)/np.log(semitone)

midC = lambda s: midA*semitone**(-9+s)

def freq_to_pitch(freq):
    A0 = 27.5 # lowest on piano?
    if freq < A0:
        return "-"
    semitones_above_A0 = logSemitone(freq/A0)
    closest_pitch = int(round(semitones_above_A0))
    #breakpoint()
    divergence = semitones_above_A0 - closest_pitch
    
    octave = (closest_pitch + 9) // 12
    named_pitch = ["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"][closest_pitch % 12]
    
    return named_pitch + str(octave) + (" " + ("+" if divergence > 0 else "") + str(int(round(divergence*100))) if round(divergence,2) != 0 else "")

def str_to_freq(f): # this is a hack, better use regex or something else
    """ 'C##4+35' middle C## plus 35 cents
    'A' A4 (octave implied)
    """
    cents = 0
    if "+" in f:
        cents = int(f.split("+")[-1])
        f = f.split("+")[0]
    elif "-" in f:
        cents = - int(f.split("-")[-1])
        f = f.split("-")[0]
    
    semi = {"C":0, "D":2, "E":4, "F":5, "G":7, "A":9, "B":11}[f[0]]
    f = f[1:]
    
    while(len(f) > 0 and f[0] in ("#", "b")):
        semi += 1 if f[0] == "#" else -1
        f = f[1:]
    
    if len(f) > 0:
        semi += 12*(int(f)-4) # octave
    
    return midC(semi+cents/100)
        

# TODO make this accessible and modifiable by user
read_freq = lambda f: (f if isnumber(f) else (str_to_freq(f) if isinstance(f, str) else f))

class IntervalRatio(): # accoustic interval, not musical one
    def __init__(self, ratio=(1,1), _float=1, cents=0):
        # assert ratio is None + _float is None + cents is None == 2
        self.ratio = ratio
        self._float = _float
        self.cents = cents
    
    def __neg__(self):
        return IntervalRatio(ratio=(self.ratio[1],self.ratio[0]),
                             _float=1/self._float,
                             cents=-self.cents)
        
    
    def __add__(self, other):
        if isinstance(other, IntervalRatio):
            # implement/import rational additions
            return IntervalRatio(ratio=(self.ratio[0]*other.ratio[1]+other.ratio[0]*self.ratio[1],
                                     self.ratio[1]*other.ratio[1]),
                        _float=self._float+other._float,
                        cents=self.cents+other.cents)
        
        # other is a "pitch"
        return other.frequency*self.__float__()
        
    
    def __sub__(self, other):
        ...
        
    def __str__(self):
        ...
    
    def __float__(self):
        return self._float * cent**self.cents * self.ratio[0] / self.ratio[1]


P8 = IntervalRatio(ratio=(2,1))
P5 = IntervalRatio(ratio=(3,2))
PM3 = IntervalRatio(ratio=(5,4))
Pm7 = IntervalRatio(ratio=(7,4))

PythM2 = IntervalRatio(ratio=(9,8)) # coincides with just intonation
PythM3 = IntervalRatio(ratio=(81,64))
# = 4*P5 - 2*P8?
PythWolf = IntervalRatio(ratio=(3**11,2**(11+6)))

EQm2 = IntervalRatio(cents=100)
EQM2 = IntervalRatio(cents=200)
EQm3 = IntervalRatio(cents=300)
EQM3 = IntervalRatio(cents=400)
EQ4 = IntervalRatio(cents=500)
EQtri = IntervalRatio(cents=600)
EQ5 = IntervalRatio(cents=700)

SyntonicComma = IntervalRatio(ratio=(81,80))

QuarterTone = IntervalRatio(cents=50)


'''

note = Pitch(midC(7)) # middle G
note.scale(EQMajor, degree=5) # rephrased as 5th degree of C Major
note += 2 # now it's a B
note.scale(EQ7) # we take that B and make it the tonic of a EQ-7-TET scale
note -= 2 # should be around F#

# note that every time a Pitch object is input to anything,
# it should be copied, as it should behave like an immutable








'''























