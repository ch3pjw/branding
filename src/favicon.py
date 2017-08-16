import os
from lxml import etree
from math import sqrt

from svg.ast import (
    Svg, Path, G, Circle, Style, Text, M, V, H, a, Z, ViewBox, Kern)
from svg.shapes import square, circle


static_path = '/static'


off_black = '#1f141f'
record_red = '#e82e1d'

text_select_none_css = '''
    svg text {
        -webkit-user-select: none;
            -moz-user-select: none;
            -ms-user-select: none;
                user-select: none;
    }
'''


def font_css(name, path):
    return '''@font-face {{
    font-family: '{name}';
    src:
        url({path}) format('woff');
}}
    '''.format(name=name, path=path)


raleway_regular_css = font_css(
    'Raleway Concert Regular',
    os.path.join(static_path, 'raleway-regular-concert.woff'))
raleway_medium_css = font_css(
    'Raleway Concert Medium',
    os.path.join(static_path, 'raleway-medium-concert.woff'))


def segment_height(chord_width, radius):
    return radius - sqrt(
        radius ** 2 - (chord_width / 2) ** 2)


def icon_data(base_width=6, inner_r=None, negative=False):
    if inner_r is None:
        inner_r = base_width / 2
    w = base_width / 2
    R = 9
    r = inner_r
    sh = segment_height(w, R)
    c1x, c1y = 18, 49 - sh
    c2x, c2y = 46, 49 - sh
    c3x, c3y = 32, 24 - R + sh
    path = (
        (
            M(8, 32 - w),
            V(32 + w),
            H(18 - w),
            V(40),
            a(R, R, 0, 1, 0, base_width, 0),
            V(32 + w),
            H(46 - w),
            V(40),
            a(R, R, 0, 1, 0, base_width, 0),
            V(32 + w),
            H(56),
            V(32 - w),
            H(32 + w),
            V(24),
            a(R, R, 0, 1, 0, -base_width, 0),
            V(32 - w),
            H(8)
        ) +
        circle(r, c1x, c1y, not negative) +
        circle(r, c2x, c2y, not negative) +
        circle(r, c3x, c3y, not negative) +
        (Z,)
    )
    return path, (c1x, c1y), (c2x, c2y), (c3x, c3y)


def favicon():
    icon_path, *_ = icon_data(negative=True)
    return Path(d=square(64) + icon_path(negative=True))


def brand_icon():
    inner_r = 4
    icon_path, (c1x, c1y), (c2x, c2y), (c3x, c3y) = icon_data(
        base_width=5, inner_r=inner_r)
    return G(
        Circle(cx=c1x, cy=c1y, r=inner_r + 0.1, fill=record_red),
        Circle(cx=c2x, cy=c2y, r=inner_r + 0.1, fill=record_red),
        Circle(cx=c3x, cy=c3y, r=inner_r + 0.1, fill=record_red),
        Path(d=icon_path),
        Path(d=square(74, -5, -5) + square(64, anticlockwise=True))
    )


if __name__ == '__main__':
    s = Svg(
        Style(raleway_medium_css + text_select_none_css),
        brand_icon(),
        Text(
            'Concert',
            font_family='Raleway Concert Medium',
            font_size='62px',
            x=82, y=57.2,
            dx=Kern(0, 0, 2.5, 4, 5, 3, 5)
        ),
        viewBox=ViewBox(-5, -5, 740, 74))
    tree = etree.ElementTree(s._etree)
    with open('../build/foo.svg', 'wb') as f:
        tree.write(
            f, pretty_print=True, xml_declaration=True, encoding='utf-8')
