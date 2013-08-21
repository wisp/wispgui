from __future__ import print_function
import logging
import sys
import time
from collections import OrderedDict
from wisp.exceptions import ReaderError
import llrp_proto as llrp

logger = logging.getLogger('wisp.reader')
logger.addHandler(logging.NullHandler())

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

    def disconnect (self):
        raise NotImplementedError("Abstract reader; use a subclass from "
                "wisp.reader instead.")

    def reset (self):
        raise NotImplementedError("Abstract reader; use a subclass from "
                "wisp.reader instead.")


################################################################################

class ImpinjReader (Reader):
    connection = None
    timeout = None

    def __init__ (self, hostname, timeout=None):
        super(ImpinjReader, self).__init__()
        self.reader_type = Reader.READER_IMPINJ
        self.hostname = hostname
        self.connection = None
        if timeout:
            self.timeout = timeout

    def inventory (self, cycles=1):
        """Run N cycles of inventory"""
        if not self.connected:
            raise ReaderError('Not connected')
        c = self.connection

        c.delete_all_rospec()
        inventory_rospec = llrp.LLRPROSpec(1)
        inventory_rospec.add(c)
        inventory_rospec.enable(c)
        inventory_rospec.start(c)
        # XXX what to do here?
        inventory_rospec.stop(c)
        inventory_rospec.disable(c)
        inventory_rospec.delete(c)

        return (1, 2, 3)

    def reset (self):
        try:
            self.connect()
            self.connection.delete_all_rospec()
            self.disconnect()
        except llrp.LLRPResponseError as ret:
            raise ReaderError(ret)

    def connect (self):
        try:
            self.connection = llrp.LLRPdConnection(self.hostname,
                timeout=self.timeout)
            self.connected = True
        except llrp.LLRPResponseError as ret:
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

    def reset ():
        self.connect()
        # XXX reset reader state
        self.disconnect()

class ReaderCollection (OrderedDict):
    """A collection of readers, to be operated on collectively."""
    def __init__ (self):
        super(ReaderCollection, self).__init__()

################################################################################

def ping (args):
    for host in args.host:
        reader = ImpinjReader(host, timeout=args.timeout)
        try:
            logger.info('Connecting to {}...'.format(host))
            reader.connect()
            logger.info('Connected.')
            logger.info('Disconnecting...')
            reader.disconnect()
            logger.info('Disconnected.')
        except ReaderError as err:
            logger.error('Reader error: %s')

def inventory (args):
    for host in args.host:
        reader = ImpinjReader(host, timeout=args.timeout)
        try:
            logger.info('Connecting to {}...'.format(host))
            reader.connect()
            logger.info('Connected.')

            print(reader.inventory())

            logger.info('Disconnecting...')
            reader.disconnect()
            logger.info('Disconnected.')
        except ReaderError as err:
            logger.error('Reader error: %s')

def reset (args):
    for host in args.host:
        reader = ImpinjReader(host, timeout=args.timeout)
        try:
            logger.info('Connecting to {}...'.format(host))
            reader.connect()
            logger.info('Connected.')

            reader.reset()

            logger.info('Disconnecting...')
            reader.disconnect()
            logger.info('Disconnected.')
        except ReaderError as err:
            logger.error('Reader error: {}'.format(err))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='RFID reader')
    parser.add_argument('-d', '--debug', action='store_true',
        help='Show debugging output')
    parser.add_argument('--timeout', metavar='SECONDS', type=int, default=10,
        help='Timeout for socket operations')
    subparsers = parser.add_subparsers(help='sub-command help')

    parser_ping = subparsers.add_parser('ping', help='ping help')
    parser_ping.add_argument('host', nargs='+',
        help='Hostname or IP address of reader')
    parser_ping.set_defaults(func=ping)

    parser_inventory = subparsers.add_parser('inventory', help='inventory help')
    parser_inventory.add_argument('host', nargs='+',
        help='Hostname or IP address of reader')
    parser_inventory.set_defaults(func=inventory)

    parser_reset = subparsers.add_parser('reset', help='reset help')
    parser_reset.add_argument('host', nargs='+',
        help='Hostname or IP address of reader')
    parser_reset.set_defaults(func=reset)

    args = parser.parse_args()

    logging.basicConfig(level=args.debug and logging.DEBUG or logging.INFO)

    # dispatch the actual command
    args.func(args)
