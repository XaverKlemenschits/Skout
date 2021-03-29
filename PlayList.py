# Class for a list of plays

import numpy as np

class PlayList:
    def __init__(self):
        self.routes = []
        self.formations = []
        self.downs = []
        self.sides = []

    def addPlays(self, dict):
        
        for play in dict:
            # TODO add logic here for duplicate counting
            self.routes.append(play['routes'])
            self.formations.append(play['formation'])
            self.downs.append(play['down'])
            self.sides.append(play['strongside'])

    def printAllPlays(self):
        for i in range(len(self.routes)):
            print("Routes: {}, formation: {}, down: {}, strongside: {}".format(self.routes[i], self.formations[i], self.downs[i], self.sides[i]))
