import re
from time_utils import convert_time

def convert_vtt_time(line):
    times = line.replace(".", ",").split(" --> ")
    if len(times[0]) == 9:
        times = ["00:" + t for t in times]
    return "{} --> {}".format(times[0], times[1].split(" ")[0])

def vtt_to_srt(text):
    if not text.startswith(u"\ufeffWEBVTT") and not text.startswith(u"WEBVTT"):
        raise Exception(".vtt format must start with WEBVTT, wrong file?")
    styles = get_vtt_styles(text)
    style_tag_re = re.compile(u'<c\.(.*)>(.*)</c>')

    lines = []
    current_sub_line = []
    for line in text.split("\n"):
        if current_sub_line:
            if line:
                style_tag = re.search(style_tag_re, line)
                if style_tag:
                    line = style_tag.group(2)  # line is just the text part
                    color = styles.get(style_tag.group(1).split(".")[0])
                    if color:
                        line = u"<font color={}>{}</font>".format(color, line)
                current_sub_line.append(line)
            else:
                lines.append("\n".join(current_sub_line) + "\n\n")
                current_sub_line = []

        elif " --> " in line:
            current_sub_line = [convert_vtt_time(line)]
    if current_sub_line:
        lines.append("\n".join(current_sub_line))

    return "".join((u"{}\n{}".format(i, l) for i, l in enumerate(lines, 1)))

def get_vtt_styles(text):  # just using it for color ATM
    styles = {}
    lines = text.split("\n")
    n = 0
    style_name_re = re.compile(u'::cue\(\.(.*)\).*')
    color_re = re.compile(u'.*color: (\#.*);')
    while n < len(lines):  # not efficient to go through all text, but it's ok
        style_name = re.search(style_name_re, lines[n])
        if style_name and style_name.groups():
            name = style_name.group(1)
            color = re.search(color_re, lines[n + 1])
            if color and color.groups():
                styles[name] = color.group(1)
        n += 1
    return styles
