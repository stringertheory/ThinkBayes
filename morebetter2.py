import random

import morebetter

def main(pingpong_mike, pingpong_dean, pool_dean, pool_mike):

    # trick: pseudocount of 1 is a uniform beta prior
    pseudocount = 1.0

    total = 0
    n_tries = 100000
    for i in range(n_tries):
        pingpong_bias = random.betavariate(pingpong_mike + pseudocount,
                                           pingpong_dean + pseudocount)
        pool_bias = random.betavariate(pool_dean + pseudocount,
                                       pool_mike + pseudocount)
        if pingpong_bias > pool_bias:
            total += 1

    p = float(total) / n_tries
    print 'Probability that Mike is more better: %.2f' % p

if __name__ == '__main__':    
    main(*morebetter.parseargs())
