from collections import OrderedDict

class Reader:
    hostname = None
    location = None
    connected = False

    READER_IMPINJ = 1
    READER_GNURADIO = 2
    reader_type = None

    def __init__ (self):
        pass

    def inventory (self):
        raise NotImplementedError("Abstract reader; use a subclass from "
                "wisp.reader instead.")

    def connect (self):
        raise NotImplementedError("Abstract reader; use a subclass from "
                "wisp.reader instead.")

class ImpinjReader (Reader):
    def __init__ (self):
        super(ImpinjReader, self).__init__()
        self.reader_type = READER_IMPINJ

    def inventory (self):
        return ()

    def connect (self):
        self.connected = True

    def disconnect (self):
        self.connected = True

class GnuRadioReader (Reader):
    def __init__ (self):
        super(GnuRadioReader, self).__init__()
        self.reader_type = READER_GNURADIO

    def inventory (self):
        return ()

    def connect (self):
        self.connected = True

    def disconnect (self):
        self.connected = False

class ReaderCollection (OrderedDict):
    def __init__ (self):
        super(ReaderCollection, self).__init__()
