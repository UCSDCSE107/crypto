from crypto.simulator.base_sim import BaseSim


class CCASim(BaseSim):
    """
    This simulator was written to be used with GameCCA. It simulates the
    game with an Adversary and allows you to compute an approximate advantage.
    """

    def run(self, b):
        """
        Runs the game in a specific world.

        :param world: 1 or 0, for different worlds.
        :return: True for success and False for failure.
        """
        self.game.initialize(b)
        return self.game.finalize(self.adversary(self.game.lr, self.game.dec))

    def compute_success_ratio(self, b):
        """
        Tries game in world and computes the ratio of success / total runs.

        :param world: Which world to compute for.
        :return: successes / total_runs
        """
        results = []
        for i in xrange(0, 1000):
            results += [self.run(b)]

        successes = results.count(True)
        failures = results.count(False)
        return successes/(successes + failures)

    def compute_advantage(self):
        """
        Adv = Pr[Right => 1] - Pr[Left => 1]

        :return: Approximate advantage computed using the above equation.
        """

        return self.compute_success_ratio(1) - (1 - self.compute_success_ratio(0))
