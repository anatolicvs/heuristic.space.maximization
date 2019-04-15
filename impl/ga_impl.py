import logging
import math
import random
import socket
import time

import numpy as np
import numpy.random as randnp
from tqdm import tqdm

from pso.p_stochastic_opt import PolygonStochasticOptimization

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG)
d = {'clientip': host_ip, 'user': host_name}


class GA(PolygonStochasticOptimization):
    """ The implementation class for stochastic optimization with generic algorithms for polygons."""

    def __init__(self, polygon, nb_Cycles, nb_Indiv, w, ro_max):
        super(GA, self).__init__()
        self.polygon = polygon
        self.Nb_Cycles = nb_Cycles
        self.Nb_Indiv = nb_Indiv
        self.w = w
        self.ro_max = ro_max

    def __repr__(self):
        return "{cls}({polygon}, {Nb_Cycles},{Nb_Indiv},{w},{ro_max})".format(
            cls=self.__class__.__name__,
            polygon=self.polygon,
            Nb_Cycles=self.Nb_Cycles,
            Nb_Indiv=self.Nb_Indiv,
            w=self.w,
            ro_max=self.ro_max)

    @staticmethod
    def __makingCenterGrav(self, polygon):
        coord0 = [0, 0]
        coord1 = [0, 0]
        angle = 0
        for line in polygon:
            coord0[0] += (line[0][0]) / len(polygon)
            coord0[1] += (line[0][1]) / len(polygon)
            coord1[0] += (line[1][0]) / len(polygon)
            coord1[1] += (line[1][1]) / len(polygon)
            angle += line[2] / len(polygon)
        return [coord0, coord1, angle]

    @staticmethod
    def __getBest(self, pop):
        global bestCoord
        bestArea = 0
        for linePop in pop:
            if self.calcArea(linePop) > bestArea:
                bestCoord = linePop
                bestArea = self.calcArea(linePop)
        return bestCoord

    @staticmethod
    def __getWorst(self, pop):
        worstArea = 0
        index = 0
        worstCoord = pop[0]
        for i, linePop in enumerate(pop):
            if self.calcArea(linePop) < worstArea:
                worstCoord = linePop
                worstArea = self.calcArea(linePop)
                index = i
        return [worstCoord, index]

    @staticmethod
    def ___makingInd(self, parents, polygon):
        try:
            flag = 1
            centGrav = self.__makingCenterGrav(self, parents)
            child = [np.array([centGrav[0][0], centGrav[0][1]]), np.array([centGrav[1][0], centGrav[1][1]]),
                     centGrav[2]]
            while flag == 1:
                for i in range(3):
                    if i == 0 or i == 1:
                        dVec = [parents[1][i][0] - parents[0][i][0],
                                parents[1][i][1] - parents[0][i][1]]
                        a = math.sqrt(
                            pow(dVec[1], 2) / (pow(dVec[0], 2) + pow(dVec[1], 2)))
                        b = math.sqrt(
                            pow(dVec[0], 2) / (pow(dVec[0], 2) + pow(dVec[1], 2)))
                        child[i][0] = (parents[0][i][0] + parents[1][i][0]) / 2 + randnp.randn() * (
                                parents[1][i][0] - parents[0][i][0]) + self.calcDist(dVec,
                                                                                     parents[2][0]) * randnp.randn() * a
                        child[i][1] = (parents[0][i][1] + parents[1][i][1]) / 2 + randnp.randn() * (
                                parents[1][i][1] - parents[0][i][1]) + self.calcDist(dVec,
                                                                                     parents[2][0]) * randnp.randn() * b
                    else:
                        child[i] = (parents[0][i] + parents[1][i]) / 2 + randnp.randn() * (
                                parents[1][i] - parents[0][i])
                        child[i] = abs(child[i]) % (math.pi * 2)
                tempArray = self.sol2rect(child)
                flag = self.inPolygon(tempArray, polygon)
            return child

        except Exception as exp_m:
            logging.error(exp_m, extra=d)

    def __exec__(self):

        global num1
        logging.info("__exec__ method is fired.", extra=d)
        print(
            "{cls}(polygon=({polygon}), Nb_Cycles=({Nb_Cycles}),Nb_Indiv=({Nb_Indiv}),w=({w}),ro_max=({ro_max}))".format(
                cls=self.__class__.__name__,
                polygon=self.polygon,
                Nb_Cycles=self.Nb_Cycles,
                Nb_Indiv=self.Nb_Indiv,
                w=self.w,
                ro_max=self.ro_max))

        try:
            for iteration in tqdm(range(30)):
                minMaxSets = self.getEdges(self.polygon)
                pop = self.initPop(self.Nb_Indiv, self.polygon)

                best = self.__getBest(self, pop)
                worst = self.__getWorst(self, pop)
                child = []

                for i in range(self.Nb_Cycles):
                    for j in range(self.Nb_Indiv):
                        flag = 0
                        num1 = num2 = num3 = 0
                        while num1 == num2 == num3 or self.calcDist(pop[num1][0], pop[num2][0]) == 0 or self.calcDist(
                                pop[num1][0], pop[num2][0]) == 0:

                            num1 = random.randint(0, self.Nb_Indiv - 1)
                            num2 = random.randint(0, self.Nb_Indiv - 1)
                            num3 = random.randint(0, self.Nb_Indiv - 1)

                            flag += 1

                            if flag == 10:
                                for i in range(3):
                                    pop[i] = self.mutation(
                                        pop[i], minMaxSets, self.polygon)

                        parents = [pop[num1], pop[num2], pop[num3]]
                        child.append(self.___makingInd(self, parents, self.polygon))

                    if self.calcArea(best) < self.calcArea(self.__getBest(self, child)):
                        best = self.__getBest(self, child)
                        pop[num1] = best

                    if self.calcArea(worst[0]) < self.calcArea(self.__getBest(self, child)):
                        pop[worst[1]] = self.__getBest(self, child)
                        worst = self.__getWorst(self, pop)

                time.sleep(1)
                self.bestResultCombination.append(best)
                self.bestResultArea.append(self.calcArea(best))

        except Exception as exp_m:
            logging.error(exp_m, extra=d)
