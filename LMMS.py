import xml.etree.ElementTree as ET # Time to grow some trees.
from copy import deepcopy

import LMMSutil
import random as r
type=0#r.choice([0,1])
# Variables
outroPosition=0
# This may be interesting later on.
numerator=4
"""
Fix the lead instruments
Humanize?"""
#-------------------------Sections------------------------------
"""
0-4 bars intro,4 or 8 bars for a section,4 or 8 bars for a chorus,0-4 bars bridge and 0-4 bars outro.
At minimum 2 sections and 1 chorus,adjusting tempo to suit the minute duration=12 bars.
At maximum 5 sections,3 chorus and the bumpers,so 4I-8S-8C-8S-8C-8S-4B-8S-8C-8S-4O=72 bars. Tempo won't need adjustment.
Basically the song duration will be taken into account (bpm*beats(=192/4)=1 maybe) to check on the upper bound.
There is no lower bound (at least as duration is considered).

The number of sections depends on the chorus count and the existence of a bridge.
Though in reality it's not necessary to keep tabs on it as the structure will be important first.
Let's keep it fixed for now,only the bridge will severly alter the structure,so the intro/outro can be included regardless.
intro-section-chorus-section(-chorus-section)(-bridge-section)(-chorus-section)-outro
    There's a guaranteed 1 chorus,there may be a second,there may be a third after the bridge.
    There may be 1 chorus and a bridge,the bridge will be played and the section following but no chorus follows it.

- Calculate the number of bars played (could be stored in a dictionary,sections and choruses are composed only once)
- Find the value that involves both BPM and tempo
- Set the upper tempo limit

"""
# Calculate section lengths in bars.
sectionLengths={"intro":r.randint(0,4),
    "verse":r.randint(4,8),
    "chorus":r.randint(4,8),
    "bridge":r.randint(0,4),
    "outro":r.randint(0,4),
    }
# A place to store valuables.
# Notes go here, the key (pitch), relative position (just add bars*192 for absolute) and length.
# They can be stored in pattern tags. The pattern tags can be stored here.
songDic={"intro":[],
    "verse":[],
    "chorus":[],
    "bridge":[],
    "outro":[],
}
# Calculate section counts.
chorusCount=r.randint(1,3)
# Graft the structure with keys of the dictionaries.
structure=["intro","verse","chorus","verse"]
# Extend structure bit
if chorusCount>1:structure.extend(["chorus","verse"])
# by
if sectionLengths["bridge"]>0:structure.extend(["bridge","verse"])
# bit
if chorusCount>2:structure.extend(["chorus","verse"])
# and finish by adding the outro.
structure.append("outro")
# Now there's a dictionary for section lengths in bars, one for section notes, and a list for the structure.
songbars=0
# Time to sum up the song length in bars.
for x in structure:
    songbars+=sectionLengths[x]
# Now songbars is a number between 12 and 72.
#spacer=int(songbars/4)
# Calculate upper limit to the bpm, e.g. with 12 bars a bpm of 12*4=48 is max for one minute.
#bpm=r.randint(songbars*2,songbars*4)
"""
So for the sake of argument,a minute song itself will be a total of 192 len/bar,4 beats/bar,120 beats/min
So 30 bars=30*192=5760 len per minute at 120bpm.
Alternatively it's bpm/numerator*192
Unless the denominator gets messed with,but that's something for another day.
"""
# Get a random tempo that's pretty low,it's okay for the song to be really long.
bpm=r.randint(int(songbars/2),songbars*2)
# A place to store valuables.
# Notes go here, the key (pitch), relative position (just add bars*192 for absolute) and length.
# They can be stored in pattern tags. The pattern tags can be stored here.
progDic={"intro":[],
    "verse":[],
    "chorus":[],
    "bridge":[],
    "outro":[],}
harmDic={"intro":[],
    "verse":[],
    "chorus":[],
    "bridge":[],
    "outro":[],}
#-------------------------Beginnings----------------------------
# Start with a single element.
lmms_project=ET.Element("lmms-project",{"version":"1.0","creator":"Devieus","creatorversion":"1.2.1","type":"song"})
# Make the tree out of that element.
tree=ET.ElementTree(lmms_project)
# Add things to the tree,starting with the header that contains the tempo,time signature,etc.
ET.SubElement(lmms_project,"head",{"timesig_numerator":str(numerator),
                                     "mastervol":"100",
                                     "timesig_denominator":"4",
                                     "bpm":str(bpm),
                                     "masterpitch":"0"})
# The song element contains the rest.
song=ET.SubElement(lmms_project,"song")
# The track container is the window containing all the tracks (the others will be coming up later).
trackcontainer=ET.SubElement(song,"trackcontainer",{"width":"1300",
                                            "x":"5",
                                            "y":"5",
                                            "maximized":"0",
                                            "height":"500",
                                            "visible":"1",
                                            "type":"song",
                                            "minimized":"0"})

#-------------------------Composing----------------------------
# Compile progressions for each section.
for section in progDic:
    # Generate a sequence of numbers between 0 (C in the key of 0) and 6 (B) starting with the tonic (0)
    progression=LMMSutil.generateProgression()
    # prog is a key that matches those in sectionLengths (which has lengths in bars)
    for bars in range(sectionLengths[section]):
        # The first entry is the tonic, but adding more doesn't matter.
        progDic[section].append(progression[bars%4])
        # The result is a list of indices for the keys list.
        # Harmonious sounds are several notes away from the progression.
        harmDic[section].append(progression[bars%4]+r.choice([2,3,4,7]))

# Great, now compose all the tracks for each section using those progressions.
for section in songDic:
    # If a section has length 0 it gets skipped.
    if sectionLengths[section]>0:
        # The pattern contains the notes.
        pattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        # The pattern contains the notes.
        bassPattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        # Every section has its own length (in bars).
        for length in range(sectionLengths[section]):
            # Whole thing is essentially two bass notes layered,starting with the one from the list.
            ET.SubElement(pattern,"note",{"pos":str(length*192),"vol":str(r.randint(60,100)),
                           "key":str(LMMSutil.keys[progDic[section][length]]),"len":"192","pan":"0"})
            # Also add this note as well.
            ET.SubElement(pattern,"note",{"pos":str(length*192),"vol":str(r.randint(60,100)),
                           "key":str(LMMSutil.keys[harmDic[section][length]]),"len":"192","pan":"0"})
            # To make the bass
            ET.SubElement(bassPattern,"note",{"pos":str(length*192),"vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),
                           "len":"48","pan":"0"})
            ET.SubElement(bassPattern,"note",{"pos":str(length*192+48),"vol":str(r.randint(60,100)),
                                                "key":str(LMMSutil.keys[progDic[section][length]]-12),
                                                "len":"48","pan":"0"})
            ET.SubElement(bassPattern,"note",{"pos":str(length*192+96),"vol":str(r.randint(60,100)),
                                                "key":str(LMMSutil.keys[harmDic[section][length]]),
                                                "len":"48","pan":"0"})
            ET.SubElement(bassPattern,"note",{"pos":str(length*192+144),"vol":str(r.randint(60,100)),
                                                "key":str(LMMSutil.keys[progDic[section][length]]),
                                                "len":"48","pan":"0"})
        # At this point, the flute needs representation as well.

        stingPattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        # However, it is done with full melodic tracks.
        LMMSutil.makeMelody(stingPattern,progDic[section],sectionLengths[section])
        # Now to add these patterns to the songDic.
        songDic[section].append(pattern)
        songDic[section].append(bassPattern)
        songDic[section].append(stingPattern)
"""
Hi,it's me again.

The track container contains tracks
Every track consists of two parts,the instrument track data,and the patterns.
    There's only one instrumenttrack,but an indefinite number patterns.

In this part,we only care about the contents of one pattern playing a layered bass. All whole notes.
"""
# This holds all the music. Type 0 is for instrument.
# Create a Nescaline track by default,pass instrumentName with this to change it.
# Adds all the bells and whistles in the process.
track=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(track,
    instrumentName=r.choice(["nes","tripleoscillator","bitinvader","sid","watsyn"]),basenote=str(57),type=type)
track2=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(track2,
    instrumentName=r.choice(["nes","tripleoscillator","bitinvader","sid","watsyn"]),basenote=str(57),type=type)
# Now to do the whole thing again,but for the mallet.
bassTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(bassTrack,
    instrumentName=[r.choice(["bitinvader","monstro","nes","tripleoscillator","sfxr","sid","watsyn"]),"malletsstk"][type],
    basenote=str(45),vol=100,type=type)
bassTrack2=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(bassTrack2,
    instrumentName=[r.choice(["bitinvader","monstro","nes","tripleoscillator","sfxr","sid","watsyn"]),"malletsstk"][type],
    basenote=str(45),vol=100,type=type)
# Now for the sting. Only once per bar,max.
fluteTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(fluteTrack,
    instrumentName=[r.choice(["bitinvader","monstro","nes","tripleoscillator","sfxr","sid","watsyn"]),"sf2player"][type],
    basenote=str(45),type=type)
fluteTrack2=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(fluteTrack2,
    instrumentName=[r.choice(["bitinvader","monstro","nes","tripleoscillator","sfxr","sid","watsyn"]),"sf2player"][type],
    basenote=str(45),type=type)
"""statelist=[]    # Change state only once per bar.
    statelist.append(LMMSutil.state)
    LMMSutil.state=r.choice(LMMSutil.statesDic[LMMSutil.state]["next"])"""# States don't do anything at the moment.

position=0
# Place the patterns according to the structure.
for section in structure:
    # If a section has length 0 it gets skipped.
    if sectionLengths[section]>0:
        if section == "verse":
            # Whole thing is essentially two bass notes layered,starting with the one from the list.
            track.append((deepcopy(songDic[section][0])))
            track[-1].attrib["pos"]=str(position)
            # And this melody
            bassTrack.append((deepcopy(songDic[section][1])))
            bassTrack[-1].attrib["pos"]=str(position)
            # And this flute, but only if the section calls for it.
            if sectionLengths[section]>3:
                fluteTrack.append((deepcopy(songDic[section][2])))
                fluteTrack[-1].attrib["pos"]=str(position+192*(sectionLengths[section]%4))
        else:
            # Whole thing is essentially two bass notes layered,starting with the one from the list.
            track2.append((deepcopy(songDic[section][0])))
            track2[-1].attrib["pos"]=str(position)
            # And this melody
            bassTrack2.append((deepcopy(songDic[section][1])))
            bassTrack2[-1].attrib["pos"]=str(position)
            # And this flute, but only if the section calls for it.
            if sectionLengths[section]>3:
                fluteTrack2.append((deepcopy(songDic[section][2])))
                fluteTrack2[-1].attrib["pos"]=str(position+192*(sectionLengths[section]%4))
        position+=sectionLengths[section]*192

#--------------------Stings-----------------------------------
# #birdPattern=ET.SubElement(birdTrack,"pattern",{"pos":"0","type":"0","muted":"0","name":LMMSutil.word(2),"steps":"16"})
pos=0
# The bird will play a fixed melody at random points.
# This melody will be a half-bar long, which means its total length is 96
birdMelody=ET.Element("pattern",{"pos":"0","type":"0","muted":"0","name":LMMSutil.word(2),"steps":"16"})
for x in range(2):
    # Melodies are four bars long (reduced to one bar due to the low BPM), it starts with a half note, followed by 4 quarter notes.
    ET.SubElement(birdMelody,"note",{"pos":str(96*x),"vol":str(r.randint(60,100)),
                                      "key":str(LMMSutil.keys[LMMSutil.scale[0]]+14),"len":"12","pan":"0"})
    # These four, as well as any subsequent note, are random notes from the major pentatonic.
    for pos in range(4):
        ET.SubElement(birdMelody,"note",{"pos":str(12+6*pos+96*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"6","pan":"0"})
    # This is followed by 3 eighth notes.
    for pos in range(3):
        ET.SubElement(birdMelody,"note",{"pos":str(36+4*pos+96*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"4","pan":"0"})
    # Followed again by 4 quarter notes.
    for pos in range(4):
        ET.SubElement(birdMelody,"note",{"pos":str(48+6*pos+96*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"6","pan":"0"})
    # This is followed by 4 eighth notes again.
    for pos in range(3):
        ET.SubElement(birdMelody,"note",{"pos":str(144+8*pos+192*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"8","pan":"0"})
    # And finally ends where it started.
    ET.SubElement(birdMelody,"note",{"pos":str(168+96*x),"vol":str(r.randint(60,100)),
                                      "key":str(LMMSutil.keys[LMMSutil.scale[0]+7]),"len":"12","pan":"0"})
# Make the track to put the melody on.
stingTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
# Give it a birdy sound.
LMMSutil.makeInstrument(stingTrack,instrumentName="monstro",basenote=str(33),vol="30",bird=1)
locations=[]
# Add the pattern a couple of time.
for x in range([1,5][type]):
    stingTrack.append(deepcopy(birdMelody))
    # And put it just about anywhere, as long as it doesn't exist there yet.
    pos=r.randint(5,songbars)*192
    while locations.count(pos)>1:
        pos=r.randint(5,songbars)*192
    stingTrack[-1].attrib["pos"]=str(pos)
    locations.append(pos)
#--------------------Drums-----------------------------------
# Add relaxing beats here.
track=ET.SubElement(trackcontainer,"track",{"type":"1","muted":"0","solo":"0","name":LMMSutil.word(2)})
track2=ET.SubElement(trackcontainer,"track",{"type":"1","muted":"0","solo":"0","name":LMMSutil.word(2)})
# A pair of BBtrack element containers.
bbtrack=ET.SubElement(track,"bbtrack")
# Inside this trackcontainer is another trackcontainer. This is the B&B window.
drumcontainer=ET.SubElement(bbtrack,"trackcontainer",{"width":"600",
                                            "x":"600",
                                            "y":"600",
                                            "maximized":"0",
                                            "height":"200",
                                            "visible":"1",
                                            "type":"song",
                                            "minimized":"0"})
# Add three drums to the BBtrack.
for x in range(3):
    # From here on it's the same old song. One instrument per drum sound.
    drumtrack=ET.SubElement(drumcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
    # Add instrument.
    instrumenttrack=LMMSutil.makeInstrument(drumtrack,fxch="2",pan=x,instrumentName=r.choice(["sid","malletsstk","nes","sfxr"]),drum=1,type=2)
    # And the drum pattern.
    pattern=ET.SubElement(drumtrack,"pattern",{"pos":"0","type":"0","muted":"0","name":"","steps":str(32)})
    for y in range(16):
        # Drums have slightly different ways of doing things. Their len is -192 and their key is 57.
        # While that can be changed, that's how drum tracks are written in the file.
        # The position still works the same however, except it should be placed in spaces in multiples of, depending, 16.
        # That doesn't mean the second hit is on 16, but on 192/16=12.
        # Not going off-beat just yet, hits are on every half note instead.
        ET.SubElement(pattern,"note",{"pos":str(24*y),"vol":"100","key":"57","len":"-192","pan":"0"}) if r.choice([True,False,False,False]) else 1
    # So here's how multiple drum tracks happen:
    pattern = ET.SubElement(drumtrack,"pattern",{"pos":"0","type":"0","muted":"0","name":"","steps":"32"})
    # You just kinda make another pattern.
    for y in range(16):
        # Drums ( `)^( `)
        ET.SubElement(pattern,"note",{"pos":str(24*y),"vol":"100","key":"57","len":"-192","pan":"0"}) if r.choice([True,False]) else 1

# Now to add this drumtrack (these are basically the patterns,but in the song window).
x=0
for section in structure:
    # Check to see if the section is the right one. No drums in intros, outros and bridges.
    if section=="verse":
        ET.SubElement(track,"bbtco",
                            {"usesyle":"1","name":"",
                            "len":str(sectionLengths["verse"]*192),
                            "color":"4294901760",
                            "pos":str(x),
                            "muted":"0"})
    # bbtco elements tell the main trackcontainer which track is active when.
    elif section=="chorus":
        ET.SubElement(track2,"bbtco",
                            {"usesyle":"1","name":"",
                            "len":str(sectionLengths["chorus"]*192),
                            "color":"4294901760",
                            "pos":str(x),
                            "muted":"0"})
    x+=sectionLengths[section]*192

#----------------------------FX--------------------------------
# This holds all the main tracks,like this automation track (type 6).
# The automation track,it actually holds all the global automation tracks,not just one of them.
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
# That's because 192 is divisible by 1,2,3,4,6,8,12,and any other power of 2 multiplied by 3.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Denominator",
                                                   "pos":"0",
                                                   "len":"192"})
# And any power of 2 of course,right until 64. That's because of triplets. It does make quintuplets a little awkward though.
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
    FXChannel=ET.SubElement(FXMixer,"fxchannel",{"num":str(x+1),
                                                     "muted":"0",
                                                     "volume":["1","0.6"][x],
                                                     "name":str(LMMSutil.word(2))})
    # Mostly the same,effects can be applied here.
    LMMSutil.FXChain(FXChannel)
    # The difference is these have a send tag for each channel it's sending to.
    ET.SubElement(FXChannel,"send",{"channel":"0","amount":"1"})
# Set the loop points.
ET.SubElement(song,"timeline",{"lp0pos":"0","lp1pos":str(songbars*192),"lpstate":"1"})
# An LFO controller.
controller=ET.SubElement(song,"controllers")
# And an LFO.
ET.SubElement(controller,"lfocontroller",{"speed":"3",
            "phase":str(r.randint(0,360)),
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
# And another.
ET.SubElement(controller,"lfocontroller",{"speed":"5.555",
            "phase":str(r.randint(0,360)),
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
title=LMMSutil.word(1)
for x in range(4):
    if title[-1]!=" ":
        # Add a space with certain chance.
        title+=" " if r.randint(1,2)==1 else ""
    title+=LMMSutil.word(1)
title=title.title()+".mmp"
print(title)
print("structure:"+str(structure))
print("lengths:"+str(sectionLengths))
print("songbars "+str(songbars))
# The opening of the file that always closes automatically with the with statement.
with open(title,'wb') as LMMS:
    # Write the tree.
    tree.write(LMMS)