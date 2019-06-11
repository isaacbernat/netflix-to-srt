__author__ = "Leonardo Brayner e Silva"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = "Leonardo Brayner e Silva"
__email__ = "brayner.l@gmail.com"

import tempfile
import subprocess
import sys
from functools import reduce

_, temp_path = tempfile.mkstemp()
temp_redir = open(temp_path, "w+")

def ensure_pip():
    subprocess.call([sys.executable, '-m', 'ensurepip', '--default-pip'],
        stdout=temp_redir,stderr=temp_redir)

ensure_pip()

def install(directive):
    command = [sys.executable, '-m', 'pip', 'install']
    if type(directive) is list:
        command = command + directive
    else:
        command.append(directive)
    subprocess.call(command,stdout=temp_redir,stderr=temp_redir)

# https://stackoverflow.com/a/37961211
def import_or_install(package):
    if type(package) is tuple:
        assembly = package[0]
        name = package[1]
    else:
        assembly = package
        name = package
    try:
        __import__(assembly)
        return False
    except ImportError:
        install(name)
        return True

def import_packages():
    install("wheel") # sidestepping a bug
    return reduce((lambda x, y: x or y),
            [import_or_install(("webvtt","webvtt-py")),
                import_or_install("html2text"),
                import_or_install("pysrt")])

if import_packages():
    print("Ran for the first time and installed packages. Please try again.")
    sys.exit(0)

import os
from webvtt import WebVTT
import html
from html2text import HTML2Text
from pysrt.srtitem import SubRipItem
from pysrt.srttime import SubRipTime

script = sys.argv[0]
args = sys.argv[1:]

def usage():
    return "%s FILE...\n" % os.path.basename(script)

if len(args) < 1:
    sys.stderr.write(usage())
    sys.exit(1)

for arg in args:
    index = 0

    file_name, file_extension = os.path.splitext(arg)

    if not file_extension.lower() == ".vtt":
        sys.stderr.write("Skipping %s.\n" % arg)
        continue

    srt = open(file_name + ".srt", "w")

    for caption in WebVTT().read(arg):
        index += 1
        start = SubRipTime(0,0,caption.start_in_seconds)
        end = SubRipTime(0,0,caption.end_in_seconds)
        srt.write(SubRipItem(
             index
            ,start
            ,end
            ,html.unescape(caption.text))
                .__str__()+"\n")
