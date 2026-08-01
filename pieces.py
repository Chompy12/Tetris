class Piece():
    def __init__(self, offsets:list):
        # Offsets must be a list of tuples of ints
        self.offsets = offsets

    def rotate_left(self):
        new_offsets = []
        for offset in self.offsets:
            new_offsets.append((-offset[1], offset[0]))
        self.offsets = new_offsets

    def rotate_right(self):
        new_offsets = []
        for offset in self.offsets:
            new_offsets.append((offset[1], -offset[0]))
        self.offsets = new_offsets

    def set_offsets(self, new_offsets):
        self.offsets = new_offsets