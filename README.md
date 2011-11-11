The simplest possible IRC bot in python. Supports SSL! Only connects
to one server, and one channel, for now.

To make the bot do something when someone says something in the
channel, add something to behavior.py . For example, to repeat what
someone just said,

```python
@method
def echo(nick, msg):
    return '%s said "%s"' % (nick, msg)
```