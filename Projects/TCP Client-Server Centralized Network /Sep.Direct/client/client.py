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

# import server

from datetime import datetime



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
        self.newClientSocket = None
        
    def get_client_id(self):
        return self.clientid

    
    def connect(self, host="127.0.0.1", port=12012):
        """
        TODO: Connects to a server. Implements exception handler if connection is resetted. 
	    Then reteves the cliend id assigned from server, and sets
        :param host: 
        :param port: 
        :return: VOID
        """
        print("Server IP address: " + host)
        print("Server port: " + str(port))
        user_name = str(input("Your id key (name): "))

        try:
            self.clientSocket.connect((host, port))

            self.send(user_name)

            data = self.receive()
            if not data:
                pass
            else:
                new_client_id = data['clientid']
                data['username'] = user_name
                self.clientid = new_client_id

            print("Successfully connected to server with IP: " + str(host) + " and port: " + str(port))
            print("Your client info is:\
                \nClient name: " + user_name + \
                "\nClient ID: " + str(self.clientid))


            while True:
                menu_options = self.receive()
                print(menu_options)

                key = int(input("\nYour option <enter a number>: "))
                send_key = {'option_selected': key}

                if key >= 1 or key <= 6:
                    if key == 1:
                        # Get user list
                        self.send(send_key)
                    elif key == 2:
                        # Send message to a user
                        s_note = input("Enter your message: ")
                        s_receiver = input("Enter recipent id: ")
                        date_now = datetime.now()
                        s_date = date_now.strftime("%m-%d-%Y %H:%M:%S")

                        s_msg = (str(s_date) + ": " + str(s_note) + " (from: " + user_name + ")")

                        message = {'recipient_id': s_receiver, 'message': s_msg}
                        send_key.update(message)

                        self.send(send_key)
                    elif key == 3:
                        # Get messages
                        self.send(send_key)
                    elif key == 4:
                        # Create a chat room
                        # Port
                        room_id = input("Enter a new room id: ")
                        chat_id = input("Enter a chat room id: ")

                        room_info = {'room_id': room_id, 'chat_id': chat_id, 'chat_user': user_name}
                        send_key.update(room_info)

                        self.send(send_key)
                    elif key == 5:
                        # Join a chat room
                        room_id = input("Enter chat room id to join: ")

                        join_info = {'room_id': room_id, 'chat_user': user_name}
                        send_key.update(join_info)

                        self.send(send_key)
                    elif key == 6:
                        # Disconnect from server
                        self.send(send_key)
                else:
                    print("\nInvalid option!")
                    pass

        except Exception as e:
            self.close()
            print("Error in connect: " + str(e))
		
	
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
        received_data = pickle.loads(raw_data)

        return received_data
        

    def close(self):
        """
        TODO: close the client socket
        :return: VOID
        """
        self.clientSocket.close()


if __name__ == '__main__':
    client = Client()
    client.connect()
