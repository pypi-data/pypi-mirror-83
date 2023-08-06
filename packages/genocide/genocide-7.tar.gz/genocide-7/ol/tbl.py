# OLIB - object library
#
#

import ol

#:
classes = ol.Object()
#:
mods = ol.Object()
#:
funcs = ol.Object()
#:
names = ol.Object()

ol.update(classes, {"Bus": ["ol.bus"], "Cfg": ["mods.udp"], "Console": ["ol.csl"], "DCC": ["mods.irc"], "Email": ["mods.mbx"], "Event": ["mods.irc"], "Feed": ["mods.rss"], "Fetcher": ["mods.rss"], "Getter": ["ol.prs"], "Handler": ["ol.hdl"], "IRC": ["mods.irc"], "Kernel": ["ol.krn"], "Loader": ["ol.ldr"], "Log": ["mods.ent"], "Option": ["ol.prs"], "Repeater": ["ol.tms"], "Rss": ["mods.rss"], "Seen": ["mods.rss"], "Setter": ["ol.prs"], "Skip": ["ol.prs"], "Timed": ["ol.prs"], "Timer": ["ol.tms"], "Todo": ["mods.ent"], "Token": ["ol.prs"], "UDP": ["mods.udp"], "User": ["mods.irc"], "Users": ["mods.irc"]})

ol.update(mods, {"cfg": "mods.cfg", "cmd": "mods.cmd", "dne": "mods.ent", "dpl": "mods.rss", "fed": "mods.rss", "fnd": "mods.fnd", "ftc": "mods.rss", "log": "mods.ent", "mbx": "mods.mbx", "rem": "mods.rss", "req": "mods.req", "rss": "mods.rss", "sts": "mods.sui", "tdo": "mods.ent", "trt": "mods.trt", "tsk": "mods.cmd", "udp": "mods.udp", "upt": "mods.cmd", "ver": "mods.cmd", "wsd": "mods.wsd"})

ol.update(funcs, {"cfg": "mods.cfg.cfg", "cmd": "mods.cmd.cmd", "dne": "mods.ent.dne", "dpl": "mods.rss.dpl", "fed": "mods.rss.fed", "fnd": "mods.fnd.fnd", "ftc": "mods.rss.ftc", "log": "mods.ent.log", "mbx": "mods.mbx.mbx", "rem": "mods.rss.rem", "req": "mods.req.req", "rss": "mods.rss.rss", "sts": "mods.sui.sts", "tdo": "mods.ent.tdo", "trt": "mods.trt.trt", "tsk": "mods.cmd.tsk", "udp": "mods.udp.udp", "upt": "mods.cmd.upt", "ver": "mods.cmd.ver", "wsd": "mods.wsd.wsd"})

ol.update(names, {"bus": ["ol.bus.Bus"], "cfg": ["mods.udp.Cfg"], "console": ["ol.csl.Console"], "dcc": ["mods.irc.DCC"], "email": ["mods.mbx.Email"], "event": ["mods.irc.Event"], "feed": ["mods.rss.Feed"], "fetcher": ["mods.rss.Fetcher"], "getter": ["ol.prs.Getter"], "handler": ["ol.hdl.Handler"], "irc": ["mods.irc.IRC"], "kernel": ["ol.krn.Kernel"], "loader": ["ol.ldr.Loader"], "log": ["mods.ent.Log"], "option": ["ol.prs.Option"], "repeater": ["ol.tms.Repeater"], "rss": ["mods.rss.Rss"], "seen": ["mods.rss.Seen"], "setter": ["ol.prs.Setter"], "skip": ["ol.prs.Skip"], "timed": ["ol.prs.Timed"], "timer": ["ol.tms.Timer"], "todo": ["mods.ent.Todo"], "token": ["ol.prs.Token"], "udp": ["mods.udp.UDP"], "user": ["mods.irc.User"], "users": ["mods.irc.Users"]})
