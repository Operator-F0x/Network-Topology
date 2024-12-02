from scapy.all import ARP, Ether, srp
import ipaddress
from typing import List

def arp_scan(network_ip: str, subnet_mask: str) -> List[str]:    
    # Create the network object using the provided network IP and subnet mask
    network = ipaddress.IPv4Network(f"{network_ip}/{subnet_mask}", strict=False)
    broadcast_ip = str(network.broadcast_address)

    # Create an ARP request packet with the target set to the network's broadcast address
    arp_request = ARP(pdst=str(network))
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = ether_frame / arp_request

    # Inform the user that the scan is in progress
    print(f"Scanning network {broadcast_ip}...")

    # Send the ARP request and wait for responses, with a timeout of 2 seconds
    answered, _ = srp(arp_request_broadcast, timeout=2, verbose=0)

    # List to store the IP addresses of active hosts
    active_hosts = []

    # Iterate through the responses and extract the IP addresses
    for sent, received in answered:
        active_hosts.append(received.psrc)

    # Return the list of active hosts
    return active_hosts

# Example usage:
if __name__ == "__main__":
    network_ip = "192.168.1.0"  # Replace with your network IP
    subnet_mask = "24"  # Replace with your subnet mask (e.g., '24' for 255.255.255.0)
    active_hosts = arp_scan(network_ip, subnet_mask)

    if active_hosts:
        print("Active hosts found:")
        for host in active_hosts:
            print(f" - {host}")
    else:
        print("No active hosts found.")
