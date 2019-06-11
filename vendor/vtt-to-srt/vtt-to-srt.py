__author__ = "Leonardo Brayner e Silva"
__copyright__ = "Copyright 2019"
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = "Leonardo Brayner e Silva"
__email__ = "brayner.l@gmail.com"

# https://thesmithfam.org/blog/2012/10/25/temporarily-suppress-console-output-in-python
# from contextlib import contextmanager
# import sys
# import os
# import tempfile

# @contextmanager
# def suppress_stdout():
#     _, temp_path = tempfile.mkstemp()
#     stdout_redir = open(temp_path, "w")
#     old_stdout = sys.stdout
#     sys.stdout = stdout_redir
#     try:  
#         yield
#     finally:
#         sys.stdout = old_stdout

# https://stackoverflow.com/a/37961211
import contextlib
import tempfile
import pip
import sys
from functools import reduce

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
        pip.main(['install', name])       
        return True

def import_packages():
    _, temp_path = tempfile.mkstemp()
    temp_redir = open(temp_path, "w")
    with contextlib.redirect_stderr(temp_redir):
        with contextlib.redirect_stdout(temp_redir):
            return reduce((lambda x, y: x or y),
                    [import_or_install("wheel"), 
                        import_or_install(("webvtt","webvtt-py")),
                        import_or_install("html2text"),
                        import_or_install("pysrt")])
            # return (import_or_install("wheel")
            #         or import_or_install(("webvtt","webvtt-py"))
            #         or import_or_install("html2text")
            #         or import_or_install("pysrt"))

if import_packages():
    print("Ran for the first time and imported packages. Please run again.")
    sys.exit(0)

# import subprocess

# # https://stackoverflow.com/a/50255019
# def install(package):
#     subprocess.call([sys.executable, "-m", "pip", "install", package])

# install("html2text")
# install("pysrt")
# install("webvtt-py")

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
