"""DNS prototype."""

class Record:
    """Single DNS record."""

    def __init__(self, name, addr):
        self.__name = name
        self.__addr = addr

    def get_name(self):
        return self.__name

    def get_addr(self):
        return self.__addr


class DnsDb:
    """DNS database."""

    def __init__(self):
        self.__records = {}
        self.__addrs = {}

    def num_records(self):
        """Return number of records."""
        return len(self.__records)

    def add_record(self, record):
        """Add record."""
        self.__check_record(record)
        self.__records[record.get_name()] = record

    def resolve(self, name):
        """Return IP address by name."""
        try:
            return self.__records[name].get_addr()
        except KeyError:
            return None

    def __check_record(self, record):
        if record.get_addr() in self.__addrs:
            raise ValueError("Duplicated address")
        self.__addrs[record.get_addr()] = True


class lookup:
    """lookup Event"""


class query:
    """query Event"""


class response:
    """response Event"""


class ReturnResponse:
    def response(self, peer, response):
        return response


class Client:
    channel = "client"

    def init(self, server, port, channel=channel):
        self.server = server
        self.port = int(port)

        self.transport = UDPClient(0, channel=self.channel).register(self)
        self.protocol = DNS(channel=self.channel).register(self)
        self.handler = ReturnResponse(channel=self.channel).register(self)

class Resolver:
    def init(self, server, port):
        self.server = server
        self.port = port

    def lookup(self, qname, qclass="IN", qtype="A"):
        channel = uuid()

        client = Client(
            self.server,
            self.port,
            channel=channel
        ).register(self)

        yield self.wait("ready", channel)

        self.fire(
            write(
                (self.server, self.port),
                DNSRecord(
                    q=DNSQuestion(
                        qname,
                        qclass=CLASS[qclass],
                        qtype=QTYPE[qtype]
                    )
                ).pack()
            )
        )

        yield (yield self.wait("response", channel))

        client.unregister()
        yield self.wait("unregistered", channel)
        del client

class ProcessQuery:
    def query(self, peer, query):
        qname = query.q.qname
        qtype = QTYPE[query.q.qtype]
        qclass = CLASS[query.q.qclass]

        response = yield self.call(lookup(qname, qclass=qclass, qtype=qtype))

        record = DNSRecord(
            DNSHeader(id=query.header.id, qr=1, aa=1, ra=1),
            q=query.q,
        )

        for rr in response.value.rr:
            record.add_answer(rr)

        yield record.pack()


class Server:
    def init(self, bind=("0.0.0.0", 53)):
        self.bind = bind

        self.transport = UDPServer(self.bind).register(self)
        self.protocol = DNS().register(self)
        self.handler = ProcessQuery().register(self)


class App:
    def init(self, bind=("0.0.0.0", 53), server="8.8.8.8", port=53,
             verbose=False):

        if verbose:
            Debugger().register(self)

        self.resolver = Resolver(server, port).register(self)
        self.server = Server(bind).register(self)

class DnsCachingResolver:
    def __init__(self, cacheTime, failCacheTime):
        self.__cache = {}
        self.__cacheTime = cacheTime
        self.__failCacheTime = failCacheTime
        self.__preferredAddrFamily = socket.AF_INET

    def setTimeouts(self, cacheTime, failCacheTime):
        self.__cacheTime = cacheTime
        self.__failCacheTime = failCacheTime

    def resolve(self, hostname):
        currTime = monotonicTime()
        cachedTime, ips = self.__cache.get(hostname, (-self.__failCacheTime-1, []))
        timePassed = currTime - cachedTime
        if (timePassed > self.__cacheTime) or (not ips and timePassed > self.__failCacheTime):
            prevIps = ips
            ips = self.__doResolve(hostname)
            if not ips:
                logging.warning("failed to resolve hostname: " + hostname)
                ips = prevIps
            self.__cache[hostname] = (currTime, ips)
        return None if not ips else random.choice(ips)

    def doResolve(self, hostname):
        try:
            addrs = socket.getaddrinfo(hostname, None)
            ips = []
            if self.__preferredAddrFamily is not None:
                ips = list(set([addr[4][0] for addr in addrs\
                                if addr[0] == self.__preferredAddrFamily]))
            if not ips:
                ips = list(set([addr[4][0] for addr in addrs]))
        except socket.gaierror:
            logging.warning('failed to resolve host %s', hostname)
            ips = []
        return ips

    _g_resolver = None

    def globalDnsResolver():
        global _g_resolver
        if _g_resolver is None:
            _g_resolver = DnsCachingResolver(cacheTime=600.0, failCacheTime=30.0)
        return _g_resolver


class Node:
    def __init__(self, id, **kwargs):
        self.__id = id
        for key in kwargs:
            setattr(self, key, kwargs[key])
            
    def __setattr__(self, name, value):
        if name == 'id':
            raise AttributeError('Node id is not mutable')
        super(Node, self).__setattr__(name, value)
