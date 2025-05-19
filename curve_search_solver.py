from time import time
import numpy as np
import psutil

from cutest_problem import Cutest_Problem

class Curve_Search_Solver:

    def __init__(self,
                 max_iters: int, max_time: float, grad_tol: float, 
                 alpha0: float, gamma: float, delta: float, min_step: float, 
                 g_factor: float,
                 alpha0mom: float, beta0mom: float, 
                 M_nm: int, 
                 ram_lim: float):

        # Stopping conditions
        self.max_iters = max_iters
        self.max_time = max_time
        self.grad_tol = grad_tol 
        
        # For Armijo-type line search
        self.alpha0 = alpha0 
        self.gamma = gamma 
        self.delta = delta 
        self.min_step = min_step 

        # Curve Search Hyperparameters
        self.g_factor = g_factor
        self.alpha0mom = alpha0mom
        self.beta0mom = beta0mom
        self.M_nm = M_nm

        # Ram settings
        self.ram_lim = ram_lim

        # Counters
        self.fevals = 0
        self.gevals = 0

    def run(self, problem: Cutest_Problem): 
        
        n_iters = 0
        t_start = time()
        self.fevals = 0
        self.gevals = 0

        xk = np.copy(problem.x0)
        f, g = self.call_f_g(problem, xk)
        g_norm = np.linalg.norm(g, ord=np.inf)

        alpha = self.alpha0

        if self.M_nm:
            f_prevs = f * np.ones(self.M_nm)

        sk = 0
        xk_1 = np.copy(xk)  

        while n_iters < self.max_iters and \
              time() - t_start <= self.max_time and \
              g_norm >= self.grad_tol and \
              alpha != 0 and \
              psutil.virtual_memory().percent <= self.ram_lim:

            if g_norm > 1e6:
                g /= g_norm

            if not n_iters:
                dd, alpha, f = self.armijoLS(problem=problem, 
                                         x=xk, 
                                         f=(f if not self.M_nm else np.max(f_prevs)), 
                                         g=g, 
                                         d=-g)
            
            else:   
                sk = xk - xk_1
                xk_1 = np.copy(xk)
                
                dd, alpha, f = self.armijoCS(problem=problem, 
                                             x=xk, 
                                             f=(f if not self.M_nm else np.max(f_prevs)), 
                                             g=g, 
                                             d=-2 * self.g_factor * g, 
                                             curve_points=[np.copy(xk), xk - self.g_factor * g, xk - self.alpha0mom * g + self.beta0mom * sk])

            xk += dd
            g = self.call_g(problem, xk)
            g_norm = np.linalg.norm(g, ord=np.inf)

            if self.M_nm:
                f_prevs = np.roll(f_prevs, 1)
                f_prevs[0] = f

            n_iters += 1
        
        return xk, \
               {"f": f, "g_norm": g_norm, "iters": n_iters, "time": time() - t_start, "fevals": self.fevals, "gevals": self.gevals}, \
               psutil.virtual_memory().percent > self.ram_lim

    def armijoLS(self, problem: Cutest_Problem, x: np.array, f: np.array, g: np.array, d: np.array):

        alpha = self.alpha0
        f_trial = self.call_f(problem, x + alpha * d)
        
        while (np.isnan(f_trial) or np.isinf(f_trial) or f_trial > f + self.gamma * alpha * np.dot(g, d)) and alpha > self.min_step:
            alpha *= self.delta
            f_trial = self.call_f(problem, x + alpha * d)
        
        if alpha <= self.min_step:
            alpha = 0
        
        return alpha * d, alpha, f_trial
    
    def armijoCS(self, problem: Cutest_Problem, x: np.array, f: np.array, g: np.array, d: np.array, curve_points: list):

        alpha = self.alpha0
        bzx = self.getBezierCurvePoint(P0=curve_points[0], P1=curve_points[1], P2=curve_points[2], t=alpha)
        f_trial = self.call_f(problem, bzx)
        
        while (np.isnan(f_trial) or np.isinf(f_trial) or f_trial > f + self.gamma * alpha * np.dot(g, d)) and alpha > self.min_step:
            alpha *= self.delta
            bzx = self.getBezierCurvePoint(P0=curve_points[0], P1=curve_points[1], P2=curve_points[2], t=alpha)
            f_trial = self.call_f(problem, bzx)
        
        if alpha <= self.min_step:
            return self.armijoLS(x=x, f=f, g=g, d=d)
    
        return bzx - x, alpha, f_trial
    
    def call_f(self, problem: Cutest_Problem, x: np.array):
        self.fevals +=1
        return problem.f(x)

    def call_f_g(self, problem: Cutest_Problem, x: np.array):
        self.fevals += 1
        self.gevals += 1
        return problem.f_g(x)

    def call_g(self, problem: Cutest_Problem, x: np.array):
        self.gevals += 1
        return problem.g(x)
    
    @staticmethod
    def getBezierCurvePoint(P0: np.array, P1: np.array, P2: np.array, t: float):
        if t == 1:
            return P2
        else:
            return (1-t)**2 * P0 + 2 * (1-t) * t * P1 + t**2 * P2