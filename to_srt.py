import codecs
import re
import math

FILE_NAME = "sample.xml"


def leading_zeros(value, digits=2):
    value = "000000" + str(value)
    return value[-digits:]


def convert_time(raw_time):
    ms = leading_zeros(int(raw_time[:-4]) % 1000, 3)
    # only interested in milliseconds, let's drop the additional digits
    time_in_seconds = int(raw_time[:-7])
    second = leading_zeros(time_in_seconds % 60)
    minute = leading_zeros(int(math.floor(time_in_seconds / 60)))
    hour = leading_zeros(int(math.floor(time_in_seconds / 3600)))
    return "{}:{}:{},{}".format(hour, minute, second, ms)


text = u""
with codecs.open(FILE_NAME, 'rb', "utf-8") as f:
    text = f.read()

sub_lines = (l for l in text.split("\n") if l.startswith("<p begin="))
subs = []
prev_time = {"start": 0, "end": 0}
prev_content = []
for s in sub_lines:
    start = re.search(u'begin\="([0-9]*)', s).group(1)
    end = re.search(u'end\="([0-9]*)', s).group(1)
    content = re.search(u'xml\:id\=\"subtitle[0-9]+\">(.*)</p>', s).group(1)
    prev_start = prev_time["start"]
    if (prev_start == start and prev_time["end"] == end) or not prev_start:
        # there may be multiple lines starting at the same time. This fixes it.
        prev_time = {"start": start, "end": end}
        prev_content.append(content)
        continue
    subs.append({
        "start_time": convert_time(prev_time["start"]),
        "end_time": convert_time(prev_time["end"]),
        "content": u"\n".join(prev_content),
        })
    prev_time = {"start": start, "end": end}
    prev_content = [content]
subs.append({
    "start_time": convert_time(start),
    "end_time": convert_time(end),
    "content": u"\n".join(prev_content),
})

with codecs.open(FILE_NAME + ".srt", 'wb', "utf-8") as f:
    lines = (u"{}\n{} --> {}\n{}\n".format(
        s+1, subs[s]["start_time"], subs[s]["end_time"], subs[s]["content"])
        for s in range(len(subs)))
    f.write(u"\n".join(lines))
