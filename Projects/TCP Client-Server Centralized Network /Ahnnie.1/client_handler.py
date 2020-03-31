#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
from menu import Menu

import threading

class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        # self.server.send_client_id(self.clientsocket, self.client_id)
        self.unread_messages = []

    def startHandler(self):
        user = self.server.receive(self.clientsocket)
        username = user['name']
        self.server.send_client_id(self.clientsocket, self.client_id)
        message = "Your client info is:\nClient name: " + username + "\nClient ID:" + str(self.client_id)

        self.server.send(self.clientsocket, message)
        self.server.clients[int(self.client_id)] = self.unread_messages
        self.server.nametoid[int(self.client_id)] = username

        self._sendMenu()

        # print(self.server.nametoid)
        try:
            while True:
                # self.lock.acquire()
                self.process_options()
                # self.lock.release()
        except:
            print("Client force closed")
            self._disconnect_from_server()

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        menu = Menu()
        data = {'menu': menu}
        self.server.send(self.clientsocket, data)

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        data = self.server.receive(self.clientsocket)
        print(data)
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6: # validates a valid option selected
            option = data['option_selected']
            if option == 1:
                self._send_user_list()
            elif option == 2:
                recipient_id = data['to']
                message = data['message']
                self._save_message(recipient_id, message)
            elif option == 3:
                self._send_messages()
            elif option == 4:
                room_id = data['room_id']
                chat_id = data['chat_id']
                c_message = data['chat_message']
                self._create_chat(room_id, chat_id, c_message)
            elif option == 5:
                # room_id = data['room_id']
                # self._join_chat(room_id)
                print("Nope")
                room_id = data['room_id']
                self._join_chat(room_id)
            elif option == 6:
                # print("am here")
                self._disconnect_from_server()
        else:
            print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        users = self.server.clients
        user_name = self.server.nametoid

        u_list = ""
        for i in users:
            u_list += str(user_name[i]) + ":" + str(i) + ", "

        send_list = "\nUsers in server: " + u_list
        self.server.send(self.clientsocket, send_list)

    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        data = (message + " (from: " + self.server.nametoid[self.client_id] + ")")
        if int(recipient_id) in self.server.clients:
            print("User found")
            send_receiver = self.server.clients[int(recipient_id)]
            send_receiver.append(data)

            data = ("Message sent!")
            self.server.send(self.clientsocket, data)
        else:
            data = ("\n" + recipient_id + " could not be found")
            self.server.send(self.clientsocket, data)


    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        if self.unread_messages == []:
            # pass
            message = ["You have no new messages"]
            self.server.send(self.clientsocket, message)
            # print(message)
        else:
            message = self.unread_messages
            self.server.send(self.clientsocket, message)
            data = self.server.receive(self.clientsocket)
            print(data)
            self.unread_messages.clear()

    def _create_chat(self, c_socket, room_id, chat_id, client_name):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        print("Create chat")
        # menu_obj = Menu()
        # message = ("-"*15) + " Chat Room " + str(room_id) + ("-"*15) #+ \
            # "\nType 'exit' to close the chat room.\nChat room created by: " + str(self.server.nametoid[self.client_id]) + \
            # "\nWaiting for other users to join...")
        # print(host_welcome)
        # self.server.send(self.clientsocket, message)
        # r_id = int(room_id)
        # c_id = int(chat_id)

        # print(self.server.chat_rooms)
        # if self.server.chat_rooms.get(r_id) == None:
        #     self.server.chat_rooms[r_id] = (c_id)
        #     print(self.server.chat_rooms)
        #     # self.server.chatrooms[int(room_id)]=[]
        #     # data = ("-"*15) + " Chat Room " + str(c_id) + " " + ("-"*15)
        #     # print(data)
        #     # self.server.send(self.clientsocket,data)
        #     data = self.server.receive(self.clientsocket)
        #     print(data)

        client_sock, addr = c_socket.accept()
        print("UserId " + str(addr[1])+" connected to the channel")
        print("Enter Bye to exit the channel")
        #client_sock.connect((host, port))
        while True:
            try:
                userMeg = client_sock.recv(4096)
                userMeg_decode = pickle.loads(userMeg)
                for x, y in userMeg_decode.items():
                    print(x+": " + y)
                user_input = input(str(client_name) + ": ")
                user_input = str(user_input)
                user_name_msg[client_name] = user_input
                if "bye" in user_input:
                    print("You have disconnect server")
                    break
                user_encode = pickle.dumps(user_name_msg)
                client_sock.send(user_encode)
            except:
                print("Client Disconnected!")
                break
            # if data['chat_message'] == 'bye':
                

            # menu_obj.option4()

            # new_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # new_client_socket.bind((self.server.host, self.server.port))
            # new_client_socket.listen(10)
            # while True:
            #     try:
            #         # chat_socket, addr = new_client_socket.recv(4096)
                    


            # self._join_chat(room_id)
        else:
            print("Closing chat")
            data = 0
            self.server.send(self.clientsocket, data)
        # print("Channel Info:")
        # print("IP Address: " + host)
        # print("Channel Clientid:" + str(port))
        # print("Waiting for users....")
        # client_sock, addr = socket.accept()
        # print("UserId " + str(addr[1])+"connected to the channel")
        # print("Enter Bye to exit the channel")
        # #client_sock.connect((host, port))
        # while True:
        #     try:
        #         userMeg = client_sock.recv(4096)
        #         userMeg_decode = pickle.loads(userMeg)
        #         for x, y in userMeg_decode.items():
        #             print(x+": " + y)
        #         user_input = input(str(client_name) + ": ")
        #         user_input = str(user_input)
        #         user_name_msg[client_name] = user_input
        #         if "bye" in user_input:
        #             print("You have disconnect server")
        #             break
        #         user_encode = pickle.dumps(user_name_msg)
        #         client_sock.send(user_encode)
        #     except:
        #         print("Client Disconnected!")
        #         break


    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        print("join chat")

        room_id = int(room_id)
        if room_id in self.server.chatrooms:
            data = "You have joined chatroom " + str(room_id) + ". Type bye to exit."
            self.server.send(self.clientsocket, data)
            room = self.server.chatrooms[room_id]
            room.append(self.unread_messages)
            name = self.server.nametoid[self.client_id]
            data = name + " Joined chat"
            for mailbox in room:
                mailbox.append(data)
            self._send_messages()
            while True:
                try:
                    data = self.server.receive(self.clientsocket)
                    data= "chat screen: "+ data + "-from:" + name
                    print(data)
                    if not data or data == "bye":
                        room.remove(self.unread_messages)
                        self.server.chatrooms[room_id].remove(self.unread_messages)
                        data = name + " left"
                        for mailbox in room:
                            mailbox.append(data)
                    else:
                        for mailbox in room:
                            mailbox.append(data)
                    self._send_messages()
                    continue
                except:
                    break
        else:
            data = 0
            self.server.send(self.clientsocket, data)

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        print("delete client")

        x = self.client_id

        print(self.server.clients)

        del self.server.clients[x]
        print(self.server.clients)


    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        # print("Disconnect server")

        closing_message = "Client closing. May take a few entries"
        self.server.send(self.clientsocket, closing_message)
        self.delete_client_data()
        self.clientsocket.close()
        print("closed")













