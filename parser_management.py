import argparse
import sys


def get_args():

    parser = argparse.ArgumentParser(prog='run_all', description='Run curve search solver on CUTEst problems')

    parser.add_argument('--problems', help='Problems to test', type=str, nargs='+', default=['HILBERTB'])

    parser.add_argument('--max_iters', help='Maximum number of iterations', type=int, default=5000)

    parser.add_argument('--max_time', help='Maximum elapsed time in seconds', type=float, default=120)

    parser.add_argument('--grad_tol', help='Threshold to declare stationarity', type=float, default=1e-3)

    parser.add_argument('--alpha0', help='Initial step size for line searches', type=float, default=1)

    parser.add_argument('--gamma', help='Coefficient for the sufficient decrease condition in line searches', type=float, default=1e-7)

    parser.add_argument('--delta', help='Coefficient for the step size contraction in line searches', type=float, default=0.5)

    parser.add_argument('--min_step', help='Minimum possible value for the step size in line searches', type=float, default=1e-10)

    parser.add_argument('--g_factor', help="factor for curve's initial velocity", type=float, nargs='+', default=[0.125])

    parser.add_argument('--alpha0mom', help='alpha for heavy-ball momentum', type=float, default=1)

    parser.add_argument('--beta0mom', help='beta for heavy-ball momentum', type=float, default=0.9)

    parser.add_argument('--M_nm', help='Memory for non-monotone mode', type=int, nargs='+', default=[0])

    parser.add_argument('--ram_lim', help='RAM Memory limit for execution', type=float, default=95)

    parser.add_argument('--save_logs', help='Name of the txt file save in the Outputs folder', type=str, default='')

    return parser.parse_args(sys.argv[1:])