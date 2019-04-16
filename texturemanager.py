from gi.repository import GdkPixbuf

bearings = [
        (( 0, -1), 10000000), # NORTH
        (( 1, -1), 1000000),
        (( 1,  0), 100000), # EAST
        (( 1,  1), 10000),
        (( 0,  1), 1000), # SOUTH
        ((-1,  1), 100),
        ((-1,  0), 10), # WEST
        ((-1, -1), 1)
    ]

class TextureManager:
    def __init__(self, folder):
        self.folder = folder
        self.cache = {0: {}, 1: {}}

    def getPixbuf(self, coords):
        tileid = 0
        for b in bearings:
            if 0 in b[0] and coords[b[0]] == 1:
                tileid += b[1]
            else:
                for i in [b[0], (b[0][0], 0), (0, b[0][1])]:
                    if coords[i] != 1:
                        break
                else:
                    tileid += b[1]
        tileid = str(tileid).zfill(8)
        return self.getFromCache(coords[(0,0)], tileid)

    def getFromCache(self, tiletype, tileid):
        if tileid not in self.cache[tiletype]:
            self.cache[tiletype][tileid] = GdkPixbuf.Pixbuf.new_from_file(self.folder + '/' + str(tiletype) + '/' + tileid + '.png')
        return self.cache[tiletype][tileid]

