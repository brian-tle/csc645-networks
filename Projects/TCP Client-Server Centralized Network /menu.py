#######################################################################################
# File:             menu.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template Menu class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this Menu class, and use a version of yours instead.
# Important:        The server sends a object of this class to the client, so the client is
#                   in charge of handling the menu. This behaivor is strictly necesary since
#                   the client does not know which services the server provides until the
#                   clients creates a connection.
# Running:          This class is dependent of other classes.
# Usage :           menu = Menu() # creates object
#
########################################################################################
from datetime import datetime
class Menu(object):
    """
    This class handles all the actions related to the user menu.
    An object of this class is serialized ans sent to the client side
    then, the client sets to itself as owner of this menu to handle all
    the available options.
    Note that user interactions are only done between client and user.
    The server or client_handler are only in charge of processing the
    data sent by the client, and send responses back.
    """

    def __init__(self):
        """
        Class constractor
        :param client: the client object on client side
        """
        self.client = 0

    def set_client(self, client):
        self.client = client

    def show_menu(self):
        """
        TODO: 1. send a request to server requesting the menu.
        TODO: 2. receive and process the response from server (menu object) and set the menu object to self.menu
        TODO: 3. print the menu in client console.
        :return: VOID
        """
        print(self.get_menu())

    def process_user_data(self, s_o):
        """
        TODO: according to the option selected by the user, prepare the data that will be sent to the server.
        :param option:
        :return: VOID
        """
        data = {}
        option = self.option_selected(s_o)
        if 1 <= option <= 6:  # validates a valid option
            # TODO: implement your code here
            # (i,e  algo: if option == 1, then data = self.menu.option1, then. send request to server with the data)
            if option == 1:
                data = self.option1()
                self.client.send(data)
                data = self.client.receive()
                print(data)
            elif option == 2:
                data = self.option2()
                print(data)
                self.client.send(data)
                print(self.client.receive())
            elif option == 3:
                data = self.option3()
                self.client.send(data)
                self._handlemessage()
            elif option == 4:
                data = self.option4()
                # data['option_selected'] = 4
                # data = self.option4create_room()
                self.client.send(data)
            elif option == 5:
                print("Menu5")
                data = self.option5()
                self.client.send(data)
            elif option == 6:
                print("Client closing. May take a few tries")
                data = self.option6()
                self.client.send(data)
        return data

    def option_selected(self, s_o):
        """
        TODO: takes the option selected by the user in the menu
        :return: the option selected.
        """
        option = int(s_o)
        # TODO: your code here.

        return option

    def _handlemessage(self):
        data = self.client.receive()
        # if data['no_message'] == None:
        #     print(data)
        # el
        if data:
            for messages in data:
                print(messages)
            # data = {'received': 1}
            # print(data)
            # self.client.send(data)

    def get_menu(self):
        """
        TODO: Inplement the following menu
        ****** TCP CHAT ******
        -----------------------
        Options Available:
        1. Get user list
        2. Sent a message
        3. Get my messages
        4. Create a new channel
        5. Chat in a channel with your friends
        6. Disconnect from server
        :return: a string representing the above menu.
        """
        menu = "\n****** TCP CHAT ****** \
        \n----------------------- \
        \nOptions Available: \
        \n1. Get user list \
        \n2. Send a message\
        \n3. Get my messages\
        \n4. Create a new channel\
        \n5. Chat in a channel with your friends\
        \n6. Disconnect from server\
        "
        # TODO: implement your code here
        return menu

    def option1(self):
        """
        TODO: Prepare the user input data for option 1 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 1.
        """
        data = {}
        data['option_selected'] = 1
        # Your code here.
        return data

    def option2(self):
        """
        TODO: Prepare the user input data for option 2 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 2.
        """
        # print("Menu2")
        data = {}
        data['option_selected'] = 2
        message = input("\nEnter your message: ")
        r_id = input("Enter recipient id: ")
        timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        message = timestamp + ": " + message
        data['message'] = message
        data['to'] = r_id
        return data

    def option3(self):
        """
        TODO: Prepare the user input data for option 3 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 3.
        """
        data = {}
        data['option_selected'] = 3
        # Your code here.
        return data

    def option4(self):
        """
        TODO: Prepare the user input data for option 4 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 4.
        """
        data = {}
        data['option_selected'] = 4
        # Your code here.
        room_info = input("\nEnter new room id: ")
        chat_id = input("Enter new chat room id: ")

        # print(message)

        data['room_id'] = room_info
        data['chat_id'] = chat_id
        while True:
            typing = input("something > ")
            if typing == "bye":
                break

            data['chat_message'] = typing
            yield data

        # print(("-"*15) + " Chat Room " + str(chat_id) + " " + ("-"*15))
        # while True:
        #     typing = input("Something here")
        #     data['chat_message'] = typing
        #     return data

        #     if typing == "bye":
        #         break

        return data

    def option4create_room(self):
        data = {}
        data['option_selected'] = 4

        room_info = input("\nEnter new room id: ")
        chat_id = input("Enter new chat room id: ")
        data['room_id'] = room_info
        data['chat_id'] = chat_id

        return data

    def option5(self):
        """
        TODO: Prepare the user input data for option 5 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 5.
        """
        data = {}
        data['option_selected'] = 5
        # Your code here.
        return data

    def option6(self):
        """
        TODO: Prepare the user input data for option 6 in the menu
        :param option:
        :return: a python dictionary with all the data needed from user in option 6.
        """
        data = {}
        data['option_selected'] = 6
        # Your code here.
        # self.client.close()
        # print("Menu6")
        data['message'] = 'closing your client'
        return data
