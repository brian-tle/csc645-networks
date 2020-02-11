########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: TCP Client Socket
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Brian Le
# Student ID: 916970215 
# Student Github Username: brian-tle
# Instructions: Read each problem carefully, and implement them correctly. Your grade in labs is based on passing
#               all the unit tests provided.
#               No partial credit will be given. Labs must be completed in class, and must be commited to your
#               personal repository by 9:45 pm on iLearn.
########################################################################################################################

# don't modify this imports.
import socket
import pickle


######################################## Client Socket ###############################################################3
"""
Client class that provides functionality to create a client socket is provided. Implement all the TODO parts 
"""

class Client(object):

    def __init__(self):
        """
        Class constructor
        """
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_id = None
        self.student_name = 'Brian Le' # TODO: your name
        self.github_username = 'brian-tle' # TODO: your username
        self.sid = 916970215 # TODO: your student id

    def connect(self, server_ip_address, server_port):
        """
        TODO: Create a connection from client to server
        :param server_ip_address:
        :param server_port:
        :return:
        """
        #TODO: 1. use the client socket implement a connection from this client to the server using the server ip and port
        #TODO: 2. once the client creates a succesful connection the server will send the client id to this client.
        #      call the method set_client_id() to implement that functionality.
        try:
            self.client.connect((server_ip_address, server_port))
            self.set_client_id()
        except Exception as e:
            print("Connection Error: " + str(e))

        # data dictionary already created for you. Don't modify.
        data = {'student_name': self.student_name, 'github_username': self.github_username, 'sid': self.sid}

        #TODO  3. send the above data to the server. using the send method which has been already implemented for you.

        while True: # client is put in listening mode to retrieve data from server.
            self.send(data)
            data = self.receive()
            if not data:
                break
            # do something with the data
        self.close()

    def send(self, data):
        """
        Serializes and then sends data to server
        :param data:
        :return:
        """
        data = pickle.dumps(data) # serialized data
        self.client.send(data)

    def receive(self, MAX_BUFFER_SIZE=4090):
        """
        Desearializes the data received by the server
        :param MAX_BUFFER_SIZE: Max allowed allocated memory for this data
        :return: the deserialized data.
        """
        raw_data = self.client.recv(MAX_BUFFER_SIZE) # deserializes the data from server
        return pickle.loads(raw_data)

    def set_client_id(self):
        """
        Sets the client id assigned by the server to this client after a succesfull connection
        :return:
        """
        data = self.receive() # deserialized data
        client_id = data['clientid'] # extracts client id from data
        self.client_id = client_id # sets the client id to this client
        print("Client id " + str(self.client_id) + " assigned by server")

    def close(self):
        """
        TODO: close this client
        :return: VOID
        """
        try:
            self.client.close()
        except Exception as e:
            print("Closing Error: " + str(e))

# main execution
if __name__ == '__main__':
    server_ip_address = "10.143.97.180"  # TODO: change this to the server ip address provided by instructor in class
    server_port = 5001
    client = Client()
    client.connect(server_ip_address, server_port)

# If your data was successfully sent to the server run by the instructor in class, you'll get full credit for this lab.


