from scapy.all import ARP, Ether, srp
import ipaddress

def arp_scan(network_ip, subnet_mask):
    
    network = ipaddress.IPv4Network(f"{network_ip}/{subnet_mask}", strict=False)
    broadcast_ip = str(network.broadcast_address)

    arp_request = ARP(pdst=str(network))
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = ether / arp_request

    print(f"Scansione in corso su {broadcast_ip}...")
    answered, _ = srp(arp_request_broadcast, timeout=2, verbose=0)

    active_hosts = []

    for sent, received in answered:
        active_hosts.append(received.psrc) 

    return active_hosts