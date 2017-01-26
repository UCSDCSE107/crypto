from crypto.primitives import random_string
from crypto.games import game


class GameCR(game.Game):
    """
    This game is used to test the collision resistance of hash functions.
    Adversaries playing this game do not have access to any oracles however
    they do have access to the key used by the hash function.
    """

    def __init__(self, hash_f, key_len):
        """
        :param hash_f: This is the hash function that the adversary is
                       playing against. It must take two parameters, a key
                       of length key_len and a message.
        :param key_len: Length of key used by hash function.
        """
        super(self.__class__, self).__init__()
        self.hash = hash_f
        self.key_len = key_len
        self.key = ''

    def initialize(self):
        """
        Generates a new key to be used by the hash function. Called by simulator
        class.

        :return: key to be used by hash function.
        """
        self.key = random_string(self.key_len)
        return self.key

    def finalize(self, (x1, x2)):
        """
        This method is called by the simulator class to determine whether or not
        the adversary produced the correct output.

        :param x1: Suspect collision member 1.
        :param x2: Suspect collision member 2.
        :return: True if collision, false otherwise.
        """
        if x1 == x2:
            return False
        return self.hash(self. key, x1) == self.hash(self.key, x2)
