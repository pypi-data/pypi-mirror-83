# -*- encoding: utf-8 -*-
# pass import - Passwords importer swiss army knife
# Copyright (C) 2017-2020 Alexandre PUJOL <alexandre@pujol.io>.
#

import io
import os
from abc import ABC
from enum import IntFlag, auto

from pass_import.errors import PMError

_MANAGERS = set()
_DETECTERS = set()


def register_managers(*managers):
    """Register new password manager(s)."""
    for cls in managers:
        _MANAGERS.add(cls)


def register_detecters(*detecters):
    """Register new detecter(s)."""
    for cls in detecters:
        _DETECTERS.add(cls)


def get_managers():
    """Return the registered password manager set."""
    return _MANAGERS


def get_detecters():
    """Return the registered detecter set."""
    return _DETECTERS


class Cap(IntFlag):
    """Set the class capabilities (IMPORT, EXPORT, FORMAT, DECRYPT)."""
    UNKNOWN = auto()
    IMPORT = auto()
    EXPORT = auto()
    FORMAT = auto()
    DECRYPT = auto()


class Asset(ABC):
    """Password managers/detectors abstract assets.

    :param Cap cap: Capabilities of the class.
    :param str name: Name of the password manager.
    :param str format: Format of the password manager supported.
    :param str version: Version of the password manager supported.
    :param bool default: ``True`` is the pm is the default pm with its name.
    :param bool only: On header check, set if the file can have more header
        than the headers set in the header list or dict given by
        :func:`~header`. Default: ``False``. Required by some managers that
        contain only a very generic header.
    :param str encoding: File encoding, default: ``utf-8``
    :param str mode: File reading mode, default: ``r``

    """
    cap = Cap.UNKNOWN
    name = ''
    format = ''
    version = ''
    default = True
    only = False
    encoding = 'utf-8'
    mode = 'r'

    def __init__(self, prefix=None):
        """Asset manager initialisation.

        :param prefix: (optional) Path, identifiant of the pm. It can also
            be a file object. Therefore, the passwords are read from it.
        :param dict settings: (optional) Additional settings for the pm.

        """
        self.prefix = None
        self.file = None
        if isinstance(prefix, io.IOBase):
            self.file = prefix
        else:
            self.prefix = prefix
        super(Asset, self).__init__()

    def open(self):
        """Open the file at ``prefix``."""
        if self.file is None:
            self.file = open(self.prefix, self.mode, encoding=self.encoding)

    def close(self):
        """Close the file."""
        if isinstance(self.file, io.IOBase):
            self.file.close()

    def exist(self):
        """Ensure the file/repository exist."""
        if isinstance(self.file, io.IOBase):
            return True
        return os.path.isfile(self.prefix)

    @classmethod
    def isvalid(cls):
        """Ensure the user has the credential to use the file/repository."""
        return True

    def __enter__(self):
        """Enter the context manager."""
        if not self.exist():
            raise PMError("%s is not a password repository." % self.prefix)
        if not self.isvalid():
            raise PMError(
                "invalid credentials, password encryption/decryption aborted.")

        self.open()
        return self

    def __exit__(self, *exc):
        """Leave the context manager."""
        self.close()
