import Queue
import datetime.datetime

class Tag:
    self.tagid = None
    self.epc = None
    self.readers = {}

    def __init__ (self):
        pass

    def appear (self, reader):
        self.readers[reader] = datetime.utcnow()
