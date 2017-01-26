from crypto.games.game import Game
from crypto.primitives import random_string


class GameINTCTXT(Game):
    """
    This game tests the integrity of a cypher text. It is to be used to test
    to see if the decryption algorithm only decrypts authentic messages that
    have been sent by the sender. The Adversary has access to an encryption
    oracle (enc) and a decryption oracle (dec) that it uses to see if it won.
    """
    def __init__(self, encrypt, decrypt, key_len):
        """
        :param encrypt: Encryption function that takes inputs, a key k of
                        key_len length and a message.
        :param decrypt: Decryption function to match encryption function.
        :param key_len: Length of key used by encrypt and decrypt.
        """
        self._enc, self._dec, self.key_len = encrypt, decrypt, key_len
        self.key = ''
        self.cyphers = []
        self.messages = []

    def initialize(self):
        """
        Initializes key to be used in encryption. Called by simulator to
        reset game state in between runs.
        """
        self.key = random_string(self.key_len)
        self.cyphers = []
        self.messages = []
        self.win = False

    def enc(self, m):
        """
        Encryption oracle, you can only query for the same message once.

        :param m: Message to be encrypted.
        :return: Cipher text if valid, ``None`` otherwise.
        """

        if m in self.messages:
            return None

        self.messages += [m]

        c = self._enc(self.key, m)
        self.cyphers += [c]
        return c

    def dec(self, c):
        """
        Decryption oracle, you can only query for the same message once.

        :param c: Cipher text to be decrypted.
        :return: True if decrypted successfully, False otherwise.
        """

        m = self._dec(self.key, c)
        if c not in self.cyphers and m is not None:
            self.win = True
            return True
        else:
            return False

    def finalize(self):
        """
        Method called by simulator to determine if adversary won.

        :return: True if win, False otherwise.
        """
        return self.win