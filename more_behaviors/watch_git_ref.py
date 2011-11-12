import difflib
import subprocess

import melchior

def watch_git_ref(clone, named_remote, ref):

    old_head = [None]
    old_log = [None]

    def inner():
        
        # A very terrible way to do this, patches welcome.
        head = subprocess.check_output('cd "%s" ; git fetch %s ; git log -1 --pretty=format:%%H %s/%s'
                                       % (clone, named_remote, named_remote, ref), shell=True)
        log = subprocess.check_output('cd "%s" ; git fetch %s ; git log %s/%s --oneline'
                                      % (clone, named_remote, named_remote, ref), shell=True)
        
        if (old_head[0] is not None) and (head != old_head[0]):
            fromfile = 'git log -1 %s' % old_head[0]
            tofile = 'git log -1 %s' % head
            to_return = '\n'.join(difflib.unified_diff(old_log[0].split('\n'), log.split('\n'), fromfile=fromfile, tofile=tofile, n=2))
        else:
            to_return = None
            
        old_head[0] = head
        old_log[0] = log
        return to_return
    
    return melchior.periodic(5)(inner)
