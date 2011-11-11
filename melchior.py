import argparse
import socket, ssl, subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--host', required=True)
parser.add_argument('--channel', required=True)
parser.add_argument('--port', required=False)
parser.add_argument('--ssl', required=False, action='store_true')
parser.add_argument('--password', required=False)
parser.add_argument('--watch', required=False)
args = parser.parse_args()
assert set(['host', 'port', 'password', 'channel']) <= set(vars(args).keys())

sock = socket.socket()
if args.ssl:
    sock = ssl.wrap_socket(sock)
sock.connect((args.host, int(args.port) if args.port else 6667))
sock.setblocking(0)

# Register
if args.password:
    sock.sendall('PASS %s\r\n' % args.password)
sock.sendall('''NICK melchiorzzz9393\r
USER melchior33zz melchiorbot33zz %s bla :Melchior33zz\r
''' % (args.host))

last_watch_time = time.time()
last_watch_outp = None
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
                if parts[0].startswith(':'):
                    parts = parts[1:]
                if parts[0] == 'PING':
                    sock.sendall('PONG %s\r\n' % parts[1])
                elif parts[0] == 'MODE':
                    # Cannot join til after given mode.
                    sock.sendall('JOIN #%s\r\n' % args.channel)
    except:
        # nonblocking i/o raises an exception when there's nothing to be read
        pass

    # Check the watch if last watch happened 5s ago
    now = time.time()
    if args.watch and (now - 5 > last_watch_time):
        last_watch_time = now
        try:
            outp = subprocess.check_output(args.watch, shell=True)
            if outp != last_watch_outp:
                for line in outp.split('\n'):
                    sock.sendall('PRIVMSG #%s :%s\n' % (args.channel, line))
                last_watch_outp = outp
        except:
            pass
        

