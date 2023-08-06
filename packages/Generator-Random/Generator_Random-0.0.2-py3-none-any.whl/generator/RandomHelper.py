import struct
import time
from os import urandom as _urandom


def _lastbit(f):
    """generate randomness based on a clock drift"""
    return struct.pack('!f', f)[-1] & 1


def _getrandbits(k):
    """Return k random bits using a relative drift of two clocks.
    Once you have getrandbits(k), it is straigforward to get a random
     integer in range [a, b], including both end points"""
    # assume time.sleep() and time.clock() use different clocks
    # though it might work even if we use the same clock
    # XXX it does not produce "good" random bits, see below for details
    result = 0
    for _ in range(k):
        time.sleep(0)
        result <<= 1
        result |= _lastbit(time.clock())
    return result


def _randbelow(n):
    """Return a random int in the range [0,n).  Raises ValueError if n<=0"""

    if n <= 0:
        raise ValueError
    k = n.bit_length()  # don't use (n-1) here because n can be 1
    r = _getrandbits(k)  # 0 <= r < 2**k
    while r >= n:  # avoid skew
        r = _getrandbits(k)
    return r


def singelton_int_bit(a, b):
    """Return random integer in range [a, b], including both end points"""
    return a + _randbelow(b - a + 1)


""
BPF = 53  # Number of bits in a float
RECIP_BPF = 2 ** -BPF


def from_bytes(cls, bytes, byteorder, *args,
               **kwargs):  # real signature unknown; NOTE: unreliably restored from __doc__
    """
    int.from_bytes(bytes, byteorder, *, signed=False) -> int

    Return the integer represented by the given array of bytes.

    The bytes argument must be a bytes-like object (e.g. bytes or bytearray).

    The byteorder argument determines the byte order used to represent the
    integer.  If byteorder is 'big', the most significant byte is at the
    beginning of the byte array.  If byteorder is 'little', the most
    significant byte is at the end of the byte array.  To request the native
    byte order of the host system, use `sys.byteorder' as the byte order value.

    The signed keyword-only argument indicates whether two's complement is
    used to represent the integer.
    """
    pass


def singelton_float_bit():
    """Get the next random number in the range [0.0, 1.0)."""
    return (int.from_bytes(_urandom(7), 'big') >> 3) * RECIP_BPF
