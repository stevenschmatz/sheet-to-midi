"""Sheet to MIDI conversion tool"""


import argparse
import os


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


def open_pdf(filename):
    if not os.path.isfile(filename):
        print("Shit.")
    else:
        print("Woohoo")

def main():
    pdf_filename, midi_filename = get_args()
    open_pdf(pdf_filename)


if __name__ == "__main__":
    main()
