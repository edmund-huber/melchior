import argparse
import re
import socket, ssl, subprocess
import time

def bye(s):
    pass

def run(host, port, use_ssl, password, channel, nick, behaviors, logger=bye):

    # Set up socket
    sock = socket.socket()
    if use_ssl:
        sock = ssl.wrap_socket(sock)
    sock.connect((host, int(port) if port else 6667))
    sock.setblocking(0)

    # Send password, and register
    if password:
        sock.sendall('PASS %s\r\n' % password)
    sock.sendall('''NICK %s\r
USER melchior melchiorbot %s bla :Melchior\r
''' % (nick, host))

    # Do scheduling,
    listeners, responders, periodics = [], [], []
    for b in behaviors:
        ty, args, m = b
        if ty == BehaviorType.LISTENER:
            listeners.append(m)
        elif ty == BehaviorType.RESPONDER:
            responders.append(m)
        elif ty == BehaviorType.PERIODIC:
            (t,) = args
            periodics.append((time.time() + t, t, m))

    def handle_method(m, *args):
        msg = m(*args)
        if msg:
            for m in msg.split('\n'):
                sock.sendall('PRIVMSG #%s :%s\r\n' % (channel, m))

    read_buffer = ''
    while True:
        time.sleep(0.25)

        try:
            read_buffer += sock.recv(4096)
        except socket.error, ssl.SSLError:
            # nonblocking i/o raises an exception when there's nothing to be read
            pass

        # Pick out the completed lines
        i = read_buffer.rfind('\n')
        if i == -1:
            lines = []
        else:
            lines = read_buffer[:i].split('\n')
            read_buffer = read_buffer[i:]

        # Deal with messages.
        for line in [l for l in lines if l]:
            line = line.strip()
            logger(line)
            parts = line.split()
            if parts:
                nick2 = None
                if parts[0].startswith(':'):
                    m = re.match(r'^:(.*?)!(.*?)@(.*)$', parts[0])
                    if m:
                        nick2 = m.group(1)
                    parts = parts[1:]
                if parts[0] == 'PING':
                    sock.sendall('PONG %s\r\n' % parts[1])
                elif parts[0] == 'MODE':
                    # Cannot join til after given mode.
                    sock.sendall('JOIN #%s\r\n' % channel)
                elif (parts[0] == 'PRIVMSG') and (parts[1] == '#%s' % channel):
                    # Call all 'listeners'
                    for method in listeners:
                        handle_method(method, nick2, ' '.join([parts[2][1:]] + parts[3:]))
                    # 'responders' only speak when spoken to.
                    if parts[2][1:].startswith(nick):
                        for method in responders:
                            handle_method(method, nick2, ' '.join(parts[3:]))

        # Deal with any periodic operations
        new_periodics = []
        for t, dt, method in periodics:
            if time.time() > t:
                handle_method(method)
                new_periodics.append((time.time() + dt, dt, method))
            else:
                new_periodics.append((t, dt, method))
        periodics = new_periodics

class BehaviorType:
    LISTENER = 0
    RESPONDER = 1
    PERIODIC = 2

def listener(f):
    return (BehaviorType.LISTENER, (), f)

def responder(f):
    return (BehaviorType.RESPONDER, (), f)

class periodic(object):

    def __init__(self, t):
        self.t = t

    def __call__(self, f):
        return (BehaviorType.PERIODIC, (self.t,), f)
