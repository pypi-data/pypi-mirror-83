#
# remt - reMarkable tablet command-line tools
#
# Copyright (C) 2018-2020 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
reMarkable tablet lines format parser.
"""

import contextvars
import enum
import logging
import struct
import typing as tp

from . import data as rdata
from .util import flatten

logger = logging.getLogger(__name__)

T = tp.TypeVar('T')
HEADER_START = b'reMarkable .lines file, version='

CTX_PARSER = contextvars.ContextVar['Version']('version')

TYPE_HEADER_PAGE = tp.Tuple[bytes, int, bytes]
TYPE_PAGE = tp.Tuple[int, int, int]
TYPE_LAYER = tp.Tuple[int]
TYPE_STROKE_V5 = tp.Tuple[int, int, int, float, int, int]
TYPE_STROKE = tp.Tuple[int, int, int, float, int]
TYPE_SEGMENT = tp.Tuple[float, float, float, float, float, float]

@enum.unique
class Version(enum.IntEnum):
    """
    Version of format of reMarkable file.
    """
    VERSION_3 = ord('3')
    VERSION_5 = ord('5')

class Parser(tp.Generic[T]):
    """
    Parser of reMarkable file binary data.

    :var parser: Binary data Struct object.
    """
    def __init__(self, spec: str):
        self.parser = struct.Struct(spec)

    def parse(self, fin: tp.BinaryIO) -> T:
        """
        Read number of bytes from a file and parse the data of a reMarkable
        document item using binary data Struct object.

        :param fin: File object.
        """
        buff = fin.read(self.parser.size)
        return tp.cast(T, self.parser.unpack(buff))

# define parsers for document items found in reMarkable table file format
FMT_HEADER_PAGE = Parser[TYPE_HEADER_PAGE](
    '<{}sB10s'.format(len(HEADER_START))
)
FMT_PAGE = Parser[TYPE_PAGE]('<BBH')  # TODO: might be 'I'
FMT_LAYER = Parser[TYPE_LAYER]('<I')
FMT_STROKE = Parser[TYPE_STROKE]('<IIIfI')
FMT_STROKE_V5 = Parser[TYPE_STROKE_V5]('<IIIfII')
FMT_SEGMENT = Parser[TYPE_SEGMENT]('<ffffff')

def parse(data: tp.BinaryIO, page_number: int) -> rdata.Items:
    """
    Parse reMarkable file and return iterator of document items.

    :param data: reMarkable file data.
    :param page_number: Page number for which data is parsed.
    """
    header, ver, *_ = FMT_HEADER_PAGE.parse(data)
    assert header.startswith(HEADER_START), 'header is {!r}'.format(header)
    CTX_PARSER.set(Version(ver))
    logger.info('file format version {}'.format(chr(ver)))
    yield from parse_page(data, page_number)

def empty_page(page_number: int) \
        -> tp.Iterable[tp.Union[rdata.Page, rdata.PageEnd]]:
    """
    Generate empty page for document rendering.

    :param page_number: Page number to be associated with the page.
    """
    yield rdata.Page(page_number)
    yield rdata.PageEnd(page_number)

def parse_page(data: tp.BinaryIO, page_number: int) \
        -> rdata.Items:
    """
    Parse page from reMarkable table file.
    """
    n, _, _ = FMT_PAGE.parse(data)
    items = (parse_layer(i, data) for i in range(n))

    yield rdata.Page(page_number)
    yield from flatten(items)
    yield rdata.PageEnd(page_number)

def parse_layer(n_layer: int, data: tp.BinaryIO) -> rdata.Items:
    n, = FMT_LAYER.parse(data)

    items = (parse_stroke(i, data) for i in range(n))

    yield rdata.Layer(n_layer)
    yield from flatten(items)

def parse_stroke(n_stroke: int, data: tp.BinaryIO) \
        -> tp.Iterable[rdata.Stroke]:

    ver = CTX_PARSER.get()
    if ver == Version.VERSION_5:
        pen, color, unk1, width, unk2, n = FMT_STROKE_V5.parse(data)
    elif ver == Version.VERSION_3:
        pen, color, a, width, n = FMT_STROKE.parse(data)

    segments = [parse_segment(i, data) for i in range(n)]
    stroke = rdata.Stroke(
        n_stroke,
        rdata.Pen(pen),
        rdata.ColorIndex(color),
        width,
        segments
    )

    yield stroke

def parse_segment(n_seg: int, data: tp.BinaryIO) -> rdata.Segment:
    x, y, speed, direction, width, pressure = FMT_SEGMENT.parse(data)
    return rdata.Segment(n_seg, x, y, speed, direction, width, pressure)

# vim: sw=4:et:ai
