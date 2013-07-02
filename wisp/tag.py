from collections import OrderedDict

class Tag:
    tagid = None
    epc = None
    readers = {}

    def __init__ (self):
        pass

    def appear (self, reader):
        self.readers[reader] = datetime.utcnow()

class TagCollection (OrderedDict):
    def __init__ (self):
        super(TagCollection, self).__init__()
