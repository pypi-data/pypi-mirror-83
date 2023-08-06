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
PDF utilities.
"""

import gi  # type: ignore
gi.require_version('Poppler', '0.18')  # noqa: E402

import pathlib  # noqa: E402
from gi.repository import Poppler  # type: ignore  # noqa: E402

from . import const  # noqa: E402
from .data import TextSelection  # noqa: E402


def pdf_open(fn: str) -> Poppler.Document:
    """
    Open PDF file and return Poppler library PDF document.

    :param fn: PDF file name.
    """
    path = pathlib.Path(fn).resolve().as_uri()
    return Poppler.Document.new_from_file(path)

def pdf_scale(page: Poppler.Page) -> float:
    """
    Get scaling factor for a PDF page to fit reMarkable tablet vector data
    onto the page.

    :param page: Poppler PDF page object.
    """
    w, h = page.get_size()
    return max(w / const.PAGE_WIDTH, h / const.PAGE_HEIGHT)

def pdf_area(page: Poppler.Page, selection: TextSelection) \
        -> Poppler.Rectangle:
    """
    Get PDF page area for a text selection data.

    :param page: Poppler PDF page object.
    :param selection: Text selection data.
    """
    factor = pdf_scale(page)
    y = selection.y * factor

    area = Poppler.Rectangle()
    area.x1 = selection.x1 * factor
    area.y1 = y - 1
    area.x2 = selection.x2 * factor
    area.y2 = y + 1

    return area

def pdf_text(page: Poppler.Page, selection: TextSelection) -> str:
    """
    Having a reMarkable tablet stroke data, get text annotated by the
    stroke.

    :param page: Poppler PDF page object.
    :param stroke: Text selection data.
    """
    area = pdf_area(page, selection)
    return page.get_text_for_area(area)

# vim: sw=4:et:ai
