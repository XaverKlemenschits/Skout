# Class for a list of plays

import numpy as np
from Route import Route, RouteList

class PlayList:
    def __init__(self):
        self.routes = []
        self.formations = []
        self.downs = []
        self.sides = []

    def addPlays(self, dict):
        
        for play in dict:
            # TODO add logic here for duplicate counting
            routes = []
            for i in range(4):
                routes.append(Route(play['routes'][i]))
            self.routes.append(RouteList(routes))
            self.formations.append(play['formation'])
            self.downs.append(play['down'])
            self.sides.append(play['strongside'])

    def printAllPlays(self):
        for i in range(len(self.routes)):
            print("Routes: {}, formation: {}, down: {}, strongside: {}".format(self.routes[i], self.formations[i], self.downs[i], self.sides[i]))

    def swapEntry(self, i, j, swappable):
        swappable[i], swappable[j] = swappable[j], swappable[i]

    def swapEntries(self, i, j):
        self.swapEntry(i, j, self.routes)
        self.swapEntry(i, j, self.formations)
        self.swapEntry(i, j, self.downs)
        self.swapEntry(i, j, self.sides)

    def sort(self):
        n = len(self.routes)

        # traverse from front
        for i in range(n-1):
            #  last elements are already in place
            for j in range(n-i-1):
                if(self.routes[j] < self.routes[j+1]):
                    self.swapEntries(j, j+1)
                    