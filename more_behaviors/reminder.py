"""
This helper sucks for two reasons:

  * only one reminder can be popped off the stack at a time, since in
    order for melchior to say something it must 'return'. I'm thinking
    of moving to a messaging model instead..

  * melchior doesn't give you a way to share data between methods or
    invocations of methods, so I'm using a global
"""

import re
import time

import melchior

reminders = []

@melchior.periodic(10)
def check_reminders():
    new_reminders = []
    global reminders
    for r in reminders:
        t, who, what = r
        if time.time() >= t:
            reminders = list(set(reminders) - set([r]))
            return '%s: reminder: %s' % (who, what)

@melchior.listener
def set_reminder(who, msg):
    m = re.search(r': remind me', msg)
    if m:
        m = re.search(r': remind me (\d*):(\d*) ?(am|pm)?\s*(.*)$', msg)
        if m:
            remind_h, remind_m, ampm, what = int(m.group(1)), int(m.group(2)), m.group(3), m.group(4)
            if 'pm' == ampm:
                remind_h += 12
            year, month, day, hour, minute, second, wday, yday, isdst = time.localtime()
            remind_tm = time.mktime((year, month, day, remind_h, remind_m, 0, wday, yday, isdst))
            reminders.append((remind_tm, who, what))
            return '%s: reminder set for %s:%s' % (who, remind_h, remind_m)
        else:
            return '%s: say something like "remind me 8:15am dentist"' % who
