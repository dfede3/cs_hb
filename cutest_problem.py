import pycutest
import numpy as np


class Cutest_Problem:
    
    def __init__(self, name: str):
        
        self.__p = pycutest.import_problem(name)
        
        self.__n = self.__p.n
        self.__x0 = np.copy(self.__p.x0)
        self.__name = self.__p.name

    def f(self, x: np.array):
        return self.__p.obj(x)

    def f_g(self, x: np.array):
        return self.__p.obj(x, gradient=True)

    def g(self, x: np.array):
        _, gr = self.__p.obj(x, gradient=True)
        return gr

    @property
    def n(self):
        return self.__n

    @property
    def x0(self):
        return self.__x0
    
    @property
    def name(self):
        return self.__name
