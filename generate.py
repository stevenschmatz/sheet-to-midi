# Sheet music generation with music21

from music21 import *
import shutil
from randomsheetmusic import generate

NUM_SAMPLES_TO_GENERATE = 100


def get_filenames(i):
    """Returns the filepaths for the output MusicXML and .png files.
   
    Parameters:
    - i: unique identifier for the score

    Returns:
    - (sheet_png_filepath, musicxml_out_filepath)
    """

    output_folder_prefix = "dataset/"
    sheet_png_out_filepath = output_folder_prefix + "{}-sheet.png".format(i)
    musicxml_out_filepath = output_folder_prefix + "{}-musicxml.xml".format(i)

    return (sheet_png_out_filepath, musicxml_out_filepath)


def main():
    """Generates random sheet music sample and MusicXML file pairs."""

    for i in xrange(NUM_SAMPLES_TO_GENERATE):
        (sheet_path, musicxml_path) = get_filenames(i)

        rand_musicxml = generate()
        rand_musicxml.write('musicxml', musicxml_path)
        filepath = rand_musicxml.write('musicxml.png')
        shutil.copy(filepath, sheet_path)


if __name__ == "__main__":
    main()
