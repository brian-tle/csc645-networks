import threading

class ClientHandler(object):
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """
    def __init__(self, server_instance, clienthandler, addr):
        """
        Class constructor already implemented for you.
        :param server_instance:
        :param clienthandler:
        :param addr:
        """
        self.clientid = addr[1] # the id of the client that owns this handler
        self.server_ip = addr[0]
        self.server = server_instance
        self.clienthandler = clienthandler

        self.student_name = 'Brian Le' # TODO: your name
        self.github_username = 'brian-tle' # TODO: your username
        self.sid = 916970215 # TODO: your student id

    def print_lock(self):
        """
        TODO: create a new print lock
        :return: the lock created
        """
        # your code here.
        write_lock = threading.Lock()

        return write_lock # modify the return to return a the lock created

    def process_client_data(self):
        """
        TODO: receives the data from the client
        TODO: prepares the data to be printed in console
        TODO: create a print lock
        TODO: adquire the print lock
        TODO: prints the data in server console
        TODO: release the print lock
        :return: VOID
        """

        data = {'student_name': self.student_name, 'github_username': self.github_username, 'sid': self.sid}
        MAX_BUFFER_SIZE=4090
        lock = print_lock()
        send = pickle.dumps(data)
        self.clienthandler.send(data)

        while True:
            try:
                data = self.clienthandler.recv(MAX_BUFFER_SIZE)
                serialized_data = pickle.loads(data)

                lock.acquire()
                if not serialized_data:
                    break
                else:
                    print(serialized_data)

                lock.release()
            except Exception as e:
                print(str(e))

        #pass # remove this line after implemented.