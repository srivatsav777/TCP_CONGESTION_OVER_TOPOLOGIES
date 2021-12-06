from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):

    '''For each node of class LinuxRouter, config is called.
    Here, config directs the control to flow within the node directory to configure BIRD on that node.'''
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')
        self.cmd('cd %s' % self.name)
        self.cmd('sudo bird -l')
        self.cmd('cd ..')


    '''When the program is terminated, terminate is called on each node.
    Here, terminate again directs the control to flow within node directory but this time, to bring the BIRD instance down.'''
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        self.cmd('cd %s' % self.name)
        self.cmd('sudo birdc -l down')
        self.cmd('cd ..')
        super(LinuxRouter, self).terminate()        


class NetworkTopo(Topo):
    def build(self, **_opts):
        r1 = self.addHost('r1', cls=LinuxRouter, ip='141.0.1.2/16')
        
        h1 = self.addHost(name='h1', ip='141.0.1.1/16', cls=LinuxRouter)
        h2 = self.addHost(name='h2', ip='142.0.1.1/16', cls=LinuxRouter)
        h3 = self.addHost(name='h3', ip='143.0.1.1/16', cls=LinuxRouter)
        h4 = self.addHost(name='h4', ip='144.0.1.1/16', cls=LinuxRouter)
        h5 = self.addHost(name='h5', ip='147.0.1.1/16', cls=LinuxRouter)
        h6 = self.addHost(name='h6', ip='148.0.1.1/16', cls=LinuxRouter)
        h7 = self.addHost(name='h7', ip='149.0.1.1/16', cls=LinuxRouter)
        h8 = self.addHost(name='h8', ip='150.0.1.1/16', cls=LinuxRouter)
        
        self.addLink(h1,r1) #r1-eth0 is booked.

        self.addLink(h2,r1,
                    intfName1='h2-eth0',
                    intfName2='r1-eth1',
                    params1={'ip': '142.0.1.1/16'},
                    params2={'ip': '142.0.1.2/16'})

        self.addLink(h3,r1,
                    intfName1='h3-eth0',
                    intfName2='r1-eth2',
                    params1={'ip': '143.0.1.1/16'},
                    params2={'ip': '143.0.1.2/16'})

        self.addLink(h4,r1,
                    intfName1='h4-eth0',
                    intfName2='r1-eth3',
                    params1={'ip': '144.0.1.1/16'},
                    params2={'ip': '144.0.1.2/16'})

        r2 = self.addHost('r2', cls=LinuxRouter, ip='145.0.1.3/16') #new router r2
        #connecting r1 with r2
        self.addLink(r1,r2,
                    intfName1='r1-eth4',
                    intfName2='r2-eth0',
                    params1={'ip': '145.0.1.2/16'},
                    params2={'ip': '145.0.1.3/16'})
        
        self.addLink(h5,r2,
                    intfName1='h5-eth0',
                    intfName2='r2-eth1',
                    params1={'ip': '147.0.1.1/16'},
                    params2={'ip': '147.0.1.2/16'})

        self.addLink(h6,r2,
                    intfName1='h6-eth0',
                    intfName2='r2-eth2',
                    params1={'ip': '148.0.1.1/16'},
                    params2={'ip': '148.0.1.2/16'})

        self.addLink(h7,r2,
                    intfName1='h7-eth0',
                    intfName2='r2-eth3',
                    params1={'ip': '149.0.1.1/16'},
                    params2={'ip': '149.0.1.2/16'})

        self.addLink(h8,r2,
                    intfName1='h8-eth0',
                    intfName2='r2-eth4',
                    params1={'ip': '150.0.1.1/16'},
                    params2={'ip': '150.0.1.2/16'})

        
def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    #Adding IP Addresses to Routers
    #info(net['r1'].cmd("ip addr add 142.0.1.2/16 r1-eth1"))
    #info(net['r1'].cmd("ip addr add 143.0.1.2/16 r1-eth2"))
    #info(net['r1'].cmd("ip addr add 144.0.1.2/16 r1-eth3"))
    #info(net['r1'].cmd("ip addr add 145.0.1.2/16 r1-eth4"))

    #info(net['r2'].cmd("ip addr add 147.0.1.2/16 r2-eth1"))
    #info(net['r2'].cmd("ip addr add 148.0.1.2/16 r2-eth2"))
    #info(net['r2'].cmd("ip addr add 149.0.1.2/16 r2-eth3"))
    #info(net['r2'].cmd("ip addr add 150.0.1.2/16 r2-eth4"))

    # Router 1
    #info(net["r1"].cmd("sudo tc qdisc del dev r1-eth0 root"))  
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth0 root handle 1: htb default 3"))  
    info(net["r1"].cmd("sudo tc class add dev r1-eth0 parent 1: classid 1:3 htb rate 1Mbit"))
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth0 parent 1:3 handle 3: bfifo limit 100KB"))

    #info(net["r1"].cmd("sudo tc qdisc del dev r1-eth1 root"))  
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth1 root handle 1: htb default 3"))  
    info(net["r1"].cmd("sudo tc class add dev r1-eth1 parent 1: classid 1:3 htb rate 5Mbit"))
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth1 parent 1:3 handle 3: bfifo limit 100KB"))

    #info(net["r1"].cmd("sudo tc qdisc del dev r1-eth2 root"))  
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth2 root handle 1: htb default 3"))  
    info(net["r1"].cmd("sudo tc class add dev r1-eth2 parent 1: classid 1:3 htb rate 25Mbit"))
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth2 parent 1:3 handle 3: bfifo limit 100KB"))

    #info(net["r1"].cmd("sudo tc qdisc del dev r1-eth2 root"))  
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth3 root handle 1: htb default 3"))  
    info(net["r1"].cmd("sudo tc class add dev r1-eth3 parent 1: classid 1:3 htb rate 125Mbit"))
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth3 parent 1:3 handle 3: bfifo limit 100KB"))

    #info(net["r1"].cmd("sudo tc qdisc del dev r1-eth2 root"))  
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth4 root handle 1: htb default 3"))  
    info(net["r1"].cmd("sudo tc class add dev r1-eth4 parent 1: classid 1:3 htb rate 50Mbit"))
    info(net["r1"].cmd("sudo tc qdisc add dev r1-eth4 parent 1:3 handle 3: bfifo limit 100KB"))


    #info(net["r1"].cmd("tc qdisc add dev r1-eth0 root handle 1: tbf rate 1mbit burst 125000   limit "+bs))
    #info(net["r1"].cmd("tc qdisc add dev r1-eth0 parent 1: handle 10: netem delay 30ms"))

    #info(net["r1"].cmd("tc qdisc add dev r1-eth1 root handle 1: tbf rate 1mbit burst 125000  limit "+bs))
    #info(net["r1"].cmd("tc qdisc add dev r1-eth1 parent 1: handle 10: netem delay 30ms"))

    #info(net["r1"].cmd("tc qdisc add dev r1-eth2 root handle 1: tbf rate 1mbit burst 125000  limit "+bs))
    #info(net["r1"].cmd("tc qdisc add dev r1-eth2 parent 1: handle 10: netem delay 30ms"))

    # Router 2

    #info(net["r2"].cmd("sudo tc qdisc del dev r2-eth0 root"))  
    info(net["r2"].cmd("sudo tc qdisc add dev r2-eth0 root handle 1: htb default 3"))  
    info(net["r2"].cmd("sudo tc class add dev r2-eth0 parent 1: classid 1:3 htb rate 5Mbit"))
    info(net["r2"].cmd("sudo tc qdisc add dev r2-eth0 parent 1:3 handle 3: bfifo limit  100KB"))

    #info(net["r2"].cmd("sudo tc qdisc del dev r2-eth1 root"))  
    info(net["r2"].cmd("sudo tc qdisc add dev r2-eth1 root handle 1: htb default 3"))  
    info(net["r2"].cmd("sudo tc class add dev r2-eth1 parent 1: classid 1:3 htb rate 5Mbit"))
    info(net["r2"].cmd("sudo tc qdisc add dev r2-eth1 parent 1:3 handle 3: bfifo limit 100KB"))

    #info(net["r2"].cmd("tc qdisc add dev r2-eth0 root handle 1: tbf rate 1mbit burst 125000  limit "+bs))
    #info(net["r2"].cmd("tc qdisc add dev r2-eth0 parent 1: handle 10: netem delay 30ms"))

    #info(net["r2"].cmd("tc qdisc add dev r2-eth1 root handle 1: tbf rate 1mbit burst 125000  limit "+bs))
    #info(net["r2"].cmd("tc qdisc add dev r2-eth1 parent 1: handle 10: netem delay 30ms"))


    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
