from client import Client
from server import Server

import math

import threading as thread
from tracker import Tracker
'''
Torrent info:
info contains content of torrent (info hash)
announce / announce-list locate peers 
'''

'''
Peer is both client / server
'''
from PWP import PWP
import hashlib #SHA1
import uuid

class Peer(Client, Server):
    DEFAULT_SERVER_PORT = 5000
    MIN_PORT = 5001
    MAX_PORT = 5010

    def __init__(self, server_ip_address = '0.0.0.0'):
        # function calls
        self.server = Server()
        Server.__init__(self)
        self.client = Client()
        Client.__init__(self)
        self.list_of_clienthandlers = []
        self.peer_id = uuid.uuid4()
        self.peer_hash = None
        self.send_hash = {}


    def peer_client_connector(self, client_port_to_bind, peer_ip_address, peer_port=DEFAULT_SERVER_PORT):
        print("\nPeer: " + str(self.peer_id) + " started running its client\n")
        client = Client()
        # tracker = Tracker(self.server)
        # print(client_port_to_bind)
        # print(peer_ip_address)
        try:
            # binds the client to the ip address assigned by LAN
            client.bind('0.0.0.0', client_port_to_bind)  # note: when you bind, the port bound will be the client id
            self.list_of_clienthandlers.append(client)

            print("List of clients: ")
            # print(self.list_of_clienthandlers)
            print("client connection: " +  str(peer_ip_address[0]) + ":" +str(client_port_to_bind))
            # print("peer port: " + str(peer_port))
            connect_args = (peer_ip_address[0], peer_port)
            thread.Thread(target=client.connect, args=(peer_ip_address[0], peer_port)).start()
            # client.send(self.peer_hash)
            # Thread(target=client.connect(), args=((peer_ip_address[0], peer_port))).start()  # threads server
            tracker.broadcast_peer_list()
            return True
        except Exception as error:
            print(error)
            client.close()
            return False

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

    def peer_runner(self, ip_addresses):
        try:
            # peer.server.run()
            # self.server.this
            # print(thread.active_count())
            # self.run()
            print("Peer: " + str(peer.peer_id) + " started running its server")
            thread.Thread(target=self.run, daemon=True).start()

            self.connect_to_all_peers(ip_addresses)
        except Exception as e:
            print("peerrunner erorr")
            print(e)

    # infite loop to listen for handshake etc / message 
    def peer_handler(self):
        pass

    def jose_run_this(self):
        tracker = Tracker(self.server)
        tracker_peer_list = tracker.get_peers_from_announce()
        self.peer_runner(tracker_peer_list)
        # self.connect_to_all_peers(tracker_peer_list)
        # tracker.broadcast_peer_list()
        # num_pieces = tracker.get_amount_of_pieces()
        # pwp = PWP(num_pieces)


if __name__ == '__main__':
    peer = Peer()
    tracker = Tracker(peer.server)
    ip_s = tracker.get_peers_from_announce()

    num_pieces = tracker.get_amount_of_pieces()
    pwp = PWP(num_pieces)

    inf_hash = tracker.get_info_unhashed()
    hash = hashlib.sha1()
    hash.update(repr(inf_hash).encode('utf-8'))
    peer.peer_hash = hash.hexdigest()

    send_handshake = pwp.handshake(peer.peer_hash, peer.peer_id)
    peer.peer_hash = send_handshake

    # peer.peer_client_send_handshake(send_handshake)
    peer.peer_runner(ip_s)