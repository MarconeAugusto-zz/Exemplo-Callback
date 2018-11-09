from __future__ import print_function

import threading
import time
import Pyro4

def conectaServer():
    ns = Pyro4.locateNS("172.18.2.145")
    uri = ns.lookup("obj")
    print("objeto requisitado")
    print(uri)
    d = input("Informe a direcao: ")
    direcao = int(d)
    a = Pyro4.Proxy(uri)
    print(a.teste(d))

class chamadaReversa():
    @Pyro4.expose
    @Pyro4.callback
    def testcall(self, di):
        print(di)
        return di


class Callback(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def registraCallback(self):
        call = chamadaReversa()
        daemon = Pyro4.core.Daemon("172.18.2.145")
        ns = Pyro4.locateNS("172.18.2.145")
        uri = daemon.register(call)
        server = ns.register("back", uri)
        print("Objeto registrado Callback")
        print(uri)
        daemon.requestLoop()

    def run(self):
        print("Starting ", self.threadID)
        print("ID", self.threadID)
        if self.threadID == 1:
            Callback.registraCallback(self)
        else:
            conectaServer()
        print("Exiting ", self.threadID)


# Create new threads
thread1 = Callback(1)
thread2 = Callback(2)
# Start new Threads
thread1.start()
time.sleep(2)
thread2.start()



