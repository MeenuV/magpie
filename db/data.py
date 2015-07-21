class MagpieData(object):
    def __init__(self, url, metadata=None):
        self.url = url
        if(metadata is not None):
            self.metadata = str(metadata._row[0])
        else:
            self.metadata = metadata
