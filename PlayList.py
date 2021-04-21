# Skout - Flagfootball Scouting Analysis Tool
#   Copyright (C) 2021  Xaver Klemenschits
#   See LICENSE.txt for details

from Route import Route, RouteList

class PlayList:
    def __init__(self):
        self.routes = []
        self.formations = []
        self.downs = []
        self.sides = []
        self.clipNumbers = []

    def setTeamNames(self, home, away):
        self.homeTeam = home
        self.awayTeam = away

    def setDate(self, date):
        self.date = date

    def setScore(self, home, away):
        self.homeScore = home
        self.awayScore = away

    def addPlays(self, dict):
        
        for play in dict:
            routes = []
            for i in range(4):
                routes.append(Route(play['routes'][i]))
            self.routes.append(RouteList(routes))
            self.formations.append(play['formation'])
            self.downs.append(play['down'])
            self.sides.append(play['strongside'])
            # optional fields
            self.clipNumbers.append(play.get('clipNumber', 0))

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
        self.swapEntry(i, j, self.clipNumbers)

    def sort(self):
        n = len(self.routes)

        # traverse from front
        for i in range(n-1):
            #  last elements are already in place
            for j in range(n-i-1):
                if(self.routes[j] < self.routes[j+1]):
                    self.swapEntries(j, j+1)
                    