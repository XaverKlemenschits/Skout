# Definition of RouteTree class
import sys
class Route:
    routeNames = ["Stop",           # 0
                  "Quick Out",      # 1
                  "Slant",          # 2
                  "Comeback Out",   # 3
                  "Comeback In",    # 4
                  "10 Out",         # 5
                  "10 In",          # 6
                  "Corner",         # 7
                  "Post",           # 8
                  "Go",             # 9
                  "5 In",           # 10
                  "5 Out",          # 11
                  "Pivot",          # 12
                  "Post-Corner",    # 13
                  "Reverse",        # 14
                  "Quick In"        # 15
                  ]

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
            if(r >= len(self.routeNames)):
                print("Error: Route out of bounds: {}".format(r))
                sys.exit()
            else:
                self.route = r

    def getRoute(self):
        return self.routeNames[self.route]

    def __str__(self):
        return self.routeNames[self.route]

class RouteList:
    numberOfRoutes = 4

    def __init__(self, routes=[]):
        if(len(routes) != self.numberOfRoutes):
            print("Warning: RouteList must have exactly 4 routes!")

        if(type(routes[0]) != Route):
            self.routes = []
            for i in range(self.numberOfRoutes):
                self.routes.append(Route(routes[i]))
        else:
            self.routes = routes

    def __lt__(self, other):
        for i in range(self.numberOfRoutes):
            if(self.routes[i].route < other[i].route):
                return True
            elif(self.routes[i].route > other[i].route):
                return False
        
        return False

    def __eq__(self, other):
        for i in range(self.numberOfRoutes):
            if(self.routes[i].route != other[i].route):
                return False
        return True

    def __str__(self):
        outputStr = "["
        for i in range(len(self.routes)-1):
            outputStr = outputStr + str(self.routes[i]) + ", "
        outputStr = outputStr + str(self.routes[self.numberOfRoutes-1]) +  "]"
        return outputStr

    def __getitem__(self, i):
        return self.routes[i]