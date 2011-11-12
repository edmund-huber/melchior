import time

import melchior

@melchior.listener
def echo(nick, msg):
    if 'a' in msg:
        return '%s said "%s"' % (nick, msg)
    else:
        return None

@melchior.responder
def who_is_melchior(nick, msg):
    if msg == 'who are you':
        return '%s, i am a bot.' % nick

@melchior.periodic(5)
def tell_the_time():    
    return 'the time is %s' % time.asctime()
