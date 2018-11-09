import threading
import time

import Pyro4
import socket
import subprocess

a = 0

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def startServer():
    print("start server")
    Ip = get_ip()
    str = "pyro4-ns --host "
    cmd = str + Ip
    print(cmd)
    subprocess.call(cmd, shell=True)


def startNS():
    print("executou")
    with Pyro4.Daemon(get_ip()) as daemon:
        # daemon = Pyro4.Daemon(get_ip())
        ns = Pyro4.locateNS(get_ip())
        uri = daemon.register(Teste)
        ns.register("obj", uri)
        print("Objeto registrado")
        print(uri)
        daemon.requestLoop()


@Pyro4.expose
@Pyro4.oneway
class Teste:
    def teste(self, d):
        print(d)
        return d


class chamadaReversa(threading.Thread):

    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID


    def paraAqui(self):
        print("aqui")
        pass

    def reversa(self):
        ns = Pyro4.locateNS(get_ip())
        uri = ns.lookup("back")
        print(uri, "back")
        d = input("Informe a direcao: ")
        direcao = int(d)
        a = Pyro4.Proxy(uri)
        a.testcall(direcao)

    def interrompeT(self):
        global a
        a = 1
        print("A t4: ", a)


    def run(self):
        print("Starting ", self.threadID)
        print("ID", self.threadID)
        if self.threadID == 1:
            startServer()
        elif self.threadID == 2:
            startNS()
        elif self.threadID == 3:
            chamadaReversa.imprimeContador(self)
        elif self.threadID == 4:
            chamadaReversa.interrompeT(self)
        else:
            chamadaReversa.reversa(self)

        print("Exiting ", self.threadID)


    def imprimeContador(self):
        global a
        print("A = ", a )
        while(a != 1):
            self.n = 0
            while(self.n < 2):
                print("Valor do A = ", a)
                time.sleep(0.5)
                self.n = self.n+1
            #self.a = self.a + 1


# Create new threads
thread1 = chamadaReversa(1)
thread2 = chamadaReversa(2)
thread3 = chamadaReversa(3)
thread4 = chamadaReversa(4)
thread5 = chamadaReversa(5)
# Start new Threads

thread1.start()
time.sleep(2)
thread2.start()
time.sleep(5)
# thread3.start()
# time.sleep(4)
# thread4.start()
# time.sleep(5)
thread5.start()

