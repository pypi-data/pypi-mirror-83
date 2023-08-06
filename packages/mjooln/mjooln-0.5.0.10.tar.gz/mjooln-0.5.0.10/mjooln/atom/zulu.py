import logging
import datetime
import pytz
import dateutil
from dateutil.parser import parse as dateparser
import re

logger = logging.getLogger(__name__)


# TODO: Same date in all examples
# TODO: Move examples to separate documentation page?
# TODO: Move Zulustring into main class


class ZuluError(Exception):
    pass


class Zulu(datetime.datetime):
    # TODO: Revise documentation
    """Timezone aware datetime objects in UTC

    From constructor::

        Zulu() or Zulu.now()
            Zulu(2020, 5, 21, 20, 5, 31, 930343, tzinfo=<UTC>)

        Zulu(2020, 5, 12)
            Zulu(2020, 5, 12, 0, 0, tzinfo=<UTC>)

        Zulu(2020, 5, 21, 20, 5, 31)
            Zulu(2020, 5, 21, 20, 5, 31, tzinfo=<UTC>)

        Zulu('20200521T202041u590718Z')
            Zulu(2020, 5, 21, 20, 20, 41, 590718, tzinfo=<UTC>)

    Zulu String is on the format ``<date>T<time>u<microseconds>Z``, and is
    \'designed\'
    to be file name and double click friendly, as well as easily recognizable
    within some string when using regular expressions.
    Printing a Zulu object will result in this string, and the constructor
    can also be instantiated with it::

        z = Zulu(2020, 5, 12)
        print(z)
            20200512T000000u000000Z

        Zulu('20200521T202041u590718Z')
            Zulu(2020, 5, 21, 20, 20, 41, 590718, tzinfo=<UTC>)

    For an ISO 8601 formatted string, use custom function::

        z = Zulu('20200521T202041u590718Z')
        z.iso()
            '2020-05-21T20:20:41.590718+00:00'

    ISO strings can be parsed with a dedicated function, or with constructor::

        z = Zulu.parse_iso('2020-05-21T20:20:41.590718+00:00')
        print(z)
            20200521T202041u590718Z

        z = Zulu('2020-05-21T20:20:41.590718+00:00')
        print(z)
            20200521T202041u590718Z


    Inputs or constructors may vary, but Zulu objects are always UTC. Hence
    the name Zulu.

    Constructor also takes regular datetime objects, provided they have
    timezone info::

        dt = datetime.datetime(2020, 5, 23, tzinfo=pytz.utc)
        Zulu(dt)
            Zulu(2020, 5, 23, 0, 0, tzinfo=<UTC>)

        dt = datetime.datetime(2020, 5, 23, tzinfo=dateutil.tz.tzlocal())
        Zulu(dt)
            Zulu(2020, 5, 22, 22, 0, tzinfo=<UTC>)

    Examples::

        z = Zulu()
        print(z)
            20200522T190137u055918Z
        z.month
            5
        z.str.month
            '05'
        z.str.date
            '20200522'
        z.add(hours=2)
            Zulu(2020, 5, 22, 21, 1, 37, 55918, tzinfo=<UTC>)

    ``Zulu.elf()`` takes the same inputs as constructor, but also allowes
    Zulu objects to pass through. If timezone is missing, it will assume
    local. It can also be told to assume a specific timezone.

    """

    ZTR_FORMAT_STRING = '%Y%m%dT%H%M%Su%fZ'

    ZTR_REGEX_STRING = r'\d{8}T\d{6}u\d{6}Z'
    ZTR_REGEX = re.compile(ZTR_REGEX_STRING)

    ISO_REGEX_STRING = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-' \
                       r'(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):' \
                       r'([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-]' \
                       r'(?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    ISO_REGEX = re.compile(ISO_REGEX_STRING)

    class ZuluString:
        """Initializes convenience strings, and is instantiated with each Zulu
        object and stored in ``Zulu.str``. Meant as the string version of the
        standard datetime.datetime integer values.

        Examples::

            z = Zulu('20200522T190137u055918Z')
            z.year
                2020
            z.str.year
                '2020'
            z.month
                5
            z.str.month
                '05'
            z.day
                22
            z.str.day
                '22'
            z.date()
                datetime.date(2020, 5, 22)
            z.str.date
                '20200522'
            z.time()
                datetime.time(19, 1, 37, 55918)
            z.str.time
                '190137'
            z.str.microsecond
                '055918'

            isinstance(z.str, ZuluString)
                True

        """

        def __init__(self, zulu):
            # Year
            self.year = f'{zulu.year:04d}'
            self.month = f'{zulu.month:02d}'
            self.day = f'{zulu.day:02d}'
            self.hour = f'{zulu.hour:02d}'
            self.minute = f'{zulu.minute:02d}'
            self.second = f'{zulu.second:02d}'
            self.microsecond = f'{zulu.microsecond:06d}'
            self.date = self.year + self.month + self.day
            self.time = self.hour + self.minute + self.second

            self.stub = str(zulu)

            self._zulu_repr = zulu.__repr__()

        def __str__(self):
            return self.stub

        def __repr__(self):
            return f'ZuluString({self._zulu_repr})'

    ############################################################################
    # String methods
    ############################################################################

    @classmethod
    def is_stub(cls,
                ts: str):
        """ Checks if string is Zulu string

        .. note::  The function looks for Zulu String, not ISO 8601

        :param ts: String that might be Zulu
        :type ts: str
        :return: True if string is Zulu, False if not
        :rtype: bool
        """
        return len(ts) == 23 and cls.ZTR_REGEX.match(ts) is not None

    @classmethod
    def is_in(cls,
              text: str):
        """ Check if input text contains a zulu stub

        .. note::  The function looks for Zulu String, not ISO 8601

        :type text: str
        :return: bool
        """
        if cls.ZTR_REGEX.search(text):
            return True
        else:
            return False

    @classmethod
    def find_one(cls,
                 text: str):
        """ Looks for and returns exactly one Zulu from text

        Will fail if there are none or multiple zulu\'s.
        Use find_all() to return a list of zulu\'s in text, including
        an empty list if there are none.

        .. note::  The function looks for Zulu String, not ISO 8601

        :type text: str
        :return: Zulu
        """
        res = cls.find_all(text)
        if not res:
            raise ZuluError(f'No zulu found in this text: {text}. '
                            f'Consider using find_all, which will return '
                            f'empty list if no zulu\'s are found.')
        elif len(res) == 1:
            return res[0]
        else:
            n = len(res)
            raise ZuluError(f'Found more than one (i.e. {n}) '
                            f'zulu in text: {text}. '
                            f'Consider using find_all, which will return '
                            f'a list of all zulu\'s found.')


    @classmethod
    def find_all(cls,
                 text: str):
        """ Finds and returns all zulu\'s in text

        Returns empty list if none are found.

        .. note::  The function looks for Zulu String, not ISO 8601

        :type text: str
        :return: [Zulu]
        """
        ztrs = re.findall(cls.ZTR_REGEX_STRING, text)
        return [cls.from_stub(x) for x in ztrs]

    @classmethod
    def is_iso(cls, ts_str):
        # TODO: Use regex instead, and include check on timezone (optional)
        """Tests if the input string is in fact an
        `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ string

        # .. note:: The test is made by converting the string to datetime
        #     and back again, making sure they are equal

        :param ts_str: Maybe an ISO formatted string
        :return: bool
        """
        try:
            if cls.ISO_REGEX.match(ts_str) is not None:
                return True
        except:
            pass
        return False
        # try:
        #     ts = Zulu._parse_iso(ts_str)
        #     return ts.isoformat() == ts_str
        # except ValueError:
        #     return False

    ############################################################################
    # Timezone methods
    ############################################################################

    @classmethod
    def all_timezones(cls):
        """ Returns a list of all allowed timezone names, except \'local\',
        which will return a datetime object with local timezone

        Wrapper for ``pytz.all_timezones``

        :return: list
        """
        return pytz.all_timezones

    @classmethod
    def _to_utc(cls, ts):
        return ts.astimezone(pytz.utc)

    @classmethod
    def _tz_from_name(cls, tz='utc'):
        if tz == 'local':
            tz = dateutil.tz.tzlocal()
        else:
            try:
                tz = pytz.timezone(tz)
            except pytz.exceptions.UnknownTimeZoneError as ue:
                raise ZuluError(f'Unknown timezone: \'{tz}\'. '
                                f'Use Zulu.all_timezones() for a list '
                                f'of actual timezones')
        return tz

    ############################################################################
    # Create methods
    ############################################################################

    @classmethod
    def now(cls,
            tz=None):
        """
        Overrides ``datetime.datetime.now()``. Equivalent to ``Zulu()``

        :raise ZuluError: If parameter ``tz`` has a value
        :param tz: Do not use. Zulu is always UTC
        :return: Zulu
        """
        if tz:
            raise ZuluError(f'Zulu.now() does not allow input time zone info. '
                            f'Zulu is always UTC. Hence the name')
        return cls()

    @classmethod
    def _from_unaware(cls, ts, tz=None):
        if not tz:
            raise ZuluError('No timezone info. Set timezone to use '
                            'with \'tz=<timezone string>\'. \'local\' will '
                            'use local timezone info. Use '
                            'Zulu.all_timezones() for a list of actual '
                            'timezones')
        return ts.replace(tzinfo=cls._tz_from_name(tz))

    @classmethod
    def _elf(cls, ts, tz=None):
        # Takes a datetime.datetime object and adds the input tzinfo if
        # none is present
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        return ts

    @classmethod
    def from_unaware(cls, ts, tz='utc'):
        """ Create Zulu from timezone unaware datetime

        :param ts: Unaware time stamp
        :type ts: datetime.datetime
        :param tz: Time zone, with 'utc' as default.
            'local' will use local time zone
        :return: Zulu
        """
        if ts.tzinfo:
            raise ZuluError(f'Input datetime already has '
                            f'time zone info: {ts}. '
                            f'Use constructor or Zulu.elf()')
        else:
            ts = cls._from_unaware(ts, tz=tz)
        return cls(ts)

    @classmethod
    def from_unaware_local(cls, ts):
        """ Create Zulu from timezone unaware local timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :return: Zulu
        """
        return cls.from_unaware(ts, tz='local')

    @classmethod
    def from_unaware_utc(cls, ts):
        """ Create Zulu from timezone unaware UTC timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :return: Zulu
        """
        return cls.from_unaware(ts, tz='utc')

    @classmethod
    def _parse_iso(cls,
                   iso: str):
        ts = dateparser(iso)
        if ts.tzinfo and str(ts.tzinfo) == 'tzutc()':
            ts = ts.astimezone(pytz.utc)
        return ts

    @classmethod
    def from_iso(cls,
                 iso: str,
                 tz=None):
        """

        :param iso: ISO 8601 string
        :param tz: Timezone string to use if missing in ts_str
        :return:
        """
        ts = cls._parse_iso(iso)
        if tz and not ts.tzinfo:
            ts = cls._from_unaware(ts, tz)
        elif ts.tzinfo and tz:
            raise ZuluError(f'Timezone info found in ISO string as well as '
                            f'input timezone argument (tz). Keep tz=None, '
                            f'or use Zulu.elf()')
        elif not tz and not ts.tzinfo:
            raise ZuluError('No timezone info in neither ISO string '
                            'nor tz argument')
        return cls(ts)

    @classmethod
    def _parse(cls,
               ts_str: str,
               pattern: str):
        return datetime.datetime.strptime(ts_str, pattern)

    @classmethod
    def parse(cls,
              ts_str: str,
              pattern: str,
              tz=None):
        """Parse time stamp string with the given pattern

        :param ts_str: Timestamp string
        :type ts_str: str
        :param pattern: Follows standard
            `python strftime reference <https://strftime.org/>`_
        :param tz: Timezone to use if timestamp does not have timezone info
        :return: Zulu
        """
        ts = cls._parse(ts_str, pattern)
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        elif tz:
            raise ZuluError('Cannot have an input timezone argument when '
                            'input string already has timezone information')
        return cls(ts)

    @classmethod
    def _from_stub(cls, ztr):
        ts = cls._parse(ztr, cls.ZTR_FORMAT_STRING)
        return cls._from_unaware(ts, tz='utc')

    @classmethod
    def from_stub(cls,
                  ztr: str):
        if not cls.is_stub(ztr):
            raise ZuluError(f'String is not ztr: {ztr}')
        ts = cls._from_stub(ztr)
        return cls(ts)

    @classmethod
    def _from_epoch(cls, epoch):
        ts = datetime.datetime.utcfromtimestamp(epoch)
        return ts.replace(tzinfo=pytz.UTC)

    @classmethod
    def from_epoch(cls, epoch):
        ts = cls._from_epoch(epoch)
        return cls(ts)

    @classmethod
    def _fill_args(cls, args):
        if len(args) < 8:
            # From date
            args = list(args)
            args += (8-len(args))*[0]
            if args[1] == 0:
                args[1] = 1
            if args[2] == 0:
                args[2] = 1
            args = tuple(args)

        if args[-1] not in [None, 0, pytz.utc]:
            raise ZuluError(f'Zulu can only be UTC. '
                            f'Invalid timezone: {args[-1]}')

        args = list(args)
        args[-1] = pytz.utc
        return tuple(args)

    @classmethod
    def elf(cls, *args, tz='local'):
        """General input Zulu constructor

        .. warning:: Elves are fickle

        Handles datetime.datetime, Zulu string, ISO 8601 string and Unix Epoch
        the same way as constructor. However, elf will assume the default
        timezone given in argument ``tz`` if the input has no timezone info.
        Default is ``tz='local'``

        :param args: Input arguments
        :param tz: Time zone to assume if missing. 'local' will use local
            time zone. Use Zulu.all_timezones() for a list of actual
            timezones. Default is 'local'
        :return: Zulu
        """
        if len(args) == 0:
            return cls()
        elif len(args) > 1:
            args = cls._fill_args(args)
            ts = datetime.datetime(*args)
            if not ts.tzinfo:
                ts = cls._from_unaware(ts, tz)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Zulu):
                return arg
            elif isinstance(arg, datetime.datetime):
                # Add timzone if missing
                ts = cls._elf(arg, tz=tz)
                return cls(ts)
            elif isinstance(arg, float):
                return cls.from_epoch(arg)
            elif isinstance(arg, int):
                # Instantiate as start of year
                return cls(arg, 1, 1)
            elif isinstance(arg, str):
                if cls.is_stub(arg):
                    return cls.from_stub(arg)
                elif cls.is_iso(arg):
                    ts = cls._parse_iso(arg)
                    # Add timzone if missing
                    ts = cls._elf(ts, tz=tz)
                else:
                    raise ZuluError(f'String is neither zulu, nor ISO: {arg}. '
                                    f'Use Zulu.parse(). Or a different string')
            else:
                raise ZuluError(f'Found no way to interpret input '
                                f'argument as Zulu: {arg} [{type(arg)}]')
        return cls(ts)


    @classmethod
    def range(cls,
              start=None,
              n=10,
              delta=datetime.timedelta(hours=1)):
        """Generate a list of Zulu of fixed intervals

        ..note:: Mainly for dev purposes. There are far better
            ways of creating a range of timestamps, such as using pandas.

        :param start: Start time Zulu, default is *now*
        :type start: Zulu
        :param n: Number of timestamps in range, with default 10
        :type n: int
        :param delta: Time delta between items, with default one hour
        :type delta: datetime.timedelta
        :return: [Zulu]
        """
        if not start:
            start = cls()
        return [Zulu.elf(start + x * delta) for x in range(n)]

    def __new__(cls, *args, **kwargs):
        # TODO: Cleanup instantiation (ZuluString is used three times)
        # TODO: Cleanup instantiation with only datetime and digits
        if len(args) == 0 and len(kwargs) == 0:
            ts = datetime.datetime.utcnow()
            ts = ts.replace(tzinfo=pytz.UTC)
        elif len(args) == 1 and len(kwargs) == 0:
            arg = args[0]
            if isinstance(arg, str):
                raise ZuluError('Cannot instantiate Zulu with a string. Use '
                                'Zulu.from_iso(), Zulu.from_stub(), '
                                'Zulu.from_string() or Zulu.parse()')
            elif isinstance(arg, float):
                raise ZuluError(f'Cannot create Zulu object from a float: '
                                f'{arg}; If float is unix epoch, '
                                f'use Zulu.epoch()')
            elif isinstance(arg, Zulu):
                raise ZuluError(f'Input argument is already Zulu: {arg}')
            elif isinstance(arg, datetime.datetime):
                ts = arg
                if not ts.tzinfo:
                    raise ZuluError('Cannot create Zulu from datetime if '
                                    'datetime object does not have timezone '
                                    'info. Use Zulu.from_unaware()')
                ts = ts.astimezone(pytz.UTC)
            else:
                raise ZuluError(f'Unable to interpret input argument: '
                                f'{arg} [{type(arg).__name__}]')
        else:
            # Handle input as regular datetime input (year, month, day etc)
            try:
                ts = datetime.datetime(*args)
            except TypeError as te:
                raise ZuluError from te
            # Add timezone info if missing (assume utc, of course)
            if not ts.tzinfo:
                ts = ts.replace(tzinfo=pytz.UTC)

        # Create actual object
        args = tuple([ts.year, ts.month, ts.day,
                      ts.hour, ts.minute, ts.second,
                      ts.microsecond, ts.tzinfo])
        self = super(Zulu, cls).__new__(cls, *args)
        self.str = cls.ZuluString(self)
        return self

    def __str__(self):
        return self.strftime(self.ZTR_FORMAT_STRING)

    def __repr__(self):
        times = [self.hour, self.minute, self.second]
        has_micro = self.microsecond > 0
        has_time = sum(times) > 0
        nums = [self.year, self.month, self.day]
        if has_time or has_micro:
            nums += times
        if has_micro:
            nums += [self.microsecond]
        numstr = ', '.join([str(x) for x in nums])
        return f'Zulu({numstr})'

    def epoch(self):
        """
        Get epoch (seconds since January 1st 1970)

        Wrapper for ``datetime.datetime.timestamp()``

        :return: Seconds since January 1st 1970
        :rtype: float
        """
        return self.timestamp()

    # TODO: Replace with stub in tests
    def stub(self):
        return str(self)

    @classmethod
    def from_string(cls, string):
        if cls.is_stub(string):
            return cls.from_stub(string)
        elif cls.is_iso(string):
            return cls.from_iso(string)
        else:
            raise ZuluError(f'Unknown string format (neither stub nor iso): '
                            f'{string}; '
                            f'Use Zulu.parse() to specify format pattern and '
                            f'timezone')

    def iso(self, full=False):
        # TODO: Implement full flag
        """Create `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ string

        Example::

            z = Zulu(2020, 5, 21)
            z.iso()
                '2020-05-21T00:00:00+00:00'

        :return: str
        """
        if full:
            raise ZuluError('Full isoformat not implemented. Full means it '
                            'has fixed length no matter the value')
        return self.isoformat()

    def format(self, pattern):
        """Format Zulu to string with the given pattern

        :param pattern: Follows standard
            `Python strftime reference <https://strftime.org/>`_
        :return: str
        """
        return self.strftime(pattern)

    def to_unaware(self):
        """
        Get timezone unaware datetime object in UTC

        :return: Timezone unaware datetime
        :rtype: datetime.datetime
        """
        return datetime.datetime.utcfromtimestamp(self.epoch())

    def to_tz(self, tz='local'):
        """ Create regular datetime with input timezone

        For a list of timezones use :meth:`.Zulu.all_timezones()`, which is a
        wrapper for

        :param tz: Time zone to use. 'local' will return the local time zone.
            Default is 'local'
        :return: datetime.datetime
        """
        ts_utc = datetime.datetime.utcfromtimestamp(self.epoch())
        ts_utc = ts_utc.replace(tzinfo=pytz.UTC)
        return ts_utc.astimezone(self._tz_from_name(tz))

    def to_local(self):
        """ Create regular datetime with local timezone

        :return: datetime.datetime
        """
        return self.to_tz(tz='local')

    @classmethod
    def delta(cls,
              days=0,
              hours=0,
              minutes=0,
              seconds=0,
              microseconds=0,
              weeks=0):
        """Wrapper for datetime.timedelta

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: datetime.timedelta
        """
        return datetime.timedelta(days=days,
                                  hours=hours,
                                  minutes=minutes,
                                  seconds=seconds,
                                  microseconds=microseconds,
                                  weeks=weeks)

    def add(self,
            days=0,
            hours=0,
            minutes=0,
            seconds=0,
            microseconds=0,
            weeks=0):
        """Adds the input to current Zulu object and returns a new one

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: Zulu
        """
        delta = self.delta(days=days,
                           hours=hours,
                           minutes=minutes,
                           seconds=seconds,
                           microseconds=microseconds,
                           weeks=weeks)
        return Zulu(self + delta)
