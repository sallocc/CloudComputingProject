from mininet.net import Mininet
from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.node import Controller, OVSKernelSwitch, RemoteController, Host, UserSwitch
# import networkx as nx
import random



class MyTopo( Topo ):
    "Jellyfish topology."

    setLogLevel('debug')

    class JellyfishNodeID(object):

        def __init__(self, dpid = None, name = None):
            if dpid:
                self.dpid = dpid
                self.sw = self.dpid
                self.pod = 1
            else:
                self.dpid = int(name[1:])
                self.sw = self.dpid
                self.pod = 1
        
        def __str__(self):
            return 's',int(self.dpid)

        def name_str(self):
            return 's',int(self.dpid)

        def ip_str(self):
            hi = (self.dpid & 0xff0000) >> 16
            mid = (self.dpid & 0xff00) >> 8
            lo = self.dpid & 0xff
            return "10.%i.%i.%i" % (hi, mid, lo)

            


    def __init__(self, dpid = None):
        self.id_gen = MyTopo.JellyfishNodeID
        self.k = 1
        self.LAYER_CORE = 0
        self.g = []
        self.switchList = []
        self.hosts = []
        self.links = []

    def build(self , degree=4, numHosts=10, numSwitches=10):
        "Create a jellyfish topology."
        switches = []
        hosts = []
        switchDegrees = [0 for i in range(numSwitches)]
        links = []
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
        print(links)

        #For the rest of the switches, pick a random link to "remove" and add a switch to the network
        #while keeping track of the link added
        print("Adding other switches")
        for k in range(4, numSwitches):
            switchNum = k + 1
            switchName = 's',switchNum
            switches.append(self.addSwitch(switchName, cls=UserSwitch, protocols='OpenFlow10'))
            linksToAdd = set()
            for j in range(degree // 2):
                randLink = random.randint(0, len(links) - 1)
                linkToRemove = links[randLink]
                start, end = linkToRemove
                links.remove(linkToRemove)
                linksToAdd.add((start, k))
                linksToAdd.add((end, k))
            for link in linksToAdd:
                links.append(link)
                switchDegrees[k] = switchDegrees[k] + 1


        #Add all of the links previously calculated
        print(links)
        for start, end in links:
            self.addLink(switches[start], switches[end])

        #Add hosts to all switches with switchDegree less than max degree
        print("Adding hosts")
        hostNum = 0
        while len(hosts) < numHosts:
            randSwitch = random.randint(0, len(switches) - 1)
            if switchDegrees[randSwitch] < degree:
                hostNum += 1
                hostName = 'h',hostNum
                host = self.addHost(hostName, cls=Host)
                hosts.append(host)
                self.addLink(switches[randSwitch], hosts[hostNum-1])
        
        self.switchList = switches
        self.hosts = hosts
        self.links = links

    def layer_nodes(self, ):
        pass

    def port(self, src, dest):

        return (0, 1)
    
    def switches(self):
        return self.switchList

    def up_nodes(self, dpid = None):
        pass



def pingTest():
    topo = MyTopo(degree=4, numSwitches=20, numHosts=16)
    net = Mininet(topo)
    net.addController(name = 'c0', controller=RemoteController, ip='127.0.0.1', port=6633)
    net.start()
    net.pingAll
    net.iperf()
    net.stop()


topos = { 'mytopo': ( lambda: MyTopo(degree=4, numSwitches=20, numHosts=10) ) }

if __name__ == "__main__":
    pingTest()