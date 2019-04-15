import calendar
import copy
import csv
import logging
import math
import random
import socket
import time

import pyclipper
from PIL import Image, ImageDraw

from pso.p_stochastic_opt_base import PolygonStochasticOptimizationBase

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

FORMAT = "%(asctime)-15s clientip=%(clientip)s user=%(user)-8s %(message)s"
logging.basicConfig(format=FORMAT,
                    level=logging.DEBUG)
d = {'clientip': host_ip, 'user': host_name}


class PolygonStochasticOptimization(PolygonStochasticOptimizationBase):
    """ The Stochastic optimization class to optimize and fit polygons on the areas """

    bestResultArea = []
    bestResultCombination = []

    @classmethod
    def getEdges(cls, polygon):
        minMaxSets = [polygon[0][0], polygon[0]
        [0], polygon[1][0], polygon[0][1]]
        for linePoly in polygon:
            if linePoly[0] < minMaxSets[0]:
                minMaxSets[0] = linePoly[0]
            elif linePoly[0] > minMaxSets[1]:
                minMaxSets[1] = linePoly[0]
            elif linePoly[1] < minMaxSets[2]:
                minMaxSets[2] = linePoly[1]
            elif linePoly[1] > minMaxSets[3]:
                minMaxSets[3] = linePoly[1]
        return minMaxSets

    @classmethod
    def inPolygon(cls, pos, polygon):
        np = len(polygon)
        for i in range(len(pos)):
            inside = False
            for i1 in range(np):
                i2 = (i1 + 1) % np
                if min(polygon[i1][0], polygon[i2][0]) < pos[i][0] < max(polygon[i1][0], polygon[i2][0]):
                    if (polygon[i1][1] + (polygon[i2][1] - polygon[i1][1]) / (polygon[i2][0] - polygon[i1][0]) * (
                            pos[i][0] - polygon[i1][0]) - pos[i][1]) > 0:
                        inside = not inside
            if inside == 0:
                return 1
        return 0

    @classmethod
    def makingCenterGravCircum(cls, polygon):
        temp = [0 for i in range(len(polygon[0]))]
        for linePoly in polygon:
            for i in range(len(linePoly)):
                temp[i] += linePoly[i]
        return temp

    @classmethod
    def makingCenterGrav2(cls, polygon):
        centGrav = [0, 0]
        for line in polygon:
            centGrav[0] += line[0] / len(polygon)
            centGrav[1] += line[1] / len(polygon)
        return centGrav

    @classmethod
    def rotate(cls, coord, angle, coord1):
        temp = [coord[0] * math.cos(angle) - coord[1] * math.sin(angle),
                coord[0] * math.sin(angle) + coord[1] * math.cos(angle)]
        temp[0] += coord1[0]
        temp[1] += coord1[1]
        return temp

    @classmethod
    def initOne(cls, polygon):
        global pos
        minMaxSets = cls.getEdges(polygon)
        flag = 1

        while flag == 1:
            pos = []
            angle = random.uniform(0, math.pi)
            pos.append([random.uniform(minMaxSets[0], minMaxSets[1]),
                        random.uniform(minMaxSets[2], minMaxSets[3])])
            pos.append([random.uniform(minMaxSets[0], minMaxSets[1]),
                        random.uniform(minMaxSets[2], minMaxSets[3])])
            pos.append(angle)
            coord = cls.sol2rect(pos)
            flag = cls.inPolygon(coord, polygon)
        return pos

    @classmethod
    def initPop(cls, nb, polygon):
        return [cls.initOne(polygon) for i in range(nb)]

    @classmethod
    def calcDist(cls, pop1, pop2):
        return math.sqrt(pow((pop1[0] - pop2[0]), 2) + pow((pop1[1] - pop2[1]), 2))

    @classmethod
    def modifyCoord(cls, pos, minMaxSets, flag, polygon):
        temp4Pos = cls.sol2rect(pos)
        if cls.inPolygon(temp4Pos, polygon) == 1:
            return flag
        return -1

    @classmethod
    def sol2rect(cls, pos):
        tempPos = []
        tempPos.append(pos[1])
        tempPos.append(cls.rotate(
            [pos[1][0] - pos[0][0], pos[1][1] - pos[0][1]], -pos[2], pos[0]))
        tempPos.append(cls.rotate(
            [pos[1][0] - pos[0][0], pos[1][1] - pos[0][1]], math.pi, pos[0]))
        tempPos.append(cls.rotate(
            [tempPos[1][0] - pos[0][0], tempPos[1][1] - pos[0][1]], math.pi, pos[0]))
        return tempPos

    @classmethod
    def calcArea(cls, pop):
        temp4Pos = cls.sol2rect(pop)
        return cls.calcDist(temp4Pos[0], temp4Pos[1]) * cls.calcDist(temp4Pos[0], temp4Pos[3])

    @classmethod
    def makingInitialBest(cls, pop, centerGrav):
        tempIndBest = [pop[0][0], pop[0][1], pop[0][2]]
        bestArea = cls.calcArea(tempIndBest)
        for linePop in pop:
            currArea = cls.calcArea(linePop)
            if bestArea < currArea:
                bestArea = currArea
                tempIndBest = copy.deepcopy(linePop)
        tempGroupBest = copy.deepcopy(tempIndBest)
        return tempIndBest, tempGroupBest

    @classmethod
    def mutation(cls, pos, minMaxSets, polygon):
        flag = 1
        while flag == 1:
            randTemp = random.randint(0, 3)
            if randTemp == 0:
                pos[0] = [random.uniform(minMaxSets[0], minMaxSets[1]), random.uniform(
                    minMaxSets[2], minMaxSets[3])]
            elif randTemp == 1:
                pos[1] = [random.uniform(minMaxSets[0], minMaxSets[1]), random.uniform(
                    minMaxSets[2], minMaxSets[3])]
            else:
                pos[2] = random.uniform(0, math.pi)
            flag = cls.inPolygon(cls.sol2rect(pos), polygon)
        return pos

    @classmethod
    def __print__(self):
        """" This function prints the best results of 30. """
        logging.info("The best Result Area", extra=d)
        for i in range(30):
            print(self.bestResultArea[i])
        print(self.bestResultCombination)
        for i in range(30):
            print(self.bestResultCombination[i])

    @classmethod
    def __draw__(self, name, polygon, color, clname):
        """Draw the polygons images according the coordinates."""
        logging.info(
            "Draw the polygons images according the coordinates.", extra=d)
        if self.bestResultCombination != []:
            for ite in range(30):
                temp4Pos = self.sol2rect(self.bestResultCombination[ite])
                for i in range(len(temp4Pos)):
                    temp4Pos[i] = tuple(temp4Pos[i])
                im = Image.new('RGB', (600, 600), clname)
                draw = ImageDraw.Draw(im)
                draw.polygon((polygon), fill=200, outline=(255, 255, 255))
                draw.polygon((tuple(temp4Pos)), fill=color,
                             outline=(255, 255, 220))
                im.save(
                    './images/' + name + '/Results/' + name + '_Results_' +
                    str(calendar.timegm(time.gmtime())) +
                    '_' + str(ite) + '.jpg',
                    quality=95)
        else:
            print("$bestResultCombination is blank")

    @classmethod
    def __csv__(self, name):
        """ Save the best result areas as csv file"""
        logging.info("Save the best result areas as csv file", extra=d)
        if self.bestResultArea != []:
            f = open('./csv/' + name + '/Results/' + name + '_Results_' +
                     str(calendar.timegm(time.gmtime())) + '.csv', 'w')
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(self.bestResultArea)
            f.close()
        else:
            print("$bestResultArea is blank")

    @classmethod
    def __isvalid__(cls, polygon):

        logging.info("__isvalid__ method is fired.", extra=d)

        for ite in range(2):
            temp4Pos = cls.sol2rect(cls.bestResultCombination[ite])

            pc = pyclipper.Pyclipper()
            pc.AddPath(polygon, pyclipper.PT_CLIP, True)
            pc.AddPaths(temp4Pos, pyclipper.PT_SUBJECT, True)

            solution = pc.Execute2(
                pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)

            print(solution)
