import xml.etree.ElementTree as ET # Time to grow some trees.
import random as r

import LMMSChip
import LMMSDrums
# This makes non-drums.
# This also makes drums. For the most part it's the same as the instruments, but the values are going to be different.
# For instance, if it makes a Nescaline drum, it makes sure the noise channel is on.
import LMMSMeditative

"""
Other utils used in this file
"""
def randbool(odds,min=0,max=100):
    return True if r.randrange(min,max)<odds else False

# Make the bass template by adding 16th notes to the four spots until a whole bar is filled.
def bassTemplate():
    result=[12, 12, 12, 12]
    # It starts with a 16th note on each of the four hits, so naturally 12 more 16ths need to be added.
    for x in range(12):
        # Increase a random index by 12
        result[r.choice(range(4))] += 12
    return result
"""
Instruments
"""
# Make an instrument and attach it to the parent parameter.
def makeInstrument(parent, pan=2, fxch="1", pitchrange="1", pitch="0",
                   basenote="57", vol="60", instrumentName="nes", type=0, env=0, animal=0, drum=0):
    # Set the basic variables every track has, pan, volume, that sort of stuff.
    instrumentTrack=ET.SubElement(parent,"instrumenttrack",{"pan":["-60","60","0"][pan],
                                                           "fxch":fxch,
                                                           "pitchrange":pitchrange,
                                                           "pitch":pitch,
                                                           "basenote":basenote,
                                                           "vol":[[vol,"20"][instrumentName=="bitinvader"],"100"][drum]})
    # A branching path emerges, depending on the instrument of choice.
    # Every instrument has a specific name, "nes" is for nescaline.
    instrument=ET.SubElement(instrumentTrack,"instrument", {"name":instrumentName})
    # Only the first tab is depending on the actual instrument name, the others are the same regardless.
    if drum>0:ET.SubElement(instrument,instrumentName,LMMSDrums.createInstrument(instrumentName,shapeSample,basenote))
    elif animal>0: ET.SubElement(instrument, instrumentName, LMMSMeditative.makeBird(instrumentName, animal))
    elif type==1:ET.SubElement(instrument,instrumentName,LMMSMeditative.createInstrument(instrumentName,shapeSample))
    else:ET.SubElement(instrument, instrumentName, LMMSChip.createInstrument(instrumentName, shapeSample))
        # This is where the branching path ends.
    # eldata is for the envelope tab.
    eldata=ET.SubElement(instrumentTrack,"eldata",{"fres":"2",
                                                   "ftype":"14",
                                                   "fcut":"14000",
                                                   "fwet":"0"})
    # Connect the formant filter to an LFO.
    if drum==0 and env==1:
        connection=ET.SubElement(eldata,"connection")
        ET.SubElement(connection,"fcut",{"id":"1"})
    # Envelope tab part 1, volume envelope.
    ET.SubElement(eldata,"elvol",{"amt":["0","1"][env],
                                    "pdel":"0",
                                    "att":"0.05",
                                    "hold":"0.5",
                                    "dec":"0.5",
                                    "sustain":"0",
                                    "rel":"0.05",
                                    "syncmode":"0",
                                    "lshp":"0",
                                    "userwavefile":"",
                                    "lpdel":"0",
                                    "latt":"0",
                                    "lspd":"0.1",
                                    "lamt":"0",
                                    "x100":"0",
                                    "ctlenvamt":"0",
                                    "lspd_denominator":"4",
                                    "lspd_numerator":"4"})
    # Envelope tab part 2, cut-off frequency envelope.
    ET.SubElement(eldata, "elcut",{"lspd_denominator":"4",
                                    "sustain":"0.5",
                                    "pdel":"0",
                                    "userwavefile":"",
                                    "dec":"0.5",
                                    "lamt":"0",
                                    "syncmode":"0",
                                    "latt":"0",
                                    "rel":"0.1",
                                    "amt":"0",
                                    "x100":"0",
                                    "att":"0",
                                    "lpdel":"0",
                                    "hold":"0.5",
                                    "lshp":"0",
                                    "lspd":"0.1",
                                    "ctlenvamt":"0",
                                    "lspd_numerator":"4"})
    # Envelope tab part 3, resonance envelope. These are all empty tags. With a shitton of attributes.
    ET.SubElement(eldata, "elres",{"lspd_denominator":"4",
                                   "sustain":"0.5",
                                   "pdel":"0",
                                   "userwavefile":"",
                                   "dec":"0.5",
                                   "lamt":"0",
                                   "syncmode":"0",
                                   "latt":"0",
                                   "rel":"0.1",
                                   "amt":"0",
                                   "x100":"0",
                                   "att":"0",
                                   "lpdel":"0",
                                   "hold":"0.5",
                                   "lshp":"0",
                                   "lspd":"0.1",
                                   "ctlenvamt":"0",
                                   "lspd_numerator":"4"})

    # Func tab part 1, Stacking; shouldn't go much further than just an octave.
    ET.SubElement(instrumentTrack,"chordcreator",{"chord":"0",
                                                  "chordrange":"1",
                                                  "chord-enabled":"0"})

    # Func tab part 2, Arpeggio, can probably stay default since arpeggios will be procedurally generated.
    ET.SubElement(instrumentTrack,"arpeggiator",{"arptime":"100",
                                                 "arprange":"1",
                                                 "arptime_denominator":"4",
                                                 "arptime_numerator":"4",
                                                 "syncmode":"0",
                                                 "arpmode":"0",
                                                 "arp-enabled":"0",
                                                 "arp":"0",
                                                 "arpdir":"0",
                                                 "arpgate":"10"})

    # midi controller tab, can stay default.
    ET.SubElement(instrumentTrack,"midiport",{"inputcontroller":"0",
                                              "fixedoutputvelocity":"-1",
                                              "inputchannel":"0",
                                              "outputcontroller":"0",
                                              "writable":"0",
                                              "outputchannel":"1",
                                              "fixedinputvelocity":"-1",
                                              "fixedoutputnote":"-1",
                                              "outputprogram":"1",
                                              "basevelocity":"63",
                                              "readable":"0"})
    # finally the FX chain.
    ET.SubElement(instrumentTrack,"fxchain",{"numofeffects":"0","enabled":"0"})
    return instrumentTrack
"""
Other track types
"""
def makeSample(parent):
    pass

def makeAutomation(parent):
    ET.SubElement(parent,"track",{"muted":"0","type":"5","name":"Automation track","solo":"0"})

def makeTrack(parent,type):
    if type==0:
        return makeInstrument(parent)
    if type==2:
        return makeSample(parent)
    if type==5:
        return makeAutomation(parent)

def FXChain(parent,addReverb=False,addStereo=False,addLimiter=False):
    if not addReverb and not addStereo and not addLimiter:return ET.SubElement(parent,"fxchain",{"numofeffects":"0","enabled":"1"})
    #return an FX chain that contains effects.
    fxchain=ET.SubElement(parent, "fxchain", {"numofeffects":str(addReverb+addStereo+addLimiter), "enabled":"1"})
    # add the TAP reverberator to the chain.
    if addReverb:
        fx=ET.SubElement(fxchain,"effect",{"name":"ladspaeffect",
            "autoquit_numerator":"4",
            "on":"1",
            "wet":"1",
            "gate":"0",
            "autoquit_syncmode":"0",
            "autoquit_denominator":"4",
            "autoquit":"1"})
        controls=ET.SubElement(fx,"ladspacontrols",{"ports":"8"})
        ET.SubElement(controls,"port00",{"data":"1500"}) #delay (ms)
        ET.SubElement(controls,"port01",{"data":"0"}) #dry
        ET.SubElement(controls,"port02",{"data":"0"}) #wet
        ET.SubElement(controls,"port03",{"data":"1"}) #comb
        ET.SubElement(controls,"port04",{"data":"1"}) #allpass
        ET.SubElement(controls,"port05",{"data":"1"}) #bandpass
        ET.SubElement(controls,"port06",{"data":"1"}) #enhanced stereo
        ET.SubElement(controls,"port07",{"data":str(r.choice([2,5,6,10,11,13,14,22,24,25,29,40,41]))}) #type
        key=ET.SubElement(fx,"key")
        ET.SubElement(key,"attribute",{"name":"file","value":"tap_reverb"})
        ET.SubElement(key,"attribute",{"name":"plugin","value":"tap_reverb"})
    # add the stereo enhancer to the chain.
    if addStereo:
        ET.SubElement(fxchain,"effect",{"name":"stereoenhancer",
            "autoquit_numerator":"4",
            "on":"1",
            "wet":"1",
            "gate":"0",
            "autoquit_syncmode":"0",
            "autoquit_denominator":"4",
            "autoquit":"1"})
    # Limiter, because mixing is hard.
    if addLimiter:
        fx=ET.SubElement(fxchain,"effect",{"name":"ladspaeffect",
            "autoquit_numerator":"4",
            "on":"1",
            "wet":"1",
            "gate":"0",
            "autoquit_syncmode":"0",
            "autoquit_denominator":"4",
            "autoquit":"1"})
        controls=ET.SubElement(fx,"ladspacontrols",{"ports": "8"})
        ET.SubElement(controls,"port04",{"data": "0"})  # Bypass
        ET.SubElement(controls,"port05",{"data": "1"})   # Input
        ET.SubElement(controls,"port06",{"data": "0.9"})   # Output
        ET.SubElement(controls,"port015",{"data": "1"})  # Limit
        ET.SubElement(controls,"port016",{"data": "5.05"})  # Lookahead
        port=ET.SubElement(controls,"port017")  # Release
        ET.SubElement(port,"data",{"value":"31.6228","id":"2074","scale_type":"log"})
        ET.SubElement(controls,"port019",{"data": "1"})  # ASC
        ET.SubElement(controls,"port021",{"data": "0.5"})  # ASC level
        key=ET.SubElement(fx,"key")
        ET.SubElement(key,"attribute",{"name": "file","value": "calf"})
        ET.SubElement(key,"attribute",{"name": "plugin","value": "Limiter"})
    return fxchain
"""
A thing about types.
Instrument tracks of any kind are type 0, this includes the audio file processor.
B+B tracks are type 1, they have their own containers
Sample tracks are type 2. Like instrument tracks, they have their own FX chain. Unlike instruments that's all they have for properties.
Automation tracks are type 5, there is no 3 or 4.
Type 6 is reserved for the global automation tracks.
"""

"""
Words
"""
# The voice track is for lyrics, these lyrics don't have to make sense, they're procedurally generated words.
# This makes a word of x syllables, x being the number of actual notes, i.e. not rests, in a bar.
# The list of consonants to be used at the beginning of a syllable.
cons=['b','c','d','f','g','h','j','k','l','m','n','p','qu','r','s','t','v','w','y','z','ch','sh','th']
# The list of consonants to be used at the end of a syllable.
cons2=['b','c','d','f','g','h','k','l','m','n','p','r','s','t','w','y','z','ch','sh','rk','th','ts','ng','nk']
# Every syllable has 1 vowel and is the definition of a syllable in a basic sense.
vow=['a','e','i','o','u']
# Make a syllable.
def syl():
    # The result string.
    result=''
    req=True
    #Does it start with a consonant?
    if r.choice([True,False]):
        result+=r.choice(cons)
        req=False
    #Then add a vowel
    result+=r.choice(vow)
    #Does it end with a consonant?
    if r.choice([True,False]) or req:
        result+=r.choice(cons2)
    return result

# Make a word with x syllables.
def word(x):
    # The result string.
    result=''
    if x<=0:
        return result
    # Run syl() as many times as it's been given.
    for y in range(x):
        result+=syl()
    return result
"""
Drawing waves
"""
# Necessary imports.
"""
A thing about wave forms.

Remember trigonometry? sin(x)=[-1,1]; x in radians (pi notation, if you will)
Sawtooth:y=x/length(*2-1 if not onlyPositive)
Square:1 if x<length*.5, else 0 (or -1)
Tri:sawtooth, but cut in half.
OPL sine:just sine, but absolute.
Smooth:Procedurally generated wave form that goes up/down small steps at random.

"""
from struct import pack
from base64 import b64encode
from math import sin
from math import pi

# All of these return a byte object.
def sinewave(length, onlyPositive):
    result=b''
    # Iterate over the whole length.
    for x in range(length):
        # Trigonometry y'all.
        # Pack the answer to y=sin(x) in radians, where 0, pi and 2pi are 0, .5pi is 1 and 1.5pi is -1.
        result+=pack('f',(.5+(sin(2*pi/length*x)/2))*15) if onlyPositive else pack('f',sin(2*pi/length*x))
        # onlyPositive means the whole thing needs to be shrunk down by half and moved up by half as well.
    return result

def squarewave(length, onlyPositive):
    result=b''
    # Simple square wave, it's either 1 or it's not.
    for x in range(length):
        if x<length/2:
            # It's 1 here.
            result+=pack('f',15) if onlyPositive else pack('f',1)
        else:
            # It's not here. It's 0 if it's called for.
            result+=pack('f',0) if onlyPositive else pack('f',-1)
    return result

def pulsewave(length, onlyPositive):
    result=b''
    wpd=r.randint(2,7)
    # Simple square wave, it's either 1 or it's not.
    for x in range(length):
        if x<length/wpd:
            # It's 1 here.
            result+=pack('f',15) if onlyPositive else pack('f',1)
        else:
            # It's not here. It's 0 if it's called for.
            result+=pack('f',0) if onlyPositive else pack('f',-1)
    return result

def sawwave(length, onlyPositive):
    result=b''
    # This is literally just a line.
    for x in range(length):
        # y=x, but it needs to slope depending on the length so it maxes out at 1.
        result+=pack('f',(x/length)*15) if onlyPositive else pack('f',((x/length)*2)-1)
    return result



def smoothwave(length, onlyPositive):
    sample=r.random()
    result=pack('f',sample)
    # Since the first sample's already added, the length is reduced by 1 (though doesn't really matter).
    # The wave needs to be smooth
    """
    Smooth waves:
    Smooth waves go to a point on the scale a number of samples away and then draw a line to it.
    Not a straight line, an interpolated line (S curve to be exact).
    Wikipedia defines one of those with a funny function, but realistically the point is to keep adding to the delta
    until the halfway point, then lowering until the goal is reached.
    e.g. point0=0,0; point1=50,-0.5. Make a point2 at 25,-0.25.
    Interpolate the steps following 1/2**y, basically the last sample before point2 should be at half.
    t=24;value=-0.125=point2.y*(1/2**(25-24)). t=23;value=half that, so point2.y*(1/2**(25-23))
    point2.y-point0.y=difference. Reduce difference by 2**x
    """
    mark=0
    while mark<length-1:
        # The first point is where it starts.
        point0=[mark,sample]
        # The second point is where it ends.
        point1=[r.randint(mark+1,length),(r.random())] if onlyPositive else [r.randint(mark,length),(r.random())*2-1]
        """
        # The third point is right in between.
        point2=[(point0[0]+point1[0])/2,(point0[1]+point1[1])/2]
        # The mark and sample will gradually shift twoards point1.
       # First part, gradually going up to point2.
        for x in range(point2[0]-int(point0[0])):
            # Mark=0 already has a sample, and is already added, so shift those.
            mark+=1
            # Calculate the value as described above.
            sample+=(point2[1]-point0[1])/(2**(point2[0]-x-point0[0]))
            # Add it.
            result+=pack('f',sample)
        # Halfway there.
        for x in range(int(point1[0])-point2[0]):
            # Same, but different.
            mark+=1
            # Calculate the value as described above.
            sample+=(point1[1]-point2[1])/(2**(point1[0]-x-point2[0]))
            # Add it.
            result+=pack('f',sample)"""
        # fuck it, linear now.
        # Every time the mark moves up one, this gets added to the sample.
        if point0[0]==point1[0]:
            # There's weird shit afoot, end it now.
            point1[0]=length
        step=(point1[1]-point0[1])/(point1[0]-point0[0])
        for x in range(point1[0]-point0[0]):
            sample+=step
            result+=pack('f',sample*15) if onlyPositive else pack('f',sample)
        # Move the marker.
        mark=point1[0]
    return result

def clamp(value, minimum, maximum):
    return min(max(value,minimum),maximum)


def smoothnoise(length, onlyPositive):
    sample=r.random()
    result=pack('f',sample)
    # Since the first sample's already added, the length is reduced by 1 (though doesn't really matter).
    for x in range(length-1):
        # Add or subtract a random value no further than .1 away. Meaning shrink down to a fifth and balance it.
        sample+=((r.random())/5)-.1
        # Make sure sample doesn't go out of bounds.
        sample=clamp(sample,0,1) if onlyPositive else clamp(sample,-1,1)
        # Pack the new sample.
        result+=pack('f', sample*15) if onlyPositive else pack('f',sample)
    return result

def noisewave(length, onlyPositive):
    result=b''
    for x in range(length):
        # Limit it to .5F to avoid screeches.
        result+=pack("f", (r.random()/2)*15) if onlyPositive else pack("f", r.random()-.5)
    return result

# Sample shaper
def shapeSample(length,onlyPositive=False):
    # A sample length of 4 (bitinvader's minimum) only needs 4 floats, but freeboy has 32 and most others have >=200.
    # The range is between 0f to 1f for freeboy (and other only positive graphs) or between -1f and 1f otherwise.
    # Math time. Split up, team. Generate a byte of floats.
    #byte=r.choice(range(6))
    byte=r.randint(0,6)
    if byte==0: byte=sinewave(length,onlyPositive)
    elif byte==1: byte=squarewave(length,onlyPositive)
    elif byte==2: byte=pulsewave(length,onlyPositive)
    elif byte==3: byte=sawwave(length,onlyPositive)
    elif byte==4: byte=smoothwave(length,onlyPositive)
    elif byte==5: byte=smoothnoise(length,onlyPositive)
    elif byte==6: byte=noisewave(length,onlyPositive)
    # do a magic.
    return str(b64encode(byte))[2:-1]
#-----------------------------------------------------------Scales--------------------------------------------------
"""
A thing about scales
The lowest note (key=0) has equivalence of C0
(which can be retuned to lower/higher values if needed by changing the basenote attribute in the instrumenttrack element).
meaning the C major scale would have 0, 2, 4, 5, 7, 9 and 11, as well as any value with multiples of 12 added for each octave
such that every C's key attribute has a value where %12=0
Seeing as it needs to be a sensible listening experience, the notes should be in the range of about C3 through C6
Thus generating a scale would be:
Resolving the 12 notes, starting at 0.
duplicate it three times.
Add 12x3 to the first scale,
Add 12x4 to the second scale,
Add 12x5 to the last scale
Cap it off by adding C6 (12x6=72)
"""
# the recepticle.
keys=[]
# For now, a fixed major scale
# A key is chosen at random, C is 0, B is 11, all exists in between.
key=r.randint(0,11)
print(key)
# Shuffle a [2,2,2,2,2,1,1] list (or pop random indices into a new list).
scale=[2,2,1,2,2,2,1]
#r.shuffle(scale)
# Now make it into a delta list and add the key to all of them.
scale=[sum(scale[:x])+key for x in range(len(scale))]
"""
Major scale, change for modes or esotheric scales. Add the key.
[0+key,2+key,4+key,5+key,7+key,9+key,11+key]
Hypothetically, this is how an esotheric scale would be constructed:
scaleTally=[1]
for x in range(12):
    if randbool(50):
        scaleTally[-1]+=1
    else:
        scaleTally.append(1)
and then the numbers would need to be converted from step to indices like so:
scale=[]
for x in range(len(scaleTally)):
    scale.append(sum(scaleTally[:x])+key)
and from there on continue as per normal.

The problem here is that it wouldn't necessarily produce heptatonic scales (if that is a problem).

A way around that is to make scaleTally=[1,1,1,1,1,1,1] and then randomly add 1s in random indices.
"""
# Add the scale two times times to make the keys list, this is the domain the everything will play in (but the octave depends on the individual track).
for x in range(3):
    # But do it in a way that adds it in different octaves.
    for y in scale:
        # Every time it gets to add a multiple of 12 in some way.
        keys.append(y+(12*(x+3)))

"""
Chords
"""
# Make a finite state machine.
state='0'
# A list of all states, 9 for now.
# states=['0','1','2','3','4','5','6','7','8']
# A dictionary of all the states.
statesDic={'0':{'name':'M','notes':[0,0,0,0],'next':['1']}, # State 1 will always be the tonic.
           '1':{'name':'M','notes':[0,0,0,0],'next':['2','3']}, # State 2 will only have majors.
           '2':{'name':'M','notes':[0,0,0,0],'next':['4','5','6','7','8']}, # State 3 will feature majors,
           '3':{'name':'M7','notes':[0,0,0,-1],'next':['4','5','6','7','8']}, # as well as 7ths and can jump out.
           '4':{'name':'M','notes':[0,0,0,0],'next':['4','8']}, # State 4 will feature majors chords.
           '5':{'name':'M7','notes':[0,0,0,-1],'next':['4','5','6','7','8']}, # 7th chords.
           '6':{'name':'bM','notes':[0,0,0,0],'next':['4','5','6','7','8']}, # More major chords.
           '7':{'name':'m7','notes':[0,-1,0,-2],'next':['4','5','6','7','8']}, # And minor 7th chords, and can jump out if it has to.
           '8':{'name':'M','notes':[0,0,0,0],'next':['0']}} # State 8 will bring it back to the tonic and will resolve the cadence.
# A basic chord
basic=[0,4,7,12]
"""Progression"""
def generateProgression():
    progression=[0]
    # A progression is 4 bars long (which is fine, there're multiples of 4 bars).
    # The way they're constructed is to start with the tonic,
    for x in range(3):
        # followed by some note that's less than the 5th (in this mode), but higher than the tonic,
        progression.append(r.choice(range(1,4)))
        # followed by something that's higher than the second (but not the 7th)
        progression.append(r.choice(range(progression[-1]+1,5)))
        # and finally one that's lower than the third.
        progression.append(r.choice(range(0, progression[-1]-1)))
    return progression


def makeMelody(pattern, progression, sectionLength, humanize=True):
    # The melody should be multiples of two bars long.
    # This could mean it sometimes won't show up in a non-0 length section,
    # but those are parts where it would thematically make sense, like the intro.
    sectionLength=sectionLength-(sectionLength%2)
    # Keep track of stuff.
    barNumber=newBar=1
    # Add a bunch of notes.
    length=0
    # Don't worry about this.
    breaker=False
    # The first note of a bar is going to be the note middle tonic (second octave).
    note=keys[progression[barNumber-1]] #same as keys[7]
    # Every section has its own length. If a section is length less than 2 bars long it gets skipped.
    while length<sectionLength*192 and not breaker:
        # pos=starting position, vol=velocity, key=pitch (60=C5), len=duration (48=quarter), pan=pan.
        # Generate a random note length.
        noteLength=r.choice([24,48])
        # Fill the gap if it's too long to prevent overlap.
        # †# remove this once multiple tracks are implemented for J-cuts/negative transition lengths.
        if noteLength+length>sectionLength*192:
            noteLength=sectionLength*192-length
            # Flip the breaker, but still add the current note (or rest; see next if statement) to round it off.
            breaker=True
            # The while statement will end now.
        # Bar check. Can be merged with the previous block.
        if noteLength+length>192*barNumber:
            # The added note exceeds the current bar. Truncate the note length.
            # noteLength=(192*barNumber)-length
            # Go to the next bar
            newBar=barNumber+1
        # Very, very crude rest implementation/adding of notes.
        if not r.choice(range(10)) == 0:
            # Add the note. Humanization makes the note slightly misaligned, by position and length.
            ET.SubElement(pattern, "note",
                          {"pos":str(length+(r.randint(-2,2)*humanize)),"vol":str(r.randint(60,100)),"key":str(note),
                           "len":str(noteLength+(r.randint(-2,2)*humanize)),"pan": "0"})
            # Choose a note and remember it.
            """A note about the melody:
            The next note should be one higher 30%, one lower 30%, two higher 10%, two lower 10%, the same 10%
            one of the tonics 5% each.
            All that without actually going out of bounds.
            So it could be a Markov chain-ish thing, but only if the note is one of the following:
                The highest note (LMMSutil.keys[len(keys)-1])
                The second-highest note (LMMSutil.keys[len(LMMSutil.keys)-2])
                The middle tonic (LMMSutil.keys[len(LMMSutil.scale)], but only if the span is two octaves)
                The lowest note (and the lower tonic) (LMMSutil.keys[0])
                The second-lowest note (LMMSutil.keys[1])
            Different things happen on each of these."""
            # The bass doesn't care about any hypothetical next note.
            if newBar == barNumber:
                # lol switch statements.
                a=keys.index(note)
                try:
                    # note's exact pitch is known, so the next note can always be relative.
                    # shift the index
                    a += {keys[len(keys)-1]: r.choice([-1, -1, -1, -1, -1, -1, -1, -1, -1,
                           -2, -2, -2, -3, -3, -4, 0, 0, 0,-len(keys), -len(scale)]), # Last note on the scale.
                          keys[len(keys)-2]: r.choice([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                           -2, -2, -2, 1, 1, 0, 0, 0,-(len(keys)-1),-(len(scale)-1)]), # Penultimate note on the scale.
                          keys[len(scale)]: r.choice([-1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1,
                           -2, -2, 2, 2, 0, 0, -(len(scale)),-(len(scale))]), # Middle note on the scale.
                          keys[1]: r.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,2, 2, 2, -1, -1, -1, 0, 0, 0,
                           (len(scale)-1)]), # Second note on the scale.
                          keys[0]: r.choice([1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 0, 0, 0, 0, len(scale),
                           len(scale)])}[note] # First note on the scale.
                    note=keys[a]
                # Exceptions are really just if statements on crack.
                except KeyError:
                    # Default action. Since it's unknown which note it is exactly, manipulating the note variable is easiest.
                    a=r.choice(
                        [a+1, a+1, a+1, a+1, a+1, a+1, a-1, a-1, a-1, a-1, a-1, a-1, a+2,
                         a+2, a-2, a-2, a, a, 0, len(scale)])
                    note=keys[a]
            # Change the note to the one given in the progression dictionary when a bar ends.
            elif newBar != barNumber:
                # Overlap doesn't matter.
                note=keys[progression[barNumber-1]]
                # Move the barNumber tracker up.
                barNumber=newBar
        # Fun fact, a bar is exactly 192 ticks long.
        length+=noteLength

def makeMelody2(pattern, progression, sectionLength, half,humanize=True):
    # This definition is the same as the other, except [odd,even] bars are silent when half is [true,false].
    sectionLength=sectionLength-(sectionLength%2)
    # Keep track of stuff.
    barNumber=newBar=1
    # Add a bunch of notes.
    length=0
    # Don't worry about this.
    breaker=False
    # The first note of a bar is going to be the note middle tonic (second octave).
    note=keys[progression[barNumber-1]] #same as keys[7]
    # Every section has its own length. If a section is length less than 2 bars long it gets skipped.
    while length<sectionLength*192 and not breaker:
        # pos=starting position, vol=velocity, key=pitch (60=C5), len=duration (48=quarter), pan=pan.
        # Generate a random note length.
        noteLength=r.choice([12,24,48,60,72])
        # odd are silent when half is true.
        if (half and barNumber%2==0) or (not half and barNumber%2==1):
            # Don't keep track of the note length as there is none.
            noteLength=0
            # The length marker needs to move up one bar.
            length+=192
            # The current bar needs to move up one bar.
            barNumber+=1
            # The next bar needs to move up one bar.
            newBar+=1
        else:
            # Fill the gap if it's too long to prevent overlap.
            # †# remove this once multiple tracks are implemented for J-cuts/negative transition lengths.
            if noteLength+length>sectionLength*192:
                noteLength=sectionLength*192-length
                # Flip the breaker, but still add the current note (or rest; see next if statement) to round it off.
                breaker=True
                # The while statement will end now.
            # Bar check. Can be merged with the previous block.
            if noteLength+length>192*barNumber:
                # The added note exceeds the current bar. Truncate the note length.
                # noteLength=(192*barNumber)-length
                # Go to the next bar
                newBar=barNumber+1
            # Very, very crude rest implementation/adding of notes.
            if not r.choice(range(10)) == 0:
                # Add the note.
                ET.SubElement(pattern, "note",
                              {"pos":str(length+(r.randint(-2,2)*humanize)),"vol": str(r.randint(60,100)),"key":str(note),
                               "len":str(noteLength+(r.randint(-2,2)*humanize)),"pan": "0"})
                # Choose a note and remember it.
                """A note about the melody:
                The next note should be one higher 30%, one lower 30%, two higher 10%, two lower 10%, the same 10%
                one of the tonics 5% each.
                All that without actually going out of bounds.
                So it could be a Markov chain-ish thing, but only if the note is one of the following:
                    The highest note (LMMSutil.keys[len(keys)-1])
                    The second-highest note (LMMSutil.keys[len(LMMSutil.keys)-2])
                    The middle tonic (LMMSutil.keys[len(LMMSutil.scale)], but only if the span is two octaves)
                    The lowest note (and the lower tonic) (LMMSutil.keys[0])
                    The second-lowest note (LMMSutil.keys[1])
                Different things happen on each of these."""
                # The bass doesn't care about any hypothetical next note.
                if newBar == barNumber:
                    # lol switch statements.
                    try:
                        # note's exact pitch is known, so the next note can always be relative.
                        a=keys.index(note)
                        # shift the index
                        a += {keys[len(keys)-1]: r.choice([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                               -2, -2, -2, -3, -3, 0, 0, 0,
                               -len(keys), -len(scale)]),
                              keys[len(keys)-2]: r.choice([-1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                               -2, -2, -2, 1, 1, 0, 0, 0,-(len(keys)-1),-(len(scale)-1)]),
                              keys[len(scale)]: r.choice([-1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1,
                               -2, -2, 2, 2, 0, 0, -(len(scale)),-(len(scale))]),
                              keys[1]: r.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1,2, 2, 2, -1, -1, -1, 0, 0, 0,
                               (len(scale)-1)]),
                              keys[0]: r.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 0, 0, 0, 0, len(scale),
                               len(scale)])}[note]
                        note=keys[a]
                    # Exceptions are really just if statements on crack.
                    except KeyError:
                        # Default action. Since it's unknown which note it is exactly, manipulating the note variable is easiest.
                        a=keys.index(note)
                        a=r.choice(
                            [a+1, a+1, a+1, a+1, a+1, a+1, a-1, a-1, a-1, a-1, a-1, a-1, a+2,
                             a+2, a-2, a-2, a, a, 0, len(scale)])
                        note=keys[a]
                # Change the note to the one given in the progression dictionary when a bar ends.
                elif newBar != barNumber:
                    # Overlap doesn't matter.
                    note=keys[progression[barNumber-1]]
                    # Move the barNumber tracker up.
                    barNumber=newBar
        # Fun fact, a bar is exactly 192 ticks long.
        length+=noteLength
"""
Drums
"""
def drumpattern(pattern,odds):
    # Drums have slightly different ways of doing things. Their len is -192 and their key is 57.
    # While that can be changed, that's how drum tracks are written in the file.
    # The position still works the same however, except it should be placed in spaces in multiples of, depending, 16.
    # That doesn't mean the second hit is on 16, but on 192/16=12.
    # Not going off-beat just yet, hits are on every half note instead.
    for y in range(16):
        ET.SubElement(pattern,"note",
                      {"pos":str(24*y),"vol":"100","key":"57","len":"-192","pan":"0"})if randbool(odds) else 1
