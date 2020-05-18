########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Server Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Brian Le
# Student ID: 916970215
# Student Github Username: brian-tle
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Program Running instructions:
#               python server.py  # compatible with python version 2
#               python3 server.py # compatible with python version 3
#
########################################################################################################################

# don't modify this imports.
import socket
import pickle
from threading import Thread

from client_handler import ClientHandler

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    def __init__(self, host="0.0.0.0", port = None):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        #self.serversocket = None # TODO: create the server socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        print("="*10 + " _listen " + "="*10)
        try:
            self._bind()
            # your code here
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server is listening at ip: " + str(self.host) + ", port: " + str(self.port))
        except Exception as e:
            print("Error _listen: " + str(e))
            self.serversocket.close()

    def _handler(self, clienthandler):
        """
        #TODO: receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
         # TODO: receive data from client
         # TODO: if no data, break the loop
         # TODO: Otherwise, send acknowledge to client. (i.e a message saying 'server got the data

        print("="*10 + " _handler " + "="*10)
        while True:
            try:
                data = self.receive(clienthandler)
                print(data)

                message = "Server got message"
                self.send(clienthandler, message)

            except socket.error as e:
                print('No data available')
                break
            

    def thread_client(self, clienthandler, addr):
        # init the client handler object
        ClientHandler(clienthandler, addr).init()
   

    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
               print("="*10 + " _accept_clients " + "="*10)
               clienthandler, addr = self.serversocket.accept()
               # TODO: from the addr variable, extract the client id assigned to the client
               # TODO: send assigned id to the new client. hint: call the send_clientid(..) method
               # Thread(target=self.thread_client, args=(clienthandler, addr)).start()
               server_ip = addr[0]
               client_id = addr[1]

               print("\tserver_ip: " + str(server_ip))
               print("\tclient_id: " + str(client_id))

               self._send_clientid(clienthandler, client_id)
               message = "Server got message"
               self.send(clienthandler, message)

               self._handler(clienthandler) # receive, process, send response to client.
               clienthandler.close()
            except Exception as e:
                print("Error _accept_clients: " + str(e))
                break
            # handle exceptions here

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        data = {'clientid': clientid}
        send_data = pickle.dumps(data)
        clienthandler.send(send_data)

    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        message = data
        serialize_data = pickle.dumps(message)
        clienthandler.send(serialize_data)

    def receive(self, clienthandler, MAX_ALLOC_MEM=4096):
        """
        # TODO: Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        receiving_data = clienthandler.recv(MAX_ALLOC_MEM)
        deserialized_data = pickle.loads(receiving_data)

        return deserialized_data #change the return value after implemente.

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """

        try:
            self._listen()
            self._accept_clients()
        except:
            print("\n" + "="*10 + " Forced close " + "="*10)

# main execution
if __name__ == '__main__':
    server = Server()
    server.run()











