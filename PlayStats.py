# Skout - Flagfootball Scouting Analysis Tool
#   Copyright (C) 2021  Xaver Klemenschits
#   See LICENSE.txt for details

import numpy as np

class PlayStats:
    def incrementStrongSide(self, strongSideList, strongSideString):
        if(strongSideString == "right"):
            strongSideList[1] += 1
        elif(strongSideString == "left"):
            strongSideList[0] += 1
        else:
            print("Warning: Invalid StrongSide string!")

    def swapEntry(self, i, j, swappable):
        swappable[i], swappable[j] = swappable[j], swappable[i]

    def swapEntries(self, i, j):
        self.swapEntry(i, j, self.routesList)
        self.swapEntry(i, j, self.occurences)
        self.swapEntry(i, j, self.downStats)
        self.swapEntry(i, j, self.formations)
        self.swapEntry(i, j, self.strongSides)

    def __init__(self, playList):
        self.homeTeam = playList.homeTeam
        self.awayTeam = playList.awayTeam
        self.date = playList.date
        self.score = (playList.homeScore, playList.awayScore)
        playList.sort()
        self.routesList = []
        self.occurences = []
        self.downStats = []
        self.formations = []
        self.strongSides = []
        
        # Calculate stats from the passed playList

        # just push 1st element
        self.routesList.append(playList.routes[0])
        self.occurences.append(1)
        downList = [0,0,0,0,0]
        downList[playList.downs[0]-1] = 1
        self.downStats.append(downList)
        self.formations.append([])
        self.formations[-1].append(playList.formations[0])
        strongside = [0,0]
        self.incrementStrongSide(strongside, playList.sides[0])
        self.strongSides.append(strongside)

        last = 0
        for i in range(1, len(playList.routes)):
            # routes are equal, so add onto earlier play
            if(self.routesList[last] == playList.routes[i]):
                self.occurences[last] += 1
                self.downStats[last][playList.downs[i]-1] += 1
                self.formations[last].append(playList.formations[i])
                self.incrementStrongSide(self.strongSides[last], playList.sides[i])

            # routes are not equal, add new play to list
            else:
                self.routesList.append(playList.routes[i])
                self.occurences.append(1)
                downList = [0,0,0,0,0]
                downList[playList.downs[i]-1] = 1
                self.downStats.append(downList)
                self.formations.append([])
                self.formations[-1].append(playList.formations[i])
                strongside = [0,0]
                self.incrementStrongSide(strongside, playList.sides[i])
                self.strongSides.append(strongside)
                last += 1

        # bubble sort results after number of occurences
        n = len(self.routesList)

        # traverse from front
        for i in range(n-1):
            #  last elements are already in place
            for j in range(n-i-1):
                if(self.occurences[j] < self.occurences[j+1]):
                    self.swapEntries(j, j+1)

    def print(self):
        for i in range(len(self.routesList)):
            outputStr = "Play " + str(i) + ":\n"
            outputStr += "Routes: " + str(self.routesList[i]) + "\n"
            outputStr += "Downcount: " + str(self.downStats[i]) + "\n"
            outputStr += "Formations: " + str(self.formations[i]) + "\n"
            outputStr += "Strongsides: " + str(self.strongSides[i]) + "\n"
            print(outputStr)

    def getFormations(self, index):
        if(len(self.formations[index]) == 0):
            return ""
        result = str(self.formations[index][0])
        for i in range(1, len(self.formations[index])):
            if(self.formations[index][i] != ""):
                if(result != ""):
                    result = result + ", "
                result = result + self.formations[index][i]

        return result