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
reMarkable strokes drawing using Cairo library.
"""

import cairo
import io
import itertools
import logging
import os.path
import pkgutil
from collections import defaultdict
from contextlib import contextmanager
from functools import singledispatch, lru_cache, partial

from . import const, tool
from . import data as rdata
from .pdf import pdf_open, pdf_scale

logger = logging.getLogger(__name__)

COLOR_STROKE = {
    rdata.ColorIndex.BLACK: rdata.Color(0, 0, 0, 1),
    rdata.ColorIndex.GREY: rdata.Color(0.5, 0.5, 0.5, 1),
    rdata.ColorIndex.WHITE: rdata.Color(1, 1, 1, 1),
}

COLOR_HIGHLIGHTER = rdata.Color(1.0, 0.8039, 0.0, 0.1)

STYLE_DEFAULT = rdata.Style(
    tool.single_line,
    COLOR_STROKE[rdata.ColorIndex.BLACK],
    cairo.LINE_JOIN_ROUND,
    cairo.LINE_CAP_ROUND,
)
style_default = STYLE_DEFAULT._replace

STYLE_HIGHLIGHTER = rdata.Style(
    tool.line_highlighter,
    COLOR_HIGHLIGHTER,
    cairo.LINE_JOIN_ROUND,
    cairo.LINE_CAP_SQUARE,
)

STYLE_MARKER = style_default(
    tool_line=tool.line_marker,
    brush='marker.png',
)

STYLE_PENCIL = style_default(
    tool_line=tool.line_mechanical_pencil,
    brush='pencil.png',
)

STYLE_ERASER = rdata.Style(
    tool.line_eraser,
    COLOR_STROKE[rdata.ColorIndex.WHITE],
    cairo.LINE_JOIN_ROUND,
    cairo.LINE_CAP_ROUND,
)

STYLE_UNKNOWN_TOOL = style_default(tool_line=tool.line_unknown, dash=[1, 5])

STYLE = defaultdict(lambda: STYLE_UNKNOWN_TOOL, {
    # Ballpoint
    rdata.Pen.BALLPOINT_1: style_default(tool_line=tool.line_ballpoint),
    rdata.Pen.BALLPOINT_2: style_default(tool_line=tool.line_ballpoint),

    # Fineliner
    rdata.Pen.FINELINER_1: style_default(tool_line=tool.line_fineliner),
    rdata.Pen.FINELINER_2: style_default(tool_line=tool.line_fineliner),

    # Marker
    rdata.Pen.MARKER_1: STYLE_MARKER,
    rdata.Pen.MARKER_2: STYLE_MARKER,

    # Highlighter
    rdata.Pen.HIGHLIGHTER_1: STYLE_HIGHLIGHTER,
    rdata.Pen.HIGHLIGHTER_2: STYLE_HIGHLIGHTER,

    # Eraser
    rdata.Pen.ERASER: STYLE_ERASER,

    # Mechanical pencil
    rdata.Pen.MECHANICAL_PENCIL_1: STYLE_PENCIL,
    rdata.Pen.MECHANICAL_PENCIL_2: STYLE_PENCIL,

    # Erase area
    rdata.Pen.ERASER_AREA: STYLE_ERASER._replace(
        tool_line=tool.line_erase_area
    ),
})


path_brush = partial(os.path.join, 'brush')

@lru_cache(maxsize=4)
def load_brush(fn: str):
    data = pkgutil.get_data('remt', path_brush(fn))
    assert data is not None
    img = cairo.ImageSurface.create_from_png(io.BytesIO(data))
    brush = cairo.SurfacePattern(img)
    brush.set_extend(cairo.EXTEND_REPEAT)
    return brush

@singledispatch
def draw(item, context):
    raise NotImplementedError('Unknown item to draw: {}'.format(item))

@draw.register(rdata.Page)
def _page(page, context):
    surface = context.cr_surface
    page_number = next(context.page_number)
    if page_number:
        surface.show_page()

    if context.pdf_doc:
        # get page and set size of the current page of the cairo surface
        pdf_page = context.pdf_doc.get_page(page_number)
        w, h = pdf_page.get_size()
        surface.set_size(w, h)

        cr = context.cr_ctx
        # render for printing to keep the quality of the document
        pdf_page.render_for_printing(cr)

        # render remarkable lines data at scale to fit the document
        cr.save()  # to be restored at page end
        factor = pdf_scale(pdf_page)
        cr.scale(factor, factor)

@draw.register(rdata.PageEnd)
def _page_end(page, context):
    if context.pdf_doc:
        context.cr_ctx.restore()

@draw.register(rdata.Layer)
def _layer(layer, context):
    pass

@draw.register(rdata.Stroke)
def _stroke(stroke, context):
    style = STYLE[stroke.pen]
    if style is STYLE_UNKNOWN_TOOL:
        logger.debug('Not supported pen for stroke: {}'.format(stroke))

    # if no predefined style color, then use stroke color
    assert stroke.color in (0, 1, 2)
    color = style.color
    color = COLOR_STROKE[stroke.color] if color is None else color

    cr = context.cr_ctx
    cr.save()

    draw_stroke = partial(draw_fill, cr) if stroke.pen == 8 else cr.stroke

    cr.set_source_rgba(*color)
    cr.set_line_join(style.join)
    cr.set_line_cap(style.cap)

    if style.dash:
        cr.set_dash(style.dash, 0)

    if style.brush:
        brush = load_brush(style.brush)
        cr.set_source(brush)

    lines = style.tool_line(stroke)
    draw_multi_line(cr, draw_stroke, lines)

    cr.restore()

def draw_multi_line(cr, draw_stroke, lines):
    """
    Draw multiple lines.

    A line is tuple

    - width of a line
    - collection of points

    :param cr: Cairo context.
    :param draw_stroke: Drawing stroke function (i.e. line or filled area).
    :param lines: Collection of lines to draw.
    """
    for width, points in lines:
        # on new path, the position of point is undefined and first
        # `line_to` call acts as `move_to`
        cr.new_path()
        cr.set_line_width(width)
        for x, y in points:
            cr.line_to(x, y)
        draw_stroke()

def draw_fill(cr):
    """
    Draw Cairo shape and fill.
    """
    cr.close_path()
    cr.fill()

@contextmanager
def draw_context(fn_pdf, fn_out):
    pdf_doc = pdf_open(fn_pdf) if fn_pdf else None
    surface = cairo.PDFSurface(fn_out, const.PAGE_WIDTH, const.PAGE_HEIGHT)
    try:
        cr_ctx = cairo.Context(surface)
        context = rdata.Context(surface, cr_ctx, pdf_doc, itertools.count())
        yield context
    finally:
        surface.finish()

# vim: sw=4:et:ai
