import xml.etree.ElementTree as ET # Time to grow some trees.
import random as r
#from LMMSutil import shapeSample
"""
A generator for meditative instruments using LMMS' built-in plug-ins (as well as a sound font).
It also makes birds. Someday it'll make other soundscape elements.
These are the instruments available:
    tripleoscillator
    bitinvader
    papu(=FreeBoy)*
    malletsstk(=Mallets)
    monstro
    OPL2(=OpulenZ)(quiet)*
    organic*
    sid
    vibedstrings(=Vibed)*
    sf2player

    * Not yet implemented
    """
def createInstrument(instrumentName,shapeSample,bird=0):
    if instrumentName=="nes":return{"vol":"1", #master volume.
    "vibr":"0", #master vibrato (depth only).
    "on1":"1", #enable channel 1, a square wave channel.
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
    "on4":"0", #channel 4 is the noise channel, used for drums.
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
    if instrumentName=="tripleoscillator":return {"modalgo2":"2", #osc1+2, how osc 2 modules osc 1.
    "modalgo3":"2",#osc2+3. phase modulate 0, amp modulate 1, mix 2, sync 3, frequency modulate 4.
    "wavetype0":r.choice(["2","3"]), #wave type, sine 0, tri 1, saw 2, square 3, moog 4, exponential 5, noise 6, custom 7
    "userwavefile0":"", #use a custom wave file as oscillator. Type must be 7
    "vol0":"10", #oscillator volume [0,200]
    "pan0":"0", #pan of osc.
    "coarse0":"0", #course detune [-24,24] in semitones (5 octave range)
    "finel0":"0", #left channel detune [-100,100].
    "finer0":"0", #right channel detune.
    "phoffset0":"0", #phase offset [0-360] degrees (2 square waves cancel eachother out at 180).
    "stphdetun0":"0", #stereo phase detune (left channel)
    "wavetype1":r.choice(["2","3"]), #all oscilllators are identical.
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
    "stphdetun2":"0",
    }
    if instrumentName=="sfxr":return {"version":"1", #does nothing.
    "waveForm":"0", #waveform, square 0, saw 1, sine 2, noise 3. All other values are normals.
    "att":"0", #attack.
    "hold":str([str(r.choice(range(10))/10)]), #hold (time until sustain).
    "sus":"0", #punch (very short).
    "dec":["0.4"], #decay (sustain time).
    "startFreq":"0.352", #0.352 is natural, use a range for drums.
    "minFreq":"0", #slide cap, but only downards.
    "slide":"0", #slide amount [-1,1], magnitude scales both speed and depth. Loses effectiveness beyond .25.
    "dSlide":"0", #delta slide, or delayed slide. Kicks in after slide finishes.
    "vibDepth":"0", #vibrato depth, best below 0.05.
    "vibSpeed":"0", #vibrato speed, both need to be set to work.
    "changeAmt":"0", #change the held note to a different pitch.
    "changeSpeed":"0", #time it takes to change pitch, <0.01 is 1 sec, anything higher is faster.
    "sqrDuty":"0", #square wave form, 0=50%, 1=0%.
    "sqrSweep":"0", #sweep to 50% on negative, to 0% on positive, with magnitute changing speed.
    "repeatSpeed":"0", #repeat the whole note played after a delay once (including change and sweeps). Higher is sooner.
    "phaserOffset":"0", #overlays a second wave on a different phase, around 0.626 cancels symetric waves (square and sine)
    "phaserSweep":"0", #sweeps phase one revolution, magintute changes speed.
    "lpFilCut":"1", #low pass filter.
    "lpFilCutSweep":"0", #sweeps cutoff level.
    "lpFilReso":"0", #low pass resonance.
    "hpFilCut":"0", #high pass filter.
    "hpFilCutSweep":"0", #sweeps cutoff level.
    }
    if instrumentName=="sid":return {"volume":"15", # The overal volume that exists for some reason.
    "filterResonance":str(r.randint(0,15)), # The filter dials only work on the tone generators that have filter enabled.
    "filterFC":str(r.randint(0,2047)), # They may be useful for individual tracks, just randomize it for kicks.
    "filterMode":str(r.randint(0,3)), # High pass, band pass, low pass.
    "chipModel":"1", # There are two models, the 6581 and the 8580. The 6581 pops in this one, so keep on 8580.
    "voice3Off":"0", # Turn off the third tone generator.
    "attack0":"0", # ADSR envelope for the first tone generator.
    "decay0":"8",
    "sustain0":"15",
    "release0":"8",
    "pulsewidth0":"2048", # If the wave form is 1, this does something, namely the shape of the square wave.
    "coarse0":"0", # Course detune in semitones from -24 (2 octaves down) to 24 (2 octaves up).
    "waveform0":"0", # Tri wave (1), square wave (0), sawtooth (2), noise (3). Note that the noise is pitched.
    "ringmod0":r.choice(["0","1"]), # Enables the ring mod for the tone generator.
    "filtered0":r.choice(["0","1"]), # Enable to make the filter mode do things.
    "test0":"0", # "Test" the chip, used for synced to external events, functionally this mutes the tone generator.
    "sync0":"0", # Synchronize with the previous (cyclic) tone generator.
    "attack1":"0", # Second tone generator.
    "decay1":"8",
    "sustain1":"15",
    "release1":"8",
    "pulsewidth1":"2048",
    "coarse1":"0",
    "waveform1":"0",
    "ringmod1":r.choice(["0","1"]),
    "filtered1":r.choice(["0","1"]),
    "test1":"0",
    "sync1":"0",
    "attack2":"0", # Third tone generator.
    "decay2":"8",
    "sustain2":"15",
    "release2":"8",
    "pulsewidth2":"2048",
    "coarse2":"0",
    "waveform2":"1",
    "ringmod2":r.choice(["0","1"]),
    "filtered2":r.choice(["0","1"]),
    "test2":"0",
    "sync2":"0"}# This one's weird.
    if instrumentName=="bitinvader":
        # Choose a random wave form length between 4 and 200.
        samplelength=r.randint(4,200)
        return {"sampleLength":str(samplelength), # The sample length. This value is king and ignores the actual shape.
    "version":"0.1", # Does nothing.
    "normalize":"1", # Stretches the wave form vertically. Tends to cause clipping if the volume's too high. Set this track to about 40 volume.
    "sampleShape":shapeSample(samplelength), # The sample shape is a series of floats encrypted to a byte64 object.
    "interpolation":r.choice(["0","1"])}# Use linear interpolation between the points instead of discrete. Little effect on smooth enough forms.
    if instrumentName=="watsyn":return {"abmix":"0", # The amount A to B is being output. -100 is only A, 100 is only B
    "envAmt":str(r.randint(-200,200)), # The strength of the envelope going from mix to A or B and back. -200 is to A, 200 is to B. Values beyond 100 increase speed.
    "envAtt":str(r.randint(0,200)), # The time it takes to go from mix to A/B in ms [0,2000].
    "envAtt_syncmode":"0", # Hidden value. Setting this to 1 sets the envAtt to 2000, does nothing otherwise.
    "envAtt_numerator":"4", # Also hidden value, probably meant to work in conjunction with the sync mode.
    "envAtt_denominator":"4", # Since sync mode cannot be saved as on, the meter values wouldn't matter anyway.
    "envHold":str(r.randint(0,200)), # Duration to stay in A/B in ms [0,2000]
    "envHold_syncmode":"0",
    "envHold_numerator":"4",
    "envHold_denominator":"4",
    "envDec":str(r.randint(0,200)), # The time it takes to go from A/B back to mix in ms [0,2000].
    "envDec_syncmode":"0",
    "envDec_numerator":"4",
    "envDec_denominator":"4",
    "xtalk":"0", # Magic number that seems to keep other wave forms in mind.
    "amod":"0", # A1 -> A2 modulation. 0 (mix), 1 (AM), 2 (Ring), 3 (PM).
    "bmod":"0", # B1 -> B2 modulation. 0 (mix), 1 (AM), 2 (Ring), 3 (PM).
    "a1_vol":"100", # Volume of the A1 wave.
    "a1_pan":"0", # Pan of the A1 wave.
    "a1_mult":"8", # Frequency multiplier of the A1 wave, which is this value /8 and can be used to adjust intonation.
    "a1_ltune":str(int(r.gauss(0,2))), # Left detune of the A1 wave in cents [-600,600] for an octave's worth of range.
    "a1_rtune":str(int(r.gauss(0,2))), # Right detune of the A1 wave in cents [-600,600] for an octave's worth of range.
    "a2_vol":"0",
    "a2_pan":"0",
    "a2_mult":"8",
    "a2_ltune":"0",
    "a2_rtune":"0",
    "b1_vol":"100",
    "b1_pan":"0",
    "b1_mult":"8",
    "b1_ltune":"0",
    "b1_rtune":"0",
    "b2_vol":"0",
    "b2_pan":"0",
    "b2_mult":"8",
    "b2_ltune":"0",
    "b2_rtune":"0",
    "a1_wave":shapeSample(250), # 250 byte long shape of the wave for A1
    "a2_wave":shapeSample(250),
    "b1_wave":shapeSample(250),
    "b2_wave":shapeSample(250)}
    # Mallet is very unwieldy, it varies from super quiet to super loud, high pitched to low.
    # It should be fine with a compressor followed by a limiter.
    # Vibraphone (1):, no compresser, 0 hardness, random spread
    # Reso (4):max position, 0 hardness, don't go higher than C5.
    # Beats (6):max position, 0 hardness
    # Clump (8)
    # Tubular bells (9):no lower than C6, really long notes only.
    if instrumentName=="malletsstk":return{"preset":r.choice(["1","4","6","9"]),# Instrument selection. Different choices when used as drums.
    "hardness":str(r.randint(0,128)), # Acts as a sort of equalizer that picks frequency. Max clarity at 95.
    "position":str(r.randint(0,64)), # Adds a kind of variation when below 64.
    "vib_gain":"0", # Vibrato depth.
    "vib_freq":"64", # Vibrato speed.
    "spread":"0", # Stereo widening.
    "modulator":"64", # Used only by the tubular bells.
    "crossfade":str(r.randint(0,128)), # Used only by the tubular bells.
    "adsr":str(r.randint(0,128)), # Used only by the tubular bells. Adds a sort of punch to the sound.
    "lfo_speed":str(r.randint(0,24)), # Used only by the tubular bells, vibrato speed.
    "lfo_depth":str(r.randint(0,128)), # Used only by the tubular bells, vibrato depth.
    "stick_mix":"0", # Balances between a stick sound at max and the bell sound at min.
    "pressure":"64", # Used by presets above 9.
    "velocity":"64", # Used by presets above 9.
    "strike":"1", # Doesn't seem to do anything.
    "oldversion":"0", # Does nothing.
    "version":"1",} # Does nothing.
    # Monstro. It's large and in charge (no joke, definitely the most powerful synth in all of LMMS), but will only be used for bird sounds.
    if instrumentName=="monstro":return[{
    "o1vol":"33","o1pan":"0","o1crs":"0","o1ftl":"0","o1ftr":"0","o1spo":"0","o1pw":str(r.randint(10,90)),"o1ssr":"0","o1ssf":"0",
    "o2vol":"33","o2pan":"0","o2crs":"0","o2ftl":"0","o2ftr":"0","o2spo":"0","o2wav":"4","o2synr":"0","o2syn":"0",
    "o3vol":"33","o3pan":"0","o3crs":"0","o3spo":"0","o3sub":"0","o3wav1":"0","o3wav2":"1","o3synr":"0","o3syn":"0",
    "o23mo":str(r.randint(0,3)),
    "l1wav":"0","l1att":"0","l1att_syncmode":"0","l1att_numerator":"4","l1att_denominator":"4",
    "l1rat":"300","l1rat_syncmode":"0","l1rat_numerator":"4","l1rat_denominator":"4",
    "l1phs":"0",
    "l2wav":"0","l2att":"0","l2att_syncmode":"0","l2att_numerator":"4","l2att_denominator":"4",
    "l2rat":"1","l2rat_syncmode":"0","l2rat_numerator":"4","l2rat_denominator":"4","l2phs":"0",
    "e1pre":"0","e1pre_syncmode":"0","e1pre_numerator":"4","e1pre_denominator":"4",
    "e1att":"0","e1att_syncmode":"0","e1att_denominator":"4","e1att_numerator":"4",
    "e1hol":"0","e1hol_syncmode":"0","e1hol_numerator":"4","e1hol_denominator":"4",
    "e1dec":"250","e1dec_syncmode":"0","e1dec_numerator":"4","e1dec_denominator":"4","e1sus":"0",
    "e1rel":"0","e1rel_syncmode":"0","e1rel_numerator":"4","e1rel_denominator":"4",
    "e1slo":"0",
    "e2pre":"0","e2pre_syncmode":"0","e2pre_numerator":"4","e2pre_denominator":"4",
    "e2att":"0","e2att_syncmode":"0","e2att_numerator":"4","e2att_denominator":"4",
    "e2hol":"0","e2hol_syncmode":"0","e2hol_numerator":"4","e2hol_denominator":"4",
    "e2dec":"0","e2dec_syncmode":"0","e2dec_numerator":"4","e2dec_denominator":"4",
    "e2sus":"1",
    "e2rel":"0","e2rel_syncmode":"0","e2rel_numerator":"4","e2rel_denominator":"4",
    "e2slo":"0",
    "v1e1":"0","v1e2":"0","v1l1":"0","v1l2":"0", # Volume
    "v2e1":"1","v2e2":"0","v2l1":"0","v2l2":"0",
    "v3e1":"0","v3e2":"0","v3l1":"0","v3l2":"0",
    "f1e1":"0","f1e2":"0","f1l1":"0","f1l2":"0", # Pitch (frequency)
    "f2e1":"0","f2e2":"0","f2l1":"1","f2l2":"0",
    "f3e1":"0","f3e2":"0","f3l1":"0","f3l2":"0",
    "p1e1":"0","p1e2":"0","p1l1":"0","p1l2":"0", # Phase
    "p2e1":"0","p2e2":"0","p2l1":"0","p2l2":"0",
    "p3e1":"0","p3e2":"0","p3l1":"0","p3l2":"0",
    "w1e1":"0","w1e2":"0","w1l1":"0","w1l2":"0", # Pulse width
    "s3e1":"0","s3e2":"0","s3l1":"0","s3l2":"0"}, # Sub mix
    {"o1vol":"0","o1pan":"0","o1crs":"0","o1ftl":"0","o1ftr":"0","o1spo":"0","o1pw":"50","o1ssr":"0","o1ssf":"0",
    "o2vol":"0","o2pan":"0","o2crs":"0","o2ftl":"0","o2ftr":"0","o2spo":"0","o2wav":"4","o2synr":"0","o2syn":"0",
    "o3vol":"33","o3pan":"0","o3crs":"0","o3spo":"0","o3sub":"0","o3wav1":"5","o3wav2":"4","o3synr":"0","o3syn":"0",
    "o23mo":"0",
    "l1wav":"0","l1att":"0","l1att_syncmode":"0","l1att_numerator":"4","l1att_denominator":"4",
    "l1rat":"300","l1rat_syncmode":"0","l1rat_numerator":"4","l1rat_denominator":"4",
    "l1phs":"0",
    "l2wav":"0","l2att":"0","l2att_syncmode":"0","l2att_numerator":"4","l2att_denominator":"4",
    "l2rat":"1","l2rat_syncmode":"0","l2rat_numerator":"4","l2rat_denominator":"4","l2phs":"0",
    "e1pre":"0","e1pre_syncmode":"0","e1pre_numerator":"4","e1pre_denominator":"4",
    "e1att":"0","e1att_syncmode":"0","e1att_denominator":"4","e1att_numerator":"4",
    "e1hol":"0","e1hol_syncmode":"0","e1hol_numerator":"4","e1hol_denominator":"4",
    "e1dec":"1000","e1dec_syncmode":"0","e1dec_numerator":"4","e1dec_denominator":"4","e1sus":"0",
    "e1rel":"0","e1rel_syncmode":"0","e1rel_numerator":"4","e1rel_denominator":"4",
    "e1slo":"0",
    "e2pre":"0","e2pre_syncmode":"0","e2pre_numerator":"4","e2pre_denominator":"4",
    "e2att":"0","e2att_syncmode":"0","e2att_numerator":"4","e2att_denominator":"4",
    "e2hol":"0","e2hol_syncmode":"0","e2hol_numerator":"4","e2hol_denominator":"4",
    "e2dec":"0","e2dec_syncmode":"0","e2dec_numerator":"4","e2dec_denominator":"4",
    "e2sus":"1",
    "e2rel":"0","e2rel_syncmode":"0","e2rel_numerator":"4","e2rel_denominator":"4",
    "e2slo":"0",
    "v1e1":"0","v1e2":"0","v1l1":"0","v1l2":"0",
    "v2e1":"1","v2e2":"0","v2l1":"2","v2l2":"0",
    "v3e1":"1","v3e2":"0","v3l1":"0","v3l2":"0",
    "f1e1":"0","f1e2":"0","f1l1":"0","f1l2":"0",
    "f2e1":"0","f2e2":"0","f2l1":"1","f2l2":"0",
    "f3e1":"0.150","f3e2":"0","f3l1":"0","f3l2":"0",
    "p1e1":"0","p1e2":"0","p1l1":"0","p1l2":"0",
    "p2e1":"0","p2e2":"0","p2l1":"0","p2l2":"0",
    "p3e1":"0","p3e2":"0","p3l1":"0","p3l2":"0",
    "w1e1":"0","w1e2":"0","w1l1":"0","w1l2":"0",
    "s3e1":"0","s3e2":"0","s3l1":"0","s3l2":"0"}][bird]
    if instrumentName=="sf2player": return{"src":"Woodwind/Flute/Flute.sf2",
    "bank":"0",
    "patch":"0",
    "gain":"3",
    "reverbOn":"0",
    "reverbRoomSize":"0.2",
    "reverbWidth":"0.5",
    "reverbLevel":"0.9",
    "reverbDamping":"0",
    "chorusOn":"0",
    "chorusLevel":"2",
    "chorusNum":"3",
    "chorusDepth":"8",
    "chorusSpeed":"0.3"}
    if instrumentName=="papu":
        # For no reason in particular, I want only one channel to output at a time.
        channel=r.randint(0,2)
        # Would you like some ADSR? Doesn't affect channel 3.
        attack=r.randint(0,1)
        return {"ch1so1":["1","0","0"][channel], # Channel 1 send output. 1 is left, 2 is right.
            "ch1so2":["1","0","0"][channel], # Channel 1 is the advanced square wave.
            "ch2so1":["0","1","0"][channel], # Channel 2 is the basice square wave.
            "ch2so2":["0","1","0"][channel],
            "ch3so1":["0","0","1"][channel], # Channel 3 is the sample wave.
            "ch3so2":["0","0","1"][channel],
            "ch4so1":"0", # Channel 4 is noise. Will have drum applications.
            "ch4so2":"0",
            "so1vol":"7",
            "so2vol":"7", # Finer tune of output. Only works if both are the same value.
            "Treble":"100", # Crude filters. They sort of do something, but 100/-1 is decent enough.
            "Bass":"-1",
            "ch1vol":["15",str(r.randint(0,6))][attack], # Volume of channel 1.
            "ch1ssl":["0",str(r.randint(2,7))][attack], # Sweep step length. Used in combination with VSwDir. 0 turns volume sweep off.
            "ch1wpd":str(r.randint(0,3)), # Wave pattern duty. 0 through 3 equals 12.5%, 25%, 50% and 75%.
            "srs":"0", # Sweep RTShift. Amount of sweep. 0 is no sweep, 1 few notes, 2 is more notes, etc. to 7.
            "st":"0", # Sweep time. Duration of sweep. 0 is off (stop), 1 through 7 increasingly longer.
            "sd":"0", # Sweep direction.
            "ch1vsd":["0","1"][attack], # Volume sweep direction, both have 0 as down, 1 as up.
            "ch2vol":["15",str(r.randint(0,6))][attack], # Volume of channel 2.
            "ch2ssl":str(r.randint(0,7)), # Volume sweep length for channel 2.
            "ch2wpd":str(r.randint(0,3)), # Wave pattern duty, same as 1. Note that 25% and 75% don't cancel eachother out.
            "ch2vsd":["0","1"][attack], # Volume sweep direction. 1 only works if chxvol!=15
            "ch3vol":"3", # Channel 3 volume.
            "sampleShape":shapeSample(32,onlyPositive=True), # Channel 3 waveform, positive values only.
            "ch4vol":"15", # Channel 4 volume.
            "ch4ssl":"2", # Volume sweep duration.
            "srw":"0", # Shift register width. 0=15 (better for higher pitches), 1=7 (better for lower).
            "ch4vsd":"0",} # Volume sweep direction
    # Might add others later, depending.

def makeBird(instrumentName,bird=1):
    # Monstro. It's large and in charge (no joke, definitely the most powerful synth in all of LMMS), but will only be used for bird sounds.
    if instrumentName=="monstro":return[{},{
    "o1vol":"0","o1pan":"0","o1crs":"0","o1ftl":"0","o1ftr":"0","o1spo":"0","o1pw":"50","o1ssr":"0","o1ssf":"0",
    "o2vol":"33","o2pan":"0","o2crs":"0","o2ftl":"0","o2ftr":"0","o2spo":"0","o2wav":"4","o2synr":"0","o2syn":"0",
    "o3vol":"0","o3pan":"0","o3crs":"0","o3spo":"0","o3sub":"0","o3wav1":"0","o3wav2":"1","o3synr":"0","o3syn":"0",
    "o23mo":"0",
    "l1wav":"0","l1att":"0","l1att_syncmode":"0","l1att_numerator":"4","l1att_denominator":"4",
    "l1rat":"300","l1rat_syncmode":"0","l1rat_numerator":"4","l1rat_denominator":"4",
    "l1phs":"0",
    "l2wav":"0","l2att":"0","l2att_syncmode":"0","l2att_numerator":"4","l2att_denominator":"4",
    "l2rat":"1","l2rat_syncmode":"0","l2rat_numerator":"4","l2rat_denominator":"4","l2phs":"0",
    "e1pre":"0","e1pre_syncmode":"0","e1pre_numerator":"4","e1pre_denominator":"4",
    "e1att":"0","e1att_syncmode":"0","e1att_denominator":"4","e1att_numerator":"4",
    "e1hol":"0","e1hol_syncmode":"0","e1hol_numerator":"4","e1hol_denominator":"4",
    "e1dec":"250","e1dec_syncmode":"0","e1dec_numerator":"4","e1dec_denominator":"4","e1sus":"0",
    "e1rel":"0","e1rel_syncmode":"0","e1rel_numerator":"4","e1rel_denominator":"4",
    "e1slo":"0",
    "e2pre":"0","e2pre_syncmode":"0","e2pre_numerator":"4","e2pre_denominator":"4",
    "e2att":"0","e2att_syncmode":"0","e2att_numerator":"4","e2att_denominator":"4",
    "e2hol":"0","e2hol_syncmode":"0","e2hol_numerator":"4","e2hol_denominator":"4",
    "e2dec":"0","e2dec_syncmode":"0","e2dec_numerator":"4","e2dec_denominator":"4",
    "e2sus":"1",
    "e2rel":"0","e2rel_syncmode":"0","e2rel_numerator":"4","e2rel_denominator":"4",
    "e2slo":"0",
    "v1e1":"0","v1e2":"0","v1l1":"0","v1l2":"0", # Volume
    "v2e1":"1","v2e2":"0","v2l1":"0","v2l2":"0",
    "v3e1":"0","v3e2":"0","v3l1":"0","v3l2":"0",
    "f1e1":"0","f1e2":"0","f1l1":"0","f1l2":"0", # Pitch (frequency)
    "f2e1":"0","f2e2":"0","f2l1":"1","f2l2":"0",
    "f3e1":"0","f3e2":"0","f3l1":"0","f3l2":"0",
    "p1e1":"0","p1e2":"0","p1l1":"0","p1l2":"0", # Phase
    "p2e1":"0","p2e2":"0","p2l1":"0","p2l2":"0",
    "p3e1":"0","p3e2":"0","p3l1":"0","p3l2":"0",
    "w1e1":"0","w1e2":"0","w1l1":"0","w1l2":"0", # Pulse width
    "s3e1":"0","s3e2":"0","s3l1":"0","s3l2":"0"}, # Sub mix
    {"o1vol":"0","o1pan":"0","o1crs":"0","o1ftl":"0","o1ftr":"0","o1spo":"0","o1pw":"50","o1ssr":"0","o1ssf":"0",
    "o2vol":"0","o2pan":"0","o2crs":"0","o2ftl":"0","o2ftr":"0","o2spo":"0","o2wav":"4","o2synr":"0","o2syn":"0",
    "o3vol":"33","o3pan":"0","o3crs":"0","o3spo":"0","o3sub":"0","o3wav1":"5","o3wav2":"4","o3synr":"0","o3syn":"0",
    "o23mo":"0",
    "l1wav":"0","l1att":"0","l1att_syncmode":"0","l1att_numerator":"4","l1att_denominator":"4",
    "l1rat":"300","l1rat_syncmode":"0","l1rat_numerator":"4","l1rat_denominator":"4","l1phs":"0",
    "l2wav":"0","l2att":"0","l2att_syncmode":"0","l2att_numerator":"4","l2att_denominator":"4",
    "l2rat":"1","l2rat_syncmode":"0","l2rat_numerator":"4","l2rat_denominator":"4","l2phs":"0",
    "e1pre":"0","e1pre_syncmode":"0","e1pre_numerator":"4","e1pre_denominator":"4",
    "e1att":"0","e1att_syncmode":"0","e1att_denominator":"4","e1att_numerator":"4",
    "e1hol":"0","e1hol_syncmode":"0","e1hol_numerator":"4","e1hol_denominator":"4",
    "e1dec":"1000","e1dec_syncmode":"0","e1dec_numerator":"4","e1dec_denominator":"4","e1sus":"0",
    "e1rel":"0","e1rel_syncmode":"0","e1rel_numerator":"4","e1rel_denominator":"4",
    "e1slo":"0",
    "e2pre":"0","e2pre_syncmode":"0","e2pre_numerator":"4","e2pre_denominator":"4",
    "e2att":"0","e2att_syncmode":"0","e2att_numerator":"4","e2att_denominator":"4",
    "e2hol":"0","e2hol_syncmode":"0","e2hol_numerator":"4","e2hol_denominator":"4",
    "e2dec":"0","e2dec_syncmode":"0","e2dec_numerator":"4","e2dec_denominator":"4",
    "e2sus":"1",
    "e2rel":"0","e2rel_syncmode":"0","e2rel_numerator":"4","e2rel_denominator":"4",
    "e2slo":"0",
    "v1e1":"0","v1e2":"0","v1l1":"0","v1l2":"0",
    "v2e1":"1","v2e2":"0","v2l1":"2","v2l2":"0",
    "v3e1":"1","v3e2":"0","v3l1":"0","v3l2":"0",
    "f1e1":"0","f1e2":"0","f1l1":"0","f1l2":"0",
    "f2e1":"0","f2e2":"0","f2l1":"1","f2l2":"0",
    "f3e1":"0.150","f3e2":"0","f3l1":"0","f3l2":"0",
    "p1e1":"0","p1e2":"0","p1l1":"0","p1l2":"0",
    "p2e1":"0","p2e2":"0","p2l1":"0","p2l2":"0",
    "p3e1":"0","p3e2":"0","p3l1":"0","p3l2":"0",
    "w1e1":"0","w1e2":"0","w1l1":"0","w1l2":"0",
    "s3e1":"0","s3e2":"0","s3l1":"0","s3l2":"0"},
    {"o1vol":"33","o1pan":"0","o1crs":"0","o1ftl":"0","o1ftr":"0","o1spo":"0","o1pw":str(r.randint(25,50)),"o1ssr":"0","o1ssf":"1",
    "o2vol":"33","o2pan":"0","o2crs":"0","o2ftl":"0","o2ftr":"0","o2spo":"0","o2wav":"8","o2synr":"1","o2syn":"1",
    "o3vol":"33","o3pan":"0","o3crs":"0","o3spo":"0","o3sub":"0","o3wav1":"6","o3wav2":"4","o3synr":"1","o3syn":"1",
    "o23mo":"0",
    "l1wav":"0","l1att":"0","l1att_syncmode":"0","l1att_numerator":"4","l1att_denominator":"4",
    "l1rat":"300","l1rat_syncmode":"0","l1rat_numerator":"4","l1rat_denominator":"4","l1phs":"0",
    "l2wav":"0","l2att":"0","l2att_syncmode":"0","l2att_numerator":"4","l2att_denominator":"4",
    "l2rat":"1","l2rat_syncmode":"0","l2rat_numerator":"4","l2rat_denominator":"4","l2phs":"0",
    "e1pre":"0","e1pre_syncmode":"0","e1pre_numerator":"4","e1pre_denominator":"4",
    "e1att":"0","e1att_syncmode":"0","e1att_denominator":"4","e1att_numerator":"4",
    "e1hol":"0","e1hol_syncmode":"0","e1hol_numerator":"4","e1hol_denominator":"4",
    "e1dec":"2800","e1dec_syncmode":"0","e1dec_numerator":"4","e1dec_denominator":"4","e1sus":"0",
    "e1rel":"0","e1rel_syncmode":"0","e1rel_numerator":"4","e1rel_denominator":"4",
    "e1slo":"0",
    "e2pre":"0","e2pre_syncmode":"0","e2pre_numerator":"4","e2pre_denominator":"4",
    "e2att":"144","e2att_syncmode":"0","e2att_numerator":"4","e2att_denominator":"4",
    "e2hol":"0","e2hol_syncmode":"0","e2hol_numerator":"4","e2hol_denominator":"4",
    "e2dec":"620","e2dec_syncmode":"0","e2dec_numerator":"4","e2dec_denominator":"4",
    "e2sus":"0",
    "e2rel":"0","e2rel_syncmode":"0","e2rel_numerator":"4","e2rel_denominator":"4",
    "e2slo":"0",
    "v1e1":"1","v1e2":"0","v1l1":"0","v1l2":"0",
    "v2e1":"1","v2e2":"0","v2l1":"0","v2l2":"0",
    "v3e1":"1","v3e2":"0","v3l1":"0","v3l2":"0",
    "f1e1":"0.150","f1e2":"0.150","f1l1":"0","f1l2":"0",
    "f2e1":"0.150","f2e2":"0.150","f2l1":"0","f2l2":"0",
    "f3e1":"0.150","f3e2":"0.150","f3l1":"0","f3l2":"0",
    "p1e1":"0","p1e2":"0","p1l1":"0","p1l2":"0",
    "p2e1":"0","p2e2":"0","p2l1":"0","p2l2":"0",
    "p3e1":"0","p3e2":"0","p3l1":"0","p3l2":"0",
    "w1e1":"0","w1e2":"0","w1l1":"0","w1l2":"0",
    "s3e1":"0","s3e2":"0","s3l1":"0","s3l2":"0"},
    {"o1vol":"0","o1pan":"0","o1crs":"0","o1ftl":"0","o1ftr":"0","o1spo":"0","o1pw":str(r.randint(25,50)),"o1ssr":"0","o1ssf":"0",
     "o2vol":"50","o2pan":"0","o2crs":"0","o2ftl":"0","o2ftr":"0","o2spo":"0","o2wav":"1","o2synr":"0","o2syn":"0",
     "o3vol":"50","o3pan":"0","o3crs":"0","o3spo":"0","o3sub":"0","o3wav1":"2","o3wav2":"1","o3synr":"0","o3syn":"0",
     "o23mo":"0",
     "l1wav":"3","l1att":"0","l1att_syncmode":"0","l1att_numerator":"4","l1att_denominator":"4",
     "l1rat":"150","l1rat_syncmode":"0","l1rat_numerator":"4","l1rat_denominator":"4",
     "l1phs":"0",
     "l2wav":"1","l2att":"0","l2att_syncmode":"0","l2att_numerator":"4","l2att_denominator":"4",
     "l2rat":"1","l2rat_syncmode":"0","l2rat_numerator":"4","l2rat_denominator":"4","l2phs":"0",
     "e1pre":"0","e1pre_syncmode":"0","e1pre_numerator":"4","e1pre_denominator":"4",
     "e1att":"200","e1att_syncmode":"0","e1att_denominator":"4","e1att_numerator":"4",
     "e1hol":"0","e1hol_syncmode":"0","e1hol_numerator":"4","e1hol_denominator":"4",
     "e1dec":"500","e1dec_syncmode":"0","e1dec_numerator":"4","e1dec_denominator":"4",
     "e1sus":"0",
     "e1rel":"0","e1rel_syncmode":"0","e1rel_numerator":"4","e1rel_denominator":"4",
     "e1slo":"0",
     "e2pre":"0","e2pre_syncmode":"0","e2pre_numerator":"4","e2pre_denominator":"4",
     "e2att":"144","e2att_syncmode":"0","e2att_numerator":"4","e2att_denominator":"4",
     "e2hol":"0","e2hol_syncmode":"0","e2hol_numerator":"4","e2hol_denominator":"4",
     "e2dec":"620","e2dec_syncmode":"0","e2dec_numerator":"4","e2dec_denominator":"4",
     "e2sus":"1",
     "e2rel":"0","e2rel_syncmode":"0","e2rel_numerator":"4","e2rel_denominator":"4",
     "e2slo":"0",
     "v1e1":"1","v1e2":"0","v1l1":"0","v1l2":"0",
     "v2e1":"1","v2e2":"1","v2l1":"0","v2l2":"0",
     "v3e1":"1","v3e2":"0","v3l1":"0","v3l2":"0",
     "f1e1":"0","f1e2":"0","f1l1":"0.150","f1l2":"0",
     "f2e1":"0","f2e2":"0","f2l1":"0.150","f2l2":"0",
     "f3e1":"0","f3e2":"0","f3l1":"0.150","f3l2":"0",
     "p1e1":"0","p1e2":"0","p1l1":"0","p1l2":"0",
     "p2e1":"0","p2e2":"0","p2l1":"0","p2l2":"0",
     "p3e1":"0","p3e2":"0","p3l1":"0","p3l2":"0",
     "w1e1":"0","w1e2":"0","w1l1":"0","w1l2":"0",
     "s3e1":"0","s3e2":"0","s3l1":"0","s3l2":"0"}
    ][bird]