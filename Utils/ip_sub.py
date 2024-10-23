#https://psutil.readthedocs.io/en/latest/
import psutil
#https://docs.python.org/3/library/socket.html
import socket

def get_local_ip_and_subnet():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        net_info = psutil.net_if_addrs()
        subnet_mask = None

        for interface, addresses in net_info.items():
            for address in addresses:
                if address.family == socket.AF_INET and address.address == local_ip:
                    subnet_mask = address.netmask

        return local_ip, subnet_mask
    except Exception as e:
        print(f"Errore durante il recupero dell'IP locale: {e}")
        return None, None
