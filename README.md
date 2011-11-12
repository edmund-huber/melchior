A simple but useful customizable IRC bot in python. Supports SSL! Only
connects to one server, and one channel, for now.

For melchior to run, it needs to be told where to connect to (host,
port, channel, etc) and what to do when it gets there (behaviors,
which are simply decorated methods).

See example.py for an example IRC bot implementing the behaviors that
will be introduced right now.

The first kind of behavior is a 'listener'. It gets called for every
message in the channel, and its return value (if truthy) is said by
the bot. The return value convention is adhered to for all types of
behaviors.

For example, to repeat what everyone says, but only if what they say
has the letter 'a' somewhere in it,

```python
import melchior
@melchior.listener
def echo(nick, msg):
    if 'a' in msg:
        return '%s said "%s"' % (nick, msg)
    else:
        return None
```

The second kind of behavior is a 'responder'. It gets called only when
the bot is mentioned by name. Suppose someone says "melchior: who are
you", here's how the bot could respond,

```python
import melchior
@melchior.responder
def who_is_melchior(nick, msg):
    if msg == 'who are you':
        return '%s, i am a bot.' % nick
```

The third kind of behavior is a 'periodic'. It gets called every N
seconds, where N is the number given to the decorator. To tell the
time every five seconds,

```python
import melchior
@melchior.periodic(5)
def time():
    import time
    return 'the time is %s' % time.asctime()
```