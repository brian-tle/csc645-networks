"""
Lab 9: Routing and Handing
Implement the routing and handling functions
"""
from server import Server # assumes server.py is in the root directory.

class Peer (Server):

    SERVER_PORT = 5000
    CLIENT_MIN_PORT_RANGE = 5001
    CLIENT_MAX_PORT_RANGE = 5010
    ROUTING_TABLE = []

    def __init__(self, server_ip_address):
        Server.__init__(server_ip_address, self.SERVER_PORT)
        self.routing_table = []


    def run_server(self):
        """
        Already implemented. puts this peer to listen for connections requests from other peers
        :return: VOID
        """
        self.run()


    def _connect_to_peer(self, client_port_to_bind, peer_ip_address):
        """
        TODO: Create a new client object and bind the port given as a
              parameter to that specific client. Then use this client
              to connect to the peer (server) listening in the ip
              address provided as a parameter
        :param client_port_to_bind: the port to bind to a specific client
        :param peer_ip_address: the peer ip address that the client needs to connect to
        :return: VOID
        """
        client = Client()
        try:
            # binds the client to the ip address assigned by LAN
            client.bind('0.0.0.0', client_port_to_bind)  # note: when you bind, the port bound will be the client id
           
            Thread(target=client.connect_to_server, args=(peer_ip_address, peer_port)).start()  # threads server
            return True
        except Exception as error:
            print(error)  # client failed to bind or connect to server
            """
              Note that the following line does not unbind the port. Sometimes, once the socket is closed 
              The port will be still bound until WAIT_TIME gets completed. If you get the error: 
              "[Errno 48] Address already in use" 
              Then, go to your terminal and do the following to unbind the port:
                  lsof -i tcp:<client_port>
              Then copy the "pid" of the process, and execute the following
                  kill -i <pid>
              There are also other ways to unbind the port in code. Try the following line in the server file right 
              after you create the server socket
                  serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
              The above line only works sometimes depending on the system and how busy is your CPU.
            """
            client.close()
            return False

    def connect(self, peers_ip_addresses):
        """
        TODO: Initialize a temporal variable to the min client port range, then
              For each peer ip address, call the method _connect_to_peer()
              method, and then increment the client´s port range that
              needs to be bind to the next client. Break the loop when the
              port value is greater than the max client port range.

        :param peers: list of peer´s ip addresses in the network
        :return: VOID
        """
        # FROM LAB 8 SOLUTIONS
        client_port = self.CLIENT_MIN_PORT_RANGE
        default_peer_port = self.SERVER_PORT
        for peer_ip in peers_ip_addresses:
            if client_port > self.CLIENT_MAX_PORT_RANGE:
                break
            if "/" in peer_ip:  # checks if the ip address includes ports
                # This part is good if your P2P supports sharing different files
                # Then the same peer can run different servers in the same machine
                ip_and_port = peer_ip.split("/")
                peer_ip = ip_and_port[0]  # the ip address of the peer
                default_peer_port = int(ip_and_port[1])  # the port of the peer
            if self._connect_to_peer(client_port, peer_ip, default_peer_port):
                # the client connected. incrementing the client port here prevents
                # wasting ports in the range of ports assigned if the client connection fails.
                client_port += 1

    def handling_clients(self, client):
        """
        TODO: handle main services that a specific client provides such as threading the client....
        :param client:
        :return:
        """
        pass # your code here

    def routing(self, piece, file_id, swarm_id, client = None):
        """
        TODO: route a piece that was received by this peer, then add that piece to the routing table
        :param piece:
        :param file_id:
        :param swarm_id:
        :return:
        """
        # pass # your code here
        # ASSUME BIT BLOCk
        # block_data = 
        if client:
            block_data = client.recv()
            block = block_data['block']
            block_id = block['block_id']
            client_id = client.getClientID()
            self.table.append({"piece": piece, "file_id": file_id, "swarm_id": swarm_id, "block": block, "block_id":block_id, "client_id": client_id})
