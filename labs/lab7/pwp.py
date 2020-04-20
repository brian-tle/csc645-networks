"""
Lab 7: Peer Wire Protocol (PWP)
Create a class with the basic implementation for the bitTorrent peer wire protocol
A basic template structure is provided, but you may need to implement more methods
For example, the payload method depending of the option selected
"""

class PWP(object):
    # pstr and pstrlen constants used by the handshake process
    PSTR = "BitTorrent protocol"
    PSTRLEN = 19
    # TODO: Define ID constants for all the message fields such as unchoked, interested....

    def __init__(self):
        """
        Empty constructor
        """
        self.keep_alive = {'len': b'0000'}
        self.choke = {'len': b'0001', 'id': 0}
        
        self.unchoke = {'len': b'0001', 'id': 1}

        self.interested = {'len': b'0001', 'id': 2}

        self.not_interested = {'len': b'0001', 'id': 3}

        self.have = {'len': b'0005', 'id': 4, 'piece_index': None}

        self._bitfield = {'len': b'0013' + self.X_BITFIELD_LENGTH, 'id': 5, 'bitfield': []}

        self.request = {'len': b'0013', 'id': 6, 'index': None, 'begin': None, 'length': None}

        self.piece = {'len': b'0009' + self.X_PIECE_LENGTH, 'id': 7, 'index': None, 'begin': None, 'block': None}

        self.cancel = {'len': b'0013', 'id': 8, 'index': None, 'begin': None, 'length': None}

    def handshake(self, info_hash, peer_id, pstrlen=PSTRLEN, pstr=PSTR):
        """
        TODO: implement the handshake
        :param options:
        :return: the handshake message
        """
        handshake = {'ptrstrlen': pstrlen, 'pstr': pstr, 'reserved': [], 'info_hash': info_hash, 'peer_id': peer_id}

    def message(self, len, message_id, payload):
        """
        TODO: implement the message
        :param len:
        :param message_id:
        :param payload:
        :return: the message
        """
        msg = Message()



