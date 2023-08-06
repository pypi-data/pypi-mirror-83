"configuration (cfg)"

import ol

from ol.spc import last
from bot.irc import Cfg

def cfg(event):
    "configure irc."
    c = Cfg()
    ol.dbs.last(c)
    o = ol.Default()
    ol.prs.parse(o, event.prs.otxt)
    if o.sets:
        ol.update(c, o.sets)
        ol.save(c)
    event.reply(ol.format(c, skip=["username", "realname"]))
