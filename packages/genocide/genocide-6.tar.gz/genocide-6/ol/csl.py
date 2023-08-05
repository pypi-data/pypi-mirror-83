# OLIB - object library
#
#

"console (csl)"

import atexit
import ol
import readline
import threading
import time

#:
cmds = []
#:
resume = {}

def init(k):
    c = Console()
    c.start()
    return c

class Console(ol.Object):

    "console class"

    def __init__(self):
        super().__init__()
        self.ready = threading.Event()
        ol.bus.bus.add(self)

    def announce(self, txt):
        "silence announcing"
        pass

    def direct(self, txt):
        "print txt"
        print(txt.rstrip())

    def input(self):
        "loop for input"
        k = ol.krn.get_kernel()
        while 1:
            try:
                event = self.poll()
            except EOFError:
                print("")
                continue
            event.orig = repr(self)
            k.queue.put(event)
            event.wait()

    def poll(self):
        "wait for input"
        e = ol.evt.Event()
        e.orig = repr(self)
        e.txt = input("> ")
        return e

    def say(self, channel, txt):
        "strip channel from output"
        self.direct(txt)

    def start(self):
        "start console"
        k = ol.krn.get_kernel()
        setcompleter(k.cmds)
        ol.tsk.launch(self.input)

def complete(text, state):
    "complete matches"
    matches = []
    if text:
        matches = [s for s in cmds if s and s.startswith(text)]
    else:
        matches = cmds[:]
    try:
        return matches[state]
    except IndexError:
        return None

def getcompleter():
    "return the completer"
    return readline.get_completer()

def setcompleter(commands):
    "set the completer"
    cmds.extend(commands)
    readline.set_completer(complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))
