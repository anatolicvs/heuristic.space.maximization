from abc import ABC, abstractmethod


class PolygonStochasticOptimizationBase(ABC):
    """ Abstract base class for stochastic optimization"""

    @classmethod
    @abstractmethod
    def getEdges(cls, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def inPolygon(cls, pos, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def makingCenterGravCircum(cls, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def makingCenterGrav2(cls, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def rotate(cls, coord, angle, coord1):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def initOne(cls, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def initPop(cls, nb, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def calcDist(cls, pop1, pop2):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def modifyCoord(cls, pos, minMaxSets, flag, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def sol2rect(cls, pos):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def calcArea(cls, pop):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def makingInitialBest(cls, pop, centerGrav):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def mutation(cls, pos, minMaxSets, polygon):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def __print__(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def __draw__(cls, name, polygon, color, clname):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def __csv__(cls, name):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def __isvalid__(cls, polygon):
        raise NotImplementedError
