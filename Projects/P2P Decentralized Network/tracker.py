"""
Tracker adds all peers to a swarm and adds IP to a dict list
Detects broadcast transmission from another tracker

decentralized network a tracker is a server which only function is to send the
ip addresses of all the peers in the swarm
"""
#bencode decoder
import torrent_parser as tp

import socket
import math

class Tracker():
	def __init__(self, server_obj, list_of_clients):
		self.server = server_obj
		self.list_of_clients = list_of_clients
		#Just ip's
		self.peer_table = []
		

	def add_peers_to_list(self, peer_ip):
		self.peer_table.append(peer_ip)

	def broadcast_peer_list(self):
		data = self.peer_table
		clienthandlers = self.list_of_clients
		try:
			for clients in clienthandlers:
				# print(clients)
				self.server.send(clients, data)
		except Exception as e:
			print("Error in broadcasting peer_list: " + str(e))

	def decode_torrent(self, torrent_path):
		data = tp.parse_torrent_file(torrent_path)
		return data

	def get_peers_from_announce(self):
		torrent_data = self.decode_torrent("age.torrent")
		announce = torrent_data['announce'] # seeder / ip address
		announce_list = torrent_data['announce-list']
		info = torrent_data['info']

		print('announce: ' + str(announce))
		print(announce_list)
		print("Comment: " + torrent_data['comment'])
		print("Created by: " + torrent_data['created by'])
		# y = info['length'] / info['piece length']
		# print(math.ceil(y))
		print("info['piece length']: " + str(info['piece length']))
		print("info['length']: " + str(info['length']))

		for connection in announce_list:
			self.peer_table.append(connection)
		return announce_list

	def add_to_peer_table(self, peer_connections):
		#check_connections
		for connection in peer_connections:
			self.peer_table.append(connection)




# if __name__ == "__main__":
# 	tracker = Tracker()
# 	tracker.add_to_peer_table(tracker.get_peers_from_announce())
# 	print(tracker.peer_table)
