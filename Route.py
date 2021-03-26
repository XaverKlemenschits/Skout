# Definition of RouteTree class
import sys
class Route:
    routeNames = ["Stop", "Quick Out", "Slant", "Deep Out", "Deep In", "10 Out", "10 In", "Corner", "Post", "Go", "5 In", "5 Out"]

    def __init__(self, r=0):
        self.route = r

    def setRoute(self, r):
        if(type(r) == str):
            foundRoute = False
            for i in range(0, len(self.routeNames)):
                if(self.routeNames[i] == r):
                    self.route = i
                    foundRoute = True

            if(not foundRoute):
                print("Error: Could not find route: {}".format(r))
                sys.exit()
            
        else:
            if(r >= len(routeNames.length)):
                print("Error: Route out of bounds: {}".format(r))
                sys.exit()
            else:
                self.route = r

    def getRoute(self):
        return self.routeNames[self.route]