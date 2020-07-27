import xml.etree.ElementTree as ET # Time to grow some trees.
import random as r

import LMMSChip
import LMMSDrums
# This makes non-drums.
# This also makes drums. For the most part it's the same as the instruments, but the values are going to be different.
# For instance, if it makes a Nescaline drum, it makes sure the noise channel is on.
import LMMSMeditative

"""These are the instruments available:
    nes(=Nescaline)+
    tripleoscillator+
    audiofileprocessor***
    bitinvader*
    papu(=FreeBoy)*
    kicker
    lb302
    malletsstk(=Mallets)
    monstro
    OPL2(=OpulenZ)(quiet)
    organic
    sfxr+
    sid
    vibedstrings(=Vibed)*
    watsyn*
    zynaddsubfx**

    * Uses a graph, optional for freeboy.
    ** Embedded synth
    *** Relative file paths
    """
"""def createInstrument(instrumentName,drum=0,bird=0):
    if instrumentName=="nes":return{"vol":"1", #master volume.
    "vibr":"0", #master vibrato (depth only).
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
    "waveForm":["0","3"][drum], #waveform, square 0, saw 1, sine 2, noise 3. All other values are normals.
    "att":["0","0.7"][drum], #attack.
    "hold":str([str(r.choice(range(10))/10),"0"][drum]), #hold (time until sustain).
    "sus":"0", #punch (very short).
    "dec":["0.4","0.5"][drum], #decay (sustain time).
    "startFreq":["0.352",str(r.choice(range(600))/1000+.2)][drum], #0.352 is natural, use a range for drums.
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
    if instrumentName=="malletsstk":return{"preset":[r.choice(["1","4","6","9"]),r.choice(["0","1","2","5","8"])][drum],
                                           # Instrument selection. Different choices when used as drums.
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
"""

# Make an instrument and attach it to the parent parameter.
def makeInstrument(parent, pan=2, fxch="1", pitchrange="1", pitch="0",
                   basenote="57", vol="60", instrumentName="nes",type=0,env=0,bird=0,drum=0):
    # Set the basic variables every track has, pan, volume, that sort of stuff.
    instrumentTrack=ET.SubElement(parent,"instrumenttrack",{"pan":["-60","60","0"][pan],
                                                           "fxch":fxch,
                                                           "pitchrange":pitchrange,
                                                           "pitch":pitch,
                                                           "basenote":basenote,
                                                           "vol":[vol,"100"][drum]})
    # A branching path emerges, depending on the instrument of choice.
    # Every instrument has a specific name, "nes" is for nescaline.
    instrument=ET.SubElement(instrumentTrack,"instrument", {"name":instrumentName})
    # Only the first tab is depending on the actual instrument name, the others are the same regardless.
    if bird: ET.SubElement(instrument,instrumentName,LMMSMeditative.makeBird(instrumentName,bird))
    elif type==0:ET.SubElement(instrument,instrumentName,LMMSChip.createInstrument(instrumentName,shapeSample))
    elif type==1:ET.SubElement(instrument,instrumentName,LMMSMeditative.createInstrument(instrumentName,shapeSample))
    elif type==2:ET.SubElement(instrument,instrumentName,LMMSDrums.createInstrument(instrumentName,shapeSample))
    # This is where the branching path ends.
    # eldata is for the envelope tab.
    eldata=ET.SubElement(instrumentTrack,"eldata",{"fres":"2",
                                                   "ftype":"14",
                                                   "fcut":"14000",
                                                   "fwet":"0"})
    """    # Connect the formant filter to an LFO.
    if drum==0:
        connection=ET.SubElement(eldata,"connection")
        ET.SubElement(connection,"fcut",{"id":"1"})"""
    # Envelope tab part 1, volume envelope.
    ET.SubElement(eldata,"elvol",{"lspd_denominator":"4",
                                    "sustain":"1",
                                    "pdel":"0",
                                    "userwavefile":"",
                                    "dec":"0.5",
                                    "lamt":"0",
                                    "syncmode":"0",
                                    "latt":"0",
                                    "rel":"0.5",
                                    "amt":["0","1"][env],
                                    "x100":"0",
                                    "att":"0.7",
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

def FXChain(parent,addReverb=False,addStereo=False,addLimiter=True):
    if not addReverb and not addStereo:return ET.SubElement(parent,"fxchain",{"numofeffects":"0","enabled":"1"})
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
    # add the stereo enhancer to the chain.
    if addStereo:
        fx=ET.SubElement(fxchain,"effect",{"name":"stereoenhancer",
            "autoquit_numerator":"4",
            "on":"1",
            "wet":"1",
            "gate":"0",
            "autoquit_syncmode":"0",
            "autoquit_denominator":"4",
            "autoquit":"1"})
        stereoControls=ET.SubElement(fx,"stereoenhancercontrols",{"width":"0"})
        con=ET.SubElement(stereoControls,"connection")
        # Connect the width dial to the same automation LFO as the formant filter.
        ET.SubElement(con,"width",{"id":"0"})
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
        result+=pack('f',.5+(sin(2*pi/length*x)/2)) if onlyPositive else pack('f',sin(2*pi/length*x))
        # onlyPositive means the whole thing needs to be shrunk down by half and moved up by half as well.
    return result

def squarewave(length, onlyPositive):
    result=b''
    # Simple square wave, it's either 1 or it's not.
    for x in range(length):
        if x<length/2:
            # It's 1 here.
            result+=pack('f',1)
        else:
            # It's not here. It's 0 if it's called for.
            result+=pack('f',0) if onlyPositive else pack('f',-1)
    return result

def sawwave(length, onlyPositive):
    result=b''
    # This is literally just a line.
    for x in range(length):
        # y=x, but it needs to slope depending on the length so it maxes out at 1.
        result+=pack('f',x/length) if onlyPositive else pack('f',((x/length)*2)-1)
    return result

def smoothwave(length, onlyPositive):
    sample=r.random()
    result=pack('f',sample)
    # Since the first sample's already added, the length is reduced by 1 (though doesn't really matter).
    for x in range(length-1):
        # Add or subtract a random value no further than .1 away. Meaning shrink down to a fifth and balance it.
        sample+=((r.random())/5)-.1
        # Make sure sample doesn't go out of bounds.
        sample=min(max(sample,0),1) if onlyPositive else min(max(sample,-1),1)
        # Pack the new sample.
        result+=pack('f', sample)
    return result


def noisewave(length, onlyPositive):
    result=b''
    for x in range(length):
        # Limit it to .5F to avoid screeches.
        result+=pack("f", r.random() / 2) if onlyPositive else pack("f", r.random() - .5)
    return result

# Sample shaper
def shapeSample(length,onlyPositive=False):
    # A sample length of 4 (bitinvader's minimum) only needs 4 floats, but freeboy has 32 and most others have >=200.
    # The range is between 0f to 1f for freeboy (and other only positive graphs) or between -1f and 1f otherwise.
    # Math time. Split up, team. Generate a byte of floats.
    byte=r.choice([sinewave(length,onlyPositive),squarewave(length,onlyPositive),
                   sawwave(length,onlyPositive),smoothwave(length,onlyPositive),
                   noisewave(length,onlyPositive)])
    #byte=smoothwave(length,onlyPositive)
    # do a magic.
    return str(b64encode(byte))[2:-1]

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
# Major scale, change for modes or esotheric scales. Add the key.
scale=[0+key,2+key,4+key,5+key,7+key,9+key,11+key]
# Add the scale two times times
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
        progression.append(r.choice(range(0,4)))
        # followed by something that's higher than the second (but not the 7th)
        progression.append(r.choice(range(progression[-1]+1,5)))
        # and finally one that's lower than the third.
        progression.append(r.choice(range(0, progression[-1]-1)))
    return progression


def makeMelody(flutePattern,progression,sectionLength):
    # The melody should be multiples of four bars long.
    # This could mean it sometimes won't show up in a non-0 length section,
    # but those are parts where it would thematically make sense, like the intro.
    sectionLength=sectionLength-(sectionLength%4)
    # Keep track of stuff.
    barNumber=newBar=1
    # Add a bunch of notes.
    length=0
    # Don't worry about this.
    breaker=False
    # The first note of a bar is going to be the note middle tonic (second octave).
    note=keys[progression[barNumber-1]] #same as keys[7]
    # Every section has its own length. If a section has length less than 3 bars long it gets skipped.
    while length<sectionLength*192 and not breaker:
        # pos=starting position, vol=velocity, key=pitch (60=C5), len=duration (48=quarter), pan=pan.
        # Generate a random note length.
        noteLength=r.choice([8,16,32,64])
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
            ET.SubElement(flutePattern, "note",
                          {"pos": str(length), "vol": str(r.randint(60, 100)), "key": str(note), "len": str(noteLength),
                           "pan": "0"})
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
# ---------------Other utils--------------
def randbool(odds):
    return True if r.randrange(0,100)<odds else False