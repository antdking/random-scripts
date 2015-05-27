import json
import sys

import hexchat

from threading import Thread

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode
except ImportError:
    from urllib2 import urlopen
    from urllib import urlencode

__module_name__ = "AutoPaste"
__module_version__ = "1.0"
__module_description__ = ("Automatically uploads longer messages/pastes to"
                          "an online paste service.")

print('Loaded module: %s version %s' % (__module_name__, __module_version__))


def worker(inputbox):
    try:
        data = urlopen('https://ptpb.pw/', 
                       data=urlencode({'c': inputbox}).encode(),
                       timeout=10).readlines()
    except:  # don't care!
        hexchat.prnt('Could not upload data')
        hexchat.command('say %s' % inputbox)
        return None

    for d in data:
        if not hasattr(d, 'encode'):
            d = d.decode()
        if d.startswith('url:'):
            url = d.split(' ')[1]

    if not url:
        hexchat.prnt('Could not parse return data.')
        hexchat.command('say %s' % inputbox)
        return None

    hexchat.command('say %s' % url.strip())


def auto_paste(word, word_eol, userdata):
    if word[2] != '\r':
        return None
    inputbox = hexchat.get_info('inputbox')
    if inputbox[0] == '/' and inputbox[1] != '/':
        return None  # don't take any chances. don't touch commands.

    if '\n' not in inputbox:
        return None
    c = inputbox.count('\n')
    if c < 4:
        return None

    hexchat.prnt('More than 4 lines. Uploading as a paste.')
    hexchat.command('settext')
    Thread(target=worker, args=(inputbox,)).start()
    return hexchat.EAT_HEXCHAT

# We need to use a key press hook because the other events clear
# the input box first, and split the message up.. so lots of events
# fire and no way to tell if they're grouped.
hexchat.hook_print('Key Press', auto_paste)
