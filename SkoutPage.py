# Skout - Flagfootball Scouting Analysis Tool
#   Copyright (C) 2021  Xaver Klemenschits
#   See LICENSE.txt for details

#import drawSvg as draw
from os import stat
from reportlab.pdfgen import canvas
from reportlab.graphics.charts.textlabels import _text2Path
import copy
from collections import Counter


class SkoutPage:
    drawingSize = (2480, 3508)
    drawingBorder = (474 / 2, 592 / 2)
    columns = 3
    rows = 5
    font = 'Ubuntu'
    boldFont = 'Ubuntu-Bold'

    def __init__(self, playStats, outputName):
        self.stats = playStats
        self.d = canvas.Canvas(
            filename=outputName, pagesize=self.drawingSize, bottomup=1, initialFontName='Ubuntu')
        self.d.setTitle(self.stats.awayTeam + " at " + self.stats.homeTeam)
        self.d.setAuthor("Skout - Copyright (C) Xaver Klemenschits")
        self.d.setSubject("American Football Scout Report")

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

    def listAsCount(self, listData):
        if(len(listData) == 0):
            return ""
        # remove empty elems from list str_list = list(filter(None, str_list))
        # generate count of appearance in list
        listData = Counter(listData)
        result = []
        for elem in listData:
            result.append(str(listData[elem]) + "x")
            if elem == "":
                result[-1] += "Spread"
            else:
                result[-1] += str(elem)

        return self.listAsComma(result)

    def getTextBounds(self, text, size, font=None):
        '''
        This function returns the size of the passed text,
        when drawn as (x-extent, y-extent)
        '''
        if font is None:
            font = self.font
        p = _text2Path(text, fontName=font, fontSize=size)
        bounds = p.getBounds()
        return (bounds[2] - bounds[0], bounds[3] - bounds[1])

    def drawBackground(self):
        self.d.setFillColor('white')
        self.d.rect(0, 0, *self.drawingSize, stroke=0, fill=1)

    def drawTitle(self):
        coords = (self.drawingSize[0]/2,
                  self.drawingSize[1] - self.drawingBorder[1])
        self.d.setFillColor('black')
        self.d.setFontSize(100)
        self.d.drawCentredString(*coords, 'Skout Report')

        # home and away teams
        fontSize = 60
        textAlignLeft = self.drawingSize[0] / 6
        textAlignTop = coords[1] - 2 * fontSize

        coords = [textAlignLeft, textAlignTop]
        self.d.setFontSize(fontSize)
        # home
        self.d.drawString(*coords, 'Home:')
        coords[0] = coords[0] + 4 * fontSize
        self.d.drawString(*coords, self.stats.homeTeam)
        # away
        coords = [textAlignLeft, coords[1] - 1.1 * fontSize]
        self.d.drawString(*coords, 'Away:')
        coords[0] = coords[0] + 4 * fontSize
        self.d.drawString(*coords, self.stats.awayTeam)

        # Final Score and date
        textAlignLeft = self.drawingSize[0] * 5 / 6 - 10 * fontSize
        coords = [textAlignLeft, textAlignTop]
        # date
        self.d.drawString(*coords, 'Date:')
        coords[0] = coords[0] + 4 * fontSize
        self.d.drawString(*coords, self.stats.date)
        # score
        coords = [textAlignLeft, coords[1] - 1.1 * fontSize]
        self.d.drawString(*coords, 'Score:')
        coords[0] = coords[0] + 4 * fontSize
        self.d.drawString(*coords, '{} - {}'.format(*self.stats.score))

        # return bottom coordinate of title block
        return coords[1] - 60

    def triangleAroundCenter(self, center, edgeLength, colour):
        halfHeight = 3**0.5 * edgeLength / 4.
        x0 = (center[0], center[1] + halfHeight)
        x1 = (x0[0] - edgeLength/2, center[1] - 3**0.5 / 2 * halfHeight)
        x2 = (x0[0] + edgeLength/2, x1[1])
        # draw path
        path = self.d.beginPath()
        path.moveTo(*x0)
        path.lineTo(*x1)
        path.lineTo(*x2)
        path.close()
        # set up style
        self.d.setLineWidth(2)
        self.d.setStrokeColor('black')
        self.d.setFillColor(colour)
        # draw path
        self.d.drawPath(path, stroke=1, fill=1)

    def L2Norm(self, normal):
        sum = (normal[0]**2 + normal[1]**2)**0.5
        return [i / sum for i in normal]

    def makeRouteArrow(self, origin, nodes, arrowLength=15):
        arrowPath = [[-arrowLength/2., -0.1],
                     [0, arrowLength], [arrowLength/2., -0.1]]

        p = self.d.beginPath()
        p.moveTo(*origin)
        for j in range(len(nodes)):
            p.lineTo(nodes[j][0], nodes[j][1])
        self.d.drawPath(p)

        # draw arrow head
        normal = [nodes[-1][0] - origin[0], nodes[-1][1] - origin[1]]
        if (len(nodes) > 1):
            normal = [normal[0] - nodes[-2][0] + origin[0],
                      normal[1] - nodes[-2][1] + origin[1]]

        # normalize normal
        normal = self.L2Norm(normal)
        cosine = normal[1]
        sine = -normal[0]

        arrowPath = [[x * cosine - y * sine, x * sine + y * cosine]
                     for [x, y] in arrowPath]
        p = self.d.beginPath()
        p.moveTo(*nodes[-1])
        for coord in arrowPath:
            p.lineTo(nodes[-1][0] + coord[0], nodes[-1][1] + coord[1])
        p.close()
        self.d.drawPath(p, fill=1)

    def drawPlay(self, x0, y0, x1, y1, index):
        # draw play Number
        playNumberSize = 30
        self.d.setFont(self.boldFont, playNumberSize)
        self.d.setStrokeColor('black')
        self.d.setFillColor('black')
        self.d.drawString(x0, y1, '#' + str(index + 1))
        self.d.setFont(self.font, playNumberSize)
        self.d.drawString(x0 + (len(str(index + 1)) + 0.5) * playNumberSize, y1, self.listAsComma(self.stats.notes[index]))

        yard2Pixels = abs(y0 - y1) / 15.  # the whole field are 15 yards
        # routes are not allowed to extend further than 4 yds laterally
        sideLineBorder = 4 * yard2Pixels

        centerLOS = (x0 + (x1 - x0) / 2., y0)
        RecALOS = (x0 + sideLineBorder, y0)
        RecDLOS = (x1 - sideLineBorder, y0)
        slotLOS = (centerLOS[0] + (RecDLOS[0] - centerLOS[0]) / 2., y0)
        LOSPositions = [RecALOS, centerLOS, slotLOS, RecDLOS]

        # draw the routes and players
        routeStrokeWidth = 8
        routeColors = ['red', 'green', 'orange', 'blue']

        for i in range(4):
            # Route
            routePoints = copy.deepcopy(
                self.stats.routesList[index][i].getRoutePath())
            self.d.setFillColor(routeColors[i])
            self.d.setStrokeColor(routeColors[i])
            self.d.setLineWidth(routeStrokeWidth)

            if (i == 0 or i == 1):  # invert x for A and C Receiver
                routePoints = [[-x, y] for [x, y] in routePoints]

            routePoints = [[LOSPositions[i][0] + x * yard2Pixels,
                            LOSPositions[i][1] + y * yard2Pixels] for [x, y] in routePoints]

            self.makeRouteArrow(LOSPositions[i], routePoints, 15)

            # draw the player
            self.d.setStrokeColor('black')
            if(i == 1):  # for the center, draw a triangle
                self.triangleAroundCenter(centerLOS, 40, routeColors[i])
                # self.d.append(self.triangleAroundCenter(centerLOS, 40, routeColors[i]))
            else:
                self.d.setLineWidth(2)
                self.d.circle(*LOSPositions[i], 15, fill=1)
                # self.d.append(draw.Circle(*LOSPositions[i], 15, stroke_width=2, stroke='black', close=True, fill=routeColors[i]))

    # x0, y0 are min coords and x1, y1 are max coords
    def drawTile(self, x0, y0, x1, y1, index):
        # print("Start: {}, {}".format(x0, y0))
        # print("End:   {}, {}".format(x1, y1))
        # total number of plays in list
        numberOfPlays = len(self.stats.routesList)

        # draw border around this play
        self.d.setLineWidth(6)
        self.d.setStrokeColor('black')
        self.d.setFillColor('black')
        self.d.rect(x0, y0, x1 - x0, y1 - y0)

        # area just for drawing the play
        drawArea = (x1 - x0, (y1 - y0) / 3 * 2)
        # draw stats separator
        self.d.line(x0, y1 - drawArea[1], x1, y1 - drawArea[1])
        # self.d.append(draw.Line(x0, y1 - drawArea[1], x1, y1 - drawArea[1], stroke_width=2, stroke="black"))

        # print stats
        statsBorder = 10
        statsBegin = (x0 + statsBorder, y1 - drawArea[1] - statsBorder)
        statsTextSize = 30
        statsTop = statsBegin[1] - statsTextSize / 1.5
        self.d.setFontSize(statsTextSize)

        # down counters
        downCountX = statsBegin[0] + 80
        downCountersText = ("1st:", "2nd:", "3rd:", "4th:", "PAT:")

        for i in range(len(downCountersText)):
            self.d.setFont(self.boldFont, statsTextSize)
            self.d.drawString(
                statsBegin[0], statsTop - i * statsTextSize, downCountersText[i])
            if (index < numberOfPlays):
                self.d.setFont(self.font, statsTextSize)
                self.d.drawString(
                    downCountX, statsTop - i * statsTextSize, str(self.stats.downStats[index][i]))

        # 2nd stats column: total and strong sides
        column2X = downCountX + 80
        column2ValueX = column2X + 160
        # total
        self.d.setFont(self.boldFont, statsTextSize)
        self.d.drawString(column2X, statsTop, "Total:")
        if (index < numberOfPlays):
            self.d.setFont(self.font, statsTextSize)
            self.d.drawString(column2ValueX, statsTop,
                              str(self.stats.occurences[index]))

        # strongsides and clipnumbers
        self.d.setFont(self.boldFont, statsTextSize)
        self.d.drawString(column2X, statsTop - statsTextSize, "SS left:")
        self.d.drawString(column2X, statsTop - 2 * statsTextSize, "SS right:")

        self.d.drawString(column2X, statsTop - 4 * statsTextSize, "vid#:")

        if (index < numberOfPlays):
            self.d.setFont(self.font, statsTextSize)
            self.d.drawString(column2ValueX, statsTop - statsTextSize,
                              str(self.stats.strongSides[index][0]))
            self.d.drawString(column2ValueX, statsTop - 2 *
                              statsTextSize, str(self.stats.strongSides[index][1]))
            self.d.drawString(column2X + 3 * statsTextSize, statsTop - 4 *
                              statsTextSize, self.listAsComma(self.stats.clipNumbers[index]))

        # 3rd statistics columns
        column3X = column2ValueX + 50
        column3ValueX = column3X + 70
        # distance
        self.d.setFont(self.boldFont, statsTextSize)
        self.d.drawString(column3X, statsTop, "Dist:")
        self.d.drawString(column3X, statsTop - statsTextSize, "Yds:")
        self.d.drawString(column3X, statsTop - 2 * statsTextSize, "Rec:")
        if (index < numberOfPlays):
            self.d.setFont(self.font, statsTextSize)
            self.d.drawString(column3ValueX, statsTop,
                              self.listAsComma(self.stats.distances[index]))
            self.d.drawString(column3ValueX, statsTop - statsTextSize,
                              self.listAsComma(self.stats.progressions[index]))
            self.d.drawString(column3ValueX, statsTop - 2 * statsTextSize,
                              self.listAsComma(self.stats.intRecs[index]))

        # formations
        formationsY = statsBegin[1] + 2*statsBorder
        self.d.setFont(self.boldFont, statsTextSize)
        self.d.drawString(statsBegin[0], formationsY, "Form.:")
        if (index < numberOfPlays):
            self.d.setFont(self.font, statsTextSize)
            self.d.drawString(statsBegin[0] + 3.5 * statsTextSize,
                              formationsY, self.listAsCount(self.stats.formations[index]))

        # draw the play itself
        playBorder = 60
        lowCorner = (x0 + playBorder, formationsY + playBorder)
        topCorner = (x1 - playBorder, y1 - playBorder)

        # draw LOS
        self.d.setLineWidth(3)
        self.d.line(*lowCorner, topCorner[0], lowCorner[1])

        yard2Pixels = abs(lowCorner[1] - topCorner[1]) / \
            15.  # the whole field are 15 yards
        # 5yd and 10yd lines
        fiveYards = 5 * yard2Pixels
        tenYards = 10 * yard2Pixels

        self.d.setLineWidth(3)
        self.d.setStrokeColor('gray')
        self.d.line(lowCorner[0], lowCorner[1] + fiveYards,
                    topCorner[0], lowCorner[1] + fiveYards)
        self.d.line(lowCorner[0], lowCorner[1] + tenYards,
                    topCorner[0], lowCorner[1] + tenYards)

        halfFontSize = self.getTextBounds('5', statsTextSize)[1] / 2.
        distanceMarkerPadding = 1.5 * statsTextSize
        self.d.setFont(self.font, statsTextSize)
        self.d.setFillColor('gray')
        self.d.drawRightString(
            topCorner[0] + distanceMarkerPadding, lowCorner[1] + fiveYards - halfFontSize, '5')
        self.d.drawRightString(
            topCorner[0] + distanceMarkerPadding, lowCorner[1] + tenYards - halfFontSize, '10')

        # if there are still plays left to display, draw them
        if (index < numberOfPlays):
            self.drawPlay(*lowCorner, *topCorner, index)

    def makePage(self, pageNumber=None):
        # set range of plays for this page
        startIndex = 0
        if(pageNumber is not None and pageNumber > 0):
            startIndex = (pageNumber-1) * self.columns * self.rows

        # Background
        self.drawBackground()

        # Title
        titleBottom = self.drawTitle()

        # draw tiles to contain the plays
        tilesStart = (self.drawingBorder[0], titleBottom - 60)
        tilesEnd = (self.drawingSize[0] -
                    self.drawingBorder[0], self.drawingBorder[1])
        tileWidth = abs(tilesEnd[0] - tilesStart[0]) / self.columns
        tileHeight = abs(tilesEnd[1] - tilesStart[1]) / self.rows

        # draw all tiles
        for i in range(self.rows):
            for j in range(self.columns):
                self.drawTile(tilesStart[0] + j * tileWidth, tilesStart[1] - (i+1) * tileHeight,
                              tilesStart[0] + (j+1) * tileWidth, tilesStart[1] - i * tileHeight, startIndex + i * self.columns + j)

        # finish this page (a new one will only be created if additional drawing operations are performed)
        self.d.showPage()

    def savePDF(self):
        self.d.save()
