# Sample sheet music generator by @lasconic
# https://github.com/lasconic/randomsheetmusic
# TODO: Clean this up

import sys
from music21 import *
import random
import urllib
import os

import zipfile
import StringIO

class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = StringIO.StringIO()

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "a", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()


def title_generator():
    adjectives = ["Red", "Blue", "Black", "White", "Playful", "Quiet", "Rebellious", "Studious", "Affectionate", "Fascinating", "Unspeakable", "Tremulous", "Perverted", "Fallacious", "Clueless", "Deep", "Passionate", "Tattered", "Fake", "Binary", "Part-Time", "Crispy", "Sufficient", "Echoing", "Progressive", "Chaotic", "Lasconic's"]
    nouns = ["Hammer", "Drill", "Cutter", "Knife", "Groove", "Fight", "Ballad", "Operetta", "Ants", "Rhythm", "Associations", "Prawns", "Afternoon", "Circumstances", "Experience", "Punishment", "Players", "Martyr", "Notturno", "Vibe", "Relics", "Operations", "Movements", "Ideas", "Lightning", "Body", "Humans", "Extravagance", "Cookies", "Eyes", "Elements", "Oratorio", "Composition"]
    randomNumber1 = random.randrange(0, len(adjectives))
    randomNumber2 = random.randrange(0, len(nouns))
    name = adjectives[randomNumber1] + " " + nouns[randomNumber2]
    return name


def inInterval(pi, note, aInterval):
    if not note:
        return True
    descInterval = aInterval.reverse()
    descInterval.noteStart = note
    aInterval.noteStart = note
    if pi.midi >= descInterval.noteEnd.pitch.midi and pi.midi <= aInterval.noteEnd.pitch.midi:
        return True
    return False


leaps = ["M2", "M3", "P4", "P5", "M6", "M7", "P8"]

def generate():
    maxMeasure = 32
    if maxMeasure <= 0 or maxMeasure >= 500:
        maxMeasure = 32

    timeSignature = "4/4"

    keySignature = "0" 
    if keySignature == "chromatic":
        keySignature = "0"
    if keySignature >= -7 and keySignature <= 7:
        keySignature = int(keySignature)
    else:
        keySignature = 0

    durations = []
    durations.append(0.125)
    durations.append(0.25)
    durations.append(0.5)
    durations.append(1.0)
    durations.append(2.0)
    durations.append(4.0)
    durations.append(0.375)
    durations.append(0.75)
    durations.append(1.5)
    durations.append(3.0)
    durations.append(6.0)

    ambitus = "59,84".split(",")
    a1 = pitch.Pitch()
    a1.midi = int(ambitus[0])
    a2 = pitch.Pitch()
    a2.midi = int(ambitus[1])

    partLower = stream.Part()
    partLower.metadata = metadata.Metadata()
    partLower.metadata.title = title_generator()
    partLower.metadata.composer = ''

    ks = key.KeySignature(keySignature)
    partLower.insert(0, ks)

    ts = meter.TimeSignature(timeSignature)
    partLower.insert(0, ts)

    maxLeap = "P8"
    if maxLeap != "nolimit" and maxLeap in leaps:
        aInterval = interval.Interval(maxLeap)
    else:
        maxLeap = "nolimit"

    noUnison = "off"

    m = 0
    prevNote = 0
    sc = ks.getScale()
    list = [p for p in sc.getPitches(a1, a2)]
    for mnb in range(0, maxMeasure):
        m = stream.Measure()
        remaining = ts.barDuration.quarterLength
        while remaining > 0:
            tmpDurations = [i for i in durations if i <= remaining]
            if prevNote and maxLeap != "nolimit":
                uInterval = aInterval
                dInterval = uInterval.reverse()
                uInterval.noteStart = prevNote
                dInterval.noteStart = prevNote
                startNote = dInterval.noteEnd.pitch
                endNote = uInterval.noteEnd.pitch
                if startNote < a1:
                    startNote = a1
                if endNote > a2:
                    endNote = a2
                shortlist = sc.getPitches(startNote.nameWithOctave, endNote.nameWithOctave)
            else:
                shortlist = list
            if (noUnison and prevNote and prevNote.pitch in shortlist):
                shortlist.remove(prevNote.pitch)
            n = note.Note(random.choice(shortlist))
            prevNote = n
            n.quarterLength = random.choice(tmpDurations)
            remaining = remaining - n.quarterLength
            m.append(n)
        if mnb != 0 and mnb != maxMeasure and mnb % 4 == 0:
            sl = layout.SystemLayout(isNew=True)
            m.insert(0, sl)
        partLower.append(m)

    if m:
        b = bar.Barline('final')
        m.rightBarline = b

    return partLower
