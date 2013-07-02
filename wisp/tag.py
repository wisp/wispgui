import Queue
import datetime.datetime

class Tag:
    tagid = None
    epc = None
    readers = {}

    def __init__ (self):
        pass

    def appear (self, reader):
        self.readers[reader] = datetime.utcnow()
