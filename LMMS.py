import xml.etree.ElementTree as ET # Time to grow some trees.
from copy import deepcopy

import LMMSutil
import random as r
# Variables
outroPosition=0
"""
So for the sake of argument, a minute song itself will be a total of 192 len/bar, 4 beats/bar, 120 beats/min
So 30 bars=30*192=5760 len per minute at 120bpm.
Alternatively it's bpm/numerator*192
Unless the denominator gets messed with, but that's something for another day.

For meditation music, there is no such thing as structure.
There are tracks, usually few, occasionally many.
There's always a bass with huge sustains, sometimes that's all there is.
The bass can be layered.
The scale of the song is mostly irrelevant, it's all about the progression.

"""
# A place to store valuables.
# Notes go here, the key (pitch), relative position (just add bars*192 for absolute) and length.
# They can be stored in pattern tags. The pattern tags can be stored here.

# Graft the structure with keys of the dictionaries.

# Determine how long the song should be.
songbars=60
# Get a random tempo that's pretty low, it's okay for the song to be really long.
bpm=r.randint(int(songbars/3),int(songbars/2))
# This may be interesting later on.
numerator=4
# Generate a sequence of numbers between 0 (C in the key of 0) and 6 (B) starting with the tonic (0).
progList=[0]
# Harmonious sounds are 2 or 3 notes away from the tonic.
harmList=[r.randint(2,3)]
#-------------------------Beginnings----------------------------
# Start with a single element.
lmms_project=ET.Element("lmms-project", {"version": "1.0", "creator": "Devieus", "creatorversion": "1.2.1", "type": "song"})
# Make the tree out of that element.
tree=ET.ElementTree(lmms_project)
# Add things to the tree, starting with the header that contains the tempo, time signature, etc.
ET.SubElement(lmms_project, "head", {"timesig_numerator": str(numerator),
                                     "mastervol": "100",
                                     "timesig_denominator": "4",
                                     "bpm": str(bpm),
                                     "masterpitch": "0"})
# The song element contains the rest.
song=ET.SubElement(lmms_project, "song")
# The track container is the window containing all the tracks (the others will be coming up later).
trackcontainer=ET.SubElement(song, "trackcontainer", {"width": "1300",
                                            "x":"5",
                                            "y":"5",
                                            "maximized":"0",
                                            "height":"300",
                                            "visible":"1",
                                            "type":"song",
                                            "minimized":"0"})
# This holds all the music. Type 0 is for instrument.
track = ET.SubElement(trackcontainer, "track", {"type": "0", "muted": "0", "solo": "0", "name": LMMSutil.word(2)})
# Creates a Nescaline track by default, pass instrumentName with this to change it.
# Adds all the bells and whistles in the process.
instrumentName=r.choice(["nes", "tripleoscillator", "bitinvader","sid","watsyn"])
instrumenttrack = LMMSutil.makeInstrument(track, instrumentName=instrumentName,basenote=str(57))
#-------------------------Composing----------------------------
# Compile progressions.
for bar in range(songbars):
    # The result is a list of indices for the keys list.
    progList.append(r.randint(0, 6))
    # No two notes the same.
    if progList[-1]==progList[-2]:
        progList[-1]+=1
    # Harmonious sounds are 2 or 3 notes away from the progList.
    harmList.append(progList[bar+1]+r.randint(2, 3))
"""
Hi, it's me again.

The track container contains tracks
Every track consists of two parts, the instrument track data, and the patterns.
    There's only one instrumenttrack, but an indefinite number patterns.

In this part, we only care about the contents of one pattern playing a layered bass. All whole notes.
"""
# The pattern contains the notes.
pattern=ET.SubElement(track,"pattern",{"pos":0,"type":"0","muted":"0","name":LMMSutil.word(2),"steps":"16"})
for bar in range(songbars):
    # Whole thing is essentially two bass notes layered, starting with the one from the list.
    ET.SubElement(pattern,"note",{"pos":str(192*bar),"vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progList[bar]]),"len":"192","pan":"0"})
    # Add this note as well.
    ET.SubElement(pattern,"note",{"pos":str(192*bar),"vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[harmList[bar]]),"len":"192","pan":"0"})
#--------------------Drums-----------------------------------
# Add relaxing beats here.
track=ET.SubElement(trackcontainer,"track",{"type":"1","muted":"0","solo":"0","name":LMMSutil.word(2)})
# A BBtrack element container.
bbtrack=ET.SubElement(track,"bbtrack")
# Inside this trackcontainer is another trackcontainer.
drumcontainer=ET.SubElement(bbtrack,"trackcontainer",{"width": "600",
                                            "x":"600",
                                            "y":"300",
                                            "maximized":"0",
                                            "height":"400",
                                            "visible":"1",
                                            "type":"song",
                                            "minimized":"0"})
# Add three drums to the BBtrack.
for x in range(3):
    # From here on it's the same old song. One instrument per drum sound.
    drumtrack=ET.SubElement(drumcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
    # Add instrument.
    instrumenttrack=LMMSutil.makeInstrument(drumtrack,fxch="2",pan=x,instrumentName="sfxr",drum=1)
    # And the drum pattern.
    pattern = ET.SubElement(drumtrack,"pattern",{"pos":"0","type":"0","muted":"0","name":"","steps":"32"})
    for y in range(16):
        # Drums have slightly different ways of doing things. Their len is -192 and their key is 57.
        # While that can be changed, that's how drum tracks are written in the file.
        # The position still works the same however, except it should be placed in spaces in multiples of, depending, 16.
        # That doesn't mean the second hit is on 16, but on 192/16=12.
        # Not going off-beat just yet, hits are on every half note instead.
        ET.SubElement(pattern,"note",{"pos":str(24*y),"vol":"100","key":"57","len":"-192","pan":"0"}) if r.choice([True,False,False,False]) else 1

# Now to add this drumtrack (these are basically the patterns, but in the song window).
ET.SubElement(track,"bbtco",
            {"usesyle":"1","name":"",
            "len":str(songbars*192),
            "color":"4294901760",
            "pos":"0",
            "muted":"0"})

#----------------------------FX--------------------------------
# This holds all the main tracks, like this automation track (type 6).
# The automation track, it actually holds all the global automation tracks, not just one of them.
automationTrack=ET.SubElement(song,"track",{"muted":"0",
                                            "type":"6",
                                            "name":"Automation track",
                                            "solo":"0"})

# An empty automation track since automation tracks don't have properties. Not super conveniently named.
ET.SubElement(automationTrack,"automationtrack")
# So getting back to that bar length again,
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Numerator",
                                                   "pos":"0",
                                                   "len":"192"})
# That's because 192 is divisible by 1, 2, 3, 4, 6, 8, 12, and any other power of 2 multiplied by 3.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Denominator",
                                                   "pos":"0",
                                                   "len":"192"})
# And any power of 2 of course, right until 64. That's because of triplets. It does make quintuplets a little awkward though.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Tempo",
                                                   "pos":"0",
                                                   "len":"192"})
# Master volume.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Master Volume",
                                                   "pos":"0",
                                                   "len":"192"})
# Master pitch.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Master pitch",
                                                   "pos":"0",
                                                   "len":"192"})
# FX mixer
FXMixer=ET.SubElement(song,"fxmixer",{"x":"5",
                                      "y":"310",
                                      "width":"561",
                                      "height":"349",
                                      "maximized":"0",
                                      "visible":"1",
                                      "minimized":"0"})
# FX channel
FXChannel=ET.SubElement(FXMixer,"fxchannel",{"num":"0",
                                           "muted":"0",
                                           "volume":"1",
                                           "name":"master"})
# FX chain
LMMSutil.FXChain(FXChannel,True,True)

# Make two subchannels
for x in range(2):
    FXChannel = ET.SubElement(FXMixer, "fxchannel", {"num": str(x+1),
                                                     "muted": "0",
                                                     "volume": ["1","0.07"][x],
                                                     "name": str(LMMSutil.word(2))})
    # Mostly the same, effects can be applied here.
    LMMSutil.FXChain(FXChannel)
    # The difference is these have a send tag for each channel it's sending to.
    ET.SubElement(FXChannel,"send",{"channel":"0","amount":"1"})
# Set the loop points.
ET.SubElement(song,"timeline",{"lp0pos":"0","lp1pos":str((songbars)*192),"lpstate":"1"})
# An LFO controller.
controller=ET.SubElement(song,"controllers")
# And an LFO.
ET.SubElement(controller,"lfocontroller",{"speed":"5.555",
            "phase":"0",
            "multiplier":"0",
            "userwavefile":"",
            "speed_numerator":"4",
            "amount":"0.555",
            "type":"1",
            "name":LMMSutil.word(2),
            "base":"0.5",
            "speed_denominator":"4",
            "speed_syncmode":"0",
            "wave":"5"})
#-------------------------Writing------------------------------
# A random word is a great name for a song.
title=(LMMSutil.word(1)+" "+LMMSutil.word(2)+" "+LMMSutil.word(1)).title()+".mmp"
# The opening of the file that always closes automatically with the with statement.
with open(title,'wb') as LMMS:
    # Write the tree.
    tree.write(LMMS)
