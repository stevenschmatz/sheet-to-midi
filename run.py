"""Sheet to MIDI conversion tool"""

from __future__ import print_function

import argparse
import os
from wand.image import Image
import atexit
import shutil


def get_args():
    """Retrieves the input and output filenames from argparse.
    
    The program requires specification of the input filename, and the output filename is optional.
    If not provided, the program writes the MIDI notes of `hello.pdf` to `hello.mid`, if a .pdf extension.
    Else, for example, the program writes `hello.ext` to `hello.ext.out`.

    Returns:
        - Tuple of (PDF filename, MIDI filename)
    """
    
    parser = argparse.ArgumentParser(description='Convert a given sheet music PDF into a MIDI file.')
    parser.add_argument('pdf_filename', metavar='pdf_filename')
    parser.add_argument('-o', '--out', metavar='midi_filename', dest='midi_filename', help='Output MIDI filename')

    args = parser.parse_args()

    pdf_filename = args.pdf_filename
    midi_filename = args.midi_filename

    if midi_filename is None:
        index = pdf_filename.find('.pdf')
        if index == -1:
            midi_filename = pdf_filename + '.mid'
        else:
            midi_filename = pdf_filename[:index] + '.mid'

    return pdf_filename, midi_filename


def create_pdf_images(pdf_filename):
    if not os.path.isfile(pdf_filename):
        print("That's not a file.")
        sys.exit(1)

    print("Converting PDF to images...")

    try:
        os.mkdir('temp')
    except OSError:
        pass

    with Image(filename=pdf_filename, resolution=200) as img:
        img.save(filename="temp/pdf.png")


def cleanup():
    """Removes the temp folder on exit."""
    #shutil.rmtree("temp")
    print("Done")


def main():
    # Register the removal of temporary files at exit
    atexit.register(cleanup)

    pdf_filename, midi_filename = get_args()
    create_pdf_images(pdf_filename)


if __name__ == "__main__":
    main()
