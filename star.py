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
        h5 = self.addHost(name='h5', ip='145.0.1.1/16', cls=LinuxRouter)
        h6 = self.addHost(name='h6', ip='146.0.1.1/16', cls=LinuxRouter)
        h7 = self.addHost(name='h7', ip='147.0.1.1/16', cls=LinuxRouter)
        h8 = self.addHost(name='h8', ip='148.0.1.1/16', cls=LinuxRouter)
        
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

        self.addLink(h5,r1,
                    intfName1='h5-eth0',
                    intfName2='r1-eth4',
                    params1={'ip': '145.0.1.1/16'},
                    params2={'ip': '145.0.1.2/16'})

        self.addLink(h6,r1,
                    intfName1='h6-eth0',
                    intfName2='r1-eth5',
                    params1={'ip': '146.0.1.1/16'},
                    params2={'ip': '146.0.1.2/16'})

        self.addLink(h7,r1,
                    intfName1='h7-eth0',
                    intfName2='r1-eth6',
                    params1={'ip': '147.0.1.1/16'},
                    params2={'ip': '147.0.1.2/16'})

        self.addLink(h8,r1,
                    intfName1='h8-eth0',
                    intfName2='r1-eth7',
                    params1={'ip': '148.0.1.1/16'},
                    params2={'ip': '148.0.1.2/16'})

       
def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    #Adding IP Addresses to Routers
    info(net['r1'].cmd("ip addr add 142.0.1.2/16 r1-eth1"))
    info(net['r1'].cmd("ip addr add 143.0.1.2/16 r1-eth2"))
    info(net['r1'].cmd("ip addr add 144.0.1.2/16 r1-eth3"))
    info(net['r1'].cmd("ip addr add 145.0.1.2/16 r1-eth4"))
    info(net['r1'].cmd("ip addr add 146.0.1.2/16 r1-eth5"))
    info(net['r1'].cmd("ip addr add 147.0.1.2/16 r1-eth6"))
    info(net['r1'].cmd("ip addr add 148.0.1.2/16 r1-eth7"))


    net.start()
    CLI(net)
    # info('*** Routing Table on Router:\n')
    # info(net['r1'].cmd('route'))
    # info(net['r2'].cmd('route'))
    # info(net['r3'].cmd('route'))
    # info(net['r4'].cmd('route'))
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()