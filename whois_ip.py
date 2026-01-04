ipv4subnet = '94.232.116.0/24'
ipv6subnet = '2001:67c:2564::/48'
# find whois owner of these subnets:
# whois -h whois.ripe.net -- '-B -T inetnum -r
# whois -h whois.ripe.net -- '-B -T inet6num -r

# find owner of 94.232.116.0/24 with python command
import ipaddress

import ipwhois
from ipwhois import IPWhois
# use ipwhois to find owner of ipv4subnet
obj = IPWhois(ipaddress.ip_network(ipv4subnet, strict=False).network_address.exploded)
res = obj.lookup_rdap(asn_methods=["whois"])
print(f"Owner of {ipv4subnet}: {res['asn_description']}")

obj6 = IPWhois(ipaddress.ip_network(ipv6subnet, strict=False).network_address.exploded)
res6 = obj6.lookup_rdap(asn_methods=["whois"])
print(f"Owner of {ipv6subnet}: {res6['asn_description']}")

# import whois




# print(whois.whois(ipaddress.ip_network(ipv4subnet, strict=False).network_address.exploded))
# print(whois.whois(ipaddress.ip_network(ipv6subnet, strict=False).network_address.exploded))
