#######################################################################
# File:             client.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template client class. You are free to modify this
#                   file to meet your own needs. Additionally, you are 
#                   free to drop this client class, and add yours instead. 
# Running:          Python 2: python client.py 
#                   Python 3: python3 client.py
#
########################################################################
import socket
import pickle
from builtins import object
from menu import Menu
from client_handler import ClientHandler

class Client(object):
    """
    The client class provides the following functionality:
    1. Connects to a TCP server 
    2. Send serialized data to the server by requests
    3. Retrieves and deserialize data from a TCP server
    """

    def __init__(self):
        """
        Class constractpr
        """
        # Creates the client socket
        # AF_INET refers to the address family ipv4.
        # The SOCK_STREAM means connection oriented TCP protocol.
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientid = 0
        self.ip = ''
        self.port = 0
        self.client_name = ''

    def get_client_id(self):
        return self.clientid

    def connect(self, host='127.0.0.1', port=12005):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
        Then retrieves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        self.ip = host
        self.port = port
        try:
            self.setupconn(host, port)

            while True:
                option_selection = input("\nYour option <enter a number>: ")

                if int(option_selection) == 4:
                    self.chat_room()
                else:
                    self.menu.process_user_data(option_selection)

                    self.menu.show_menu()
        except socket.error:
            self.close()
            print("Error client_connection")

    def chat_room(self):
        try:
            room_info = input("\nEnter new room id: ")
            chat_id = input("Enter new chat room id: ")

            new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            new_socket.bind((self.ip, self.port))
            new_socket.listen(10)
            client_sock, addr = new_socket.accept()
            c_handler = ClientHandler(self, client_sock, addr)

            c_handler._create_chat(new_socket, room_info, chat_id, self.client_name)
        except:
            print("No room")


        # while True:
        #     c_m = input(str(self.clientid) + "> ")

        #     if c_m == "bye":
        #         break
        #     else:
        #         print("some message")

        # print("leave")


    def setupconn(self, host, port):
        print("Server IP address: " + str(host))
        print("Server port: " + str(port))
        user_name = input("Your id key (name): ")
        self.client_name = user_name
        send_username = {'name': user_name}
        while True:
            try:
                self.clientSocket.connect((host, port))
                print("Successfully connected to server with IP: " + str(host) + " and port: " + str(port))

                self.send(send_username)
                break
            except socket.error:
                print("Error in connecting to server")
                break

        data = self.receive()
        print(data)

        self.clientid = data['clientid']
        print(self.receive())

        data = self.receive()
        print(data)
        if data['menu']:
            self.setupmenu(data['menu'])

    def setupmenu(self, menu):
        try:
            self.menu = menu
            self.menu.set_client(self)
        except Exception as e:
            print("Error in connect: " + str(e))
            self.close()
        self.menu.show_menu()


    def send(self, data):
        """
        TODO: Serializes and then sends data to server
        :param data:
        :return:
        """
        serialize_data = pickle.dumps(data)
        self.clientSocket.send(serialize_data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        TODO: Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.clientSocket.recv(MAX_BUFFER_SIZE)
        deserialized_data = pickle.loads(raw_data)
        return deserialized_data


    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        self.clientSocket.close()





if __name__ == '__main__':
    client = Client()
    client.connect()
