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
Unit tests for methods of data classes representing reMarkable tablet
information.
"""

from ..data import Pen, TextSelection

def test_pen_higlighter():
    """
    Test checking if a pen is a highlighter.
    """
    assert Pen.is_highlighter(Pen.HIGHLIGHTER_1)
    assert Pen.is_highlighter(Pen.HIGHLIGHTER_2)
    assert not Pen.is_highlighter(Pen.FINELINER_1)

def test_text_selection_order():
    """
    Test sorting of text selection.
    """
    items = [
        TextSelection(50, 100, 15),
        TextSelection(10, 40, 15),
        TextSelection(10, 100, 25),
        TextSelection(10, 100, 5),
    ]
    result = sorted(items)

    expected = [
        TextSelection(10, 100, 5),
        TextSelection(10, 40, 15),
        TextSelection(50, 100, 15),
        TextSelection(10, 100, 25),
    ]

    assert expected == list(result)

def test_text_selection_overlap():
    """
    Test overlapping check of text selections.
    """
    ts1 = TextSelection(10, 100, 15)
    ts2 = TextSelection(101, 200, 20)
    ts3 = TextSelection(100, 200, 20)

    assert not ts1.overlaps(ts2, 10)
    assert ts1.overlaps(ts3, 10)
    assert ts2.overlaps(ts3, 10)
    assert not ts1.overlaps(ts3, 1)

def test_text_selection_merge():
    """
    Test merging f text selections.
    """
    ts1 = TextSelection(10, 100, 15)
    ts2 = TextSelection(101, 200, 25)

    assert TextSelection(10, 200, 20) == ts1.merge(ts2)

# vim: sw=4:et:ai
