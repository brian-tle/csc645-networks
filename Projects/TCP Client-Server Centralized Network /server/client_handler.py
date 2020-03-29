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
# import menu

from menu import Menu

saved_messages = {" ": [" "]}
global_messages = []

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
        # self.server.clients[int(self.client_id)] = self.unread_messages

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        menu = Menu(self)
        data = {'menu': menu}
        self.server.send(self.clientsocket, data)
        # print(data)
        # display = menu.show_menu()
        # display = {'display': menu.show_menu()}
        # print(display)

        # self.server.send(self.clientsocket, display)
        # self.server.send(self.clientsocket, data)

    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        data = self.server.receive(self.clientsocket)
        # print(data)
        if 'option_selected' in data.keys() and 1 <= data['option_selected'] <= 6: # validates a valid option selected
            option = data['option_selected']
            if option == 1:
                self._send_user_list()
            elif option == 2:
                recipient_id = data['recipient_id']
                message = data['message']
                self._save_message(recipient_id, message)
            elif option == 3:
                self._send_messages()
            elif option == 4:
                room_id = data['room_id']

                chat_id = data['chat_id']
                host = data['chat_user']
                self._create_chat(room_id, chat_id, host)
                # self._create_chat(room_id)
            elif option == 5:
                room_id = data['room_id']
                user_id = data['chat_user']
                self._join_chat(room_id)
            elif option == 6:
                self._disconnect_from_server()
        else:
            mes = "The option selected is invalid"
            self.server.send(self.clientsocket, mes)
            print("User option selected is invalid")


    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        users = self.server.clients
        # print(users)
        u_list = ""
        position = 0
        for i in users:
            # print(i) # name
            # print(users[i]) # id
            u_list += str(i) + ":" + str(users[i]) + ", "


        send_list = "\nUsers in server: " + u_list

        self.server.send(self.clientsocket, send_list)

        return 0

    # Does not save to global list yet
    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        menu = Menu(self.clientsocket)
        users = self.server.clients

        # menu.option2()
        # self.server.send(menu.option2())

        # data = {'option': 2, 'recipient_id': recipient_id, 'message': message

        for ids in users.values():
            if int(recipient_id) == int(ids):
                r_id = recipient_id #data['recipient_id']
                store = message #data['message']

                u_msg = {r_id: store}

                # recipienthandler = self.server.clients[int(recipient_id)]
                # recipienthandler.append(data)
                # print(recipienthandler)

                self.unread_messages.append(u_msg)

                # self.server.send(self.clientsocket, 'Message sent!')
                print("found")
            # else:
            #     # self.server.send(self.clientsocket, 'User ID not found')
            #     print("not found")

        print(self.unread_messages)
        return 0


    def _send_messages(self):
        """
        TODO: send all the unreaded messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """

        #  if self.unread_messages == []:
        #     message = "You have no new messages"
        #     self.server.send(self.clientsocket, message)
        # else:
        #     message = self.unread_messages
        #     self.server.send(self.clientsocket, message)
        #     data = self.server.receive(self.clientsocket)
        #     # print(data)
        #     if data['received'] == 1:
        #         self.unread_messages.clear()
        #         print("all messages cleared")

        if self.unread_messages == []:
            message = "There are no messages"
            print(message)
            self.server.send(self.clientsocket, message)
        else:
            message = self.unread_messages
            print(message)
            self.server.send(self.clientsocket, message)
        # if /self.unread_messages == []:
        # if str(self.client_id) in self.unread_messages[0].keys():
        #     message = self.unread_messages
        #     print(message)
        #     # self.server.send(self.clientsocket, message)
        #     # data = self.server.receive(self.clientsocket
        # else:
        #     message = "No new messages"
        #     print(message)
            # self.server.send(self.clientsocket, message)

            # print(data)
            # if data['message'] == 1:
            #     self.unread_messages.clear()
            #     print("all messages cleared")sg in self.server.secret_messages:



        # if int(self.client_id) not in users.items():
        #     print("No messages")
        # else:
        #     print(self.client_id + " exists")

        return 0

    # port == roomid
    def _create_chat(self, room_id, chat_id, host):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        init_room = ("="*20) + " Chat Room " + str(chat_id) + " " + ("="*20) + "\nType 'exit' to close the chat room." + \
        "\nChat room created by: " + str(host) + "\nWaiting for other users to join....\n"
        self.server.send(self.clientsocket, init_room)

        # self._join_chat(room_id, host)

        while True:
            try:
                # messages = self.server.receive()
                # print("in here")
                words = input("testing send back: ")
                self.server.send(self.clientsocket, words)


            except:
                print("Client disconnected!")
        return 0


    def _join_chat(self, room_id, client_name):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        # while True:

        pass


    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        # menu = Menu(self.clientsocket)
        # menu.option6()
        users = self.server.clients
        del_client = self.client_id
        del_list = []

        for name, u_id in users.items():
            if u_id == del_client:
                del_list.append(name)

        for i in del_list:
            del users[i]

        return 0


    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        try:
            self.server.send(self.clientsocket, "You are disconnecting from server")
            self.delete_client_data()
            self.clientsocket.close()
        # except Exception as e:
        #     print("Disconnection error: " + str(e))
        except:
            print("Disconnection exception")

        return 0