class Artesao(object):

    def __init__(self, id, ociosity=False, time_ociosity, start_ociosity):
        self.id = id
        self.ociosity = ociosity
        self.time_ociosity = time_ociosity
        self.start_ociosity = start_ociosity

    def setId(self, id):
        self.id = id

    def setOciosity(self, ociosity):
        self.ociosity = ociosity

    def setTimeOciosity(self, time_ociosity):
        self.time_ociosity = time_ociosity

    def setStartOciosity(self, start_ociosity):
        self.start_ociosity = start_ociosity

    def getId(self):
        return self.id

    def getOciosity(self):
        return self.ociosity

    def getTimeOciosity(self):
        return self.time_ociosity

    def getStartOciosity(self):
        return self.start_ociosity

