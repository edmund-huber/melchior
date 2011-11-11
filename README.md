The simplest possible IRC bot in python. Supports SSL! Only connects
to one server, and one channel, for now.

The bot's behavior is defined in behavior.py .

For example, to repeat what someone just said, add this to behavior.py ,

```python
@listener
def echo(nick, msg):
    return '%s said "%s"' % (nick, msg)
```

To respond to a user,

```python
@responder
def who_is_melchior(nick, msg):
    if msg == 'who are you':
        return '%s, i am a bot.' % nick
```

To say something perodically,

```python
@periodic(5)
def time():
    import time
    return 'the time is %s' % time.asctime()
```