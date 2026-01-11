import socket
import threading
from typing import Dict, List


class ClusterManager:
    def __init__(self, node_id: str, nodes: List[str]):
        self.node_id = node_id
        self.nodes = nodes  # Diğer node IP:port listesi
        self.active_nodes: Dict[str, bool] = {n: False for n in nodes}
        self.lock = threading.Lock()
        self.is_leader = False
        self.leader_id = None

    def discover_nodes(self):
        # Basit TCP ile node keşfi
        for node in self.nodes:
            try:
                ip, port = node.split(":")
                with socket.create_connection((ip, int(port)), timeout=2):
                    with self.lock:
                        self.active_nodes[node] = True
            except Exception:
                with self.lock:
                    self.active_nodes[node] = False

    def elect_leader(self):
        # Basit: En küçük node_id lider
        all_nodes = [self.node_id] + [n for n, active in self.active_nodes.items() if active]
        self.leader_id = min(all_nodes)
        self.is_leader = (self.node_id == self.leader_id)

    def distribute_load(self, task_id: str) -> str:
        # Basit round-robin
        active = [n for n, a in self.active_nodes.items() if a] + [self.node_id]
        idx = hash(task_id) % len(active)
        return active[idx]

    def handle_failover(self):
        # Lider node down ise tekrar seçim
        if self.leader_id is None or not self.active_nodes.get(self.leader_id, True):
            self.elect_leader()

    def sync_data(self, data: dict):
        # Gerçek veri senkronizasyonu için ağ üzerinden paylaşım gerekir
        pass
        pass
        pass
