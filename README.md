# Jellyfish vs. XPander Topologies
---
This project was created for the Johns Hopkins course Cloud Computing taught by Soudeh Ghorbani. 

# Summary
---
- Getting Started
- Running Tests
- Authors
- Acknowledgements

## Getting Started
To get started, you will need to download the mininet VM image and a virtual machine.
Find the mininet VM here: https://github.com/mininet/mininet/releases/
I used VirtualBox as my virtual machine(https://www.virtualbox.org/wiki/Downloads), but you can 
also use VMWare(https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html). 

After you spin up the VM add two routers as a NAT and a host-only adapter. Then, you can ssh into 
the host-only adapter which should have an IP address
of the form 192.168.56.xxx. I used PuTTy to connect (https://www.putty.org/). You can also ssh from 
any terminal using 'ssh mininet@192.168.56.101 -p mininet'

You will also need to use pox for routing, but this is preinstalled with mininet.

To change the parameters of the topology, simply go into the topology files and 
change the parameter values in the line 'topos = { 'mytopo': ( lambda: MyTopo(degree=4, numSwitches=4, numHosts=4) ) }'

## Running Tests
To run the connectivity tests for the jellyfish and xpander topologies, simply run the python files from the mininet VM
with 'python jellyfish_topology.py' and 'python xpander_topology.py'


## Authors
Simon Allocca - Graduate CS at Johns Hopkins University

## Acknowledgements
- POX help: https://www.brianlinkletter.com/2015/04/using-the-pox-sdn-controller/
- Topology visualizer: http://mininet.spear.narmox.com/
- Mininet Python API: http://mininet.org/api/index.html
- OpenFlow and POX: https://padakuu.com/openflow-and-the-pox-controllermininet-967-article


