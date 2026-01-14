import numpy as np
import datetime
import json
from nexus_one import NexusOne

class SovereignServer:
    def __init__(self, server_id, capacity, latency_threshold):
        """
        Initialize the Sovereign Server.
        
        Args:
            server_id (int): Unique ID of the server.
            capacity (int): Maximum number of players the server can handle.
            latency_threshold (float): Maximum allowed latency in milliseconds.
        """
        self.server_id = server_id
        self.capacity = capacity
        self.latency_threshold = latency_threshold
        self.current_players = 0
        self.latency_history = []

    def add_player(self, player_id):
        """
        Add a new player to the server.
        
        Args:
            player_id (int): Unique ID of the player.
        
        Returns:
            bool: True if the player was successfully added, False otherwise.
        """
        if self.current_players < self.capacity:
            self.current_players += 1
            return True
        return False

    def remove_player(self, player_id):
        """
        Remove a player from the server.
        
        Args:
            player_id (int): Unique ID of the player.
        
        Returns:
            bool: True if the player was successfully removed, False otherwise.
        """
        if self.current_players > 0:
            self.current_players -= 1
            return True
        return False

    def update_latency(self, latency):
        """
        Update the server's latency history.
        
        Args:
            latency (float): Current latency in milliseconds.
        """
        self.latency_history.append(latency)
        if len(self.latency_history) > 100:
            self.latency_history.pop(0)

    def get_latency(self):
        """
        Get the average latency of the server over the last 100 measurements.
        
        Returns:
            float: Average latency in milliseconds.
        """
        if self.latency_history:
            return sum(self.latency_history) / len(self.latency_history)
        return 0.0

    def is_stable(self):
        """
        Check if the server is stable (i.e., average latency is below the threshold).
        
        Returns:
            bool: True if the server is stable, False otherwise.
        """
        return self.get_latency() < self.latency_threshold


class NetworkStability:
    def __init__(self):
        """
        Initialize the Network Stability component.
        """
        self.servers = {}

    def add_server(self, server_id, capacity, latency_threshold):
        """
        Add a new server to the network.
        
        Args:
            server_id (int): Unique ID of the server.
            capacity (int): Maximum number of players the server can handle.
            latency_threshold (float): Maximum allowed latency in milliseconds.
        """
        self.servers[server_id] = SovereignServer(server_id, capacity, latency_threshold)

    def remove_server(self, server_id):
        """
        Remove a server from the network.
        
        Args:
            server_id (int): Unique ID of the server.
        
        Returns:
            bool: True if the server was successfully removed, False otherwise.
        """
        if server_id in self.servers:
            del self.servers[server_id]
            return True
        return False

    def update_server_latency(self, server_id, latency):
        """
        Update the latency of a server.
        
        Args:
            server_id (int): Unique ID of the server.
            latency (float): Current latency in milliseconds.
        """
        if server_id in self.servers:
            self.servers[server_id].update_latency(latency)

    def get_server_latency(self, server_id):
        """
        Get the average latency of a server.
        
        Args:
            server_id (int): Unique ID of the server.
        
        Returns:
            float: Average latency in milliseconds.
        """
        if server_id in self.servers:
            return self.servers[server_id].get_latency()
        return 0.0

    def is_server_stable(self, server_id):
        """
        Check if a server is stable.
        
        Args:
            server_id (int): Unique ID of the server.
        
        Returns:
            bool: True if the server is stable, False otherwise.
        """
        if server_id in self.servers:
            return self.servers[server_id].is_stable()
        return False


# Integrate with the existing NEXUS-ONE codebase
nexus_one = NexusOne()
network_stability = NetworkStability()

# Add servers to the network
network_stability.add_server(1, 1000, 50.0)
network_stability.add_server(2, 500, 20.0)

# Update server latency
network_stability.update_server_latency(1, 30.0)
network_stability.update_server_latency(2, 10.0)

# Check server stability
print(network_stability.is_server_stable(1))  # Output: True
print(network_stability.is_server_stable(2))  # Output: True