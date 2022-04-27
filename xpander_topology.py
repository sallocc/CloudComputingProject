from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import UserSwitch, Host, RemoteController
from mininet.net import Mininet
import random

class XpanderTopo( Topo ):
    "The XPander topology."

    setLogLevel('debug')
    def build(self, numSwitches=16, numHosts= 10):
        switches = []
        hosts = []
        links = []
        switchDegrees = [0 for i in range(numSwitches)]

        print("Adding initial switches")
        #Add an initial complete graph
        switches.append(self.addSwitch('s1', cls=UserSwitch, protocols='OpenFlow10'))
        switches.append(self.addSwitch('s2', cls=UserSwitch, protocols='OpenFlow10'))
        switches.append(self.addSwitch('s3', cls=UserSwitch, protocols='OpenFlow10'))
        switches.append(self.addSwitch('s4', cls=UserSwitch, protocols='OpenFlow10'))
        print("Adding initial switch links")
        for i in range(1, len(switches)):
            for j in range(i):
                links.append((i, j))
                switchDegrees[i] = switchDegrees[i]+1
                switchDegrees[j] = switchDegrees[j]+1

        #2-lift while loop
        while len(switches) < numSwitches:
            #Double the amount of switches
            prevNumSwitches = len(switches)
            for i in range(prevNumSwitches):
                switches.append(self.addSwitch(f's{len(switches) + 1}', cls=UserSwitch, protocols='OpenFlow10'))
            #For each link (i, j) in the previous graph, either link up the   
            # (i + len/2, j) and (i, j + len/2) or (i, j) and (i + len/2, j + len/2)  
            # randomly seeded 
            linksToAdd = []
            #Choose which links to add to the new graph
            for link in links:
                a,b = link
                choice = random.randint(0, 1)
                if choice == 0:
                    linksToAdd.append((a + prevNumSwitches, b))
                    linksToAdd.append((a, b + prevNumSwitches))
                else:
                    linksToAdd.append((a + prevNumSwitches, b + prevNumSwitches))
                    linksToAdd.append((a, b))
            #Replace previous links with new chosen ones
            links = linksToAdd

        # Add all links to graph
        for (i, j) in links:
            self.addLink(switches[i], switches[j])

        #Connect hosts to switches
        for i in range(numSwitches):
            hostAdd = self.addHost(f'h{i + 1}', cls=Host)
            self.addLink(hostAdd, switches[i])

def pingTest():
    topo = XpanderTopo(degree=4, numSwitches=20, numHosts=16)
    net = Mininet(topo)
    net.addController(name = 'c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.start()
    net.pingAll
    net.iperf()
    net.stop()

topos = { 'xpander': ( lambda: XpanderTopo(numSwitches=32, numHosts=32) ) }

if __name__ == "__main__":
    pingTest()