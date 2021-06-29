# Skout - Flagfootball Scouting Analysis Tool
#   Copyright (C) 2021  Xaver Klemenschits
#   See LICENSE.txt for details

import drawSvg as draw
import Route
import copy

cairoAvalaible = True
try:
    import cairosvg
except OSError as e:
    cairoAvalaible = False
except ImportError as e:
    cairoAvalaible = False

class SkoutPage:
    drawingSize = (2480, 3508)
    drawingBorder = (474 / 2, 592 / 2)
    columns = 3
    rows = 5

    def __init__(self, playStats, writeSvg=not cairoAvalaible):
        self.stats = playStats
        self.d = draw.Drawing(*self.drawingSize)
        self.writeSvg = writeSvg

        # define static drawing objects
        self.arrowHead = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=4, orient='auto')
        # self.arrowHead.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))

    def listAsComma(self, listData):
        if(len(listData) == 0):
            return ""
        result = str(listData[0])
        for i in range(1, len(listData)):
            if(str(listData[i]) != ""):
                if(result != ""):
                    result = result + ","
                result = result + str(listData[i])
        return result

    def drawBackground(self):
        r = draw.Rectangle(0, 0, *self.drawingSize, fill='#ffffff')
        r.appendTitle("Background")
        self.d.append(r)

    def drawTitle(self):
        titleCenter = (self.drawingSize[0]/2, self.drawingSize[1] - self.drawingBorder[1])
        titleText = draw.Text('Skout Report', 100, *titleCenter, center=True, fill='black')
        self.d.append(titleText)

        # home and away teams
        homeText = draw.Text('Home: {}\nAway: {}'.format(self.stats.homeTeam, self.stats.awayTeam), 60, self.drawingSize[0]/4, titleCenter[1] - 120, fill='black')
        self.d.append(homeText)

        # Final Score and date
        dateText = draw.Text("Date: {}\nScore: {} - {}".format(self.stats.date, self.stats.score[0], self.stats.score[1]), 60, self.drawingSize[0]/2 + 200, titleCenter[1] - 120, fill='black')
        self.d.append(dateText)

        # return bottom coordinate of title block
        return titleCenter[1] - 180

    def triangleAroundCenter(self, center, edgeLength, colour):
        halfHeight = 3**0.5 * edgeLength / 4.
        x0 = (center[0], center[1] + halfHeight)
        x1 = (x0[0] - edgeLength/2, center[1] - 3**0.5 / 2 * halfHeight)
        x2 = (x0[0] + edgeLength/2, x1[1])
        triangle = draw.Lines(*x0, *x1, *x2, stroke_width=2, stroke='black', close=True, fill=colour)
        return triangle

    def drawPlay(self, x0, y0, x1, y1, index):
        # draw play Number
        self.d.append(draw.Text("#" + str(index+1), 30, x0, y1, font_weight='bold'))

        yard2Pixels = abs(y0 - y1) / 15. # the whole field are 15 yards
        sideLineBorder = 4 * yard2Pixels # routes are not allowed to extend further than 4 yds laterally

        centerLOS = (x0 + (x1 - x0) / 2., y0)
        RecALOS = (x0 + sideLineBorder, y0)
        RecDLOS = (x1 - sideLineBorder, y0)
        slotLOS = (centerLOS[0] + (RecDLOS[0] - centerLOS[0]) / 2., y0)
        LOSPositions = [RecALOS, centerLOS, slotLOS, RecDLOS]

        # draw the routes and players
        routeStrokeWidth = 10
        routeColors = ['red', 'green', 'orange', 'blue']
        
        for i in range(4):
            # Route
            routePoints = self.stats.routesList[index][i].getRoutePath()
            #define arrowHead for the route
            arrow = copy.deepcopy(self.arrowHead)
            arrow.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill=routeColors[i], close=True))
            # make path with arrowHead at the end
            p = draw.Path(stroke=routeColors[i], stroke_width=routeStrokeWidth, fill='none',
                    marker_end=arrow)
            # move to start position of player
            p.M(*LOSPositions[i])
            # lines according to route
            for j in range(len(routePoints)):
                xCoord = LOSPositions[i][0] + routePoints[j][0] * yard2Pixels
                yCoord = LOSPositions[i][1] + routePoints[j][1] * yard2Pixels
                if(i == 0 or i == 1): # invert x for A and C Receiver
                    xCoord = LOSPositions[i][0] - routePoints[j][0] * yard2Pixels
                # move path by making line
                p.L(xCoord, yCoord)
            # add path
            self.d.append(p)

            # draw the player
            if(i == 1): # for the center, draw a triangle
                self.d.append(self.triangleAroundCenter(centerLOS, 40, routeColors[i]))
            else:
                self.d.append(draw.Circle(*LOSPositions[i], 15, stroke_width=2, stroke='black', close=True, fill=routeColors[i]))

    # x0, y0 are min coords and x1, y1 are max coords
    def drawTile(self, x0, y0, x1, y1, index):
        # print("Start: {}, {}".format(x0, y0))
        # print("End:   {}, {}".format(x1, y1))
        # total number of plays in list
        numberOfPlays = len(self.stats.routesList)

        # draw border around this play
        border = draw.Lines(x0, y0, x1, y0, x1, y1, x0, y1, stroke='black', stroke_width=4, close=True, fill='none')
        border.appendTitle("PlayBorder")
        self.d.append(border)

        # area just for drawing the play
        drawArea = (x1 - x0, (y1 - y0) / 3 * 2)
        # draw LOS
        self.d.append(draw.Line(x0, y1 - drawArea[1], x1, y1 - drawArea[1], stroke_width=2, stroke="black"))

        # print stats
        statsBorder = 10
        statsBegin = (x0 + statsBorder, y1 - drawArea[1] - statsBorder)
        statsTextSize = 30

        # down counters
        downCountX = statsBegin[0] + 80
        downCountersText = ("1st:", "2nd:", "3rd:", "4th:", "PAT:")
        for i in range(len(downCountersText)):
            self.d.append(draw.Text(downCountersText[i], statsTextSize, statsBegin[0], statsBegin[1] - i * statsTextSize, fill='black', valign='top'))
            if (index < numberOfPlays):
                self.d.append(draw.Text(str(self.stats.downStats[index][i]), statsTextSize, downCountX, statsBegin[1] - i * statsTextSize, fill='black', valign='top'))

        # 2nd stats column: total and strong sides
        column2X = downCountX + 80
        column2ValueX = column2X + 160
        #total
        self.d.append(draw.Text("Total:", statsTextSize, column2X, statsBegin[1], fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(str(self.stats.occurences[index]), statsTextSize, column2ValueX, statsBegin[1], fill='black', valign='top'))
        #strongsides
        self.d.append(draw.Text("SS left:", statsTextSize, column2X, statsBegin[1] - statsTextSize, fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(str(self.stats.strongSides[index][0]), statsTextSize, column2ValueX, statsBegin[1] - statsTextSize, fill='black', valign='top'))
        self.d.append(draw.Text("SS right:", statsTextSize, column2X, statsBegin[1] - 2*statsTextSize, fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(str(self.stats.strongSides[index][1]), statsTextSize, column2ValueX, statsBegin[1] - 2*statsTextSize, fill='black', valign='top'))
        
        # clipNumbers
        self.d.append(draw.Text("vid#:", statsTextSize, column2X, statsBegin[1] - 4*statsTextSize, fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(self.listAsComma(self.stats.clipNumbers[index]), statsTextSize, column2X + 100, statsBegin[1] - 4*statsTextSize, fill='black', valign='top'))

        # 3rd statistics columns
        column3X = column2ValueX + 50
        column3ValueX = column3X + 100
        # distance
        self.d.append(draw.Text("Dist:", statsTextSize, column3X, statsBegin[1], fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(str(self.listAsComma(self.stats.distances[index])), statsTextSize, column3ValueX, statsBegin[1], fill='black', valign='top'))
        # progression
        self.d.append(draw.Text("Yds:", statsTextSize, column3X, statsBegin[1]- statsTextSize, fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(str(self.listAsComma(self.stats.progressions[index])), statsTextSize, column3ValueX, statsBegin[1]- statsTextSize, fill='black', valign='top'))
        # intended receiver
        self.d.append(draw.Text("Rec:", statsTextSize, column3X, statsBegin[1] - 2*statsTextSize, fill='black', valign='top'))
        if (index < numberOfPlays):
            self.d.append(draw.Text(str(self.listAsComma(self.stats.intRecs[index])), statsTextSize, column3ValueX, statsBegin[1] - 2*statsTextSize, fill='black', valign='top'))

        # formations
        formationsY = statsBegin[1] + 2*statsBorder
        if (index < numberOfPlays):
            self.d.append(draw.Text("Formations: " + self.listAsComma(self.stats.formations[index]), statsTextSize, statsBegin[0], formationsY, fill='black'))
        # self.d.append(draw.Text(str(self.stats.getFormations(index)), statsTextSize, statsBegin[0] + 200, formationsY, fill='black'))

        

        # draw the play itself
        playBorder = 60
        lowCorner = (x0 + playBorder, formationsY + playBorder)
        topCorner = (x1 - playBorder, y1 - playBorder)

        # draw LOS
        self.d.append(draw.Line(*lowCorner, topCorner[0], lowCorner[1], stroke_width=3, stroke="black"))

        yard2Pixels = abs(lowCorner[1] - topCorner[1]) / 15. # the whole field are 15 yards
        # 5yd and 10yd lines
        fiveYards = 5 * yard2Pixels
        tenYards = 10 * yard2Pixels
        self.d.append(draw.Line(lowCorner[0], lowCorner[1] + fiveYards, topCorner[0], lowCorner[1] + fiveYards, stroke_width=2, stroke="gray"))
        self.d.append(draw.Line(lowCorner[0], lowCorner[1] + tenYards, topCorner[0], lowCorner[1] + tenYards, stroke_width=2, stroke="gray"))
        self.d.append(draw.Text("5", 30, topCorner[0], lowCorner[1] + fiveYards, valign='middle'))
        self.d.append(draw.Text("10", 30, topCorner[0], lowCorner[1] + tenYards, valign='middle'))

        # if there are still plays left to display, draw them
        if (index < numberOfPlays):
            self.drawPlay(*lowCorner, *topCorner, index)

    def makePage(self, pageNumber=None):
        # set range of plays for this page
        startIndex = 0
        if(pageNumber is not None and pageNumber>0):
            startIndex = (pageNumber-1) * self.columns * self.rows

        # Background
        self.drawBackground()

        # Title
        titleBottom = self.drawTitle()

        # draw tiles to contain the plays
        tilesStart = (self.drawingBorder[0], titleBottom - 60)
        tilesEnd = (self.drawingSize[0] - self.drawingBorder[0], self.drawingBorder[1])
        tileWidth = abs(tilesEnd[0] - tilesStart[0]) / self.columns
        tileHeight = abs(tilesEnd[1] - tilesStart[1]) / self.rows

        # draw all tiles
        for i in range(self.rows):
            for j in range(self.columns):
                self.drawTile(tilesStart[0] + j * tileWidth, tilesStart[1] - (i+1) * tileHeight,
                                tilesStart[0] + (j+1) * tileWidth, tilesStart[1] - i * tileHeight, startIndex + i * self.columns + j)

        self.d.setPixelScale(1)  # Set number of pixels per geometry unit
        #d.setRenderSize(400,200)  # Alternative to setPixelScale
        fileName = self.stats.homeTeam + "_v_" + self.stats.awayTeam + "-" + self.stats.date.replace(".", "_")
        if(pageNumber is not None):
            fileName = fileName + "_" + str(pageNumber)

        # write PDF if cairoSvg is available
        if cairoAvalaible:
            cairosvg.svg2pdf(bytestring=self.d.asSvg(), write_to=fileName + ".pdf")
            print("Wrote Skout to file \'{}\'".format(fileName + ".pdf"))
        if self.writeSvg:
            self.d.saveSvg(fileName + ".svg")
            print("Wrote Skout to file \'{}\'".format(fileName + ".svg"))