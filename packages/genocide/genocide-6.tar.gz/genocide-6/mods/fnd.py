# GENOCIDE - the king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io
#
#

"find objects (fnd)"

import ol
import os
import time

def fnd(event):
    "locate and show objects on disk"
    if not event.args:
        wd = os.path.join(ol.wd, "store", "")
        ol.cdir(wd)
        fns = os.listdir(wd)
        fns = sorted({x.split(os.sep)[0].split(".")[-1].lower() for x in fns})
        if fns:
            event.reply(",".join(fns))
        return
    nr = -1
    args = []
    try:
        args = event.prs.args[1:]
    except IndexError:
        args = ol.keys(o)
    for otype in event.types:
        for o in ol.dbs.find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            pure = True
            if "f" in event.prs.opts:
                pure = False
            txt = "%s %s" % (str(nr), ol.format(o, args, pure, event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (ol.tms.elapsed(time.time() - ol.tms.fntime(o.stp)))
            event.reply(txt)
