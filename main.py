from pysat.formula import IDPool, CNF
from pysat.solvers import Glucose4
from threading import Timer
import sys

n = 3

while True:
    vpool = IDPool()
    k = int(sys.argv[1])
    # n = int(sys.argv[2])
    cnf = CNF()
    g = Glucose4(use_timer=True)

    for x in range(n):
        for y in range(n):
            if y < x:
                clause = []
                for c in range(k):
                    # print('P_{}_{}k{}'.format(x, y, c))
                    clause += [vpool.id('P_{}_{}k{}'.format(x + 1, y + 1, c + 1))]
                # cnf.append(clause)
                g.add_clause(clause)
    # print('-----------------------------------------')
    # print ('clauses1 = ' + str(g.nof_clauses()))

    for x in range(n):
        for y in range(n):
            if y < x:
                for c in range(k):
                    # print('P_{}_{}k{}'.format(x, y, c))
                    edge = -vpool.id('P_{}_{}k{}'.format(x + 1, y + 1, c + 1))
                    for c2 in range(k):
                        if c2 > c: # c2 != c
                            # print('P_{}_{}k{}'.format(x, y, c2))
                            cnf.append([edge, -vpool.id('P_{}_{}k{}'.format(x + 1, y + 1, c2 + 1))])
                            g.add_clause([edge, -vpool.id('P_{}_{}k{}'.format(x + 1, y + 1, c2 + 1))])
    # print('-----------------------------------------')
    # print ('clauses1 = ' + str(g.nof_clauses()))

    for x in range(n):
        for y in range(n):
            for z in range(n):
                for c in range(k):
                    if x != y and y != z and z != x:
                        if x > y > z:
                            # print('Px{}y{}k{}'.format(x, y, c))
                            # print('Py{}z{}k{}'.format(y, z, c))
                            # print('Pz{}x{}k{}'.format(x, z, c))
                            # print('-----------------------------------------')

                            g.add_clause([-vpool.id('P_{}_{}k{}'.format(x + 1, y + 1, c + 1)),
                                          -vpool.id('P_{}_{}k{}'.format(y + 1, z + 1, c + 1)),
                                          -vpool.id('P_{}_{}k{}'.format(x + 1, z + 1, c + 1))])

    # g.append_formula(cnf.clauses)
    print('n = ' + str(n))
    print('vars = ' + str(g.nof_vars()))
    print('clauses = ' + str(g.nof_clauses()))

    if not g.solve_limited():
        print(n - 1)
        break
    else:
        n = n + 1

    g.delete()
# for i in range(1, 13):
# 	print('i = ' + str(i) + ' -> ' + str(vpool.obj(i)))

