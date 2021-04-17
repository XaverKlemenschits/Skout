import drawSvg as draw
import Route

class SkoutPage:
    drawingSize = (2480, 3508)
    drawingBorder = (474 / 2, 592 / 2)
    columns = 3
    rows = 5

    def __init__(self, playStats):
        self.stats = playStats
        self.d = draw.Drawing(*self.drawingSize)

        # define static drawing objects
        self.arrowHead = draw.Marker(-0.1, -0.5, 0.9, 0.5, scale=4, orient='auto')
        self.arrowHead.append(draw.Lines(-0.1, -0.5, -0.1, 0.5, 0.9, 0, fill='black', close=True))

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

    # x0, y0 are min coords and x1, y1 are max coords
    def drawTile(self, x0, y0, x1, y1):
        print("Start: {}, {}".format(x0, y0))
        print("End:   {}, {}".format(x1, y1))
        # draw border around this play
        border = draw.Lines(x0, y0, x1, y0, x1, y1, x0, y1, stroke='black', stroke_width=4, close=True, fill='none')
        border.appendTitle("PlayBorder")
        self.d.append(border)

        # area just for drawing the play
        drawArea = (x1 - x0, (y0 - y1) / 3 * 2)
        # draw LOS
        # print("LOS: {}".format(drawArea[1]))
        self.d.append(draw.Line(x0, y0 - drawArea[1], x1, y0 - drawArea[1], stroke_width=2, stroke="black"))

        # # print stats
        # self.d.append(draw.Text("I: ".format(), 12, x, y, fill='black')) # TODO

    def draw(self):
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
        for i in range(self.columns):
            for j in range(self.rows):
                self.drawTile(tilesStart[0] + i * tileWidth, tilesStart[1] - j * tileHeight,
                                tilesStart[0] + (i+1) * tileWidth, tilesStart[1] - (j+1) * tileHeight)
        # self.drawTile(1200, 1000, 2000, 2000)
        
        p = draw.Path(stroke='red', stroke_width=10, fill='none',
                    marker_end=self.arrowHead)  # Add an arrow to the end of a path
        p.M(1000, 400).L(1000, 800)#.L(0, -20)  # Chain multiple path operations
        self.d.append(p)
        self.d.append(draw.Lines(30, 20, 700, 500, 1200, 500,
                    stroke='red', stroke_width=2, fill='none',
                    marker_end=self.arrowHead))  # Add an arrow to the end of a line

        self.d.setPixelScale(1)  # Set number of pixels per geometry unit
        #d.setRenderSize(400,200)  # Alternative to setPixelScale
        self.d.saveSvg('example.svg')

# page = skoutPage("homeTeam", "awayTeam", "01.01.2020", (13, 27))
# page.draw()