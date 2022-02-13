import xml.etree.ElementTree as ET # Time to grow some trees.
from copy import deepcopy

import LMMSutil
import random as r
"""There are an unlimited amount of genres this could make, but it is finite, so these are the song types:
0: Rock-ish
1: Meditative slow thing
2: Ska-ish
3: Calypso
4: Free jazz"""
songType=r.choice(range(5))
print(f"songtype: {songType}")
# Variables
outroPosition=0
# A bar is 192 long, if the numerator and denominator is 4
# and 144 when the signature is 3/4.
# If the denominator remains fixed, bar lengths would be numerator*48
numerator=4
ticks=numerator*48
"""Vocals?
More/different animals (or just better stings in general)
Genres: calypso, freejazz
Loop endpoint"""
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
sectionLengths={"intro":r.randint(1,3)*2,
    "verse":r.randint(4,8),
    "chorus":r.randint(4,8),
    "bridge":r.randint(4,8),
    "outro":r.randint(0,5),
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
if songType==2:
        structure.extend(["chorus","verse"])
        sectionLengths["outro"]=5
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
So for the sake of argument, a minute song itself will be a total of 192 len/bar, 4 beats/bar, 120 beats/min
So 30 bars=30*192=5760 len per minute at 120bpm.
Alternatively it's bpm/numerator*192
Unless the denominator gets messed with,but that's something for another day.
"""
# Get a random tempo that's pretty low, it's okay for the song to be really long.
bpm=r.randint(int(songbars),songbars*4)
# Meditative tracks are much slower. Maybe.
if songType==1: bpm=5*LMMSutil.clamp(bpm,20,60)
# Calypso is double time.
if songType==4:
    # Technically the numerator should be 2, but that just makes all notes be half length in the current form.
    bpm*=2
    # Double all lengths.
    for x in sectionLengths:
        sectionLengths[x]*=2
    # Also double songbars.
    songbars*=2
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
if songType==1:
    # Meditative tracks have only one section, it's just really, really long.
    sectionLengths={"1":80} # Like, really long. 80*4=5 minutes on 60 bpm
    songDic={"1":[]}
    progDic={"1":[]}
    harmDic={"1":[]}
    structure=["1"]
    songbars=5*80
#-------------------------Beginnings----------------------------
# Start with a single element.
lmms_project=ET.Element("lmms-project",{"version":"1.0","creator":"Devieus","creatorversion":"1.2.2","type":"song"})
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
trackcontainer=ET.SubElement(song,"trackcontainer",{"width":"1620",
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
        harmDic[section].append(progression[bars%4]+r.choice([2,3,4]))
bassTemplate=LMMSutil.bassTemplate(numerator)
chorusBassTemplate=LMMSutil.bassTemplate(numerator)
# Great, now compose all the tracks for each section using those progressions.
for section in songDic:
    # If a section has length 0 it gets skipped.
    if sectionLengths[section]>0:
        # The pattern contains the notes.
        bassPattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        # The pattern contains the notes.
        rhythmPattern=ET.Element("pattern", {"pos":0, "type": "0", "muted": "0", "name":section, "steps": "16"})
        # Every section has its own length (in bars).
        for length in range(sectionLengths[section]):
            if songType==2:
                # In ska, the bass and rhythm plays only on the off-beats. That means they play at positions 24, 24+(24*2), 24+(24*4), etc
                for x in range(4):
                    # Whole thing is essentially two bass notes layered, starting with the one from the list.
                    ET.SubElement(bassPattern, "note", {"pos": str(length*ticks+24+48*x), "vol": str(r.randint(60, 100)),
                                                        "key": str(LMMSutil.keys[progDic[section][length]]),
                                                        "len": "24", "pan":"0"})
                    # Also add this note as well.
                    ET.SubElement(bassPattern, "note", {"pos": str(length*ticks+24+48*x), "vol": str(r.randint(60, 100)),
                                                        "key": str(LMMSutil.keys[harmDic[section][length]]),
                                                        "len": "24", "pan":"0"})
                # Splendid, now for the rhythm.
                for x in range(4):
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+24+48*x),"vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),
                "len":"24","pan":"0"})
                """ET.SubElement(rhythmPattern,"note",{"pos":str(length*192+24+48*1),"vol":str(r.randint(60,100)),
                "key":str(LMMSutil.keys[progDic[section][length]]+12),"len":"24","pan":"0"})
                ET.SubElement(rhythmPattern,"note",{"pos":str(length*192+24+48*2),"vol":str(r.randint(60,100)),
                "key":str(LMMSutil.keys[harmDic[section][length]]),"len":"24","pan":"0"})
                ET.SubElement(rhythmPattern,"note",{"pos":str(length*192+24+48*3),"vol":str(r.randint(60,100)),
                "key":str(LMMSutil.keys[progDic[section][length]]),"len":"24","pan":"0"})"""
            else:
                # Whole thing is essentially two bass notes layered, starting with the one from the list.
                ET.SubElement(bassPattern,"note",{"pos":str(length*ticks),"vol":str(r.randint(60,100)),
                               "key":str(LMMSutil.keys[progDic[section][length]]),"len":f"{ticks}","pan":"0"})
                # Also add this note as well.
                ET.SubElement(bassPattern,"note",{"pos":str(length*ticks),"vol":str(r.randint(60,100)),
                               "key":str(LMMSutil.keys[harmDic[section][length]]),"len":f"{ticks}","pan":"0"})
                # To make the rhythm,
                if section=="chorus":
                    # Place the right notes in the right place.
                    for x in range(numerator):
                        ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+sum(chorusBassTemplate[:x])),
                        "vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),"len":str(chorusBassTemplate[0]),"pan":"0"})
                    
                    """
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks),
                    "vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),"len":str(chorusBassTemplate[0]),"pan":"0"})
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+chorusBassTemplate[0]),
                    "vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]-12),"len":str(chorusBassTemplate[1]),"pan":"0"})
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+chorusBassTemplate[0]+chorusBassTemplate[1]),
                    "vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[harmDic[section][length]]),"len":str(chorusBassTemplate[2]),"pan":"0"})
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+chorusBassTemplate[0]+chorusBassTemplate[1]+chorusBassTemplate[2]),
                    "vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),"len":str(chorusBassTemplate[3]),"pan":"0"})
                    """
                else:
                    # Trust me, this should work.
                    for x in range(numerator):
                        ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+sum(bassTemplate[:x])),
                        "vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),"len":str(bassTemplate[x]),"pan":"0"})
                    """
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks),"vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[progDic[section][length]]),
                    "len":str(bassTemplate[0]),"pan":"0"})
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+bassTemplate[0]),
                    "vol":str(r.randint(60,100)),
                    "key":str(LMMSutil.keys[progDic[section][length]]-12),
                    "len":str(bassTemplate[1]),"pan":"0"})
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+bassTemplate[0]+bassTemplate[1]),
                    "vol":str(r.randint(60,100)),
                    "key":str(LMMSutil.keys[harmDic[section][length]]),
                    "len":str(bassTemplate[2]),"pan":"0"})
                    ET.SubElement(rhythmPattern,"note",{"pos":str(length*ticks+bassTemplate[0]+bassTemplate[1]+bassTemplate[2]),
                    "vol":str(r.randint(60,100)),
                    "key":str(LMMSutil.keys[progDic[section][length]]),
                    "len":str(bassTemplate[3]),"pan":"0"})
                    """
        # At this point,the lead needs representation as well.
        leadPattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        # However, it is done with full melodic tracks.
        LMMSutil.makeMelody(leadPattern,progDic[section],sectionLengths[section])
        # The call track as the lead.
        callPattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        LMMSutil.makeMelody2(callPattern, progDic[section], sectionLengths[section],False)
        # The response track to talk with the call.
        responsePattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        LMMSutil.makeMelody2(responsePattern,progDic[section],sectionLengths[section],False)
        # Now to add these patterns to the songDic.
        songDic[section].append(bassPattern)
        songDic[section].append(rhythmPattern)
        songDic[section].append(leadPattern)
        songDic[section].append(callPattern)
        songDic[section].append(responsePattern)
"""
Hi,it's me again.

The track container contains tracks
Every track consists of two parts,the instrument track data,and the patterns.
    There's only one instrumenttrack,but an indefinite number patterns.

In this part,we only care about the contents of one pattern playing a layered bass. All whole notes.
"""
# ---------Tracks----------
# This holds all the music. Type 0 is for instrument.
# Create a Nescaline track by default,pass instrumentName with this to change it.
# Adds all the bells and whistles in the process.
bassTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(bassTrack,instrumentName=r.choice(["bitinvader","nes","papu","sid","tripleoscillator","watsyn"]),basenote="69",type=songType,vol="30")

bassTrack2=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(bassTrack2,instrumentName=r.choice(["bitinvader","nes","papu","sid","tripleoscillator","watsyn"]),basenote="69",type=songType,vol="30")

bassTrackBridge=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
LMMSutil.makeInstrument(bassTrackBridge,instrumentName=r.choice(["bitinvader","nes","papu","sid","tripleoscillator","watsyn"]),basenote="69",type=songType,vol="30")

# Now to do the whole thing again, but for the harmony.
harmonyTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
instrumentName="malletsstk" if songType==1 else r.choice(["bitinvader","monstro","nes","papu","sfxr","sid","tripleoscillator","watsyn"])
LMMSutil.makeInstrument(harmonyTrack,instrumentName=instrumentName,basenote="45",vol="30",type=songType)

harmonyTrack2=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
instrumentName="malletsstk" if songType==1 else r.choice(["bitinvader","monstro","nes","papu","sfxr","sid","tripleoscillator","watsyn"])
LMMSutil.makeInstrument(harmonyTrack2,instrumentName=instrumentName,basenote="45",vol="30",type=songType,env=1)

harmonyTrackBridge=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
instrumentName="malletsstk" if songType==1 else r.choice(["bitinvader","monstro","nes","papu","sfxr","sid","tripleoscillator","watsyn"])
LMMSutil.makeInstrument(harmonyTrackBridge,instrumentName=instrumentName,basenote="45",vol="30",type=songType,env=1)

# Now for the sting. Only once per bar, max.
leadTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
# Only meditative uses SF2, use a boolean to select it inline.
LMMSutil.makeInstrument(leadTrack,instrumentName=[r.choice(["bitinvader","monstro","nes","papu","sfxr","sid","tripleoscillator","watsyn"]),"sf2player"][songType==1],basenote="45",type=songType)
callTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
# It might not necessarily be only meditative, though genres that Also use SF2 are going to be an issue.
LMMSutil.makeInstrument(callTrack,instrumentName=[r.choice(["bitinvader","nes","papu","sfxr","sid","tripleoscillator","watsyn"]),"sf2player"][songType==1],basenote="45",type=songType)
# Call/response track that harmonizes during the verse.
responseTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
instrumentName="sf2player" if songType==1 else r.choice(["bitinvader","nes","papu","sfxr","sid","tripleoscillator","watsyn"])
LMMSutil.makeInstrument(responseTrack,instrumentName=instrumentName,basenote="57", type=songType)
"""statelist=[]    # Change state only once per bar.
    statelist.append(LMMSutil.state)
    LMMSutil.state=r.choice(LMMSutil.statesDic[LMMSutil.state]["next"])"""# States don't do anything at the moment.
# ---------Placement-------
position=0
# Place the patterns according to the structure.
for section in structure:
    # If a section has length 0 it gets skipped.
    if sectionLengths[section]>0:
        if section=="intro":
            # No bass in the intro (or drums, but that'll be later).
            callTrack.append((deepcopy(songDic[section][3])))
            callTrack[-1].attrib["pos"] = str(position + ticks * (sectionLengths[section] % 2))
            # Any other section hi-jacks half the melody into the response track with its own melody track.
            responseTrack.append((deepcopy(songDic[section][4])))
            responseTrack[-1].attrib["pos"] = str(position + ticks * (sectionLengths[section] % 2))
        elif section == "chorus":
            # During the chorus, the leads play simultaneously.
            bassTrack.append((deepcopy(songDic[section][0])))
            bassTrack[-1].attrib["pos"]=str(position)
            # And this harmony
            harmonyTrack.append((deepcopy(songDic[section][1])))
            harmonyTrack[-1].attrib["pos"]=str(position)
            # And this melody, but only if the section calls for it.
            if sectionLengths[section]>3:
                leadTrack.append((deepcopy(songDic[section][2])))
                leadTrack[-1].attrib["pos"]=str(position+ticks*(sectionLengths[section]%2))
                # During the verse, the response track harmonizes with the lead.
                responseTrack.append((deepcopy(songDic[section][2])))
                responseTrack[-1].attrib["pos"]=str(position+ticks*(sectionLengths[section]%2))
        elif section=="bridge":
            # During the chorus, the leads play simultaneously.
            bassTrackBridge.append((deepcopy(songDic[section][0])))
            bassTrackBridge[-1].attrib["pos"]=str(position)
            # And this harmony
            harmonyTrackBridge.append((deepcopy(songDic[section][1])))
            harmonyTrackBridge[-1].attrib["pos"]=str(position)
            # And this melody, but only if the section calls for it.
            if sectionLengths[section]>3:
                leadTrack.append((deepcopy(songDic[section][2])))
                leadTrack[-1].attrib["pos"]=str(position+ticks*(sectionLengths[section]%2))
                # During the verse, the response track harmonizes with the lead.
                responseTrack.append((deepcopy(songDic[section][2])))
                responseTrack[-1].attrib["pos"]=str(position+ticks*(sectionLengths[section]%2))
        elif section=="outro":
            # During the outro, some sections don't get played. Only the bass
            outro=ET.SubElement(bassTrack2,"pattern",{"pos":str(position),"steps":"16","type":"1","muted":"0","name":"outro"})
            """ET.SubElement(outro,"note",{"pos":"48","len":f"{ticks}","key":str(LMMSutil.keys[2]+4),"pan":"0","vol":str(r.randint(80,100))})
            """
            LMMSutil.makeMelody(outro,progDic[section],sectionLengths[section]-1,False)
            ET.SubElement(outro,"note",{"pos":"0","len":"96","key":str(LMMSutil.keys[0]),"pan":"0","vol":str(r.randint(80,100))})
            #bassTrack2.append((deepcopy(songDic[section][0])))
            #bassTrack2[-1].attrib["pos"]=str(position)
            # And this harmony
            outro=ET.SubElement(harmonyTrack2,"pattern",{"pos":str(position),"steps":"16","type":"1","muted":"0","name":"outro"})
            ET.SubElement(outro,"note",{"pos":"48","len":f"{ticks}","key":str(LMMSutil.keys[2]),"pan":"0","vol":str(r.randint(80,100))})
            ET.SubElement(outro,"note",{"pos":"48","len":f"{ticks}","key":str(LMMSutil.keys[6]),"pan":"0","vol":str(r.randint(80,100))})
            ET.SubElement(outro,"note",{"pos":"240","len":f"{ticks*2}","key":str(LMMSutil.keys[0]),"pan":"0","vol":str(r.randint(80,100))})
            ET.SubElement(outro,"note",{"pos":"240","len":f"{ticks*2}","key":str(LMMSutil.keys[4]),"pan":"0","vol":str(r.randint(80,100))})
            #harmonyTrack2.append((deepcopy(songDic[section][1])))
            #harmonyTrack2[-1].attrib["pos"]=str(position)
        else:
            # Whole thing is essentially two bass notes layered,starting with the one from the list.
            bassTrack2.append((deepcopy(songDic[section][0])))
            bassTrack2[-1].attrib["pos"]=str(position)
            # And this harmony
            harmonyTrack2.append((deepcopy(songDic[section][1])))
            harmonyTrack2[-1].attrib["pos"]=str(position)
            # And this melody, but only if the section calls for it.
            if sectionLengths[section]>1:
                callTrack.append((deepcopy(songDic[section][3])))
                callTrack[-1].attrib["pos"]=str(position+ticks*(sectionLengths[section]%2))
                # Any other section hi-jacks half the melody into the response track with its own melody track.
                responseTrack.append((deepcopy(songDic[section][4])))
                responseTrack[-1].attrib["pos"]=str(position+ticks*(sectionLengths[section]%2))
        position+=sectionLengths[section]*ticks

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
        ET.SubElement(birdMelody,"note",{"pos":str(144+8*pos+ticks*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"8","pan":"0"})
    # And finally ends where it started.
    ET.SubElement(birdMelody,"note",{"pos":str(168+96*x),"vol":str(r.randint(60,100)),
                                      "key":str(LMMSutil.keys[LMMSutil.scale[0]+7]),"len":"12","pan":"0"})

birdMelody2=ET.Element("pattern",{"pos":"0","type":"0","muted":"0","name":LMMSutil.word(2),"steps":"16"})
for x in range(2):
    # Melodies are four bars long (reduced to one bar due to the low BPM), it starts with a half note, followed by 4 quarter notes.
    ET.SubElement(birdMelody2,"note",{"pos":str(96*x),"vol":str(r.randint(60,100)),
                                      "key":str(LMMSutil.keys[LMMSutil.scale[0]]+14),"len":"12","pan":"0"})
    # These four, as well as any subsequent note, are random notes from the major pentatonic.
    for pos in range(4):
        ET.SubElement(birdMelody2,"note",{"pos":str(12+6*pos+96*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"6","pan":"0"})
    # This is followed by 3 eighth notes.
    for pos in range(3):
        ET.SubElement(birdMelody2,"note",{"pos":str(36+4*pos+96*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"4","pan":"0"})
    # Followed again by 4 quarter notes.
    for pos in range(4):
        ET.SubElement(birdMelody2,"note",{"pos":str(48+6*pos+96*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"6","pan":"0"})
    # This is followed by 4 eighth notes again.
    for pos in range(3):
        ET.SubElement(birdMelody2,"note",{"pos":str(144+8*pos+ticks*x),"vol":str(r.randint(60,100)),
                                          "key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":"8","pan":"0"})
    # And finally ends where it started.
    ET.SubElement(birdMelody2,"note",{"pos":str(168+96*x),"vol":str(r.randint(60,100)),
                                      "key":str(LMMSutil.keys[LMMSutil.scale[0]+7]),"len":"12","pan":"0"})


# Make the track to put the melody on.
stingTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
# Give it a birdy sound.
LMMSutil.makeInstrument(stingTrack, instrumentName="monstro", basenote=str(33), vol="30", animal=1)
locations=[]
# Add the pattern a couple of times.
for _ in range([1,5,1,1,1][songType]):
    stingTrack.append(deepcopy(birdMelody))
    # And put it just about anywhere, as long as it doesn't exist there yet.
    pos=r.randint(5,songbars-1)
    while locations.count(pos)>0:
        pos=r.randint(5,songbars-1)
    stingTrack[-1].attrib["pos"]=str(pos*ticks)
    locations.append(pos-1)
    locations.append(pos)
    locations.append(pos+1)
    stingTrack.append(deepcopy(birdMelody2))
    # And put it just about anywhere, as long as it doesn't exist there yet.
    pos = r.randint(5,songbars-1)
    while locations.count(pos)>0:
        pos = r.randint(5, songbars-1)
    stingTrack[-1].attrib["pos"]=str(pos*ticks)
    locations.append(pos-1)
    locations.append(pos)
    locations.append(pos+1)

# Someone wanted a dinosaur. This is the dinosuar.
dinosaurMelody=ET.Element("pattern",{"pos":"0","type":"0","muted":"0","name":LMMSutil.word(2),"steps":"16"})
# It's just one note, really.
ET.SubElement(dinosaurMelody,"note",{"pos":"0","vol":str(r.randint(60,100)),"key":str(LMMSutil.keys[r.choice([7,8,9,11,12])]),"len":f"{ticks}","pan":"0"})
# A place to call home.
dinoTrack=ET.SubElement(trackcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
# The dino sound.
LMMSutil.makeInstrument(dinoTrack, instrumentName="monstro", basenote=str(93), vol="30", animal=3)
# Put the pattern into the track.
dinoTrack.append(deepcopy(dinosaurMelody))
# Put it somewhere nice.
pos=r.randint(5, songbars-1)
while locations.count(pos)>1:
    pos = r.randint(5, songbars)
dinoTrack[-1].attrib["pos"]=str(pos * ticks)
locations.append(pos-1)
locations.append(pos)
locations.append(pos+1)

# Someone else wanted a hyena. This is no longer the hyena.
flockMelody=ET.Element("pattern", {"pos": "0", "type": "0", "muted": "0", "name":LMMSutil.word(2), "steps": "16"})
# Just put notes randomly, so it can feel like a pack.
for _ in range(20):
    # Melodies are two bar long, notes placed should have their pos limited to 192. Since the note lengths are still a thing, it might overshoot. That's fine.
    ET.SubElement(flockMelody, "note", {"pos":str(r.randint(0, ticks)), "vol":str(r.randint(60, 100)), "key":str(LMMSutil.keys[r.choice([7, 8, 9, 11, 12])]), "len": "24", "pan": "0"})
# A place to call home.
flockTrack=ET.SubElement(trackcontainer, "track", {"type": "0", "muted": "0", "solo": "0", "name":LMMSutil.word(2)})
# The hyena sound.
LMMSutil.makeInstrument(flockTrack, instrumentName="monstro", basenote=str(57), vol="20", animal=4)
# Put the pattern into the track.
flockTrack.append(deepcopy(flockMelody))
# Put it somewhere nice.
pos=r.randint(5, songbars-1)
while locations.count(pos)>1:
    pos=r.randint(5, songbars-1)
flockTrack[-1].attrib["pos"]=str(pos * ticks)
#--------------------Drums-----------------------------------
# Add relaxing beats here.
bassTrack=ET.SubElement(trackcontainer, "track", {"type": "1", "muted": "0", "solo": "0", "name":LMMSutil.word(2)})
bassTrack2=ET.SubElement(trackcontainer, "track", {"type": "1", "muted": "0", "solo": "0", "name":LMMSutil.word(2)})
# A pair of BBtrack element containers.
bbtrack=ET.SubElement(bassTrack, "bbtrack")
# Inside this trackcontainer is another trackcontainer. This is the B&B window.
drumcontainer=ET.SubElement(bbtrack,"trackcontainer",{"width":"700",
                                            "x":"570",
                                            "y":"510",
                                            "maximized":"0",
                                            "height":"300",
                                            "visible":"1",
                                            "type":"song",
                                            "minimized":"0"})
# Add three drums to the BBtrack.
for x in range(3):
    # From here on it's the same old song. One instrument per drum sound.
    drumtrack=ET.SubElement(drumcontainer,"track",{"type":"0","muted":"0","solo":"0","name":LMMSutil.word(2)})
    # Add instrument.
    #instrumenttrack=LMMSutil.makeInstrument(drumtrack,fxch="2",pan=x,instrumentName=r.choice(["nes","papu","sfxr","sid"]),drum=1,type=2,basenote=r.randint(21,69))
    instrumenttrack = LMMSutil.makeInstrument(drumtrack, fxch="2", pan=x,instrumentName=r.choice(["papu","nes","sfxr","sid"]), drum=1,basenote=r.randint(21, 69))
    # And the drum pattern.
    pattern=ET.SubElement(drumtrack,"pattern",{"pos":"0","type":"0","muted":"0","name":"","steps":"32"})
    if songType==3:LMMSutil.drumpattern(pattern,25,songType+x)
    else: LMMSutil.drumpattern(pattern,25,songType)
    # So here's how multiple drum tracks happen:
    pattern = ET.SubElement(drumtrack,"pattern",{"pos":"0","type":"0","muted":"0","name":"","steps":"32"})
    # You just kinda make another pattern.
    if songType==3:LMMSutil.drumpattern(pattern,50,songType+x)
    else:LMMSutil.drumpattern(pattern,50,songType+x)

# Now to add this drumtrack (these are basically the patterns, but in the song window).
x=0
for section in structure:
    # Check to see if the section is the right one. No drums in intros, outros and bridges.
    if section=="verse":
        ET.SubElement(bassTrack, "bbtco",{"usesyle":"1","name":"",
        "len":str(sectionLengths["verse"]*ticks),"color":"4294901760",
        "pos":str(x),"muted":"0"})
    # bbtco elements tell the main trackcontainer which track is active when.
    elif section=="chorus":
        ET.SubElement(bassTrack2, "bbtco",{"usesyle":"1","name":"",
        "len":str(sectionLengths["chorus"]*ticks),"color":"4294901760",
        "pos":str(x),"muted":"0"})
    x+=sectionLengths[section]*ticks
if songType==1:
    ET.SubElement(bassTrack,"bbtco",{"usesyle":"1","name":"","len":str(songbars*ticks),"color":"4294901760","pos":"0","muted":"0"})
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
                                                   "len":f"{ticks}"})
# That's because 192 is divisible by 1,2,3,4,6,8,12,and any other power of 2 multiplied by 3.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Denominator",
                                                   "pos":"0",
                                                   "len":f"{ticks}"})
# And any power of 2 of course,right until 64. That's because of triplets. It does make quintuplets a little awkward though.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Tempo",
                                                   "pos":"0",
                                                   "len":f"{ticks}"})
# Master volume.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Master Volume",
                                                   "pos":"0",
                                                   "len":f"{ticks}"})
# Master pitch.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Master pitch",
                                                   "pos":"0",
                                                   "len":f"{ticks}"})
# FX mixer
FXMixer=ET.SubElement(song,"fxmixer",{"x":"5",
                                      "y":"500",
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
LMMSutil.FXChain(FXChannel,addReverb=True,addStereo=False,addLimiter=True)

# Controller rack
ET.SubElement(song,"ControllerRackView",{"x":"1300",
                                      "y":"500",
                                      "width":"350",
                                      "height":"200",
                                      "maximized":"0",
                                      "visible":"1",
                                      "minimized":"0"})
# Make two subchannels
for x in range(2):
    FXChannel=ET.SubElement(FXMixer,"fxchannel",{"num":str(x+1),
                                                     "muted":"0",
                                                     "volume":["1","0.6"][x],
                                                     "name":str(LMMSutil.word(2))})
    # Mostly the same,effects can be applied here.
    LMMSutil.FXChain(FXChannel,addReverb=x)
    # The difference is these have a send tag for each channel it's sending to.
    ET.SubElement(FXChannel,"send",{"channel":"0","amount":"1"})
# Project notes are structured in HTML (as HTML 4.0, but that's irrelevant).
body=ET.SubElement(ET.SubElement(ET.SubElement(song,"projectnotes"),"html"),"body")
body.text=f"structure: {structure}<br>\
lengths:{sectionLengths}<br>\
songbars: {songbars}<br>\
scale: {LMMSutil.scale}<br>\
key:['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][key]"
# Set the loop points.
ET.SubElement(song,"timeline",{"lp0pos":"0","lp1pos":str(songbars*ticks),"lpstate":"1"})
#-------------------------Writing------------------------------
# A random word is a great name for a song.
title=LMMSutil.word(1)
for _ in range(4):
    if title[-1]!=" ":
        # Add a space with certain chance.
        title+=" " if r.randint(1,2)==1 else ""
    title+=LMMSutil.word(1)
title=title.title()+".mmp"
print(title)
print(f"structure: {structure}")
print(f"lengths:{sectionLengths}")
print(f"songbars: {songbars}")
print(f"scale: {LMMSutil.scale}")
# The opening of the file that always closes automatically with the with statement.
with open(title,'wb') as LMMS:
    # Write the tree.
    tree.write(LMMS)
