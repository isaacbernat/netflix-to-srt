import codecs
import re
import math
import argparse


def leading_zeros(value, digits=2):
    value = "000000" + str(value)
    return value[-digits:]


def convert_time(raw_time):
    ms = leading_zeros(int(raw_time[:-4]) % 1000, 3)
    # only interested in milliseconds, let's drop the additional digits
    time_in_seconds = int(raw_time[:-7])
    second = leading_zeros(time_in_seconds % 60)
    minute = leading_zeros(int(math.floor(time_in_seconds / 60)) % 60)
    hour = leading_zeros(int(math.floor(time_in_seconds / 3600)))
    return "{}:{}:{},{}".format(hour, minute, second, ms)


def to_srt(text):
    def append_subs(start, end, prev_content):
        subs.append({
            "start_time": convert_time(start),
            "end_time": convert_time(end),
            "content": u"\n".join(prev_content),
        })

    sub_lines = (l for l in text.split("\n") if l.startswith("<p begin="))
    subs = []
    prev_time = {"start": 0, "end": 0}
    prev_content = []
    start_re = re.compile(u'begin\="([0-9]*)')
    end_re = re.compile(u'end\="([0-9]*)')
    content_re = re.compile(u'xml\:id\=\"subtitle[0-9]+\">(.*)</p>')
    alt_content_re = re.compile(u'<span style=\"style_0\">(.*)</span>')
    for s in sub_lines:
        content = re.search(content_re, s).group(1)
        alt_content = re.search(alt_content_re, s)
        if alt_content:  # some background text has additional styling
            content = alt_content.group(1)

        prev_start = prev_time["start"]
        start = re.search(start_re, s).group(1)
        end = re.search(end_re, s).group(1)
        if (prev_start == start and prev_time["end"] == end) or not prev_start:
            # Fix for multiple lines starting at the same time
            prev_time = {"start": start, "end": end}
            prev_content.append(content)
            continue
        append_subs(prev_time["start"], prev_time["end"], prev_content)
        prev_time = {"start": start, "end": end}
        prev_content = [content]
    append_subs(start, end, prev_content)

    lines = (u"{}\n{} --> {}\n{}\n".format(
        s+1, subs[s]["start_time"], subs[s]["end_time"], subs[s]["content"])
        for s in range(len(subs)))
    return u"\n".join(lines)


def main():
    filename = "sample.xml"
    help_text = "path to the {} file (defaults to {})"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=filename,
                        help=help_text.format("input", filename))
    parser.add_argument("-o", "--output", type=str, default=filename + ".srt",
                        help=help_text.format("output", filename + ".srt"))
    a = parser.parse_args()

    with codecs.open(a.input, 'rb', "utf-8") as f:
        text = f.read()

    with codecs.open(a.output, 'wb', "utf-8") as f:
        f.write(to_srt(text))

if __name__ == '__main__':
    main()
