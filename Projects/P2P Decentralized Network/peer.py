from client import Client
from server import Server

import math

import threading as Thread
from tracker import Tracker
'''
Torrent info:
info contains content of torrent (info hash)
announce / announce-list locate peers 
'''

'''
Peer is both client / server
'''

class Peer(Client, Server):
    DEFAULT_SERVER_PORT = 5000
    MIN_PORT = 5001
    MAX_PORT = 5010

    def __init__(self, server_ip_address = '0.0.0.0'):
        #function calls
        self.server = Server()
        Server.__init__(self)
        # self.client = Client()
        self.list_of_clienthandlers = []

    def peer_client_connector(self, client_port_to_bind, peer_ip_address, peer_port=5000):
        print("\npeer_client_connector")
        client = Client()
        print(client_port_to_bind)
        print(peer_ip_address)
        try:
            # binds the client to the ip address assigned by LAN
            client.bind('0.0.0.0', client_port_to_bind)  # note: when you bind, the port bound will be the client id
            self.list_of_clienthandlers.append(client)
            Thread(target=client.connect, args=(peer_ip_address, peer_port)).start()  # threads server
            return True
        except Exception as error:
            print(error)
            client.close()
            return False

    def peer_client_to_server_connect(self, client_obj, client_ip, client_port):
        client_obj.connect(client_ip, client_port)
        

    def connect_to_all_peers(self, peer_ip_addresses):
        print("connecting to all peers")
        peer_client_port = self.MIN_PORT
        default_peer_port = self.DEFAULT_SERVER_PORT

        for peer_ip in peer_ip_addresses:
            if peer_client_port > self.MAX_PORT:
                break
            if "/" in peer_ip:
                ip_and_port = peer_ip.split("/")
                peer_ip = ip_and_port[0]
                default_peer_port = int(ip_and_port[1])
            # if self.peer_client_connector(peer_client_port, peer_ip, default_peer_port):
            if self.peer_client_connector(peer_client_port, peer_ip):
                peer_client_port += 1

    def peer_runner(self):
        try:
            Thread(target=self.run(), daemon=True).start()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    peer = Peer()
    tracker = Tracker(peer.server, peer.list_of_clienthandlers)
    # tracker.get_peers_from_announce()
    peer.peer_runner()
    peer.connect_to_all_peers(tracker.get_peers_from_announce())
    tracker.broadcast_peer_list()
