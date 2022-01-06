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
