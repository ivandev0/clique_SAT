from pysat.formula import IDPool, CNF
from pysat.solvers import Glucose4
import subprocess

import sys

file_name = "shatter/data/cnf_formula"
sym_extension = ".Sym.cnf"
shatter_path = "./shatter/shatter.pl"
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
            cnf.append([var_pool.id('P_{}_{}k{}'.format(x, y, c)) for c in range(k)])

    for x in range(n):
        for y in range(x):
            for z in range(y):
                for c in range(k):
                    cnf.append([-var_pool.id('P_{}_{}k{}'.format(x, y, c)),
                                -var_pool.id('P_{}_{}k{}'.format(y, z, c)),
                                -var_pool.id('P_{}_{}k{}'.format(x, z, c))])

    cnf.to_file(file_name)
    subprocess.check_call([shatter_path, file_name])
    cnf.from_file(file_name + sym_extension)
    g = Glucose4()
    g.append_formula(cnf.clauses)
    print('analyzing clique with ' + str(n) + ' vertices')
    # print('vars = ' + str(g.nof_vars()))
    # print('clauses = ' + str(g.nof_clauses()))

    if not g.solve():
        print('for k = ' + str(k) + ' the answer is : n = ' + str(n - 1))
        break
    else:
        n = n + 1

    g.delete()
