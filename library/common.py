"""Computer and service sketch."""


class NetworkInterface:
    """Network interface."""

    def __init__(self):
        self.net = None
        self.addr = None
        self.msg = None

    def setup(self, net, addr):
        """Set net and address to interface."""
        self.net = net
        self.addr = addr

    def ping(self, addr):
        """Send ping to address."""
        if not self.net:
            return "No network"
        return self.net.ping(self.addr, addr)
    
    def sendMessage(self, data, dst):
        msg = [data, self.addr, dst]
        return msg
        
    def readMessage(self, msg):
        if(msg[2] == self.addr):
            return f"\"{msg[0]}\" from {msg[1]}"
        else:
            return "No messages"


class Comp:
    """Computer."""

    def __init__(self):
        self.__iface = NetworkInterface()

    def iface(self):
        """Return network interface."""
        return self.__iface


class Network:
    """Network represents net."""

    def __init__(self):
        self.__hosts = {}
        self.storage = None 

    def add_host(self, comp, addr):
        """Add host to net."""
        self.__hosts[addr] = comp
        comp.iface().setup(self, addr)

    def ping(self, src, dst):
        """Ping sends ping to host."""
        if dst in self.__hosts:
            return f"ping from {src} to {dst}"

        return "Unknown host"
