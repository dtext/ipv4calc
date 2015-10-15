__author__ = 'dt'

from ipv4calc import Ipv4Address

a = Ipv4Address("10.0.35.254", Ipv4Address.slash_to_string(12))
print(a)
print("Netz:       " + a.netstr())
print("Broadcast:  " + a.broadcaststr())
print("Hostanzahl: " + str(a.hostcount()))