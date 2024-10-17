import argparse
import codecs
import os
from time_utils import convert_time
from xml_converter import xml_to_srt
from vtt_converter import vtt_to_srt

SUPPORTED_EXTENSIONS = [".xml", ".vtt"]

def to_srt(text, extension):
    if extension.lower() == ".xml":
        return xml_to_srt(text)
    if extension.lower() == ".vtt":
        return vtt_to_srt(text)

def main():
    directory = "."
    help_text = u"path to the {} directory (defaults to current directory)"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=directory,
                        help=help_text.format("input", directory))
    parser.add_argument("-o", "--output", type=str, default=directory,
                        help=help_text.format("output", directory))
    a = parser.parse_args()
    filenames = [fn for fn in os.listdir(a.input)
                 if fn[-4:].lower() in SUPPORTED_EXTENSIONS]
    for fn in filenames:
        with codecs.open(u"{}/{}".format(a.input, fn), 'rb', "utf-8") as f:
            text = f.read()
        with codecs.open(u"{}/{}.srt".format(a.output, fn), 'wb', "utf-8") as f:
            f.write(to_srt(text, fn[-4:]))

if __name__ == '__main__':
    main()
