# Copyright 2019-2020 Rémy Taymans <remytms@tsmail.eu>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

"""Library to read and write a Zoom R16 project file."""

__productname__ = "zoomrlib"
__version__ = "1.0.0"
__copyright__ = "Copyright 2019 Rémy Taymans"
__author__ = "Rémy Taymans"
__author_email__ = "remytms@tsmail.eu"
__description__ = "Library to read and write a ZoomR16 project file"
__url__ = "https://gitlab.com/remytms/zoomrlib"
__license__ = "GPL-3.0+"


import io

from .lib import MUTE, PLAY, REC, Project


# pylint: disable=redefined-builtin
def open(file, mode="r", **kwargs):
    """
    Open a zoom project file as bytes. The returned object can be
    directly given to `load()` or `dump()`.

    :param mode: reading "r" mode or writing "w" mode.
    :type mode: str

    It's a wrapper around `io.open()` which ensure that `io.open()` is
    used with binary mode.
    """
    if not isinstance(mode, str):
        raise TypeError("Invalid mode: %r" % mode)
    if mode not in ("r", "w"):
        raise ValueError("Invalid mode: %r. Choose between 'r' or 'w'." % mode)
    return io.open(file, mode + "b", **kwargs)


def load(fp):
    """
    Convert fp (a .read()-supporting file-like object representing the
    content of a prjdata.zdt file as bytes) to a zoomrlib.Project
    object.

    :param fp: a file-like object with the content of prjdata.zdt as
    byte.
    """
    return Project(raw=fp.read())


def dump(obj, fp):
    """
    Write ojb (a zoomrlibProject object) into fp (a .read()-supporting
    file-like object).

    :param obj: a zoomrlib.Project object.
    :type obj: zoomrlib.Project

    :param fp: a file-like object with the content of prjdata.zdt as
    byte.
    """
    if not isinstance(obj, Project):
        raise TypeError("Invalid obj type: %s" % type(obj))
    return fp.write(obj.raw)
