"""
💠 NEXUS-QUANTUM-VERIFIED - REAL-WORLD IMPLEMENTATION
📅 Upgraded: 2026-01-15 01:21
🚀 Status: ACTIVE / PRODUCTION
"""

import scapy.all as scapy
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.http import HTTPRequest
from collections import defaultdict
import pandas as pd

class NetworkPacketAnalyzer:
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file
        self.packets = scapy.rdpcap(pcap_file)

    def analyze_packets(self):
        packet_info = defaultdict(list)
        for packet in self.packets:
            if packet.haslayer(IP):
                packet_info['src_ip'].append(packet[IP].src)
                packet_info['dst_ip'].append(packet[IP].dst)
                packet_info['protocol'].append(packet[IP].proto)

                if packet.haslayer(TCP):
                    packet_info['tcp_src_port'].append(packet[TCP].sport)
                    packet_info['tcp_dst_port'].append(packet[TCP].dport)
                elif packet.haslayer(UDP):
                    packet_info['udp_src_port'].append(packet[UDP].sport)
                    packet_info['udp_dst_port'].append(packet[UDP].dport)
                elif packet.haslayer(ICMP):
                    packet_info['icmp_type'].append(packet[ICMP].type)

                if packet.haslayer(HTTPRequest):
                    packet_info['http_method'].append(packet[HTTPRequest].Method)
                    packet_info['http_host'].append(packet[HTTPRequest].Host)

        return pd.DataFrame(packet_info)

    def get_packet_stats(self):
        packet_stats = {
            'total_packets': len(self.packets),
            'tcp_packets': sum(1 for packet in self.packets if packet.haslayer(TCP)),
            'udp_packets': sum(1 for packet in self.packets if packet.haslayer(UDP)),
            'icmp_packets': sum(1 for packet in self.packets if packet.haslayer(ICMP)),
            'http_packets': sum(1 for packet in self.packets if packet.haslayer(HTTPRequest))
        }
        return packet_stats

def main():
    analyzer = NetworkPacketAnalyzer('example.pcap')
    packet_info = analyzer.analyze_packets()
    packet_stats = analyzer.get_packet_stats()
    print(packet_info)
    print(packet_stats)

if __name__ == '__main__':
    main()