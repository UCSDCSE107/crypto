
from crypto.games.game import Game
from crypto.primitives import random_string


class GameUFCMA(Game):
    """
    This game is meant to test the security of message authentication schemes.
    Adversaries playing this game have access to a tag and verify oracle.
    """
    def __init__(self, _tag, _verify, key_len=0, key_gen=None):
        """
        :param _tag: This must be a callable python function that returns
                     message tags and takes in a key and message (key should
                     be of length key_len).
        :param _verify: This must be a callable python function that returns
                        1 when a tag is valid and 0 when it is not. Its
                        parameters should be key, message, and tag.
        :param key_len: This is the length of the key used by the MAC in bytes.
        """
        super(GameUFCMA, self).__init__()
        self._tag, self._verify, self.key_len = _tag, _verify, key_len
        self.key = ''
        self.messages = []
        self.key_gen = key_gen

    def initialize(self):
        """
        Initializes the game and resets the state. Called every time you would
        like to play the game again, usually by the simulator class. Resets
        key and internal storage.
        """
        if self.key_gen == None:
            self.key = random_string(self.key_len)
        else:
            self.key = self.key_gen()
        self.messages = []
        self.win = False

    def tag(self, message):
        """
        This is the tag oracle that the adversary has access to.

        :param message: Message to be tagged.
        :return: Tag of ``message``.
        """
        t = self._tag(self.key, message)
        self.messages += [message]
        return t


    def finalize(self, (message, tag)):
        """
        This method is usually called automatically by the simulator class
        to determine whether or not the adversary won the game.

        :return: True if successful, False otherwise.
        """
        if message is None or tag is None:
            return False

        d = self._verify(self.key, message,tag)
        if message not in self.messages and d:
            self.win = True
        return self.win
