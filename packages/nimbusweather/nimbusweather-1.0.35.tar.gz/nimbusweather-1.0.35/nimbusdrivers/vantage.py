#
#    Copyright (c) 2009-2015 Tom Keffer <tkeffer@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""Classes and functions for interfacing with a Davis VantagePro, VantagePro2,
or VantageVue weather station"""

from __future__ import with_statement

import datetime
import struct
import sys
import time
import logging

from nimbusdrivers import *
from functools import reduce

DRIVER_NAME = 'Vantage'
DRIVER_VERSION = '3.0'


def loader(config_dict):
    return Vantage(**config_dict[DRIVER_NAME])


_table = [
    0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50a5, 0x60c6, 0x70e7,  # 0x00
    0x8108, 0x9129, 0xa14a, 0xb16b, 0xc18c, 0xd1ad, 0xe1ce, 0xf1ef,  # 0x08
    0x1231, 0x0210, 0x3273, 0x2252, 0x52b5, 0x4294, 0x72f7, 0x62d6,  # 0x10
    0x9339, 0x8318, 0xb37b, 0xa35a, 0xd3bd, 0xc39c, 0xf3ff, 0xe3de,  # 0x18
    0x2462, 0x3443, 0x0420, 0x1401, 0x64e6, 0x74c7, 0x44a4, 0x5485,  # 0x20
    0xa56a, 0xb54b, 0x8528, 0x9509, 0xe5ee, 0xf5cf, 0xc5ac, 0xd58d,  # 0x28
    0x3653, 0x2672, 0x1611, 0x0630, 0x76d7, 0x66f6, 0x5695, 0x46b4,  # 0x30
    0xb75b, 0xa77a, 0x9719, 0x8738, 0xf7df, 0xe7fe, 0xd79d, 0xc7bc,  # 0x38
    0x48c4, 0x58e5, 0x6886, 0x78a7, 0x0840, 0x1861, 0x2802, 0x3823,  # 0x40
    0xc9cc, 0xd9ed, 0xe98e, 0xf9af, 0x8948, 0x9969, 0xa90a, 0xb92b,  # 0x48
    0x5af5, 0x4ad4, 0x7ab7, 0x6a96, 0x1a71, 0x0a50, 0x3a33, 0x2a12,  # 0x50
    0xdbfd, 0xcbdc, 0xfbbf, 0xeb9e, 0x9b79, 0x8b58, 0xbb3b, 0xab1a,  # 0x58
    0x6ca6, 0x7c87, 0x4ce4, 0x5cc5, 0x2c22, 0x3c03, 0x0c60, 0x1c41,  # 0x60
    0xedae, 0xfd8f, 0xcdec, 0xddcd, 0xad2a, 0xbd0b, 0x8d68, 0x9d49,  # 0x68
    0x7e97, 0x6eb6, 0x5ed5, 0x4ef4, 0x3e13, 0x2e32, 0x1e51, 0x0e70,  # 0x70
    0xff9f, 0xefbe, 0xdfdd, 0xcffc, 0xbf1b, 0xaf3a, 0x9f59, 0x8f78,  # 0x78
    0x9188, 0x81a9, 0xb1ca, 0xa1eb, 0xd10c, 0xc12d, 0xf14e, 0xe16f,  # 0x80
    0x1080, 0x00a1, 0x30c2, 0x20e3, 0x5004, 0x4025, 0x7046, 0x6067,  # 0x88
    0x83b9, 0x9398, 0xa3fb, 0xb3da, 0xc33d, 0xd31c, 0xe37f, 0xf35e,  # 0x90
    0x02b1, 0x1290, 0x22f3, 0x32d2, 0x4235, 0x5214, 0x6277, 0x7256,  # 0x98
    0xb5ea, 0xa5cb, 0x95a8, 0x8589, 0xf56e, 0xe54f, 0xd52c, 0xc50d,  # 0xA0
    0x34e2, 0x24c3, 0x14a0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,  # 0xA8
    0xa7db, 0xb7fa, 0x8799, 0x97b8, 0xe75f, 0xf77e, 0xc71d, 0xd73c,  # 0xB0
    0x26d3, 0x36f2, 0x0691, 0x16b0, 0x6657, 0x7676, 0x4615, 0x5634,  # 0xB8
    0xd94c, 0xc96d, 0xf90e, 0xe92f, 0x99c8, 0x89e9, 0xb98a, 0xa9ab,  # 0xC0
    0x5844, 0x4865, 0x7806, 0x6827, 0x18c0, 0x08e1, 0x3882, 0x28a3,  # 0xC8
    0xcb7d, 0xdb5c, 0xeb3f, 0xfb1e, 0x8bf9, 0x9bd8, 0xabbb, 0xbb9a,  # 0xD0
    0x4a75, 0x5a54, 0x6a37, 0x7a16, 0x0af1, 0x1ad0, 0x2ab3, 0x3a92,  # 0xD8
    0xfd2e, 0xed0f, 0xdd6c, 0xcd4d, 0xbdaa, 0xad8b, 0x9de8, 0x8dc9,  # 0xE0
    0x7c26, 0x6c07, 0x5c64, 0x4c45, 0x3ca2, 0x2c83, 0x1ce0, 0x0cc1,  # 0xE8
    0xef1f, 0xff3e, 0xcf5d, 0xdf7c, 0xaf9b, 0xbfba, 0x8fd9, 0x9ff8,  # 0xF0
    0x6e17, 0x7e36, 0x4e55, 0x5e74, 0x2e93, 0x3eb2, 0x0ed1, 0x1ef0   # 0xF8
]


def crc16(string, crc_start=0):
    """ Calculate CRC16 sum"""

    crc_sum = reduce(lambda crc, ch: (_table[(crc >> 8) ^ ord(ch)] ^ (crc << 8)) & 0xffff, string, crc_start)

    return crc_sum


# A few handy constants:
_ack = chr(0x06)
_resend = chr(0x15)  # NB: The Davis documentation gives this code as 0x21, but it's actually decimal 21

# ===============================================================================
#                           class BaseWrapper
# ===============================================================================


class BaseWrapper(object):
    """Base class for (Serial|Ethernet)Wrapper"""

    # ===============================================================================
    #          Primitives for working with the Davis Console
    # ===============================================================================

    def wakeup_console(self, max_tries=3, wait_before_retry=1.2):
        """Wake up a Davis Vantage console.

        If unsuccessful, an exception of type weewx.WakeupError is thrown"""

        # Wake up the console. Try up to max_tries times
        for unused_count in xrange(max_tries):
            try:
                # Clear out any pending input or output characters:
                self.flush_output()
                self.flush_input()
                # It can be hard to get the console's attention, particularly
                # when in the middle of a LOOP command. Send a whole bunch of line feeds.
                # Use separate calls, as this forces the WLIP implementation to invoke the
                # tcp_send_delay between each one.
                self.write('\n')
                self.write('\n')
                self.write('\n')
                time.sleep(0.5)
                # Now flush everything, do it again, then look for the \n\r acknowledgment
                self.flush_input()
                self.write('\n')
                _resp = self.read(2)
                if _resp == '\n\r':
                    logging.debug("vantage: successfully woke up console")
                    return
                print "Unable to wake up console... sleeping"
                time.sleep(wait_before_retry)
                print "Unable to wake up console... retrying"
            except WeeWxIOError:
                pass

        logging.error("vantage: Unable to wake up console")
        raise WakeupError("Unable to wake up Vantage console")

    def send_data(self, data):
        """Send data to the Davis console, waiting for an acknowledging <ACK>

        If the <ACK> is not received, no retry is attempted. Instead, an exception
        of type weewx.WeeWxIOError is raised

        data: The data to send, as a string"""

        self.write(data)

        # Look for the acknowledging ACK character
        _resp = self.read()
        if _resp != _ack:
            logging.error("vantage: No <ACK> received from console")
            raise WeeWxIOError("No <ACK> received from Vantage console")

    def send_data_with_crc16(self, data, max_tries=3):
        """Send data to the Davis console along with a CRC check, waiting for an acknowledging <ack>.
        If none received, resend up to max_tries times.

        data: The data to send, as a string"""

        # Calculate the crc for the data:
        _crc = crc16(data)

        # ...and pack that on to the end of the data in big-endian order:
        _data_with_crc = data + struct.pack(">H", _crc)

        # Retry up to max_tries times:
        for unused_count in xrange(max_tries):
            try:
                self.write(_data_with_crc)
                # Look for the acknowledgment.
                _resp = self.read()
                if _resp == _ack:
                    return
            except WeeWxIOError:
                pass

        logging.error("vantage: Unable to pass CRC16 check while sending data")
        raise CRCError("Unable to pass CRC16 check while sending data to Vantage console")

    def send_command(self, command, max_tries=3, wait_before_retry=1.2):
        """Send a command to the console, then look for the string 'OK' in the response.

        Any response from the console is split on \n\r characters and returned as a list."""

        for unused_count in xrange(max_tries):
            try:
                self.wakeup_console(max_tries=max_tries, wait_before_retry=wait_before_retry)

                self.write(command)
                # Takes a bit for the VP to react and fill up the buffer. Sleep for a half sec:
                time.sleep(0.5)
                # Can't use function serial.readline() because the VP responds with \n\r, not just \n.
                # So, instead find how many bytes are waiting and fetch them all
                nc = self.queued_bytes()
                _buffer = self.read(nc)
                # Split the buffer on the newlines
                _buffer_list = _buffer.strip().split('\n\r')
                # The first member should be the 'OK' in the VP response
                if _buffer_list[0] == 'OK':
                    # Return the rest:
                    return _buffer_list[1:]

            except WeeWxIOError:
                # Caught an error. Keep trying...
                continue

        logging.error("vantage: Max retries exceeded while sending command %s" % command)
        raise RetriesExceeded("Max retries exceeded while sending command %s" % command)

    def get_data_with_crc16(self, nbytes, prompt=None, max_tries=3):
        """Get a packet of data and do a CRC16 check on it, asking for retransmit if necessary.

        It is guaranteed that the length of the returned data will be of the requested length.
        An exception of type CRCError will be thrown if the data cannot pass the CRC test
        in the requested number of retries.

        nbytes: The number of bytes (including the 2 byte CRC) to get.

        prompt: Any string to be sent before requesting the data. Default=None

        max_tries: Number of tries before giving up. Default=3

        returns: the packet data as a string. The last 2 bytes will be the CRC"""
        if prompt:
            self.write(prompt)

        first_time = True

        for unused_count in xrange(max_tries):
            try:
                if not first_time:
                    self.write(_resend)
                _buffer = self.read(nbytes)
                if crc16(_buffer) == 0:
                    return _buffer
            except WeeWxIOError:
                pass
            first_time = False

        logging.error("vantage: Unable to pass CRC16 check while getting data")
        raise CRCError("Unable to pass CRC16 check while getting data")

# ===============================================================================
#                           class Serial Wrapper
# ===============================================================================


def guard_termios(fn):
    """Decorator function that converts termios exceptions into weewx exceptions."""
    # Some functions in the module 'serial' can raise undocumented termios
    # exceptions. This catches them and converts them to weewx exceptions.
    try:
        import termios

        def guarded_fn(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except termios.error as e:
                raise WeeWxIOError(e)
    except ImportError:
        def guarded_fn(*args, **kwargs):
            return fn(*args, **kwargs)
    return guarded_fn


class SerialWrapper(BaseWrapper):
    """Wraps a serial connection returned from package serial"""

    def __init__(self, port, baudrate, timeout):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    @guard_termios
    def flush_input(self):
        self.serial_port.flushInput()

    @guard_termios
    def flush_output(self):
        self.serial_port.flushOutput()

    @guard_termios
    def queued_bytes(self):
        return self.serial_port.inWaiting()

    def read(self, chars=1):
        import serial
        try:
            _buffer = self.serial_port.read(chars)
        except serial.serialutil.SerialException as e:
            logging.error("vantage: SerialException.")
            logging.error("   ****  %s" % e)
            logging.error("   ****  Is there a competing process running??")
            # Reraise as a Weewx error I/O error:
            raise WeeWxIOError(e)
        N = len(_buffer)
        if N != chars:
            raise WeeWxIOError("Expected to read %d chars; got %d instead" % (chars, N))
        return _buffer

    def write(self, data):
        N = self.serial_port.write(data)
        # Python version 2.5 and earlier returns 'None', so it cannot be used to test for completion.
        if N is not None and N != len(data):
            raise WeeWxIOError("Expected to write %d chars; sent %d instead" % (len(data), N))

    def openPort(self):
        import serial
        # Open up the port and store it
        self.serial_port = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
        logging.debug("vantage: Opened up serial port %s; baud %d; timeout %.2f" %
                      (self.port, self.baudrate, self.timeout))

    def closePort(self):
        try:
            # This will cancel any pending loop:
            self.wakeup_console(max_tries=1)
        except BaseException:
            pass
        self.serial_port.close()

# ===============================================================================
#                           class EthernetWrapper
# ===============================================================================


class EthernetWrapper(BaseWrapper):
    """Wrap a socket"""

    def __init__(self, host, port, timeout, tcp_send_delay):

        self.host = host
        self.port = port
        self.timeout = timeout
        self.tcp_send_delay = tcp_send_delay

    def openPort(self):
        import socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
        except (socket.error, socket.timeout, socket.herror) as ex:
            logging.error("vantage: Socket error while opening port %d to ethernet host %s." % (self.port, self.host))
            # Reraise as a weewx I/O error:
            raise WeeWxIOError(ex)
        except BaseException:
            logging.error("vantage: Unable to connect to ethernet host %s on port %d." % (self.host, self.port))
            raise
        logging.debug("vantage: Opened up ethernet host %s on port %d" % (self.host, self.port))

    def closePort(self):
        import socket
        try:
            # This will cancel any pending loop:
            self.wakeup_console(max_tries=1)
        except BaseException:
            pass
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

    def flush_input(self):
        """Flush the input buffer from WeatherLinkIP"""
        try:
            # This is a bit of a hack, but there is no analogue to pyserial's flushInput()
            self.socket.settimeout(0)
            self.read(4096)
        except BaseException:
            pass
        finally:
            self.socket.settimeout(self.timeout)

    def flush_output(self):
        """Flush the output buffer to WeatherLinkIP

        This function does nothing as there should never be anything left in
        the buffer when using socket.sendall()"""
        pass

    def queued_bytes(self):
        """Determine how many bytes are in the buffer"""
        import socket
        length = 0
        try:
            self.socket.settimeout(0)
            length = len(self.socket.recv(8192, socket.MSG_PEEK))
        except socket.error:
            pass
        finally:
            self.socket.settimeout(self.timeout)
        return length

    def read(self, chars=1):
        """Read bytes from WeatherLinkIP"""
        import socket
        _buffer = ''
        _remaining = chars
        while _remaining:
            _N = min(4096, _remaining)
            try:
                _recv = self.socket.recv(_N)
            except (socket.timeout, socket.error) as ex:
                # Reraise as a weewx I/O error:
                raise WeeWxIOError(ex)
            _nread = len(_recv)
            if _nread == 0:
                raise WeeWxIOError("vantage: Expected %d characters; got zero instead" % (_N,))
            _buffer += _recv
            _remaining -= _nread
        return _buffer

    def write(self, data):
        """Write to a WeatherLinkIP"""
        import socket
        try:
            self.socket.sendall(data)
            time.sleep(self.tcp_send_delay)
        except (socket.timeout, socket.error) as ex:
            logging.error("vantage: Socket write error.")
            # Reraise as a weewx I/O error:
            raise WeeWxIOError(ex)

# ===============================================================================
#                           class Vantage
# ===============================================================================


class Vantage(AbstractDevice):
    """Class that represents a connection to a Davis Vantage console.

    The connection to the console will be open after initialization"""

    # Various codes used internally by the VP2:
    barometer_unit_dict = {0: 'inHg', 1: 'mmHg', 2: 'hPa', 3: 'mbar'}
    temperature_unit_dict = {0: 'degree_F', 1: 'degree_10F', 2: 'degree_C', 3: 'degree_10C'}
    altitude_unit_dict = {0: 'foot', 1: 'meter'}
    rain_unit_dict = {0: 'inch', 1: 'mm'}
    wind_unit_dict = {0: 'mile_per_hour', 1: 'meter_per_second', 2: 'km_per_hour', 3: 'knot'}
    wind_cup_dict = {0: 'small', 1: 'large'}
    rain_bucket_dict = {0: "0.01 inches", 1: "0.2 MM", 2: "0.1 MM"}
    transmitter_type_dict = {0: 'iss', 1: 'temp', 2: 'hum', 3: 'temp_hum', 4: 'wind',
                             5: 'rain', 6: 'leaf', 7: 'soil', 8: 'leaf_soil',
                             9: 'sensorlink', 10: 'none'}

    def __init__(self, **vp_dict):
        """Initialize an object of type Vantage.

        NAMED ARGUMENTS:

        connection_type: The type of connection (serial|ethernet) [Required]

        port: The serial port of the VP. [Required if serial/USB
        communication]

        host: The Vantage network host [Required if Ethernet communication]

        baudrate: Baudrate of the port. [Optional. Default 19200]

        tcp_port: TCP port to connect to [Optional. Default 22222]

        tcp_send_delay: Block after sending data to WeatherLinkIP to allow it
        to process the command [Optional. Default is 1]

        timeout: How long to wait before giving up on a response from the
        serial port. [Optional. Default is 5]

        wait_before_retry: How long to wait before retrying. [Optional.
        Default is 1.2 seconds]

        max_tries: How many times to try again before giving up. [Optional.
        Default is 4]

        iss_id: The station number of the ISS [Optional. Default is 1]
        """

        # TODO: These values should really be retrieved dynamically from the VP:
        self.model_type = 2  # = 1 for original VantagePro, = 2 for VP2

        # These come from the configuration dictionary:
        self.wait_before_retry = float(vp_dict.get('wait_before_retry', 1.2))
        self.max_tries = int(vp_dict.get('max_tries', 4))
        self.iss_id = vp_dict.get('iss_id')
        if self.iss_id is not None:
            self.iss_id = int(self.iss_id)

        self.save_monthRain = None
        self.max_dst_jump = 7200

        # Get an appropriate port, depending on the connection type:
        self.port = Vantage._port_factory(vp_dict)

        # Open it up:
        self.port.openPort()

        # Read the EEPROM and fill in properties in this instance
        self._setup()

    def openPort(self):
        """Open up the connection to the console"""
        self.port.openPort()

    def closePort(self):
        """Close the connection to the console. """
        self.port.closePort()

    def genLoopPackets(self):
        """Generator function that returns loop packets"""

        while True:
            # Get LOOP packets in big batches This is necessary because there is
            # an undocumented limit to how many LOOP records you can request
            # on the VP (somewhere around 220).
            for _loop_packet in self.genDavisLoopPackets(200):
                yield _loop_packet

    def genDavisLoopPackets(self, N=1):
        """Generator function to return N loop packets from a Vantage console

        N: The number of packets to generate [default is 1]

        yields: up to N loop packets (could be less in the event of a
        read or CRC error).
        """

        logging.debug("vantage: Requesting %d LOOP packets." % N)

        self.port.wakeup_console(self.max_tries, self.wait_before_retry)

        # Request N packets:
        self.port.send_data("LOOP %d\n" % N)

        ntries = 1

        for loop in range(N):

            if ntries > self.max_tries:
                logging.error("vantage: Max retries (%d) exceeded." % self.max_tries)
                raise RetriesExceeded("Max retries exceeded while getting LOOP data.")

            try:
                # Fetch a packet
                _buffer = self.port.read(99)
            except WeeWxIOError as e:
                logging.error("vantage: LOOP #%d; read error. Try #%d" % (loop, ntries))
                logging.error("   ****  %s" % e)
                ntries += 1
                continue

            if crc16(_buffer):
                logging.error("vantage: LOOP #%d; CRC error. Try #%d" % (loop, ntries))
                ntries += 1
                continue
            # ... decode it
            loop_packet = self._unpackLoopPacket(_buffer[:95])
            # Yield it
            yield loop_packet
            ntries = 1

    def genStartupRecords(self):
        """A generator function to return archive packets from a Davis Vantage station.

        since_ts: A timestamp. All data since (but not including) this time will be returned.
        Pass in None for all data

        yields: a sequence of dictionaries containing the data
        """

        _vantageDateStamp = _vantageTimeStamp = 0
        logging.debug('vantage: Getting all archive packets')

        # Pack the date and time into a string, little-endian order
        _datestr = struct.pack("<HH", _vantageDateStamp, _vantageTimeStamp)

        # Save the last good time:
        _last_good_ts = 0

        # Try to retrieve the starting page and index:
        for n in range(self.max_tries):
            try:
                # Wake up the console...
                self.port.wakeup_console(self.max_tries, self.wait_before_retry)
                # ... request a dump...
                self.port.send_data('DMPAFT\n')
                # ... from the designated date (allow only one try because that's all the console allows):
                self.port.send_data_with_crc16(_datestr, max_tries=1)

                # Get the response with how many pages and starting index and decode it. Again, allow only one try:
                _buffer = self.port.get_data_with_crc16(6, max_tries=1)
                break
            except WeeWxIOError as e:
                logging.debug("vantage: Failed attempt %d receiving starting page. Error %s" % (n + 1, e))
                if n >= self.max_tries - 1:
                    logging.error("vantage: Unable to retrieve starting page")
                    raise

        (_npages, _start_index) = struct.unpack("<HH", _buffer[:4])
        logging.debug("vantage: Retrieving %d page(s); starting index= %d" % (_npages, _start_index))

        # Cycle through the pages...
        for unused_ipage in xrange(_npages):
            # ... get a page of archive data
            _page = self.port.get_data_with_crc16(267, prompt=_ack, max_tries=self.max_tries)
            # Now extract each record from the page
            for _index in xrange(_start_index, 5):
                # Get the record string buffer for this index:
                _record_string = _page[1 + 52 * _index:53 + 52 * _index]
                # If the console has been recently initialized, there will
                # be unused records, which are filled with 0xff. Detect this
                # by looking at the first 4 bytes (the date and time):
                if _record_string[0:4] == 4 * chr(0xff) or _record_string[0:4] == 4 * chr(0x00):
                    # This record has never been used. We're done.
                    logging.debug("vantage: empty record page %d; index %d"
                                  % (unused_ipage, _index))
                    return

                # Unpack the archive packet from the string buffer:
                _record = self._unpackArchivePacket(_record_string)

                # Check to see if the time stamps are declining, which would
                # signal that we are done.
                if _record['dateTime'] is None or _record['dateTime'] <= _last_good_ts - self.max_dst_jump:
                    # The time stamp is declining. We're done.
                    logging.debug("vantage: Catch up complete.")
                    return
                # Set the last time to the current time, and yield the packet
                _last_good_ts = _record['dateTime']
                _record['archive_interval'] = _record['interval']
                yield _record

            # The starting index for pages other than the first is always zero
            _start_index = 0

    def genLoggerSummary(self):
        """A generator function to return a summary of each page in the logger.

        yields: A 8-way tuple containing (page, index, year, month, day, hour, minute, timestamp)
        """

        # Wake up the console...
        self.port.wakeup_console(self.max_tries, self.wait_before_retry)
        # ... request a dump...
        self.port.send_data('DMP\n')

        logging.debug("vantage: Starting logger summary.")

        # Cycle through the pages...
        for _ipage in xrange(512):
            # ... get a page of archive data
            _page = self.port.get_data_with_crc16(267, prompt=_ack, max_tries=self.max_tries)
            # Now extract each record from the page
            for _index in xrange(5):
                # Get the record string buffer for this index:
                _record_string = _page[1 + 52 * _index:53 + 52 * _index]
                # If the console has been recently initialized, there will
                # be unused records, which are filled with 0xff. Detect this
                # by looking at the first 4 bytes (the date and time):
                if _record_string[0:4] == 4 * chr(0xff) or _record_string[0:4] == 4 * chr(0x00):
                    # This record has never been used.
                    y = mo = d = h = mn = time_ts = None
                else:
                    # Extract the date and time from the raw buffer:
                    datestamp, timestamp = struct.unpack("<HH", _record_string[0:4])
                    time_ts = _archive_datetime(datestamp, timestamp)
                    y = (0xfe00 & datestamp) >> 9    # year
                    mo = (0x01e0 & datestamp) >> 5    # month
                    d = (0x001f & datestamp)         # day
                    h = timestamp // 100             # hour
                    mn = timestamp % 100              # minute
                yield (_ipage, _index, y, mo, d, h, mn, time_ts)
        logging.debug("Vantage: Finished logger summary.")

    def getTime(self):
        """Get the current time from the console, returning it as timestamp"""

        time_dt = self.getConsoleTime()
        return time.mktime(time_dt.timetuple())

    def getConsoleTime(self):
        """Return the raw time on the console, uncorrected for DST or timezone."""

        # Try up to max_tries times:
        for unused_count in xrange(self.max_tries):
            try:
                # Wake up the console...
                self.port.wakeup_console(max_tries=self.max_tries, wait_before_retry=self.wait_before_retry)
                # ... request the time...
                self.port.send_data('GETTIME\n')
                # ... get the binary data. No prompt, only one try:
                _buffer = self.port.get_data_with_crc16(8, max_tries=1)
                (sec, minute, hr, day, mon, yr, unused_crc) = struct.unpack("<bbbbbbH", _buffer)

                return datetime.datetime(yr + 1900, mon, day, hr, minute, sec)

            except WeeWxIOError:
                # Caught an error. Keep retrying...
                continue
        logging.error("vantage: Max retries exceeded while getting time")
        raise RetriesExceeded("While getting console time")

    def setTime(self):
        """Set the clock on the Davis Vantage console"""

        for unused_count in xrange(self.max_tries):
            try:
                # Wake the console and begin the setTime command
                self.port.wakeup_console(max_tries=self.max_tries, wait_before_retry=self.wait_before_retry)
                self.port.send_data('SETTIME\n')

                # Unfortunately, clock resolution is only 1 second, and transmission takes a
                # little while to complete, so round up the clock up. 0.5 for clock resolution
                # and 0.25 for transmission delay
                newtime_tt = time.localtime(int(time.time() + 0.75))

                # The Davis expects the time in reversed order, and the year is since 1900
                _buffer = struct.pack("<bbbbbb", newtime_tt[5], newtime_tt[4], newtime_tt[3], newtime_tt[2],
                                      newtime_tt[1], newtime_tt[0] - 1900)

                # Complete the setTime command
                self.port.send_data_with_crc16(_buffer, max_tries=1)
                return
            except WeeWxIOError:
                # Caught an error. Keep retrying...
                continue
        logging.error("vantage: Max retries exceeded while setting time")
        raise RetriesExceeded("While setting console time")

    def setDST(self, dst='auto'):
        """Turn DST on or off, or set it to auto.

        dst: One of 'auto', 'on' or 'off' """

        _dst = dst.strip().lower()
        if _dst not in ['auto', 'on', 'off']:
            raise ViolatedPrecondition("Invalid DST setting %s" % dst)

        # Set flag whether DST is auto or manual:
        man_auto = 0 if _dst == 'auto' else 1
        self.port.send_data("EEBWR 12 01\n")
        self.port.send_data_with_crc16(chr(man_auto))

        # If DST is manual, set it on or off:
        if _dst in ['on', 'off']:
            on_off = 0 if _dst == 'off' else 1
            self.port.send_data("EEBWR 13 01\n")
            self.port.send_data_with_crc16(chr(on_off))

    def setTZcode(self, code):
        """Set the console's time zone code. See the Davis Vantage manual for the table
        of preset time zones."""
        if code < 0 or code > 46:
            raise ViolatedPrecondition("Invalid time zone code %d" % code)
        # Set the GMT_OR_ZONE byte to use TIME_ZONE value
        self.port.send_data("EEBWR 16 01\n")
        self.port.send_data_with_crc16(chr(0))
        # Set the TIME_ZONE value
        self.port.send_data("EEBWR 11 01\n")
        self.port.send_data_with_crc16(chr(code))

    def setTZoffset(self, offset):
        """Set the console's time zone to a custom offset.

        offset: Offset. This is an integer in hundredths of hours. E.g., -175 would be 1h45m negative offset."""
        # Set the GMT_OR_ZONE byte to use GMT_OFFSET value
        self.port.send_data("EEBWR 16 01\n")
        self.port.send_data_with_crc16(chr(1))
        # Set the GMT_OFFSET value
        self.port.send_data("EEBWR 14 02\n")
        self.port.send_data_with_crc16(struct.pack("<h", offset))

    def setBucketType(self, new_bucket_code):
        """Set the rain bucket type.

        new_bucket_code: The new bucket type. Must be one of 0, 1, or 2
        """
        if new_bucket_code not in (0, 1, 2):
            raise ViolatedPrecondition("Invalid bucket code %d" % new_bucket_code)
        old_setup_bits = self._getEEPROM_value(0x2B)[0]
        new_setup_bits = (old_setup_bits & 0xCF) | (new_bucket_code << 4)

        # Tell the console to put one byte in hex location 0x2B
        self.port.send_data("EEBWR 2B 01\n")
        # Follow it up with the data:
        self.port.send_data_with_crc16(chr(new_setup_bits), max_tries=1)
        # Then call NEWSETUP to get it to stick:
        self.port.send_data("NEWSETUP\n")

        self._setup()
        logging.info("vantage: Rain bucket type set to %d (%s)" % (self.rain_bucket_type, self.rain_bucket_size))

    def setRainYearStart(self, new_rain_year_start):
        """Set the start of the rain season.

        new_rain_year_start: Must be in the closed range 1...12
        """
        if new_rain_year_start not in range(1, 13):
            raise ViolatedPrecondition("Invalid rain season start %d" % (new_rain_year_start,))

        # Tell the console to put one byte in hex location 0x2C
        self.port.send_data("EEBWR 2C 01\n")
        # Follow it up with the data:
        self.port.send_data_with_crc16(chr(new_rain_year_start), max_tries=1)

        self._setup()
        logging.info("vantage: Rain year start set to %d" % (self.rain_year_start,))

    def setBarData(self, new_barometer_inHg, new_altitude_foot):
        """Set the internal barometer calibration and altitude settings in the console.

        new_barometer_inHg: The local, reference barometric pressure in inHg.

        new_altitude_foot: The new altitude in feet."""

        new_barometer = int(new_barometer_inHg * 1000.0)
        new_altitude = int(new_altitude_foot)

        command = "BAR=%d %d\n" % (new_barometer, new_altitude)
        self.port.send_command(command)
        self._setup()
        logging.info("vantage: Set barometer calibration.")

    def setArchiveInterval(self, archive_interval_seconds):
        """Set the archive interval of the Vantage.

        archive_interval_seconds: The new interval to use in minutes. Must be one of
        60, 300, 600, 900, 1800, 3600, or 7200
        """
        if archive_interval_seconds not in (60, 300, 600, 900, 1800, 3600, 7200):
            raise ViolatedPrecondition("vantage: Invalid archive interval (%d)" % (archive_interval_seconds,))

        # The console expects the interval in minutes. Divide by 60.
        command = 'SETPER %d\n' % (archive_interval_seconds / 60)

        self.port.send_command(command, max_tries=self.max_tries)

        self._setup()
        logging.info("vantage: archive interval set to %d seconds" % (archive_interval_seconds,))

    def setLamp(self, onoff='OFF'):
        """Set the lamp on or off"""
        try:
            _setting = {'off': '0', 'on': '1'}[onoff.lower()]
        except KeyError:
            raise ValueError("Unknown lamp setting '%s'" % onoff)

        _command = "LAMPS %s\n" % _setting
        self.port.send_command(_command, max_tries=self.max_tries)

        logging.info("vantage: Lamp set to '%s'" % onoff)

    def setTransmitterType(self, new_channel, new_transmitter_type, new_extra_temp, new_extra_hum):
        """Set the transmitter type for one of the eight channels."""

        # Default value just for tidiness.
        new_temp_hum_bits = 0xFF

        # Check arguments are consistent.
        if new_channel not in range(0, 8):
            raise ViolatedPrecondition("Invalid channel %d" % new_channel)
        if new_transmitter_type not in range(0, 11):
            raise ViolatedPrecondition("Invalid transmitter type %d" % new_transmitter_type)
        if Vantage.transmitter_type_dict[new_transmitter_type] in ['temp', 'temp_hum']:
            if new_extra_temp not in range(1, 9):
                raise ViolatedPrecondition("Invalid extra temperature number %d" % new_extra_temp)
            # Extra temp is origin 0.
            new_temp_hum_bits = new_temp_hum_bits & 0xF0 | (new_extra_temp - 1)
        if Vantage.transmitter_type_dict[new_transmitter_type] in ['hum', 'temp_hum']:
            if new_extra_hum not in range(1, 9):
                raise ViolatedPrecondition("Invalid extra humidity number %d" % new_extra_hum)
            # Extra humidity is origin 1.
            new_temp_hum_bits = new_temp_hum_bits & 0x0F | (new_extra_hum << 4)

        # Preserve top nibble, is related to repeaters.
        old_type_bits = self._getEEPROM_value(0x19 + (new_channel - 1) * 2)[0]
        new_type_bits = old_type_bits & 0xF0 | new_transmitter_type
        # Transmitter type 10 is "none"; turn off listening too.
        usetx = 1 if new_transmitter_type != 10 else 0
        old_usetx_bits = self._getEEPROM_value(0x17)[0]
        new_usetx_bits = old_usetx_bits & ~(1 << (new_channel - 1)) | usetx * (1 << new_channel - 1)

        # Tell the console to put two bytes in hex location 0x19 or 0x1B or ... depending on channel.
        self.port.send_data("EEBWR %X 02\n" % (0x19 + (new_channel - 1) * 2))
        # Follow it up with the data:
        self.port.send_data_with_crc16(chr(new_type_bits) + chr(new_temp_hum_bits), max_tries=1)
        # Tell the console to put one byte in hex location 0x17
        self.port.send_data("EEBWR 17 01\n")
        # Follow it up with the data:
        self.port.send_data_with_crc16(chr(new_usetx_bits), max_tries=1)
        # Then call NEWSETUP to get it to stick:
        self.port.send_data("NEWSETUP\n")

        self._setup()
        logging.info("vantage: Transmitter type for channel %d set to %d (%s)" % (
            new_channel, new_transmitter_type, Vantage.transmitter_type_dict[new_transmitter_type]))

    def setCalibrationWindDir(self, offset):
        """Set the on-board wind direction calibration."""
        if offset < -359 or offset > 359:
            raise ViolatedPrecondition("Offset %d out of range [-359, 359]." % offset)
        nbytes = struct.pack("<h", offset)
        # Tell the console to put two bytes in hex location 0x4D
        self.port.send_data("EEBWR 4D 02\n")
        # Follow it up with the data:
        self.port.send_data_with_crc16(nbytes, max_tries=1)
        logging.info("vantage: Wind calibration set to %d" % (offset))

    def setCalibrationTemp(self, variable, offset):
        """Set an on-board temperature calibration."""
        # Offset is in tenths of degree Fahrenheit.
        if offset < -12.8 or offset > 12.7:
            raise ViolatedPrecondition("Offset %.1f out of range [-12.8, 12.7]." % offset)
        byte = struct.pack("b", int(round(offset * 10)))
        variable_dict = {'outTemp': 0x34}
        for i in range(1, 8):
            variable_dict['extraTemp%d' % i] = 0x34 + i
        for i in range(1, 5):
            variable_dict['soilTemp%d' % i] = 0x3B + i
        for i in range(1, 5):
            variable_dict['leafTemp%d' % i] = 0x3F + i
        if variable == "inTemp":
            # Inside temp is special, needs ones' complement in next byte.
            complement_byte = struct.pack("B", ~int(round(offset * 10)) & 0xFF)
            self.port.send_data("EEBWR 32 02\n")
            self.port.send_data_with_crc16(byte + complement_byte, max_tries=1)
        elif variable in variable_dict:
            # Other variables are just sent as-is.
            self.port.send_data("EEBWR %X 01\n" % variable_dict[variable])
            self.port.send_data_with_crc16(byte, max_tries=1)
        else:
            raise ViolatedPrecondition("Variable name %s not known" % variable)
        logging.info("vantage: Temperature calibration %s set to %.1f" % (variable, offset))

    def setCalibrationHumid(self, variable, offset):
        """Set an on-board humidity calibration."""
        # Offset is in percentage points.
        if offset < -100 or offset > 100:
            raise ViolatedPrecondition("Offset %d out of range [-100, 100]." % offset)
        byte = struct.pack("b", offset)
        variable_dict = {'inHumid': 0x44, 'outHumid': 0x45}
        for i in range(1, 8):
            variable_dict['extraHumid%d' % i] = 0x45 + i
        if variable in variable_dict:
            self.port.send_data("EEBWR %X 01\n" % variable_dict[variable])
            self.port.send_data_with_crc16(byte, max_tries=1)
        else:
            raise ViolatedPrecondition("Variable name %s not known" % variable)
        logging.info("vantage: Humidity calibration %s set to %d" % (variable, offset))

    def clearMemory(self):
        self._clearLog()

    def _clearLog(self):
        """Clear the internal archive memory in the Vantage."""

        self.port.wakeup_console(self.max_tries, self.wait_before_retry)

        for unused_count in xrange(self.max_tries):
            try:
                self.port.send_data("CLRLOG\n")
                return
            except WeeWxIOError as e:
                logging.error("vantage: Error while clearing log: %s" % str(e))
                continue
        logging.error("vantage: Max retries exceeded while clearing log")
        raise RetriesExceeded("While clearing log")

    def getRX(self):
        """Returns reception statistics from the console.

        Returns a tuple with 5 values: (# of packets, # of missed packets,
        # of resynchronizations, the max # of packets received w/o an error,
        the # of CRC errors detected.)"""

        rx_list = self.port.send_command('RXCHECK\n')

        # The following is a list of the reception statistics, but the elements are strings
        rx_list_str = rx_list[0].split()
        # Convert to numbers and return as a tuple:
        rx_list = tuple(int(x) for x in rx_list_str)
        return rx_list

    def getBarData(self):
        """Gets barometer calibration data. Returns as a 9 element list."""
        _bardata = self.port.send_command("BARDATA\n")
        _barometer = float(_bardata[0].split()[1]) / 1000.0
        _altitude = float(_bardata[1].split()[1])
        _dewpoint = float(_bardata[2].split()[2])
        _virt_temp = float(_bardata[3].split()[2])
        _c = float(_bardata[4].split()[1])
        _r = float(_bardata[5].split()[1]) / 1000.0
        _barcal = float(_bardata[6].split()[1]) / 1000.0
        _gain = float(_bardata[7].split()[1])
        _offset = float(_bardata[8].split()[1])

        return (_barometer, _altitude, _dewpoint, _virt_temp,
                _c, _r, _barcal, _gain, _offset)

    def getFirmwareDate(self):
        """Return the firmware date as a string. """
        return self.port.send_command('VER\n')[0]

    def getFirmwareVersion(self):
        """Return the firmware version as a string."""
        return self.port.send_command('NVER\n')[0]

    def getStnInfo(self):
        """Return lat / lon, time zone, etc."""

        (stnlat, stnlon) = self._getEEPROM_value(0x0B, "<2h")
        stnlat /= 10.0
        stnlon /= 10.0
        man_or_auto = "MANUAL" if self._getEEPROM_value(0x12)[0] else "AUTO"
        dst = "ON" if self._getEEPROM_value(0x13)[0] else "OFF"
        gmt_or_zone = "GMT_OFFSET" if self._getEEPROM_value(0x16)[0] else "ZONE_CODE"
        zone_code = self._getEEPROM_value(0x11)[0]
        gmt_offset = self._getEEPROM_value(0x14, "<h")[0] / 100.0

        return (stnlat, stnlon, man_or_auto, dst, gmt_or_zone, zone_code, gmt_offset)

    def getStnTransmitters(self):
        """ Get the types of transmitters on the eight channels."""

        transmitters = []
        use_tx = self._getEEPROM_value(0x17)[0]
        transmitter_data = self._getEEPROM_value(0x19, "16B")

        for transmitter_id in range(8):
            transmitter_type = Vantage.transmitter_type_dict[transmitter_data[transmitter_id * 2] & 0x0F]
            transmitter = {"transmitter_type": transmitter_type,
                           "listen": (use_tx >> transmitter_id) & 1}
            if transmitter_type in ['temp', 'temp_hum']:
                # Extra temperature is origin 0.
                transmitter['temp'] = (transmitter_data[transmitter_id * 2 + 1] & 0xF) + 1
            if transmitter_type in ['hum', 'temp_hum']:
                # Extra humidity is origin 1.
                transmitter['hum'] = transmitter_data[transmitter_id * 2 + 1] >> 4
            transmitters.append(transmitter)
        return transmitters

    def getStnCalibration(self):
        """ Get the temperature/humidity/wind calibrations built into the console. """
        (inTemp, inTempComp, outTemp,
            extraTemp1, extraTemp2, extraTemp3, extraTemp4, extraTemp5, extraTemp6, extraTemp7,
            soilTemp1, soilTemp2, soilTemp3, soilTemp4, leafTemp1, leafTemp2, leafTemp3, leafTemp4,
            inHumid,
            outHumid, extraHumid1, extraHumid2, extraHumid3, extraHumid4, extraHumid5, extraHumid6, extraHumid7,
            wind) = self._getEEPROM_value(0x32, "<27bh")
        # inTempComp is 1's complement of inTemp.
        if inTemp + inTempComp != -1:
            logging.error("vantage: Inconsistent EEPROM calibration values")
            return None
        # Temperatures are in tenths of a degree F; Humidity in 1 percent.
        return {
            "inTemp": inTemp / 10,
            "outTemp": outTemp / 10,
            "extraTemp1": extraTemp1 / 10,
            "extraTemp2": extraTemp2 / 10,
            "extraTemp3": extraTemp3 / 10,
            "extraTemp4": extraTemp4 / 10,
            "extraTemp5": extraTemp5 / 10,
            "extraTemp6": extraTemp6 / 10,
            "extraTemp7": extraTemp7 / 10,
            "soilTemp1": soilTemp1 / 10,
            "soilTemp2": soilTemp2 / 10,
            "soilTemp3": soilTemp3 / 10,
            "soilTemp4": soilTemp4 / 10,
            "leafTemp1": leafTemp1 / 10,
            "leafTemp2": leafTemp2 / 10,
            "leafTemp3": leafTemp3 / 10,
            "leafTemp4": leafTemp4 / 10,
            "inHumid": inHumid,
            "outHumid": outHumid,
            "extraHumid1": extraHumid1,
            "extraHumid2": extraHumid2,
            "extraHumid3": extraHumid3,
            "extraHumid4": extraHumid4,
            "extraHumid5": extraHumid5,
            "extraHumid6": extraHumid6,
            "extraHumid7": extraHumid7,
            "wind": wind
        }

    def startLogger(self):
        self.port.send_command("START\n")

    def stopLogger(self):
        self.port.send_command('STOP\n')

    # ===========================================================================
    #              Davis Vantage utility functions
    # ===========================================================================

    @property
    def hardware_name(self):
        if self.hardware_type == 16:
            return "VantagePro2"
        elif self.hardware_type == 17:
            return "VantageVue"
        else:
            raise UnsupportedFeature("Unknown hardware type %d" % self.hardware_type)

    @property
    def archive_interval(self):
        return self.archive_interval_

    def _setup(self):
        """Retrieve the EEPROM data block from a VP2 and use it to set various properties"""

        self.port.wakeup_console(max_tries=self.max_tries, wait_before_retry=self.wait_before_retry)

        # Determine the type of hardware:
        self.port.send_data("WRD" + chr(0x12) + chr(0x4d) + "\n")
        self.hardware_type = ord(self.port.read())

        unit_bits = self._getEEPROM_value(0x29)[0]
        setup_bits = self._getEEPROM_value(0x2B)[0]
        self.rain_year_start = self._getEEPROM_value(0x2C)[0]
        self.archive_interval_ = self._getEEPROM_value(0x2D)[0] * 60

        barometer_unit_code = unit_bits & 0x03
        temperature_unit_code = (unit_bits & 0x0C) >> 2
        altitude_unit_code = (unit_bits & 0x10) >> 4
        rain_unit_code = (unit_bits & 0x20) >> 5
        wind_unit_code = (unit_bits & 0xC0) >> 6

        self.wind_cup_type = (setup_bits & 0x08) >> 3
        self.rain_bucket_type = (setup_bits & 0x30) >> 4

        self.barometer_unit = Vantage.barometer_unit_dict[barometer_unit_code]
        self.temperature_unit = Vantage.temperature_unit_dict[temperature_unit_code]
        self.altitude_unit = Vantage.altitude_unit_dict[altitude_unit_code]
        self.rain_unit = Vantage.rain_unit_dict[rain_unit_code]
        self.wind_unit = Vantage.wind_unit_dict[wind_unit_code]
        self.wind_cup_size = Vantage.wind_cup_dict[self.wind_cup_type]
        self.rain_bucket_size = Vantage.rain_bucket_dict[self.rain_bucket_type]

        # Adjust the translation maps to reflect the rain bucket size:
        if self.rain_bucket_type == 1:
            _archive_map['rain'] = _archive_map['rainRate'] = _loop_map['stormRain'] = _loop_map['dayRain'] = \
                _loop_map['monthRain'] = _loop_map['yearRain'] = _bucket_1
            _loop_map['rainRate'] = _bucket_1_None
        elif self.rain_bucket_type == 2:
            _archive_map['rain'] = _archive_map['rainRate'] = _loop_map['stormRain'] = _loop_map['dayRain'] = \
                _loop_map['monthRain'] = _loop_map['yearRain'] = _bucket_2
            _loop_map['rainRate'] = _bucket_2_None
        else:
            _archive_map['rain'] = _archive_map['rainRate'] = _loop_map['stormRain'] = _loop_map['dayRain'] = \
                _loop_map['monthRain'] = _loop_map['yearRain'] = _val100
            _loop_map['rainRate'] = _big_val100

        # Try to guess the ISS ID for gauging reception strength.
        if self.iss_id is None:
            stations = self.getStnTransmitters()
            # Wind retransmitter is best candidate.
            for station_id in range(0, 8):
                if stations[station_id]['transmitter_type'] == 'wind':
                    self.iss_id = station_id + 1  # Origin 1.
                    break
            else:
                # ISS is next best candidate.
                for station_id in range(0, 8):
                    if stations[station_id]['transmitter_type'] == 'iss':
                        self.iss_id = station_id + 1  # Origin 1.
                        break
                else:
                    # On Vue, can use VP2 ISS, which reports as "rain"
                    for station_id in range(0, 8):
                        if stations[station_id]['transmitter_type'] == 'rain':
                            self.iss_id = station_id + 1  # Origin 1.
                            break
                    else:
                        self.iss_id = 1   # Pick a reasonable default.

    def _getEEPROM_value(self, offset, v_format="B"):
        """Return a list of values from the EEPROM starting at a specified offset, using a specified format"""

        nbytes = struct.calcsize(v_format)
        # Don't bother waking up the console for the first try. It's probably
        # already awake from opening the port. However, if we fail, then do a
        # wakeup.
        firsttime = True

        command = "EEBRD %X %X\n" % (offset, nbytes)
        for unused_count in xrange(self.max_tries):
            try:
                if not firsttime:
                    self.port.wakeup_console(max_tries=self.max_tries, wait_before_retry=self.wait_before_retry)
                    firsttime = False
                self.port.send_data(command)
                _buffer = self.port.get_data_with_crc16(nbytes + 2, max_tries=1)
                _value = struct.unpack(v_format, _buffer[:-2])
                return _value
            except WeeWxIOError:
                continue

        logging.error("vantage: Max retries exceeded while getting EEPROM data at address 0x%X" % offset)
        raise RetriesExceeded("While getting EEPROM data value at address 0x%X" % offset)

    @staticmethod
    def _port_factory(vp_dict):
        """Produce a serial or ethernet port object"""

        timeout = float(vp_dict.get('timeout', 5.0))

        # Get the connection type. If it is not specified, assume 'serial':
        connection_type = vp_dict.get('type', 'serial').lower()

        if connection_type == "serial":
            port = vp_dict['port']
            baudrate = int(vp_dict.get('baudrate', 19200))
            return SerialWrapper(port, baudrate, timeout)
        elif connection_type == "ethernet":
            hostname = vp_dict['host']
            tcp_port = int(vp_dict.get('tcp_port', 22222))
            tcp_send_delay = int(vp_dict.get('tcp_send_delay', 1))
            return EthernetWrapper(hostname, tcp_port, timeout, tcp_send_delay)
        raise UnsupportedFeature(vp_dict['type'])

    def _unpackLoopPacket(self, raw_loop_string):
        """Decode a raw Davis LOOP packet, returning the results as a dictionary in physical units.

        raw_loop_string: The loop packet data buffer, passed in as a string.

        returns:

        A dictionary. The key will be an observation type, the value will be
        the observation in physical units."""

        # Unpack the data, using the compiled stuct.Struct string 'loop_fmt'
        data_tuple = loop_fmt.unpack(raw_loop_string)

        # Put the results in a dictionary. The values will not be in physical units yet,
        # but rather using the raw values from the console.
        raw_loop_packet = dict(zip(loop_types, data_tuple))

        # Detect the kind of LOOP packet. Type 'A' has the character 'P' in this
        # position. Type 'B' contains the 3-hour barometer trend in this position.
        if raw_loop_packet['loop_type'] == ord('P'):
            raw_loop_packet['trend'] = None
            raw_loop_packet['loop_type'] = 'A'
        else:
            raw_loop_packet['trend'] = raw_loop_packet['loop_type']
            raw_loop_packet['loop_type'] = 'B'

        loop_packet = {'dateTime': int(time.time() + 0.5),
                       'units': US}

        for _type in raw_loop_packet:
            # Get the mapping function for this type:
            func = _loop_map.get(_type)
            # It it exists, apply it:
            if func:
                # Call the function, with the value as an argument, storing the result:
                loop_packet[_type] = func(raw_loop_packet[_type])

        # Because the Davis stations do not offer bucket tips in LOOP data, we
        # must calculate it by looking for changes in rain totals. This won't
        # work for the very first rain packet.
        if self.save_monthRain is None:
            delta = None
        else:
            delta = loop_packet['monthRain'] - self.save_monthRain
            # If the difference is negative, we're at the beginning of a month.
            if delta < 0:
                delta = None
        loop_packet['rain'] = delta
        self.save_monthRain = loop_packet['monthRain']

        return loop_packet

    def _unpackArchivePacket(self, raw_archive_string):
        """Decode a Davis archive packet, returning the results as a dictionary.

        raw_archive_string: The archive packet data buffer, passed in as a string. This will be unpacked and
        the results placed a dictionary"""

        # Figure out the packet type:
        packet_type = ord(raw_archive_string[42])

        if packet_type == 0xff:
            # Rev A packet type:
            archive_format = rec_fmt_A
            dataTypes = rec_types_A
        elif packet_type == 0x00:
            # Rev B packet type:
            archive_format = rec_fmt_B
            dataTypes = rec_types_B
        else:
            raise UnknownArchiveType("Unknown archive type = 0x%x" % (packet_type,))

        data_tuple = archive_format.unpack(raw_archive_string)

        raw_archive_packet = dict(zip(dataTypes, data_tuple))

        archive_packet = {'dateTime': _archive_datetime(raw_archive_packet['date_stamp'], raw_archive_packet['time_stamp']),
                          'units': US}

        for _type in raw_archive_packet:
            # Get the mapping function for this type:
            func = _archive_map.get(_type)
            # It it exists, apply it:
            if func:
                # Call the function, with the value as an argument, storing the result:
                archive_packet[_type] = func(raw_archive_packet[_type])

        # Divide archive interval by 60 to keep consistent with wview
        archive_packet['interval'] = self.archive_interval
        archive_packet['rxCheckPercent'] = _rxcheck(self.model_type, archive_packet['interval'],
                                                    self.iss_id, raw_archive_packet['number_of_wind_samples'])
        return archive_packet

# ===============================================================================
#                                 LOOP packet
# ===============================================================================


# A list of all the types held in a Vantage LOOP packet in their native order.
loop_format = [('loop', '3s'), ('loop_type', 'b'), ('packet_type', 'B'),
               ('next_record', 'H'), ('barometer', 'H'), ('inTemp', 'h'),
               ('inHumidity', 'B'), ('outTemp', 'h'), ('windSpeed', 'B'),
               ('windSpeed10', 'B'), ('windDir', 'H'), ('extraTemp1', 'B'),
               ('extraTemp2', 'B'), ('extraTemp3', 'B'), ('extraTemp4', 'B'),
               ('extraTemp5', 'B'), ('extraTemp6', 'B'), ('extraTemp7', 'B'),
               ('soilTemp1', 'B'), ('soilTemp2', 'B'), ('soilTemp3', 'B'),
               ('soilTemp4', 'B'), ('leafTemp1', 'B'), ('leafTemp2', 'B'),
               ('leafTemp3', 'B'), ('leafTemp4', 'B'), ('outHumidity', 'B'),
               ('extraHumid1', 'B'), ('extraHumid2', 'B'), ('extraHumid3', 'B'),
               ('extraHumid4', 'B'), ('extraHumid5', 'B'), ('extraHumid6', 'B'),
               ('extraHumid7', 'B'), ('rainRate', 'H'), ('UV', 'B'),
               ('radiation', 'H'), ('stormRain', 'H'), ('stormStart', 'H'),
               ('dayRain', 'H'), ('monthRain', 'H'), ('yearRain', 'H'),
               ('dayET', 'H'), ('monthET', 'H'), ('yearET', 'H'),
               ('soilMoist1', 'B'), ('soilMoist2', 'B'), ('soilMoist3', 'B'),
               ('soilMoist4', 'B'), ('leafWet1', 'B'), ('leafWet2', 'B'),
               ('leafWet3', 'B'), ('leafWet4', 'B'), ('insideAlarm', 'B'),
               ('rainAlarm', 'B'), ('outsideAlarm1', 'B'), ('outsideAlarm2', 'B'),
               ('extraAlarm1', 'B'), ('extraAlarm2', 'B'), ('extraAlarm3', 'B'),
               ('extraAlarm4', 'B'), ('extraAlarm5', 'B'), ('extraAlarm6', 'B'),
               ('extraAlarm7', 'B'), ('extraAlarm8', 'B'), ('soilLeafAlarm1', 'B'),
               ('soilLeafAlarm2', 'B'), ('soilLeafAlarm3', 'B'), ('soilLeafAlarm4', 'B'),
               ('txBatteryStatus', 'B'), ('consBatteryVoltage', 'H'), ('forecastIcon', 'B'),
               ('forecastRule', 'B'), ('sunrise', 'H'), ('sunset', 'H')]

# Extract the types and struct.Struct formats for the LOOP packets:
loop_types, fmt = zip(*loop_format)
loop_fmt = struct.Struct('<' + ''.join(fmt))

# ===============================================================================
#                              archive packet
# ===============================================================================

rec_format_A = [('date_stamp', 'H'), ('time_stamp', 'H'), ('outTemp', 'h'),
                ('highOutTemp', 'h'), ('lowOutTemp', 'h'), ('rain', 'H'),
                ('rainRate', 'H'), ('barometer', 'H'), ('radiation', 'H'),
                ('number_of_wind_samples', 'H'), ('inTemp', 'h'), ('inHumidity', 'B'),
                ('outHumidity', 'B'), ('windSpeed', 'B'), ('windGust', 'B'),
                ('windGustDir', 'B'), ('windDir', 'B'), ('UV', 'B'),
                ('ET', 'B'), ('invalid_data', 'B'), ('soilMoist1', 'B'),
                ('soilMoist2', 'B'), ('soilMoist3', 'B'), ('soilMoist4', 'B'),
                ('soilTemp1', 'B'), ('soilTemp2', 'B'), ('soilTemp3', 'B'),
                ('soilTemp4', 'B'), ('leafWet1', 'B'), ('leafWet2', 'B'),
                ('leafWet3', 'B'), ('leafWet4', 'B'), ('extraTemp1', 'B'),
                ('extraTemp2', 'B'), ('extraHumid1', 'B'), ('extraHumid2', 'B'),
                ('readClosed', 'H'), ('readOpened', 'H'), ('unused', 'B')]

rec_format_B = [('date_stamp', 'H'), ('time_stamp', 'H'), ('outTemp', 'h'),
                ('highOutTemp', 'h'), ('lowOutTemp', 'h'), ('rain', 'H'),
                ('rainRate', 'H'), ('barometer', 'H'), ('radiation', 'H'),
                ('number_of_wind_samples', 'H'), ('inTemp', 'h'), ('inHumidity', 'B'),
                ('outHumidity', 'B'), ('windSpeed', 'B'), ('windGust', 'B'),
                ('windGustDir', 'B'), ('windDir', 'B'), ('UV', 'B'),
                ('ET', 'B'), ('highRadiation', 'H'), ('highUV', 'B'),
                ('forecastRule', 'B'), ('leafTemp1', 'B'), ('leafTemp2', 'B'),
                ('leafWet1', 'B'), ('leafWet2', 'B'), ('soilTemp1', 'B'),
                ('soilTemp2', 'B'), ('soilTemp3', 'B'), ('soilTemp4', 'B'),
                ('download_record_type', 'B'), ('extraHumid1', 'B'), ('extraHumid2', 'B'),
                ('extraTemp1', 'B'), ('extraTemp2', 'B'), ('extraTemp3', 'B'),
                ('soilMoist1', 'B'), ('soilMoist2', 'B'), ('soilMoist3', 'B'),
                ('soilMoist4', 'B')]

# Extract the types and struct.Struct formats for the two types of archive packets:
rec_types_A, fmt_A = zip(*rec_format_A)
rec_types_B, fmt_B = zip(*rec_format_B)
rec_fmt_A = struct.Struct('<' + ''.join(fmt_A))
rec_fmt_B = struct.Struct('<' + ''.join(fmt_B))


def _rxcheck(model_type, interval, iss_id, number_of_wind_samples):
    """Gives an estimate of the fraction of packets received.

    Ref: Vantage Serial Protocol doc, V2.1.0, released 25-Jan-05; p42"""
    # The formula for the expected # of packets varies with model number.
    if model_type == 1:
        _expected_packets = float(interval * 60) / (2.5 + (iss_id - 1) / 16.0) -\
            float(interval * 60) / (50.0 + (iss_id - 1) * 1.25)
    elif model_type == 2:
        _expected_packets = 960.0 * interval / float(41 + iss_id - 1)
    else:
        return None
    _frac = number_of_wind_samples * 100.0 / _expected_packets
    if _frac > 100.0:
        _frac = 100.0
    return _frac

# ===============================================================================
#                      Decoding routines
# ===============================================================================


def _archive_datetime(datestamp, timestamp):
    """Returns the epoch time of the archive packet."""
    try:
        # Construct a time tuple from Davis time. Unfortunately, as timestamps come
        # off the Vantage logger, there is no way of telling whether or not DST is
        # in effect. So, have the operating system guess by using a '-1' in the last
        # position of the time tuple. It's the best we can do...
        time_tuple = ((0xfe00 & datestamp) >> 9,    # year
                      (0x01e0 & datestamp) >> 5,    # month
                      (0x001f & datestamp),         # day
                      timestamp // 100,             # hour
                      timestamp % 100,              # minute
                      0,                            # second
                      0, 0, -1)                     # have OS guess DST
        # Convert to epoch time:
        ts = int(time.mktime(time_tuple))
    except (OverflowError, ValueError, TypeError):
        ts = None
    return ts


def _loop_date(v):
    """Returns the epoch time stamp of a time encoded in the LOOP packet,
    which, for some reason, uses a different encoding scheme than the archive packet.
    Also, the Davis documentation isn't clear whether "bit 0" refers to the least-significant
    bit, or the most-significant bit. I'm assuming the former, which is the usual
    in little-endian machines."""
    if v == 0xffff:
        return None
    time_tuple = ((0x007f & v) + 2000,  # year
                  (0xf000 & v) >> 12,   # month
                  (0x0f80 & v) >> 7,   # day
                  0, 0, 0,              # h, m, s
                  0, 0, -1)
    # Convert to epoch time:
    try:
        ts = int(time.mktime(time_tuple))
    except (OverflowError, ValueError):
        ts = None
    return ts


def _stime(v):
    h = v / 100
    m = v % 100
    # Return seconds since midnight
    return 3600 * h + 60 * m


def _big_val(v):
    return float(v) if v != 0x7fff else None


def _big_val10(v):
    return float(v) / 10.0 if v != 0x7fff else None


def _big_val100(v):
    return float(v) / 100.0 if v != 0xffff else None


def _val100(v):
    return float(v) / 100.0


def _val1000(v):
    return float(v) / 1000.0


def _val1000Zero(v):
    return float(v) / 1000.0 if v != 0 else None


def _little_val(v):
    return float(v) if v != 0x00ff else None


def _little_val10(v):
    return float(v) / 10.0 if v != 0x00ff else None


def _little_temp(v):
    return float(v - 90) if v != 0x00ff else None


def _null(v):
    return v


def _null_float(v):
    return float(v)


def _null_int(v):
    return int(v)


def _windDir(v):
    return float(v) * 22.5 if v != 0x00ff else None

# Rain bucket type "1", a 0.2 mm bucket


def _bucket_1(v):
    return float(v) * 0.00787401575


def _bucket_1_None(v):
    return float(v) * 0.00787401575 if v != 0xffff else None

# Rain bucket type "2", a 0.1 mm bucket


def _bucket_2(v):
    return float(v) * 0.00393700787


def _bucket_2_None(v):
    return float(v) * 0.00393700787 if v != 0xffff else None


# This dictionary maps a type key to a function. The function should be able to
# decode a sensor value held in the LOOP packet in the internal, Davis form into US
# units and return it.
_loop_map = {'barometer': _val1000Zero,
             'inTemp': _big_val10,
             'inHumidity': _little_val,
             'outTemp': _big_val10,
             'windSpeed': _little_val,
             'windSpeed10': _little_val,
             'windDir': _big_val,
             'extraTemp1': _little_temp,
             'extraTemp2': _little_temp,
             'extraTemp3': _little_temp,
             'extraTemp4': _little_temp,
             'extraTemp5': _little_temp,
             'extraTemp6': _little_temp,
             'extraTemp7': _little_temp,
             'soilTemp1': _little_temp,
             'soilTemp2': _little_temp,
             'soilTemp3': _little_temp,
             'soilTemp4': _little_temp,
             'leafTemp1': _little_temp,
             'leafTemp2': _little_temp,
             'leafTemp3': _little_temp,
             'leafTemp4': _little_temp,
             'outHumidity': _little_val,
             'extraHumid1': _little_val,
             'extraHumid2': _little_val,
             'extraHumid3': _little_val,
             'extraHumid4': _little_val,
             'extraHumid5': _little_val,
             'extraHumid6': _little_val,
             'extraHumid7': _little_val,
             'rainRate': _big_val100,
             'UV': _little_val10,
             'radiation': _big_val,
             'stormRain': _val100,
             'stormStart': _loop_date,
             'dayRain': _val100,
             'monthRain': _val100,
             'yearRain': _val100,
             'dayET': _val1000,
             'monthET': _val100,
             'yearET': _val100,
             'soilMoist1': _little_val,
             'soilMoist2': _little_val,
             'soilMoist3': _little_val,
             'soilMoist4': _little_val,
             'leafWet1': _little_val,
             'leafWet2': _little_val,
             'leafWet3': _little_val,
             'leafWet4': _little_val,
             'insideAlarm': _null,
             'rainAlarm': _null,
             'outsideAlarm1': _null,
             'outsideAlarm2': _null,
             'extraAlarm1': _null,
             'extraAlarm2': _null,
             'extraAlarm3': _null,
             'extraAlarm4': _null,
             'extraAlarm5': _null,
             'extraAlarm6': _null,
             'extraAlarm7': _null,
             'extraAlarm8': _null,
             'soilLeafAlarm1': _null,
             'soilLeafAlarm2': _null,
             'soilLeafAlarm3': _null,
             'soilLeafAlarm4': _null,
             'txBatteryStatus': _null_int,
             'consBatteryVoltage': lambda v: float((v * 300) >> 9) / 100.0,
             'forecastIcon': _null,
             'forecastRule': _null,
             'sunrise': _stime,
             'sunset': _stime}

# This dictionary maps a type key to a function. The function should be able to
# decode a sensor value held in the archive packet in the internal, Davis form into US
# units and return it.
_archive_map = {'barometer': _val1000Zero,
                'inTemp': _big_val10,
                'outTemp': _big_val10,
                'highOutTemp': lambda v: float(v / 10.0) if v != -32768 else None,
                'lowOutTemp': _big_val10,
                'inHumidity': _little_val,
                'outHumidity': _little_val,
                'windSpeed': _little_val,
                'windDir': _windDir,
                'windGust': _null_float,
                'windGustDir': _windDir,
                'rain': _val100,
                'rainRate': _val100,
                'ET': _val1000,
                'radiation': _big_val,
                'highRadiation': _big_val,
                'UV': _little_val10,
                'highUV': _little_val10,
                'extraTemp1': _little_temp,
                'extraTemp2': _little_temp,
                'extraTemp3': _little_temp,
                'soilTemp1': _little_temp,
                'soilTemp2': _little_temp,
                'soilTemp3': _little_temp,
                'soilTemp4': _little_temp,
                'leafTemp1': _little_temp,
                'leafTemp2': _little_temp,
                'extraHumid1': _little_val,
                'extraHumid2': _little_val,
                'soilMoist1': _little_val,
                'soilMoist2': _little_val,
                'soilMoist3': _little_val,
                'soilMoist4': _little_val,
                'leafWet1': _little_val,
                'leafWet2': _little_val,
                'leafWet3': _little_val,
                'leafWet4': _little_val,
                'forecastRule': _null,
                'readClosed': _null,
                'readOpened': _null}
