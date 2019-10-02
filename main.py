from pysat.formula import IDPool, CNF
from pysat.solvers import Glucose4

import sys

k = int(sys.argv[1])
n = 3

# little hack to get rid of resolving point to point graph
if k == 1:
    print(2)
    exit(0)

while True:
    var_pool = IDPool()
    cnf = CNF()

    for x in range(n):
        for y in range(x):
            cnf.append([var_pool.id('P_{}_{}k{}'.format(x + 1, y + 1, c + 1)) for c in range(k)])

    for x in range(n):
        for y in range(x):
            for c in range(k):
                edge = -var_pool.id('P_{}_{}k{}'.format(x + 1, y + 1, c + 1))
                for c2 in range(c):
                    cnf.append([edge, -var_pool.id('P_{}_{}k{}'.format(x + 1, y + 1, c2 + 1))])

    for x in range(n):
        for y in range(x):
            for z in range(y):
                for c in range(k):
                    cnf.append([-var_pool.id('P_{}_{}k{}'.format(x + 1, y + 1, c + 1)),
                                -var_pool.id('P_{}_{}k{}'.format(y + 1, z + 1, c + 1)),
                                -var_pool.id('P_{}_{}k{}'.format(x + 1, z + 1, c + 1))])

    g = Glucose4()
    g.append_formula(cnf.clauses)
    print('analyzing clique with ' + str(n) + ' vertices')
    # print('vars = ' + str(g.nof_vars()))
    # print('clauses = ' + str(g.nof_clauses()))

    if not g.solve():
        print('the answer is : n = ' + str(n - 1))
        break
    else:
        n = n + 1

    g.delete()
