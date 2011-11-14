import melchior

import time

def once_a_day(hour, minute, warn_s, notify_msg):

    announced = set()
    check_s = 5
    assert check_s < warn_s

    def inner():
        t = time.localtime()
        y, m, d, h, mi, s, wday, yday, isdst = t
        now = time.mktime(t)
        if (y, m, d) not in announced:
            todays_standup = time.mktime((y, m, d, hour, minute, 0, wday, yday, isdst))
            if now + warn_s >= todays_standup:
                announced.add((y, m, d))
                return notify_msg

    return melchior.periodic(check_s)(inner)
