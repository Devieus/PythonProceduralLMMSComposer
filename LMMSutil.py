import xml.etree.ElementTree as ET # Time to grow some trees.
import random as r
import base64
# This makes non-drums.
# This also makes drums. For the most part it's the same as the instruments, but the values are going to be different.
# For instance, if it makes a Nescaline drum, it makes sure the noise channel is on.
def createInstrument(instrumentName,drum=0):
    if instrumentName=="nes": return{"vol":"1", #master volume.
    "vibr": "0", #master vibrato (depth only).
    "on1":["1","0"][drum], #enable channel 1, a square wave channel.
    "vol1":"15", #volume of channel 1.
    "crs1":"0", #course detune of channel 1.
    "envon1":"0", #enable envelope of channel 1.
    "envlen1":"0", #decay length of channel 1 (requires envon to be 1).
    "envloop1":"0", #repeat channel 1 after decayed.
    "dc1":str(r.randint(0,3)), #square wave duty [0,3]
    "sweep1":"0", #enable sweep for channel 1.
    "swamt1":"0", #sweep amount [-7,7]
    "swrate1":"0", #sweep rate [0,7]
    "on2":"0", #channel 2 is also a square wave and can do the exact same thing as 1.
    "vol2":"15",
    "crs2":"0",
    "envon2":"0",
    "envlen2":"0",
    "envloop2":"0",
    "dc2":"2",
    "sweep2":"0",
    "swamt2":"0",
    "swrate2":"0",
    "on3":"0", #channel 3 is a tri wave. It can only do two things.
    "vol3":"15",
    "crs3":"0",
    "on4":["0","1"][drum], #channel 4 is the noise channel, used for drums.
    "vol4":"15",
    "nfreq4":str(r.choice(range(7))+3), #noise frequency [0,15], ignored if note is enabled.
    "envon4":"1",
    "envlen4":"0",
    "envloop4":"0",
    "nswp4":"0", #noise sweep [-7,7]. Negative numbers go down, positive up. bigger numbers go faster.
    "nq4":"0", #quantization, pitch.
    "nmode4":r.choice(["0","1"]), #noise mode, 1 is more melodic.
    "nfrqmode4":"0" #note, causes pitch to change the average frequency.
    }
    # Triple oscillator, for now, as well as the few next to this, no specifics.
    #  wavetype2="0" finel1="0" wavetype0="0" pan1="0" modalgo1="2" coarse0="0" phoffset0="0" finer2="0" userwavefile0="" finer0="0" modalgo2="2" vol0="33" pan2="0" coarse1="-12" userwavefile2="" vol2="33" vol1="33" phoffset2="0" finel2="0" coarse2="-24" finer1="0" pan0="0" userwavefile1="" phoffset1="0" wavetype1="0" stphdetun2="0" modalgo3="2" stphdetun0="0" finel0="0" stphdetun1="0"
    if instrumentName=="tripleoscillator": return {"modalgo2":"2", #osc1+2, how osc 2 modules osc 1.
    "modalgo3":"2",#osc2+3. phase modulate 0, amp modulate 1, mix 2, sync 3, frequency modulate 4.
    "wavetype0":"2", #wave type, sine 0, tri 1, saw 2, square 3, moog 4, exponential 5, noise 6, custom 7
    "userwavefile0":"", #use a custom wave file as oscillator. Type must be 7
    "vol0":"10", #oscillator volume [0,200]
    "pan0":"0", #pan of osc.
    "coarse0":"0", #course detune [-24,24] in semitones (5 octave range)
    "finel0":"0", #left channel detune [-100,100].
    "finer0":"0", #right channel detune.
    "phoffset0":"0", #phase offset [0-360] degrees (2 square waves cancel eachother out at 180).
    "stphdetun0":"0", #stereo phase detune (left channel)
    "wavetype1":"2", #all oscilllators are identical.
    "userwavefile1":"",
    "vol1":"10",
    "pan1":"0",
    "coarse1":"0",
    "finel1":"-5",
    "finer1":"5",
    "stphdetun1":"0",
    "modalgo1":"2",
    "phoffset1":"0",
    "wavetype2":"0", #osc 3
    "userwavefile2":"",
    "vol2":"0",
    "pan2":"0",
    "coarse2":"-24",
    "finel2":"0",
    "finer2":"0",
    "phoffset2":"0",
    "stphdetun2":"0",}
    if instrumentName=="sfxr": return {"version": "1", #does nothing.
    "waveForm": ["0","3"][drum], #waveform, square 0, saw 1, sine 2, noise 3. All other values are normals.
    "att": "0", #attack.
    "hold": str([str(r.choice(range(10))/10),"0"][drum]), #hold (time until sustain).
    "sus": "0", #punch (very short).
    "dec": ["0.4","0.1"][drum], #decay (sustain time).
    "startFreq": ["0.352",str(r.choice(range(600))/1000+.2)][drum], #0.352 is natural, use a range for drums.
    "minFreq": "0", #slide cap, but only downards.
    "slide": "0", #slide amount [-1,1], magnitude scales both speed and depth. Loses effectiveness beyond .25.
    "dSlide": "0", #delta slide, or delayed slide. Kicks in after slide finishes.
    "vibDepth": "0", #vibrato depth, best below 0.05.
    "vibSpeed": "0", #vibrato speed, both need to be set to work.
    "changeAmt": "0", #change the held note to a different pitch.
    "changeSpeed": "0", #time it takes to change pitch, <0.01 is 1 sec, anything higher is faster.
    "sqrDuty": "0", #square wave form, 0=50%, 1=0%.
    "sqrSweep": "0", #sweep to 50% on negative, to 0% on positive, with magnitute changing speed.
    "repeatSpeed": "0", #repeat the whole note played after a delay once (including change and sweeps). Higher is sooner.
    "phaserOffset": "0", #overlays a second wave on a different phase, around 0.626 cancels symetric waves (square and sine)
    "phaserSweep": "0", #sweeps phase one revolution, magintute changes speed.
    "lpFilCut": "1", #low pass filter.
    "lpFilCutSweep": "0", #sweeps cutoff level.
    "lpFilReso": "0", #low pass resonance.
    "hpFilCut": "0", #high pass filter.
    "hpFilCutSweep": "0", #sweeps cutoff level.
    }
    # Might add others later, depending.


# Make an instrument and attach it to the parent parameter.
def makeInstrument(parent, pan=2, fxch="0", pitchrange="1", pitch="0",
                   basenote="57", vol="100", instrumentName="nes",drum=0):
    # Set the basic variables every track has, pan, volume, that sort of stuff.
    instrumentTrack=ET.SubElement(parent,"instrumenttrack",{"pan":["-60","60","0"][pan],
                                                           "fxch":fxch,
                                                           "pitchrange":pitchrange,
                                                           "pitch":pitch,
                                                           "basenote":basenote,
                                                           "vol":["60",vol][drum]})
    # A branching path emerges, depending on the instrument of choice. (TBA)
    """These are the instruments available:
        nes(=Nescaline)
        tripleoscillator
        audiofileprocessor***
        bitinvader*
        papu(=FreeBoy)*
        kicker
        lb302
        malletsstk(=Mallets)
        monstro
        OPL2(=OpulenZ)(quiet)
        organic
        sfxr
        sid
        vibedstrings(=Vibed)*
        watsyn*
        zynaddsubfx**
        
        * Uses a graph, optional for freeboy.
        ** Embedded synth
        *** Relative file paths
        """
    # Every instrument has a specific name, "nes" is for nescaline.
    instrument=ET.SubElement(instrumentTrack,"instrument", {"name":instrumentName})
    # Only the first tab is depending on the actual instrument name, the others are the same regardless.
    ET.SubElement(instrument,instrumentName,createInstrument(instrumentName,drum))
    # This is where the branching path ends.
    # eldata is for the envelope tab.
    eldata=ET.SubElement(instrumentTrack,"eldata",{"fres":"0.5",
                                                   "ftype":"0",
                                                   "fcut":"14000",
                                                   "fwet":"0"})
    # Envelope tab part 1, volume envelope.
    ET.SubElement(eldata,"elvol",{"lspd_denominator":"4",
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

def FXChain(parent):
    #return an FX chain that contains the TAP reverberator.
    fxchain=ET.SubElement(parent, "fxchain", {"numofeffects": "1", "enabled": "1"})
    fx=ET.SubElement(fxchain,"effect",{"name":"ladspaeffect",
        "autoquit_numerator":"4",
        "on":"1",
        "wet":"1",
        "gate":"0",
        "autoquit_syncmode":"0",
        "autoquit_denominator":"4",
        "autoquit":"1"})
    controls=ET.SubElement(fx,"ladspacontrols",{"ports":"8"})
    ET.SubElement(controls,"port00",{"data":"1000"}) #delay (ms)
    ET.SubElement(controls,"port01",{"data":"0"}) #dry
    ET.SubElement(controls,"port02",{"data":"0"}) #wet
    ET.SubElement(controls,"port03",{"data":"1"}) #comb
    ET.SubElement(controls,"port04",{"data":"1"}) #allpass
    ET.SubElement(controls,"port05",{"data":"1"}) #bandpass
    ET.SubElement(controls,"port06",{"data":"1"}) #enhanced stereo
    ET.SubElement(controls,"port07",{"data":str(r.randint(0,42))}) #type
    key=ET.SubElement(fx,"key")
    ET.SubElement(key,"attribute",{"name":"file","value":"tap_reverb"})
    ET.SubElement(key,"attribute",{"name":"plugin","value":"tap_reverb"})
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
# A key is chosen at random, C is 0, B is 7, all exists in between.
key=r.randint(0,7)
# Major scale, change for modes or esotheric scales. Add the key.
scale=[0+key,2+key,4+key,5+key,7+key,9+key,11+key]
# Add the scale two times times
for x in range(2):
    # But do it in a way that adds it in different octaves.
    for y in scale:
        # Every time it gets to add a multiple of 12 in some way.
        keys.append(y+(12*(x+3)))

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
vow=['a','e','i','o','u','oi','ea']
# Make a syllable.
def syl():
    # The result string.
    result=''
    #Does it start with a consonant?
    if r.choice([True,False]):
        result+=r.choice(cons)
    #Then add a vowel
    result+=r.choice(vow)
    #Does it end with a consonant?
    if r.choice([True,False]):
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