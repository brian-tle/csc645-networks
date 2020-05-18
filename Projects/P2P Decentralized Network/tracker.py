"""
Tracker adds all peers to a swarm and adds IP to a dict list
Detects broadcast transmission from another tracker

decentralized network a tracker is a server which only function is to send the
ip addresses of all the peers in the swarm

announce contains who has file?
"""
#bencode decoder
import torrent_parser as tp

import socket
import math

class Tracker():
	def __init__(self, server_obj):
		self.server = server_obj
		# self.list_of_clients = list_of_clients
		#Just ip's
		self.peer_table = []
		
	# def add_new_peer(self, peer_ip):
	# 	self.server._accept

	def add_peers_to_list(self, peer_ip):
		self.peer_table.append(peer_ip)

	def broadcast_peer_list(self, client):
		print("broadcasting peer list")
		data = self.peer_table
		# clienthandlers = self.list_of_clients
		try:
			# for clients in clienthandlers:
			# 	# print(clients)
			# 	self.server.send(clients, data)
			self.server.send(client,data)
		except Exception as e:
			print("Error in broadcasting peer_list: " + str(e))

	def broadcast_not_send(self):
		print("HELLO WORLDS")
		print(self.peer_table)

	def decode_torrent(self, torrent_path):
		data = tp.parse_torrent_file(torrent_path)
		return data

	def get_peers_from_announce(self):
		torrent_data = self.decode_torrent("age.torrent")
		announce = torrent_data['announce'] # seeder / ip address
		announce_list = torrent_data['announce-list']
		info = torrent_data['info']

		print('\nannounce: ' + str(announce))
		print(announce_list)
		print("Comment: " + torrent_data['comment'])
		print("Created by: " + torrent_data['created by'])
		print("info['piece length']: " + str(info['piece length']))
		print("info['length']: " + str(info['length']))
		print()

		for connection in announce_list:
			self.peer_table.append(connection)
		return announce_list

	def add_to_peer_table(self, peer_connections):
		#check_connections
		for connection in peer_connections:
			self.peer_table.append(connection)

	def get_amount_of_pieces(self):
		torrent_data = self.decode_torrent("age.torrent")
		info = torrent_data['info']
		y = info['length'] / info['piece length']
		pieces = math.ceil(y)
		# print(pieces)

		return pieces

	def get_info_unhashed(self):
		torrent_data = self.decode_torrent("age.torrent")
		info = torrent_data['info']

		return info