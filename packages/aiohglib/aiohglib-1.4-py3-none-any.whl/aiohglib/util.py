import os, subprocess, sys, asyncio
import pytz
from aiohglib import error
try:
    from io import BytesIO
except ImportError:
    from io import StringIO as BytesIO
try:
    import chardet
except ImportError:
    chardet = None

integertypes = (int,)

def b(s):
    """Encode the string as bytes."""
    return s.encode('utf-8')

def u(obj, enable_chardet=False):
    if type(obj) is not str:
        if enable_chardet and chardet is not None:
            result = chardet.detect(obj)
        else:
            result = {}
        if "encoding" in result and result["encoding"]:
            return obj.decode(result["encoding"])
        return obj.decode("utf-8")
    return obj

def strtobytes(s):
    """Return the bytes of the string representation of an object."""
    return str(s).encode('utf-8')

def grouper(n, iterable):
    ''' list(grouper(2, range(4))) -> [(0, 1), (2, 3)] '''
    args = [iter(iterable)] * n
    return zip(*args)

def eatlines(s, n):
    """
    >>> eatlines(b("1\\n2"), 1) == b('2')
    True
    >>> eatlines(b("1\\n2"), 2) == b('')
    True
    >>> eatlines(b("1\\n2"), 3) == b('')
    True
    >>> eatlines(b("1\\n2\\n3"), 1) == b('2\\n3')
    True
    """
    cs = BytesIO(s)

    for line in cs:
        n -= 1
        if n == 0:
            return cs.read()
    return b('')

def skiplines(s, prefix):
    """
    Skip lines starting with prefix in s

    >>> skiplines(b('a\\nb\\na\\n'), b('a')) == b('b\\na\\n')
    True
    >>> skiplines(b('a\\na\\n'), b('a')) == b('')
    True
    >>> skiplines(b(''), b('a')) == b('')
    True
    >>> skiplines(b('a\\nb'), b('b')) == b('a\\nb')
    True
    """
    cs = BytesIO(s)

    for line in cs:
        if not line.startswith(prefix):
            return line + cs.read()

    return b('')

def _cmdval(val):
    if isinstance(val, bytes):
        return val
    else:
        return strtobytes(val)

def cmdbuilder(name, *args, **kwargs):
    """
    A helper for building the command arguments

    args are the positional arguments

    kwargs are the options
    keys that are single lettered are prepended with '-', others with '--',
    underscores are replaced with dashes

    keys with False boolean values are ignored, lists add the key multiple times

    None arguments are skipped

    >>> cmdbuilder(b('cmd'), a=True, b=False, c=None) == [b('cmd'), b('-a')]
    True
    >>> cmdbuilder(b('cmd'), long=True) == [b('cmd'), b('--long')]
    True
    >>> cmdbuilder(b('cmd'), s=b('hort')) == [b('cmd'), b('-short')]
    True
    >>> cmdbuilder(b('cmd'), str=b('s')) == [b('cmd'), b('--str=s')]
    True
    >>> cmdbuilder(b('cmd'), d_ash=True) == [b('cmd'), b('--d-ash')]
    True
    >>> cmdbuilder(b('cmd'), _=True) == [b('cmd'), b('-')]
    True
    >>> cmdbuilder(b('cmd'), l=[1, 2]) == [b('cmd'), b('-l1'), b('-l2')]
    True
    >>> expect = [b('cmd'), b('--list=1'), b('--list=2')]
    >>> cmdbuilder(b('cmd'), list=[1, 2]) == expect
    True
    >>> cmdbuilder(b('cmd'), None) == [b('cmd')]
    True
    >>> cmdbuilder(b('cmd'), b('-a')) == [b('cmd'), b('--'), b('-a')]
    True
    >>> cmdbuilder(b('cmd'), b('')) == [b('cmd'), b('--'), b('')]
    True
    >>> cmdbuilder(b('cmd'), s=b('')) == [b('cmd'), b('-s'), b('')]
    True
    >>> cmdbuilder(b('cmd'), s=[b('')]) == [b('cmd'), b('-s'), b('')]
    True
    >>> cmdbuilder(b('cmd'), long=b('')) == [b('cmd'), b('--long=')]
    True
    """
    cmd = [name]
    for arg, val in list(kwargs.items()):
        if val is None:
            continue

        arg = pfx = arg.encode('latin-1').replace(b('_'), b('-'))
        short = (len(arg) == 1)
        if arg != b('-'):
            if short:
                arg = pfx = b('-') + arg
            else:
                arg = b('--') + arg
                pfx = arg + b('=')
        if isinstance(val, bool):
            if val:
                cmd.append(arg)
        elif isinstance(val, list):
            for v in val:
                s = _cmdval(v)
                if s or not short:
                    cmd.append(pfx + s)
                else:
                    cmd.extend([arg, s])
        else:
            s = _cmdval(val)
            if s or not short:
                cmd.append(pfx + s)
            else:
                cmd.extend([arg, s])

    args = [a for a in args if a is not None]
    if args:
        cmd.append(b('--'))
    for a in args:
        cmd.append(a)

    return cmd

class reterrorhandler(object):
    """This class is meant to be used with rawcommand() error handler
    argument. It remembers the return value the command returned if
    it's one of allowed values, which is only 1 if none are given.
    Otherwise it raises a CommandError.

    >>> e = reterrorhandler('')
    >>> bool(e)
    True
    >>> e(1, 'a', '')
    'a'
    >>> bool(e)
    False

    """
    def __init__(self, args, allowed=None):
        self.args = args
        self.ret = 0
        if allowed is None:
            self.allowed = [1]
        else:
            self.allowed = allowed

    def __call__(self, ret, out, err):
        self.ret = ret
        if ret not in self.allowed:
            raise error.CommandError(self.args, ret, out, err)
        return out

    def __bool__(self):
        """ Returns True if the return code was 0, False otherwise """
        return self.ret == 0


class propertycache(object):
    """
    Decorator that remembers the return value of a function call.

    >>> execcount = 0
    >>> class obj(object):
    ...     def func(self):
    ...         global execcount
    ...         execcount += 1
    ...         return []
    ...     func = propertycache(func)
    >>> o = obj()
    >>> o.func
    []
    >>> execcount
    1
    >>> o.func
    []
    >>> execcount
    1
    """
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    def __get__(self, obj, type=None):
        result = self.func(obj)
        setattr(obj, self.name, result)
        return result

POSSIBLE_TIMEZONES = [
        pytz.UTC,
        pytz.timezone("Europe/Prague"),
        pytz.timezone("Europe/London"),
        pytz.timezone("Africa/Cairo"),
        pytz.timezone("Europe/Brussels"),
        pytz.timezone("Europe/Moscow"),
        pytz.timezone("Atlantic/Azores"),
        pytz.timezone("Asia/Tehran"),
        pytz.timezone("Atlantic/South_Georgia"),
        pytz.timezone("Asia/Dubai"),
        pytz.timezone("America/Argentina/Buenos_Aires"),
        pytz.timezone("Asia/Kabul"),
        pytz.timezone("Canada/Newfoundland"),
        pytz.timezone("Asia/Tashkent"),
        pytz.timezone("America/Caracas"),
        pytz.timezone("Asia/Kolkata"),
        pytz.timezone("America/New_York"),
        pytz.timezone("Asia/Kathmandu"),
        pytz.timezone("America/Mexico_City"),
        pytz.timezone("Asia/Dhaka"),
        pytz.timezone("Canada/Mountain"),
        pytz.timezone("Asia/Yangon"),
        pytz.timezone("America/Los_Angeles"),
        pytz.timezone("Asia/Jakarta"),
        pytz.timezone("America/Anchorage"),
        pytz.timezone("Asia/Shanghai"),
        pytz.timezone("Pacific/Marquesas"),
        pytz.timezone("Australia/Eucla"),
        pytz.timezone("Pacific/Honolulu"),
        pytz.timezone("Asia/Tokyo"),
        pytz.timezone("Pacific/Niue"),
        pytz.timezone("Australia/Darwin"),
        pytz.timezone("Australia/Brisbane"),
        pytz.timezone("Australia/Adelaide"),
        pytz.timezone("Australia/Melbourne"),
        pytz.timezone("Asia/Anadyr"),
        pytz.timezone("Pacific/Auckland"),
        pytz.timezone("Pacific/Chatham"),
        pytz.timezone("Pacific/Kiritimati"),
    ]

close_fds = os.name == 'posix'
stream_limit = 1024

startupinfo = None
if os.name == 'nt':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

def popen(args, env=None):
    environ = None
    if env:
        environ = dict(os.environ)
        environ.update(env)

    return asyncio.create_subprocess_exec(args[0], *args[1:], stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, close_fds=close_fds,
            startupinfo=startupinfo, env=environ, limit=stream_limit)
