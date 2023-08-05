# GENOCIDE - the king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io
#
#

"data entry"

import ol

class Log(ol.Object):

    "log items"

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(ol.Object):

    "todo items"

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    "flag a todo item as done (dne)"
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for o in ol.dbs.find("mods.ent.Todo", selector):
        o._deleted = True
        ol.save(o)
        event.reply("ok")
        break

def log(event):
    "log some text (log)"
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    ol.save(l)
    event.reply("ok")

def tdo(event):
    "add a todo item (tdo)"
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    ol.save(o)
    event.reply("ok")
