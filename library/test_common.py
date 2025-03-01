import unittest
from common import *


class TestComp(unittest.TestCase):
    def test_no_ping(self):
        comp = Comp()
        ans = comp.iface().ping("1.2.3.4")
        self.assertEqual(ans, "No network")


class TestNetwork(unittest.TestCase):
    def test_empty(self):
        net = Network()
        ans = net.ping("", "1.2.3.4")
        self.assertEqual(ans, "Unknown host")

    def test_ping_host_exists(self):
        net = Network()
        comp1 = Comp()
        comp2 = Comp()
        comp3 = Comp()
        net.add_host(comp1, "1.2.3.4")
        net.add_host(comp2, "2.3.4.5")
        net.add_host(comp3, "3.4.5.6")
        ans = comp1.iface().ping("3.4.5.6")
        self.assertEqual(ans, "ping from 1.2.3.4 to 3.4.5.6")

        ans = comp2.iface().ping("1.2.3.4")
        self.assertEqual(ans, "ping from 2.3.4.5 to 1.2.3.4")

        ans = comp1.iface().ping("3.4.5.7")
        self.assertEqual(ans, "Unknown host")

if __name__ == '__main__':
    unittest.main()
