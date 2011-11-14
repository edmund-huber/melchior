import argparse

import melchior
import example_behaviors

parser = argparse.ArgumentParser()
parser.add_argument('--host', required=True)
parser.add_argument('--port', required=False)
parser.add_argument('--ssl', required=False, action='store_true')
parser.add_argument('--password', required=False)
parser.add_argument('--channel', required=True)
parser.add_argument('--nick', required=False, default='melchior')
args = parser.parse_args()
assert set(['host', 'port', 'password', 'channel']) <= set(vars(args).keys())

def to_stdout(s):
    print s

melchior.run(args.host, args.port, args.ssl, args.password, args.channel, args.nick, [
        example_behaviors.echo,
        example_behaviors.who_is_melchior,
        example_behaviors.tell_the_time,
        ], logger=to_stdout)
