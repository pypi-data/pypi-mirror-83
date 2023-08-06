"""
IPC connection.
"""

from __future__ import absolute_import

import os
from struct import Struct

try:
    # python2's cPickle is an accelerated (C extension) version of pickle:
    import cPickle as pickle
except ImportError:
    # python3's pickle automatically uses the accelerated version and falls
    # back to the python version, see:
    # http://docs.python.org/3.3/whatsnew/3.0.html?highlight=cpickle
    import pickle


__all__ = [
    'Connection',
]

HEADER = Struct("!L")


class Connection(object):

    """
    Pipe-like IPC connection using file objects.

    For most purposes this should behave like the connection objects
    returned by :func:`multiprocessing.Pipe`.

    This class combines two orthogonal functionalities. In general this is
    bad practice, meaning the class should be refactored into two classes,
    but for our specific purpose this will do it.

    - build a bidirectional stream from two unidirectional streams
    - build a serialized connection from pure data streams (pickle)
    """

    def __init__(self, recv, send):
        """Create duplex connection from two unidirectional streams."""
        self._recv = recv
        self._send = send

    def recv(self):
        """Receive a pickled message from the remote end."""
        header = read(self._recv, HEADER.size)
        payload = read(self._recv, *HEADER.unpack(header))
        return pickle.loads(payload)

    def send(self, data):
        """Send a pickled message to the remote end."""
        # '-1' instructs pickle to use the latest protocol version. This
        # improves performance by a factor ~50-100 in my tests:
        payload = pickle.dumps(data, -1)
        self._send.write(HEADER.pack(len(payload)))
        self._send.write(payload)

    def close(self):
        """Close the connection."""
        self._recv.close()
        self._send.close()

    @property
    def closed(self):
        """Check if the connection is fully closed."""
        return self._recv.closed or self._send.closed

    @classmethod
    def from_fd(cls, recv_fd, send_fd):
        """Create a connection from two file descriptors."""
        return cls(os.fdopen(recv_fd, 'rb', 0),
                   os.fdopen(send_fd, 'wb', 0))


def read(file, size):
    """Read a fixed size buffer from """
    parts = []
    while size > 0:
        part = file.read(size)
        if not part:
            raise EOFError
        parts.append(part)
        size -= len(part)
    return b''.join(parts)
