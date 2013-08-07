from collections import OrderedDict
from exceptions import ReaderError
import llrp_proto as llrp

################################################################################

class Reader (object):
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

################################################################################

class ImpinjReader (Reader):
    connection = None

    def __init__ (self, hostname):
        super(ImpinjReader, self).__init__()
        self.reader_type = Reader.READER_IMPINJ
        self.hostname = hostname
        self.connection = None

    def inventory (self, cycles=1):
        """Run N cycles of inventory"""
        return ()

    def connect (self):
        try:
            self.connection = llrp.LLRPdConnection(self.hostname)
            self.connected = True
        except llrp.LLRPResponseError, ret:
            raise ReaderError(ret)

    def disconnect (self):
        if self.connection:
            self.connection.close()
            self.connected = False

################################################################################

class GnuRadioReader (Reader):
    def __init__ (self):
        super(GnuRadioReader, self).__init__()
        self.reader_type = READER_GNURADIO

    def inventory (self):
        """Run N cycles of inventory"""
        return ()

    def connect (self):
        self.connected = True

    def disconnect (self):
        self.connected = False

class ReaderCollection (OrderedDict):
    """A collection of readers, to be operated on collectively."""
    def __init__ (self):
        super(ReaderCollection, self).__init__()

################################################################################

def ping (args):
    host = args.host
    reader = ImpinjReader(host)
    try:
        print 'Connecting to {}...'.format(host)
        reader.connect()
        print 'Connected.'
        print 'Disconnecting...'
        reader.disconnect()
        print 'Disconnected.'
    except ReaderError, err:
        print 'Reader error: %s'

def inventory (args):
    raise NotImplementedError()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='RFID reader')
    parser.add_argument('host', help='Hostname or IP address of reader')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_ping = subparsers.add_parser('ping', help='ping help')
    parser_ping.set_defaults(func=ping)
    parser_inventory = subparsers.add_parser('inventory', help='inventory help')
    parser_inventory.set_defaults(func=inventory)
    args = parser.parse_args()
    args.func(args)
