methods = []
def method(f):
    methods.append(f)
    return f

@method
def echo(nick, msg):
    return '%s said "%s"' % (nick, msg)
