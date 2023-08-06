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
PDF annotations indexer.
"""

import cytoolz.functoolz as ftz  # type: ignore
import textwrap
import typing as tp
from functools import partial, reduce
from statistics import fmean

from .data import DocumentItem, Items, Pen, Page, Stroke, TextSelection, \
    PEN_WIDTH_HIGHLIGHTER
from .pdf import Poppler, pdf_text
from .util import split, to_point_y

FMT_PAGE = 'Page {} ({})'.format

PageStrokes = tp.Iterable[tp.Tuple[Page, tp.Tuple[Stroke]]]
PageTexts = tp.Iterable[tp.Tuple[Poppler.Page, tp.Iterable[str]]]

def ann_text(pdf_doc: Poppler.Document, items: Items) -> PageTexts:
    """
    Get annotated text from PDF document using document items parsed from
    reMarkable file.
    """
    get_page = pdf_doc.get_page
    strokes = page_strokes(items)
    selections = ((p, page_selections(s)) for p, s in strokes)

    # get PDF pages
    pages = ((get_page(p.number), s) for p, s in selections)

    # for each page and stroke get text under stroke
    texts = ((p, t) for p, s in pages if (t := page_text(p, s)))
    yield from texts

def page_strokes(items: Items) -> PageStrokes:
    """
    Get reMarkable tablet page and stroke information.
    """
    is_page = ftz.flip(isinstance, Page)

    # find pages and strokes
    items = (v for v in items if is_page(v) or is_highlighter(v))

    # split into (page, strokes)
    yield from split(is_page, items)

def page_selections(strokes: tp.Tuple[Stroke]) -> tp.List[TextSelection]:
    """
    Detect line selections from reMarkable table stroke data.

    The line selections are sorted and overlapping line selections are
    merged.
    """
    selections = [sel for st in strokes if (sel := to_line_selection(st))]
    selections = sorted(selections)
    return merge_line_selection(selections)

def page_text(page: Poppler.Page, selections: tp.List[TextSelection]) \
        -> tp.List[str]:
    """
    Get text for each page stroke.

    Empty strings are filtered out.

    :param page: Poppler PDF page object.
    :param selections: Collection of text selections.
    """
    to_text = partial(pdf_text, page)
    return [t for s in selections if (t := to_text(s))]

def fmt_ann_text(items: PageTexts) -> tp.Iterable[tp.Tuple[str, str]]:
    """
    Format annotated text read from PDF document as reStructuredText
    document.
    """
    texts = ((fmt_header(p), fmt_text(t)) for p, t in items)
    yield from texts

def fmt_header(page: Poppler.Page) -> str:
    """
    Format page header in reStructuredText format.
    """
    header = FMT_PAGE(page.get_label(), page.get_index())
    return '{}\n{}'.format(header, '=' * len(header))

def fmt_text(texts: tp.Iterable[str]) -> str:
    """
    Format collection of text items in reStructuredText format.
    """
    result = '\n'.join(texts)
    result = textwrap.indent(result, ' ' * 4)
    result = '::\n\n{}\n'.format(result)
    return result

def is_highlighter(item: DocumentItem) -> bool:
    """
    Check if reMarkable tablet data item is a highlighter.

    :pram item: reMarkable data item data.
    """
    return isinstance(item, Stroke) and Pen.is_highlighter(item.pen)

def is_horizontal_line(
        y_min: float,
        y_max: float,
        ys: float,
        width: float,
    ) -> bool:
    """
    Check if stroke with y-axis coordinates between `y_min` and `y_max`
    values can be treated as horizontal line at `ys` of certain width.

    :param y_min: Minimum y-axis coordinate of a candidate line.
    :param y_max: Maximum y-axis coordinate of a candidate line.
    :param ys: Horizontal line y-axis coordinate.
    :param width: Horizontal line width.
    """
    w = width / 2
    return y_min >= ys - w and ys + w >= y_max

def to_line_selection(stroke: Stroke) -> tp.Optional[TextSelection]:
    """
    Create text selection data from a reMarkable tablet stroke information.

    If stroke does not create a horizontal line, then null is returned.

    :param stroke: reMarkable tablet stroke information.
    """
    x1 = min(s.x for s in stroke.segments)
    x2 = max(s.x for s in stroke.segments)
    y1 = min(s.y for s in stroke.segments)
    y2 = max(s.y for s in stroke.segments)

    ys = fmean(to_point_y(s) for s in stroke.segments)

    w = 1.1 * PEN_WIDTH_HIGHLIGHTER / 2  # allow 10% wiggle room
    if is_horizontal_line(y1, y2, ys, w):
        return TextSelection(x1, x2, ys)
    else:
        return None

def merge_line_selection(selections: tp.Iterable[TextSelection]) \
        -> tp.List[TextSelection]:
    """
    Merge text selection data if text selection data overlaps.

    The input should be sorted using text selection ordering.
    """
    return reduce(merge_line_selection_item, selections, [])

def merge_line_selection_item(acc: tp.List[TextSelection], ls: TextSelection) \
        -> tp.List[TextSelection]:

    to_merge = acc and acc[-1].overlaps(ls, PEN_WIDTH_HIGHLIGHTER)
    result, item = (acc[:-1], acc[-1].merge(ls)) if to_merge else (acc, ls)
    return result + [item]

# vim: sw=4:et:ai
