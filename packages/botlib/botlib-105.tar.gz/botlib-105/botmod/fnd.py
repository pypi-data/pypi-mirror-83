"find objects (fnd)"

import ol
import os
import time

from ol.spc import elapsed, find, fntime, get_kernel

k = get_kernel()

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
        args = event.args[1:]
    except IndexError:
        pass
    types = ol.get(k.names, event.args[0], [event.cmd,])
    for otype in types:
        for o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            pure = True
            if not args:
                args = ol.keys(o)
            if "f" in event.prs.opts:
                pure = False
            txt = "%s %s" % (str(nr), ol.format(o, args, pure, event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(o.stp)))
            event.reply(txt)
