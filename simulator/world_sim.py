
from crypto.simulator.base_sim import BaseSim


class WorldSim(BaseSim):
    """
    This simulator was written to be used with GamePRF. It simulates the game
    with an Adversary and allows you to compute an approximate advantage.
    """

    def run(self, world):
        """
        Runs the game in a specific world.

        :param world: 1 or 0, for different worlds.
        :return: 1 for success and 0 for failure.
        """
        self.game.initialize(world)
        return self.game.finalize(self.adversary(self.game.fn))

    def compute_success_ratio(self, world):
        """
        Tries game in world and computes the ratio of success / total runs.

        :param world: Which world to compute for.
        :return: successes / total_runs
        """
        results = []
        for i in xrange(0, 1000):
            results += [self.run(world)]

        successes = float(results.count(1))
        failures = float(results.count(0))

        return successes / (successes + failures)

    def compute_advantage(self):
        """
        Adv = Pr[Real => 1] - Pr[Rand => 1]

        :return: Approximate advantage computed using the above equation.
        """

        pr_real_1 = float(self.compute_success_ratio(1))
        pr_rand_1 = float(1 - self.compute_success_ratio(0))

        return pr_real_1 - pr_rand_1
