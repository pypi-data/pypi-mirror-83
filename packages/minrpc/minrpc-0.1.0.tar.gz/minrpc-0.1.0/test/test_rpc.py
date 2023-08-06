from __future__ import absolute_import

# standard library
import os
import tempfile
import unittest

# tested modules
from minrpc.client import Client


class TestRPC(unittest.TestCase):

    # This test is currently only useful for windows. On linux open file
    # descriptors don't prevent the file from being deleted.
    # TODO: change this test such that it checks "directly" whether the file
    # handle is still open.
    def test_no_leaking_file_handles(self):
        fd, filename = tempfile.mkstemp()
        svc, proc = Client.spawn_subprocess()
        os.close(fd)
        try:
            os.remove(filename)
            file_can_be_deleted = True
        except OSError:
            file_can_be_deleted = False
        svc.close()
        proc.wait()
        if not file_can_be_deleted:
            os.remove(filename)
        self.assertTrue(file_can_be_deleted)

    # TODO: add tests to check that other resources get closed correctly.


if __name__ == '__main__':
    unittest.main()
