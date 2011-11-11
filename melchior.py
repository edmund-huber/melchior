import argparse
import socket, ssl, subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--host')
parser.add_argument('--port')
parser.add_argument('--password')
parser.add_argument('--channel')
parser.add_argument('--watch')
args = parser.parse_args()
assert set(['host', 'port', 'password', 'channel']) <= set(vars(args).keys())

ssl_sock = ssl.wrap_socket(socket.socket())
ssl_sock.connect((args.host, int(args.port)))
ssl_sock.setblocking(0)

ssl_sock.sendall('''PASS %s
NICK melchior
USER melchior melchiorbot %s bla :Melchior
''' % (args.password, args.host))

last_watch_time = time.time()
last_watch_outp = None
read_buffer = ''
while True:
    time.sleep(1)

    # Pick out the completed lines
    try:
        read_buffer += ssl_sock.recv()
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
                    ssl_sock.sendall('PONG %s\n' % parts[1])
                elif parts[0] == 'MODE':
                    # Cannot join til after given mode.
                    ssl_sock.sendall('JOIN #%s\n' % args.channel)
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
                    ssl_sock.sendall('PRIVMSG #%s :%s\n' % (args.channel, line))
                last_watch_outp = outp
        except:
            pass
        

