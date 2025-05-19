import sys
import os
from tabulate import tabulate


from cutest_problem import Cutest_Problem
from curve_search_solver import Curve_Search_Solver

from parser_management import get_args

args = get_args()

if args.save_logs != '':
    sys.stdout = open(os.path.join("Outputs", "{}.txt".format(args.save_logs)), "w", buffering=1)

for problem_name in args.problems:

    problem = Cutest_Problem(problem_name)
    print()
    print("{}, N = {}".format(problem.name, problem.n))

    table_results = []

    for M_nm in args.M_nm:
        for g_factor in args.g_factor:
            bcs = Curve_Search_Solver(args.max_iters, args.max_time, args.grad_tol, 
                                       args.alpha0, args.gamma, args.delta, args.min_step, 
                                       g_factor, 
                                       args.alpha0mom, args.beta0mom, 
                                       M_nm, 
                                       args.ram_lim)
            
            xk, info, ram_issue = bcs.run(problem)

            if ram_issue:
                raise OverflowError('RAM Memory limit reached!')
            
            table_results.append(['BC_g{}{}'.format(g_factor, '' if not M_nm else '_M{}'.format(M_nm)), 
                                  info['f'], info['g_norm'], info['iters'], info['time'], info['fevals'], info['gevals']])
            
    table = tabulate(table_results, headers=['Algorithm', 'f_star', 'g_norm', 'n_it', 'T', 'f_evals', 'g_evals'], tablefmt='orgtbl')
    print(table)    
  