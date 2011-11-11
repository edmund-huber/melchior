import socket, ssl, sys

host, port, passw = sys.argv[1:]

ssl_sock = ssl.wrap_socket(socket.socket())
ssl_sock.connect((host, int(port)))

ssl_sock.sendall('''PASS %s
NICK melchior
USER melchior melchiorbot %s bla :Melchior
''' % (passw, host))

read_buffer = ''
while True:

    # Pick out the completed lines,
    read_buffer += ssl_sock.recv()
    i = read_buffer.rfind('\n')
    if i == -1:
        lines = []
    else:
        lines = read_buffer[:i].split('\n')
        read_buffer = read_buffer[i:]
    
    # Deal with messages.
    for line in lines:
        parts = line.strip().split()
        if parts:
            if parts[0].startswith(':'):
                parts = parts[1:]
            if parts[0] == 'PING':
                ssl_sock.sendall('PONG %s\n' % parts[1])
            elif parts[0] == 'MODE':
                # Cannot join til after given mode.
                ssl_sock.sendall('JOIN #photoz\n')
