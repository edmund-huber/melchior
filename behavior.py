listeners = []
def listener(f):
    listeners.append(f)
    return f

responders = []
def responder(f):
    responders.append(f)
    return f

periodics = []
class periodic(object):
    def __init__(self, t):
        self.t = t
    def __call__(self, f):
        periodics.append((self.t, f))

@listener
def echo(nick, msg):
    return '%s said "%s"' % (nick, msg)

@responder
def who_is_melchior(nick, msg):
    if msg == 'who are you':
        return '%s, i am a bot.' % nick

@periodic(5)
def time():
    import time
    return 'the time is %s' % time.asctime()
