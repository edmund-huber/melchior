import argparse
import re
import socket, ssl, subprocess
import time

import behavior

parser = argparse.ArgumentParser()
parser.add_argument('--host', required=True)
parser.add_argument('--channel', required=True)
parser.add_argument('--port', required=False)
parser.add_argument('--ssl', required=False, action='store_true')
parser.add_argument('--password', required=False)
parser.add_argument('--nick', required=False, default='melchior')
args = parser.parse_args()
assert set(['host', 'port', 'password', 'channel']) <= set(vars(args).keys())

# Set up socket
sock = socket.socket()
if args.ssl:
    sock = ssl.wrap_socket(sock)
sock.connect((args.host, int(args.port) if args.port else 6667))
sock.setblocking(0)

# Register
if args.password:
    sock.sendall('PASS %s\r\n' % args.password)
sock.sendall('''NICK %s\r
USER melchior melchiorbot %s bla :Melchior\r
''' % (args.nick, args.host))

# Schedule the first round of periodic behaviors,
periodic_schedule = [(time.time() + t, t, f) for t, f in behavior.periodics]

def maybe_say_in_channel(msg):
    if msg:
        sock.sendall('PRIVMSG #%s :%s\r\n' % (args.channel, msg))

read_buffer = ''
while True:
    time.sleep(0.25)

    # Pick out the completed lines
    try:
        read_buffer += sock.recv(4096)
        i = read_buffer.rfind('\n')
        if i == -1:
            lines = []
        else:
            lines = read_buffer[:i].split('\n')
            read_buffer = read_buffer[i:]

        # Deal with messages.
        for line in lines:
            print line
            parts = line.strip().split()
            if parts:
                nick = None
                if parts[0].startswith(':'):
                    m = re.match(r'^:(.*?)!(.*?)@(.*)$', parts[0])
                    if m:
                        nick = m.group(1)
                    parts = parts[1:]
                if parts[0] == 'PING':
                    sock.sendall('PONG %s\r\n' % parts[1])
                elif parts[0] == 'MODE':
                    # Cannot join til after given mode.
                    sock.sendall('JOIN #%s\r\n' % args.channel)
                elif (parts[0] == 'PRIVMSG') and (parts[1] == '#%s' % args.channel):
                    # Call all 'listeners'
                    for method in behavior.listeners:
                        maybe_say_in_channel(method(nick, ' '.join([parts[2][1:]] + parts[3:])))
                    # 'responders' only speak when spoken to.
                    if parts[2][1:].startswith(args.nick):
                        for method in behavior.responders:
                            maybe_say_in_channel(method(nick, ' '.join(parts[3:])))
                            
    except socket.error, ssl.SSLError:
        # nonblocking i/o raises an exception when there's nothing to be read
        pass

    # Deal with any periodic operations
    new_periodic_schedule = []
    for t, dt, method in periodic_schedule:
        if time.time() > t:
            maybe_say_in_channel(method())
            new_periodic_schedule.append((time.time() + dt, dt, method))
        else:
            new_periodic_schedule.append((t, dt, method))
    periodic_schedule = new_periodic_schedule
