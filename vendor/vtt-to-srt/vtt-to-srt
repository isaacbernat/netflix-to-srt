#!/usr/bin/env python3

import sys
from webvtt import WebVTT
import html
import os
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
