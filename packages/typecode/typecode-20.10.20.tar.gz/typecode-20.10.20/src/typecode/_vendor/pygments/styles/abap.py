# -*- coding: utf-8 -*-
"""
    pygments.styles.abap
    ~~~~~~~~~~~~~~~~~~~~

    ABAP workbench like style.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from typecode._vendor.pygments.style import Style
from typecode._vendor.pygments.token import Keyword, Name, Comment, String, Error, \
    Number, Operator


class AbapStyle(Style):
    default_style = ""
    styles = {
        Comment:                'italic #888',
        Comment.Special:        '#888',
        Keyword:                '#00f',
        Operator.Word:          '#00f',
        Name:                   '#000',
        Number:                 '#3af',
        String:                 '#5a2',

        Error:                  '#F00',
    }
