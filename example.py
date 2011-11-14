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

import more_behaviors.once_a_day

melchior.run(args.host, args.port, args.ssl, args.password, args.channel, args.nick, [
        more_behaviors.once_a_day.once_a_day(11, 0, 30, 'jtwang, davidh, edmund, jrheard, steng: SEO standup')
        ], logger=to_stdout)
