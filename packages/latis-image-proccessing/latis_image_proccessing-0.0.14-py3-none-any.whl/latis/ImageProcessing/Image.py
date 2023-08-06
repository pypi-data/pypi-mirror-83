class Image(object):

    def __init__(self, pixelData, cols, rows, dataset):
        self.pixelData = pixelData
        self.height = cols
        self.width = rows
        self.dataset = dataset
