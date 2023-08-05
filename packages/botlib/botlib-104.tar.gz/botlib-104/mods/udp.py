# GENOCIDE - the king of the netherlands commits genocide - OTP-CR-117/19/001 - otp.informationdesk@icc-cpi.int - https://genocide.rtfd.io
#
#

"udp to irc relay"

import ol
import select
import socket
import sys
import time

def init(kernel):
    "start a udp to irc relay server and return it"
    u = UDP()
    u.start()
    return u

class Cfg(ol.Cfg):

    "udp configuration"

    def __init__(self):
        super().__init__()
        self.host = "localhost"
        self.port = 5500

class UDP(ol.Object):

    "udp to irc relay server"

    def __init__(self):
        super().__init__()
        self.stopped = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._sock.setblocking(1)
        self._starttime = time.time()
        self.cfg = Cfg()

    def output(self, txt, addr):
        "output message on fleet"
        k = get_fleet()
        for bot in k.fleet.bots:
            bot.announce(txt.replace("\00", ""))

    def server(self):
        "loop for output"
        try:
            self._sock.bind((self.cfg.host, self.cfg.port))
        except socket.gaierror:
            return
        while not self.stopped:
            (txt, addr) = self._sock.recvfrom(64000)
            if self.stopped:
                break
            data = str(txt.rstrip(), "utf-8")
            if not data:
                break
            self.output(data, addr)

    def exit(self):
        "stop udp to irc relay server"
        self.stopped = True
        self._sock.settimeout(0.01)
        self._sock.sendto(bytes("exit", "utf-8"), (self.cfg.host, self.cfg.port))

    def start(self):
        "start udp to irc relay server"
        ol.dbs.last(self.cfg)
        ol.tsk.launch(self.server)

def toudp(host, port, txt):
    "send text over udp to the udp to irc relay server"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(txt.strip(), "utf-8"), (host, port))
