import math

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
