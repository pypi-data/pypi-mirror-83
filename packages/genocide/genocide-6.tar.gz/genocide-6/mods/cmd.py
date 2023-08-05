# GENOCIDE - the king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io
#
#

"basic commands (cmd)"

import mods, ol, threading, time

k = ol.krn.get_kernel()

def cmd(event):
    "list commands (cmd)"
    c = sorted(ol.keys(ol.tbl.mods))
    if c:
        event.reply(",".join(c))

def tsk(event):
    "list tasks (tsk)"
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        d = vars(thr)
        o = ol.Object()
        ol.update(o, d)
        if ol.get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - ol.krn.starttime)
        thrname = thr.getName()
        result.append((up, psformat % (thrname, ol.tms.elapsed(up))))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append(txt)
    event.reply(" | ".join(res))

def upt(event):
    "show uptime (utp)"
    event.reply(ol.tms.elapsed(time.time() - ol.krn.starttime))

def ver(event):
    "show version (ver)"
    event.reply("GENOCIDE %s | %s" % (mods.__version__, mods.__txt2__))
