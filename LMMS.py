import xml.etree.ElementTree as ET # Time to grow some trees.
import LMMSutil
import random as r
# Variables
"""
So for the sake of argument, a minute song itself will be a total of 192 len/bar, 4 beats/bar, 120 beats/min
So 30 bars=30*192=5760 len per minute at 120bpm.
Alternatively it's bpm/numerator*192
Unless the denominator gets messed with, but that's something for another day.

However, if some semblance of structure is to be discovered, it must be split into bars.
0-4 bars intro, 4 or 8 bars for a section, 4 or 8 bars for a chorus, 0-4 bars bridge and 0-4 bars outro.
At minimum 2 sections and 1 chorus, adjusting tempo to suit the minute duration=12 bars.
At maximum 5 sections, 3 chorus and the bumpers, so 4I-8S-8C-8S-8C-8S-4B-8S-8C-8S-4O=72 bars. Tempo won't need adjustment.
Basically the song duration will be taken into account (bpm*beats(=192/4)=1 maybe) to check on the upper bound.
There is no lower bound (at least as duration is considered).

The number of sections depends on the chorus count and the existence of a bridge.
Though in reality it's not necessary to keep tabs on it as the structure will be important first.
Let's keep it fixed for now, only the bridge will severly alter the structure, so the intro/outro can be included regardless.
intro-section-chorus-section(-chorus-section)(-bridge-section)(-chorus-section)-outro
    There's a guaranteed 1 chorus, there may be a second, there may be a third after the bridge.
    There may be 1 chorus and a bridge, the bridge will be played and the section following but no chorus follows it.

- Calculate the number of bars played (could be stored in a dictionary, sections and choruses are composed only once)
- Find the value that involves both BPM and tempo
- Set the upper tempo limit

"""
# Calculate section lengths.
sectionLengths={"intro":r.randint(0, 4),
    "section":r.randint(4,8),
    "chorus":r.randint(4,8),
    "bridge":r.randint(0,4),
    "outro":r.randint(0,4),
                }
# A place to store valuables.
# Notes go here, the key (pitch), relative position (just add bars*192 for absolute) and length.
# They can be stored in pattern tags. The pattern tags can be stored here.
songDic={"intro":[],
    "section":[],
    "chorus":[],
    "bridge":[],
    "outro":[],
}
# Calculate section counts.
chorusCount=r.randint(1,3)
# Graft the structure with keys of the dictionaries.
structure=["intro","section","chorus","section"]
# Extend structure bit
if chorusCount>1: structure.extend(["chorus","section"])
# by
if sectionLengths["bridge"]>1: structure.extend(["bridge", "section"])
# bit
if chorusCount>2: structure.extend(["chorus","section"])
# and finish by adding the outro.
structure.append("outro")
# Now there's a dictionary for section lengths in bars, one for section notes, and a list for the structure.
songbars=0
# Time to sum up the song length in bars.
for x in structure:
    songbars+=sectionLengths[x]
# Now songbars is a number between 12 and 72.
# Calculate upper limit to the bpm, e.g. with 12 bars a bpm of 12*4=48 is max for one minute.
bpm=r.randint(songbars/2,songbars)
# This may be interesting later on.
numerator=4
#-------------------------Beginnings----------------------------
# Start with a single element.
lmms_project=ET.Element("lmms-project", {"version": "1.0", "creator": "LMMS", "creatorversion": "1.2.1", "type": "song"})
# Make the tree out of that element.
tree=ET.ElementTree(lmms_project)
# Add things to the tree, starting with the header that contains the tempo, time signature, etc.
ET.SubElement(lmms_project, "head", {"timesig_numerator": str(numerator),
                                     "mastervol": "100",
                                     "timesig_denominator": "4",
                                     "bpm": str(bpm), ##This one can be randomized.
                                     "masterpitch": "0"})
# The song element contains the rest.
song=ET.SubElement(lmms_project, "song")
# The track container is the window containing all the tracks (the others will be coming up later).
trackcontainer=ET.SubElement(song, "trackcontainer", {"width": "600",
                                            "x":"5",
                                            "y":"5",
                                            "maximized":"0",
                                            "height":"300",
                                            "visible":"1",
                                            "type":"song",
                                            "minimized":"0"})
#-------------------------Composing----------------------------
"""
Hi it's me again.

The track container contains tracks
Every track consists of two parts, the instrument track data, and the patterns.
    There's only one instrumenttrack, but many patterns.

In this part, we only care about the contents of the patterns
These patterns can have names, which will be the keys of songDic/sectionLengths.
    (iterating over a dictionary causes the iterator to be the key)

Pattern tags will be created and appended in the dictionary. This will be repeated for every track.
"""
# Compose three tracks for every section
for tracknumber in range(3):
    # Every section has an entry here
    for section in songDic:
        # The pattern contains the notes.
        #†# The position needs to match its position in the timeline to not overlap!
        # Do this with pattern.attrib["pos"]=x, but since it will be hidden away, use
        # songDic[section][tracknumber].attrib=whatever the current position is based on sectionLengths*192
        pattern=ET.Element("pattern",{"pos":0,"type":"0","muted":"0","name":section,"steps":"16"})
        # Add a bunch of notes.
        length=0
        # Every section has its own length. If a section has length 0 it gets skipped.
        while length<sectionLengths[section]*192:
            # pos=starting position, vol=velocity, key=pitch (60=C5), len=duration (48=quarter), pan=pan.
            noteLength=r.randint(1,4)*24
            ET.SubElement(pattern,"note",{"pos":str(length),"vol":"100","key":str(r.choice(LMMSutil.keys)),"len":str(noteLength),"pan":"0"})
            # Fun fact, a bar is exactly 192 ticks long.
            length+=noteLength
        # Add this pattern to the dictionary.
        songDic[section].append(pattern)
"""
Great, now to add the section patterns in the right place and the right order.
"""
# Place sections in the tree. Three times for three tracks.
for tracknumber in range(3):
    # Keep track of the position in the song.
    position=0
    # This holds all the music. Type 0 is for instrument.
    track = ET.SubElement(trackcontainer, "track", {"type": "0", "muted": "0", "solo": "0", "name": LMMSutil.word(2)})
    # Creates a Nescaline track by default, pass instrumentName with this to change it.
    # Adds all the bells and whistles in the process.
    instrumenttrack = LMMSutil.makeInstrument(track, instrumentName=r.choice(["nes", "tripleoscillator", "sfxr"]))
    for section in structure:
        # Check if this section has length.
        if sectionLengths[section]==0:
            # Intros, outros and bridges shouldn't be added if they have no length.
            break
        # Add the corresponding pattern here
        added=ET.SubElement(songDic[section][tracknumber])
        # Shift this pattern's position.
        added.attrib["pos"]+=position
        # Move the position up to the new value.
        position+=sectionLengths[section]*192

# Add phat beats here.
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
    instrumenttrack=LMMSutil.makeInstrument(drumtrack,instrumentName=r.choice(["nes","sfxr"]),drum=1)
    # And the drum pattern.
    pattern = ET.SubElement(drumtrack,"pattern",{"pos":"0","type":"0","muted":"0","name":"","steps":"16"})
    for y in range(8):
        # Drums have slightly different ways of doing things. Their len is -192 and their key is 57.
        # While that can be changed, that's how drum tracks are written in the file.
        # The position still works the same however, except it should be placed in spaces in multiples of, depending, 16.
        # That doesn't mean the second hit is on 16, but on 192/16=12.
        # Not going off-beat just yet, hits are on every half note instead.
        ET.SubElement(pattern,"note",{"pos":str(24*y),"vol":"100","key":"57","len":"-192","pan":"0"}) if r.choice([True,False]) else 1
# Now to add this drumtrack
bbtco=ET.SubElement(track,"bbtco",
                    {"usesyle":"1","name":"",
                    "len":str(int(songbars*192)),
                    "color":"4286611584",
                    "pos":"0","muted":"0"})
#----------------------------FX--------------------------------
# It also holds all the main tracks, like this automation track (type 6).

# The automation track, it actually holds all the global automation tracks, not just one of them.
automationTrack=ET.SubElement(song,"track",{"muted":"0",
                                            "type":"6",
                                            "name":"Automation track",
                                            "solo":"0"})

# An empty automation track since automation tracks don't have properties.
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
# And any power of 2 of course, right until 64.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Tempo",
                                                   "pos":"0",
                                                   "len":"192"})
# That's because of triplets.
ET.SubElement(automationTrack,"automationpattern",{"tens":"1",
                                                   "mute":"0",
                                                   "name":"Master Volume",
                                                   "pos":"0",
                                                   "len":"192"})
# It does make quintuplets a little awkward though.
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
FXChannel=ET.SubElement(FXMixer,"fxchain",{"num":"0",
                                           "muted":"0",
                                           "volume":"1",
                                           "name":"master"})
# FX chain
LMMSutil.FXChain(FXChannel)


#-------------------------Writing------------------------------
# Time for the homebrew helper definitions to make random words.
import abcutil
# A random word is a great name for a song.
title=LMMSutil.word(2)+" "+LMMSutil.word(2)+".mmp"
# The opening of the file that always closes automatically with the with statement.
with open(title,'wb') as LMMS:
    # Write the tree.
    tree.write(LMMS)
