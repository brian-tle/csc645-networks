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
from tracker import Tracker

class Server(object):
    """
    The server class implements a server socket that can handle multiple client connections.
    It is really important to handle any exceptions that may occur because other clients
    are using the server too, and they may be unaware of the exceptions occurring. So, the
    server must not be stopped when a exception occurs. A proper message needs to be show in the
    server console.
    """
    MAX_NUM_CONN = 10 # keeps 10 clients in queue

    # host 0.0.0.0
    def __init__(self, host='0.0.0.0', port = 5000):
        """
        Class constructor
        :param host: by default localhost. Note that '0.0.0.0' takes LAN ip address.
        :param port: by default 12000
        """
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TODO: create the server socket
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def _bind(self):
        """
        # TODO: bind host and port to this server socket
        :return: VOID
        """
        # pass #remove this line after implemented.
        self.serversocket.bind((self.host, self.port))

    def _listen(self):
        """
        # TODO: puts the server in listening mode.
        # TODO: if succesful, print the message "Server listening at ip/port"
        :return: VOID
        """
        try:
            self._bind()
            # your code here
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server listening at " + str(self.host) + "/" + str(self.port))
        except:
            self.serversocket.close()

    def _handler(self, clienthandler):
        """
        #TODO: receive, process, send response to the client using this handler.
        :param clienthandler:
        :return:
        """
        while True:
             # TODO: receive data from client
             # TODO: if no data, break the loop
             # TODO: Otherwise, send acknowledge to client. (i.e a message saying 'server got the data
             # pass  # remove this line after implemented.
             try:
                data = self.receive(clienthandler)
                if data:
                    print("Server got the data: " + str(data))
                else:
                    break

             except Exception as e:
                print("Error receving by server: " + str(e))
                break

    def _accept_clients(self):
        """
        #TODO: Handle client connections to the server
        :return: VOID
        """
        while True:
            try:
                clienthandler, addr = self.serversocket.accept()
                # TODO: from the addr variable, extract the client id assigned to the client
                # TODO: send assigned id to the new client. hint: call the send_clientid(..) method

                _clientid = addr[1]
                # print(_clientid)
                self._send_clientid(clienthandler, _clientid)

                self._handler(clienthandler) # receive, process, send response to client.
            except Exception as e:
                # handle exceptions here
                print("Error in accepting client: " + str(e))
                break
                # pass #remove this line after implemented.

    def _send_clientid(self, clienthandler, clientid):
        """
        # TODO: send the client id to a client that just connected to the server.
        :param clienthandler:
        :param clientid:
        :return: VOID
        """
        # pass  # remove this line after implemented.
        client_id = {'clientid': clientid}

        self.send(clienthandler, client_id)


    def send(self, clienthandler, data):
        """
        # TODO: Serialize the data with pickle.
        # TODO: call the send method from the clienthandler to send data
        :param clienthandler: the clienthandler created when connection was accepted
        :param data: raw data (not serialized yet)
        :return: VOID
        """
        # pass #remove this line after implemented.
        serialized_data = pickle.dumps(data)
        clienthandler.send(serialized_data)

    def receive(self, clienthandler, MAX_ALLOC_MEM=4096):
        """
        # TODO: Deserialized the data from client
        :param MAX_ALLOC_MEM: default set to 4096
        :return: the deserialized data.
        """
        # return None #change the return value after implemente.
        r_data = clienthandler.recv(MAX_ALLOC_MEM)
        deserializer = pickle.loads(r_data)

        return deserializer

    def run(self):
        """
        Already implemented for you
        Run the server.
        :return: VOID
        """
        try:
            self._listen()
            self._accept_clients() 
        except KeyboardInterrupt:
            print("stopped")
        except:
            print("error in server running")