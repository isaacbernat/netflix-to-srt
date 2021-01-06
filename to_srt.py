import argparse
import codecs
import math
import os
import re


SUPPORTED_EXTENSIONS = [".xml", ".vtt"]


def leading_zeros(value, digits=2):
    value = "000000" + str(value)
    return value[-digits:]


def convert_time(raw_time):
    if int(raw_time) == 0:
        return "{}:{}:{},{}".format(0, 0, 0, 0)

    ms = '000'
    if len(raw_time) > 4:
        ms = leading_zeros(int(raw_time[:-4]) % 1000, 3)
    time_in_seconds = int(raw_time[:-7]) if len(raw_time) > 7 else 0
    second = leading_zeros(time_in_seconds % 60)
    minute = leading_zeros(int(math.floor(time_in_seconds / 60)) % 60)
    hour = leading_zeros(int(math.floor(time_in_seconds / 3600)))
    return "{}:{}:{},{}".format(hour, minute, second, ms)


def xml_id_display_align_before(text):
    """
    displayAlign="before" means the current sub will be displayed on top.
    That is and not at bottom. We check what's the xml:id associated to it
    to have an {\an8} position tag in the output file.
    """
    align_before_re = re.compile(u'<region.*tts:displayAlign=\"before\".*xml:id=\"(.*)\"/>')
    has_align_before = re.search(align_before_re, text)
    if has_align_before:
        return has_align_before.group(1)
    return u""


def xml_get_cursive_style_ids(text):
    style_section = re.search("<styling>(.*)</styling>", text, flags=re.DOTALL)
    if not style_section:
        return []
    style_ids_re = re.compile(
        '<style.* tts:fontStyle="italic".* xml:id=\"([a-zA-Z0-9_.]+)\"')
    return [re.search(style_ids_re, line).groups()[0]
            for line in style_section.group().split("\n")
            if re.search(style_ids_re, line)]


def xml_cleanup_spans_start(span_id_re, cursive_ids, text):
    has_cursive = []
    span_start_tags = re.findall(span_id_re, text)
    for s in span_start_tags:
        has_cursive.append(u"<i>" if s[1] in cursive_ids else u"")
        text = has_cursive[-1].join(text.split(s[0], 1))
    return text, has_cursive


def xml_cleanup_spans_end(span_end_re, text, has_cursive):
    span_end_tags = re.findall(span_end_re, text)
    for s, cursive in zip(span_end_tags, has_cursive):
        cursive = u"</i>" if cursive else u""
        text = cursive.join(text.split(s, 1))
    return text


def to_srt(text, extension):
    if extension.lower() == ".xml":
        return xml_to_srt(text)
    if extension.lower() == ".vtt":
        return vtt_to_srt(text)


def convert_vtt_time(line):
    times = line.replace(".", ",").split(" --> ")
    if len(times[0]) == 9:
        times = ["00:" + t for t in times]
    return "{} --> {}".format(times[0], times[1].split(" ")[0])


def vtt_to_srt(text):
    if not text.startswith(u"\ufeffWEBVTT") and not text.startswith(u"WEBVTT"):
        raise Exception(".vtt format must start with WEBVTT, wrong file?")

    lines = []
    current_sub_line = []
    for line in text.split("\n"):
        if current_sub_line:
            current_sub_line.append(line)
            if not line:
                lines.append("\n".join(current_sub_line) + "\n")
                current_sub_line = []

        elif " --> " in line:
            current_sub_line = [convert_vtt_time(line)]
    if current_sub_line:
        lines.append("\n".join(current_sub_line))

    return "".join((u"{}\n{}".format(i, l) for i, l in enumerate(lines, 1)))


def xml_to_srt(text):
    def append_subs(start, end, prev_content, format_time):
        subs.append({
            "start_time": convert_time(start) if format_time else start,
            "end_time": convert_time(end) if format_time else end,
            "content": u"\n".join(prev_content),
        })

    display_align_before = xml_id_display_align_before(text)
    begin_re = re.compile(u"\s*<p begin=")
    sub_lines = (l for l in text.split("\n") if re.search(begin_re, l))
    subs = []
    prev_time = {"start": 0, "end": 0}
    prev_content = []
    start = end = ''
    start_re = re.compile(u'begin\="([0-9:\.]*)')
    end_re = re.compile(u'end\="([0-9:\.]*)')
    content_re = re.compile(u'\">(.*)</p>')

    # some span tags are used for italics, we'll replace them by <i> and </i>,
    # which is the standard for .srt files. We ignore all other uses.
    cursive_ids = xml_get_cursive_style_ids(text)
    span_id_re = re.compile(u'(<span style=\"([a-zA-Z0-9_.]+)\">)+')
    span_end_re = re.compile(u'(</span>)+')
    br_re = re.compile(u'(<br\s*\/?>)+')
    fmt_t = True
    for s in sub_lines:
        s, has_cursive = xml_cleanup_spans_start(
            span_id_re, cursive_ids, s)

        string_region_re = r'<p(.*region="' + display_align_before + r'".*")>(.*)</p>'
        s = re.sub(string_region_re, r'<p\1>{\\an8}\2</p>', s)
        content = re.search(content_re, s).group(1)

        br_tags = re.search(br_re, content)
        if br_tags:
            content = u"\n".join(content.split(br_tags.group()))

        content = xml_cleanup_spans_end(
            span_end_re, content, has_cursive)

        prev_start = prev_time["start"]
        start = re.search(start_re, s).group(1)
        end = re.search(end_re, s).group(1)
        if len(start.split(":")) > 1:
            fmt_t = False
            start = start.replace(".", ",")
            end = end.replace(".", ",")
        if (prev_start == start and prev_time["end"] == end) or not prev_start:
            # Fix for multiple lines starting at the same time
            prev_time = {"start": start, "end": end}
            prev_content.append(content)
            continue
        append_subs(prev_time["start"], prev_time["end"], prev_content, fmt_t)
        prev_time = {"start": start, "end": end}
        prev_content = [content]
    append_subs(start, end, prev_content, fmt_t)

    lines = (u"{}\n{} --> {}\n{}\n".format(
        s + 1, subs[s]["start_time"], subs[s]["end_time"], subs[s]["content"])
        for s in range(len(subs)))
    return u"\n".join(lines)


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
        with codecs.open("{}/{}".format(a.input, fn), 'rb', "utf-8") as f:
            text = f.read()
        with codecs.open("{}/{}.srt".format(a.output, fn), 'wb', "utf-8") as f:
            f.write(to_srt(text, fn[-4:]))


if __name__ == '__main__':
    main()
