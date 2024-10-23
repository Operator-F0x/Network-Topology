#https://networkx.org/documentation/stable/reference/introduction.html
import networkx as nx
#https://matplotlib.org/stable/users/index
import matplotlib.pyplot as plt
#https://scapy.readthedocs.io/en/latest/
from scapy.all import ARP, Ether, srp

from Utils.arp import arp_scan
from Utils.ip_sub import get_local_ip_and_subnet
from Utils.router_ip import get_router_ip

def create_network_topology(local_ip, subnet_mask):
    try:
        # Trova l'indirizzo IP del router
        router_ip = get_router_ip(local_ip, subnet_mask)
        if router_ip is None:
            print("Impossibile determinare l'indirizzo IP del router.")
            return

        print(f"Router IP trovato: {router_ip}")

        active_hosts = arp_scan(local_ip, subnet_mask)

        if not active_hosts:
            print("Nessun host attivo trovato nella rete.")
            return
        else:
            print(f"{len(active_hosts)} host attivi trovati.")

        G = nx.Graph()

        G.add_node(router_ip, pos=(0.5, 1), color='red')

        for i, host in enumerate(active_hosts):
            G.add_node(str(host), pos=(i / (len(active_hosts) + 1), 0), color='lightblue')
            G.add_edge(router_ip, str(host))  

        print(f"Host attivi: {active_hosts}")

        pos = nx.get_node_attributes(G, 'pos') 
        colors = nx.get_node_attributes(G, 'color')  
        node_colors = [colors[node] for node in G.nodes()]

        pos = nx.spring_layout(G)

        nx.draw(G, pos, with_labels=True, node_size=3000, node_color=node_colors, font_size=10, font_weight='bold')

        plt.title(f"Topologia di rete per {local_ip}/{subnet_mask}")
        plt.show()
    except Exception as e:
        print(f"Errore nella creazione della topologia: {e}")

    
if __name__ == "__main__":

    locip, submask = get_local_ip_and_subnet()

    print(f"IP locale ottenuto: {locip}, Subnet Mask: {submask}")

    create_network_topology(locip, submask)
