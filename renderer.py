from gi.repository import GdkPixbuf
import itertools
from constants import WALL_TILE

class Renderer:
    def __init__(self, rhs, tilewidth, tileheight, texturemanager):
        self.texturemanager = texturemanager
        self.pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, tilewidth * 24, tileheight * 24)
        self.tilewidth = tilewidth
        self.tileheight = tileheight
        self.walls = {}
        for (x,y) in itertools.product(range(tilewidth), range(tileheight)):
            if rhs is not None and (x,y) in rhs.walls:
                self.walls[(x,y)] = rhs.walls[(x,y)]
            else:
                self.walls[(x,y)] = WALL_TILE
        for (x,y) in itertools.product(range(tilewidth), range(tileheight)):
            self.update(x, y)

    def update(self, x, y):
        coords = {}
        for (i,j) in itertools.product(range(-1, 2), range(-1, 2)):
            coords[(i,j)] = self.getTile(x + i, y + j)
        self.texturemanager.getPixbuf(coords).copy_area(0, 0, 24, 24, self.pixbuf, x * 24, y * 24)

    def getTile(self, x, y):
        if (x,y) in self.walls:
            return self.walls[(x,y)]
        else:
            return WALL_TILE

    def setTile(self, x, y, tile):
        self.walls[(x,y)] = tile
        for (i,j) in itertools.product(
                range(max(0, x - 1), min(self.tilewidth, x + 2)),
                range(max(0, y - 1), min(self.tileheight, y + 2))):
            self.update(i,j)

    def getPixbuf(self):
        return self.pixbuf

