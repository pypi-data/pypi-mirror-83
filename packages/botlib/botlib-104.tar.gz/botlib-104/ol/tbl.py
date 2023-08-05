# OLIB - object library
#
#

import ol

classes = ol.Object()
mods = ol.Object()
funcs = ol.Object()
names = ol.Object()

ol.update(classes, {"Bus": ["ol.bus"], "Cfg": ["mods.udp"], "Console": ["ol.csl"], "Email": ["mods.mbx"], "Event": ["ol.evt"], "Feed": ["mods.rss"], "Fetcher": ["mods.rss"], "Getter": ["ol.prs"], "Handler": ["ol.hdl"], "Kernel": ["ol.krn"], "Loader": ["ol.ldr"], "Log": ["mods.ent"], "Option": ["ol.prs"], "Repeater": ["ol.tms"], "Rss": ["mods.rss"], "Seen": ["mods.rss"], "Setter": ["ol.prs"], "Skip": ["ol.prs"], "Timed": ["ol.prs"], "Timer": ["ol.tms"], "Todo": ["mods.ent"], "Token": ["ol.prs"], "UDP": ["mods.udp"]})

ol.update(mods, {"cfg": "mods.cfg", "cmd": "mods.cmd", "cor": "mods.mbx", "dne": "mods.ent", "dpl": "mods.rss", "fed": "mods.rss", "fnd": "mods.fnd", "ftc": "mods.rss", "log": "mods.ent", "mbx": "mods.mbx", "rem": "mods.rss", "rss": "mods.rss", "tdo": "mods.ent", "tsk": "mods.cmd", "upt": "mods.cmd", "ver": "mods.cmd"})

ol.update(funcs, {"cfg": "mods.cfg.cfg", "cmd": "mods.cmd.cmd", "cor": "mods.mbx.cor", "dne": "mods.ent.dne", "dpl": "mods.rss.dpl", "fed": "mods.rss.fed", "fnd": "mods.fnd.fnd", "ftc": "mods.rss.ftc", "log": "mods.ent.log", "mbx": "mods.mbx.mbx", "rem": "mods.rss.rem", "rss": "mods.rss.rss", "tdo": "mods.ent.tdo", "tsk": "mods.cmd.tsk", "upt": "mods.cmd.upt", "ver": "mods.cmd.ver"})

ol.update(names, {"bus": ["ol.bus.Bus"], "cfg": ["mods.udp.Cfg"], "console": ["ol.csl.Console"], "email": ["mods.mbx.Email"], "event": ["ol.evt.Event"], "feed": ["mods.rss.Feed"], "fetcher": ["mods.rss.Fetcher"], "getter": ["ol.prs.Getter"], "handler": ["ol.hdl.Handler"], "kernel": ["ol.krn.Kernel"], "loader": ["ol.ldr.Loader"], "log": ["mods.ent.Log"], "option": ["ol.prs.Option"], "repeater": ["ol.tms.Repeater"], "rss": ["mods.rss.Rss"], "seen": ["mods.rss.Seen"], "setter": ["ol.prs.Setter"], "skip": ["ol.prs.Skip"], "timed": ["ol.prs.Timed"], "timer": ["ol.tms.Timer"], "todo": ["mods.ent.Todo"], "token": ["ol.prs.Token"], "udp": ["mods.udp.UDP"]})
