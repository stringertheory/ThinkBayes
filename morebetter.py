"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

"""This file contains a partial solution to a problem from
MacKay, "Information Theory, Inference, and Learning Algorithms."

    Exercise 3.15 (page 50): A statistical statement appeared in
    "The Guardian" on Friday January 4, 2002:

        When spun on edge 250 times, a Belgian one-euro coin came
        up heads 140 times and tails 110.  'It looks very suspicious
        to me,' said Barry Blight, a statistics lecturer at the London
        School of Economics.  'If the coin were unbiased, the chance of
        getting a result as extreme as that would be less than 7%.'

MacKay asks, "But do these data give evidence that the coin is biased
rather than fair?"

"""
# standard library
import sys

# 3rd party
import numpy as np

# local
import thinkbayes
import thinkplot

# how discrete is the set of hypotheses
N_BINS = 10001

class PingPong(thinkbayes.Suite):
    """Represents hypotheses about the probability of Mike beating Dean at
    ping pong.
    """

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: float value of x, the probability of mike beating dean
        data: string 'M' or 'D'
        """
        x = hypo
        if data == 'M':
            return x
        else:
            return 1-x

class Pool(thinkbayes.Suite):
    """Represents hypotheses about the probability of Dean beating Mike at
    pool.
    """

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: float value of x, the probability of dean beating mike
        data: string 'H' or 'T'
        """
        x = hypo
        if data == 'D':
            return x
        else:
            return 1-x

def main(mike_ping_pong_wins, mike_ping_pong_losses,
            dean_pool_wins, dean_pool_losses):

    ping_pong = PingPong(np.linspace(0, 1, N_BINS))
    ping_pong_data = 'M' * mike_ping_pong_wins + 'D' * mike_ping_pong_losses
    ping_pong.UpdateSet(ping_pong_data)
    ping_pong_cdf = ping_pong.MakeCdf(name='ping_pong')
    print 'MAP estimate of Mike beating Dean in ping pong: %.2f' % \
        ping_pong.Mean()

    pool = Pool(np.linspace(0, 1, N_BINS))
    pool_wins, pool_losses = 3, 1
    pool_data = 'D' * dean_pool_wins + 'M' * dean_pool_losses
    pool.UpdateSet(pool_data)
    pool_cdf = pool.MakeCdf(name='pool')
    print 'MAP estimate of Dean beating Mike in pool: %.2f' % pool.Mean()

    mike_is_more_better = 0
    n_tries = 100000
    mike_values = ping_pong_cdf.Sample(n_tries)
    dean_values = pool_cdf.Sample(n_tries)
    for mike_value, dean_value in zip(mike_values, dean_values):

        # if mike_value == dean_value, give the tie to dean --- he
        # needs it.
        if mike_value > dean_value:
            mike_is_more_better += 1

    p_mike_is_more_better = mike_is_more_better / float(n_tries)
    print 'Probability that Mike is more better: %.2f' % p_mike_is_more_better

    thinkplot.Pmf(ping_pong, label='Mike beating Dean at Ping Pong')
    thinkplot.Pmf(pool, label='Dean beating Mike at Pool')
    thinkplot.Show()
    
def parseargs():
    pingpong_record = sys.argv[1]
    pool_record = sys.argv[2]

    pingpong_mike, pingpong_dean = [int(i) for i in pingpong_record.split('-')]
    pool_dean, pool_mike = [int(i) for i in pool_record.split('-')]

    return pingpong_mike, pingpong_dean, pool_dean, pool_mike

if __name__ == '__main__':
    main(*parseargs())
