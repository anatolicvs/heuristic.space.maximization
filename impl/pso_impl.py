import copy
import logging
import math
import random
import socket
import time

from tqdm import tqdm

from pso.p_stochastic_opt import PolygonStochasticOptimization

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

FORMAT = "%(asctime)-15s clientip=%(clientip)s user=%(user)-8s %(message)s"
logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG)
d = {'clientip': host_ip, 'user': host_name}


class PSO(PolygonStochasticOptimization):
    """ The implementation class for stochastic optimization for polygons."""

    def __init__(self, polygon, nb_Cycles, nb_Indiv, w, ro_max):
        super(PSO, self).__init__()
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
    def updateVelocity(pos, v, w, ro_max, indBest, groupBest):
        for i in range(len(v)):
            if i == 0 or i == 1:
                for j in range(len(v[i])):
                    v[i][j] = w * v[i][j] + random.uniform(0, ro_max) * (indBest[i][j] - pos[i][j]) + random.uniform(0,
                                                                                                                     ro_max) * (
                                          groupBest[i][j] - pos[i][j])
            else:
                v[i] = w * v[i] + random.uniform(0, ro_max) * (indBest[i] - pos[i]) + random.uniform(0, ro_max) * (
                            groupBest[i] - pos[i])
                v[i] = abs(v[i]) % (2 * math.pi)
                if v[i] > math.pi:
                    v[i] -= math.pi
        return v

    @staticmethod
    def updatePosition(pos, v):
        for i in range(len(pos)):
            if i == 0 or i == 1:
                for j in range(len(v[i])):
                    pos[i][j] += v[i][j]
            else:
                pos[i] += v[i]
        return pos

    def __exec__(self):
        """ The main execution function is responsible for initialization of polygons and calculation of the best areas for them. """
        try:
            logging.info("__exec__ method is fired.", extra=d)
            global j, tempBestArea
            print(
                "{cls}(polygon=({polygon}), Nb_Cycles=({Nb_Cycles}),Nb_Indiv=({Nb_Indiv}),w=({w}),ro_max=({ro_max}))".format(
                    cls=self.__class__.__name__,
                    polygon=self.polygon,
                    Nb_Cycles=self.Nb_Cycles,
                    Nb_Indiv=self.Nb_Indiv,
                    w=self.w,
                    ro_max=self.ro_max))

            for ite in tqdm(range(30)):
                minMaxSets = self.getEdges(self.polygon)
                centerGrav = self.makingCenterGravCircum(self.polygon)
                pop = self.initPop(self.Nb_Indiv, self.polygon)
                indBest, groupBest = self.makingInitialBest(pop, centerGrav)
                bestArea = self.calcArea(groupBest)
                velocity = [[0, 0], [0, 0], 0]

                for i in range(self.Nb_Cycles):
                    flag2 = 0
                    for j in range(self.Nb_Indiv):
                        tempPos = copy.deepcopy(pop[j])
                        flag1 = 1
                        while flag1 != 0:
                            velocity = self.updateVelocity(tempPos, velocity, self.w, self.ro_max, indBest, groupBest)
                            tempPos = self.updatePosition(tempPos, velocity)
                            flag1 = self.modifyCoord(tempPos, minMaxSets, flag1, self.polygon)
                            flag1 += 1
                            if flag1 == 10:
                                tempPos = self.mutation(tempPos, minMaxSets, self.polygon)
                                flag1 = 1
                        tempArea = self.calcArea(tempPos)
                        if self.calcArea(pop[j]) < tempArea:
                            flag2 = 1
                            pop[j] = copy.deepcopy(tempPos)
                            del tempPos
                            tempBestArea = tempArea
                    if flag2 == 1:
                        if bestArea < tempBestArea:
                            bestArea = tempBestArea
                            groupBest = copy.deepcopy(pop[j])
                    tempBestArea = 0
                time.sleep(1)
                self.bestResultCombination.append(groupBest)
                self.bestResultArea.append(self.calcArea(groupBest))

        except Exception as exp_m:
            logging.error(exp_m, extra=d)
