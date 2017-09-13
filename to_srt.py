import argparse
import codecs
import math
import os
import re


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


def to_srt(text):
    def append_subs(start, end, prev_content, format_time):
        subs.append({
            "start_time": convert_time(start) if format_time else start,
            "end_time": convert_time(end) if format_time else end,
            "content": u"\n".join(prev_content),
        })
    # displayAlign="before" means the current sub will be displayed on top, and not at bottom,
    # so we check what's the xml:id associated to it to have an {\an8} position tag in the output file
    check_display_align_before_re = re.compile(u'<region.*tts:displayAlign=\"before\".*xml:id=\"(.*)\"/>')
    xml_id_display_align_before = re.search(check_display_align_before_re, text).group(1)    
    begin_re = re.compile(u"\s*<p begin=")
    sub_lines = (l for l in text.split("\n") if re.search(begin_re, l))
    subs = []
    prev_time = {"start": 0, "end": 0}
    prev_content = []
    start = end = ''
    start_re = re.compile(u'begin\="([0-9:\.]*)')
    end_re = re.compile(u'end\="([0-9:\.]*)')
    # this regex was sometimes too strict. I hope the new one is never too lax
    # content_re = re.compile(u'xml\:id\=\"subtitle[0-9]+\">(.*)</p>')
    content_re = re.compile(u'\">(.*)</p>')
	# span tags are only used for italics, so we'll get rid of them
	# and replace them by <i> and </i>, which is the standard for .srt files
    # alt_content_re = re.compile(u'<span style=\"[a-zA-Z0-9_]+\">(.*?)</span>')
    span_start_re = re.compile(u'(<span style=\"[a-zA-Z0-9_.]+\">)+')
    span_end_re = re.compile(u'(</span>)+')
    br_re = re.compile(u'(<br\s*\/?>)+')
    fmt_t = True
    for s in sub_lines:
        span_start_tags = re.search(span_start_re, s)
        if span_start_tags:
            s = u"<i>".join(s.split(span_start_tags.group()))
        string_region_re = r'<p(.*region="' + xml_id_display_align_before + r'".*")>(.*)</p>'		
        #s = re.sub(r'<p(.*region="region.top.centre".*")>(.*)</p>', r'<p\1>{\\an8}\2</p>', s)
        s = re.sub(string_region_re, r'<p\1>{\\an8}\2</p>', s)
        content = []
        # alt_content = re.search(alt_content_re, s)
        # while (alt_content):  # background text may have additional styling.
            # background may also contain several `<span> </span>` groups
            # s = s.replace(alt_content.group(0), alt_content.group(1))
            # alt_content = re.search(alt_content_re, s)
        content = re.search(content_re, s).group(1)

        br_tags = re.search(br_re, content)
        if br_tags:
            content = u"\n".join(content.split(br_tags.group()))
		
        span_end_tags = re.search(span_end_re, content)
        if span_end_tags:
           content = u"</i>".join(content.split(span_end_tags.group()))		
		
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
    help_text = "path to the {} directory (defaults to current directory)"
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, default=directory,
                        help=help_text.format("input", directory))
    parser.add_argument("-o", "--output", type=str, default=directory,
                        help=help_text.format("output", directory))
    a = parser.parse_args()
    xmls = [x for x in os.listdir(a.input) if x[-4:] == ".xml"]
    for x in xmls:
        with codecs.open("{}/{}".format(a.input, x), 'rb', "utf-8") as f:
            text = f.read()
        with codecs.open("{}/{}.srt".format(a.output, x), 'wb', "utf-8") as f:
            f.write(to_srt(text))


if __name__ == '__main__':
    main()
