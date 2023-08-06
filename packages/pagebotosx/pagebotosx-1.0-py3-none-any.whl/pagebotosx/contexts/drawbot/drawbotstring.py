#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     drawbotstring.py
#

import re
from AppKit import NSAttributeDictionary, NSRange
from CoreText import (CTFramesetterCreateWithAttributedString,
        CTFramesetterCreateFrame, CTFrameGetLines, CTFrameGetLineOrigins)
from Quartz import CGPathAddRect, CGPathCreateMutable, CGRectMake
from pagebot.constants import LEFT, DEFAULT_FONT_SIZE, DEFAULT_LEADING
from pagebot.contexts.base.babelstring import getLineHeight, BabelString
from pagebot.toolbox.color import color, noColor
from pagebot.toolbox.units import pt, upt, units, em
import drawBot as drawBotBuilder
from pagebotosx.strings.textline import TextLine

def pixelBounds(fs):
    """Answers the pixel-bounds rectangle of the text.

    NOTE that @by can be a negative value, if there is text (e.g. overshoot)
    below the baseline.

    - @bh is the amount of pixels above the baseline.
    - For the total height of the pixel-map, calculate @ph - @py.
    - For the total width of the pixel-map, calculate @pw - @px."""
    if not fs:
        return pt(0, 0, 0, 0)
    p = drawBotBuilder.BezierPath()
    p.text(fs, (0, 0))

    '''
    OS X answers `bw` and `bh` as difference with `bx` and `by`. This is not
    very intuitive; in this situation the the total (width, height) always
    needs to be calculated by the caller. Instead, the width and height
    answered is the complete bounding box, and (x, y) is the position of the
    bounding box, compared to (0, 0) of the string origin.
    '''
    bx, by, bw, bh = p.bounds()
    return pt(bx, by, bw - bx, bh - by)

class DrawBotString(BabelString):
    """DrawBotString is a wrapper around the standard DrawBot FormattedString."""

    BABEL_STRING_TYPE = 'fs'
    formattedAttrKeys = ['font', 'fallbackFont', 'fontSize', 'fill',
            'cmykFill', 'stroke', 'cmykStroke', 'strokeWidth', 'align',
            'lineHeight', 'tracking', 'baselineShift', 'underline',
            'openTypeFeatures', 'fontVariations', 'tabs', 'indent',
            'tailIndent', 'firstLineIndent', 'paragraphTopSpacing',
            'paragraphBottomSpacing', 'language', ]


    def __init__(self, s, context, style=None):
        """Constructor of the DrawBotString, wrapper around DrawBot
        FormattedString. Optionally stores the (latest) style that was used to
        produce the formatted string.

        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Pagebot-Regular')
        >>> style = dict(font=font, fontSize=pt(80))
        >>> bs = context.newString('Example Text', style=style)
        >>> bs.fontSize, round(upt(bs.xHeight)), bs.xHeight, bs.capHeight, bs.ascender, bs.descender
        (80pt, 42, 0.53em, 0.71em, 0.93em, -0.24em)
        >>> #bs.font # FIXME: returns Roboto instead of PageBot font.
        >>> #'PageBot-Regular.ttf' in bs.font
        #True
        >>> #'/PageBot' in bs.fontPath
        #True
        >>> style = dict(font='Verdana', fontSize=pt(100), leading=em(1.4))
        >>> bs = context.newString('Example Text', style=style)
        >>> from pagebot.contexts.base.babelstring import BabelString
        >>> isinstance(bs, BabelString)
        True
        >>> bs[2:]
        ample Text
        >>> #lines = bs.getTextLines(w=100)
        >>> #lines
        #[<TextLine #0 y:181.00 Runs:1>, <TextLine #1 y:41.00 Runs:1>]
        >>> #len(lines)
        #2
        >>> #line = lines[0]
        >>> #line.xHeight, line.capHeight # Max metrics of all runs in line as Em
        #(0.55em, 0.73em)
        >>> #run = line.textRuns[0]
        >>> #run.xHeight, run.capHeight
        #(0.55em, 0.73em)
        >>> fs = context.newString('blablabla')
        >>> fs[2:]
        ablabla
        >>> fs
        blablabla
        >>> fs[:5]
        blabl
        >>> fs[0]
        b
        >>> fs[5]
        a
        """
        fsAttrs = {}
        # Some checking, in case we get something else here.
        assert style is None or isinstance(style, dict)

        # Optional style to set the context parameters. In case defined, store
        # current status here as property and set the current FormattedString
        # for future additions. Also the answered metrics will not be based on
        # these values.
        if style is None:
            style = {}

        self.style = style
        self.language = style.get('language')

        for k, v in style.items():
            if k  == 'leading':
                fontSize = style.get('fontSize', DEFAULT_FONT_SIZE)
                lineHeight = getLineHeight(v, fontSize)
                fsAttrs['lineHeight'] = lineHeight
            elif k == 'hyphenation':
                # Global, not a FS attribute.
                self.hyphenation = v
            elif k in self.formattedAttrKeys:
                fsAttrs[k] = v
            else:
                print('%s not allowed' % k)

        # Turns plain text string `s` into a FormattedString.
        self.s = context.b.FormattedString(s, **fsAttrs)

        # Sets Variable Font fitting parameters.
        self.fittingFontSize = pt(style.get('fontSize'))
        self.fittingFont = style.get('font')
        self.fittingLocation = style.get('location')
        self.isFitting = True
        super().__init__(context)

    def _get_s(self):
        """Answers the embedded FormattedString using a property to force string
        type checking."""
        return self._s

    def _set_s(self, s):
        """ Checks the type of `s`. Three types are supported here: plain
        strings, DrawBot FormattedString and the class self."""
        assert isinstance(s, (DrawBotString, str)) or s.__class__.__name__ == 'FormattedString'

        if isinstance(s, str):
            # newString() instead to inherit default styles?
            s = self.context.b.FormattedString(s)

        elif isinstance(s, DrawBotString):
            # TODO: needs a deeper copy?
            s = s.s

        self._s = s

    s = property(_get_s, _set_s)

    def columnStart(self, firstColumnIndent):
        bs = self
        style = self.getStyleAtIndex(0)

        # Something going on at start?
        if style.get('firstLineIndent') is not None or firstColumnIndent is not None:

            # Really really small place holder period.
            style['fontSize'] = pt(0.0001)

            # Transparant, so it will never show.
            style['textFill'] = color(1, 1, 1, 1)

            # Then make this one work.
            style['firstLineIndent'] = firstColumnIndent or 0
            bs = self.context.newString('.', style=style) + bs
        return bs

    def _get_font(self):
        """Answers the current state of fontName."""
        return self.style.get('font')

    def _set_font(self, fontName):
        if fontName is not None:
            self.context.font(fontName)
        self.style['font'] = fontName

    font = property(_get_font, _set_font)

    def _get_fontSize(self):
        """Answers the current state of the fontSize.

        >>> from pagebot.toolbox.units import mm
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='Verdana', fontSize=pt(85), leading=em(1.4))
        >>> bs = context.newString('Example Text', style=style)
        >>> bs.fontSize
        85pt
        >>> # Auto-convert to points
        >>> bs.fontSize = 96
        >>> bs.fontSize
        96pt
        >>> # Set at unit.
        >>> bs.fontSize = mm(5)
        >>> bs.fontSize
        5mm
        >>> #bs.leading
        >>>
        1.4em
        """
        return units(self.style.get('fontSize'))

    def _set_fontSize(self, fontSize):
        if fontSize is not None:
            self.context.fontSize(upt(fontSize))
        self.style['fontSize'] = fontSize

    fontSize = property(_get_fontSize, _set_fontSize)

    def getStyleAtIndex(self, index):
        """Answers the style dictionary with values at position index of the
        string.

        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> c1 = color(0.2, 0.3, 0.4)
        >>> c2 = color(1, 0, 0.22)
        >>> style = style=dict(font='Verdana', fontSize=pt(17), leading=pt(21), textFill=c1, textStroke=c2, textStrokeWidth=pt(3))
        >>> bs = context.newString('Example Text1', style=style)
        >>> bs.getStyleAtIndex(3)['fontSize']
        17pt
        >>> style = dict(font='Georgia', fontSize=pt(20), leading=pt(25), textFill=c2, textStroke=c1, textStrokeWidth=pt(2))
        >>> bs += context.newString('Another Text', style=style)
        >>> bs.getStyleAtIndex(20)['leading']
        25pt
        >>> bs.getStyleAtIndex(20)['textFill']
        Color(r=1.0, g=0, b=0.22)
        """
        attrString = self.s.getNSObject()
        cIndex = 0
        style = {}

        if attrString:
            for nsObject in attrString.attributesAtIndex_effectiveRange_(index, None):
                if isinstance(nsObject, NSAttributeDictionary):
                    nsColor = nsObject.get('NSColor')
                    if nsColor is not None:
                        style['textFill'] = color(nsColor.redComponent(), nsColor.greenComponent(), nsColor.blueComponent())

                    nsColor = nsObject.get('NSStrokeColor')

                    if nsColor is not None:
                        style['textStroke'] = color(nsColor.redComponent(), nsColor.greenComponent(), nsColor.blueComponent())

                    strokeWidth = nsObject.get('NSStrokeWidth')

                    if strokeWidth is not None:
                        style['strokeWidth'] = pt(strokeWidth)

                    nsFont = nsObject.get('NSFont')

                    if nsFont is not None:
                        style['font'] = nsFont.fontName()
                        style['fontSize'] = pt(nsFont.pointSize())

                    pgStyle = nsObject.get('NSParagraphStyle')
                    style['tabs'] = tabs = {}
                    #for tab in pgStyle.tabStops:
                    #    tabe[tab] = 'a'
                    style['leading'] = pt(pgStyle.minimumLineHeight())
                    style['firstLineIndent'] = pt(pgStyle.firstLineHeadIndent())
                    style['indent'] = pt(pgStyle.headIndent())
                    style['tailIndent'] = pt(pgStyle.tailIndent())
                    # MORE FROM: Alignment 4, LineSpacing 0, ParagraphSpacing 0, ParagraphSpacingBefore 0,
                    #  0, LineHeight 21/21, LineHeightMultiple 0, LineBreakMode 0, Tabs (), DefaultTabInterval 0,
                    # Blocks (), Lists (), BaseWritingDirection -1, HyphenationFactor 0, TighteningForTruncation NO, HeaderLevel 0
                elif isinstance(nsObject, NSRange):
                    if cIndex >= index: # Run through until matching index, so the style cumulates.
                        break
                    cIndex += nsObject.length
        return style

    def asText(self):
        """Answers the text string.

        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> bs = context.newString('Example Text')
        >>> bs.asText()
        'Example Text'
        """
        return str(self.s) #  Convert to text

    def textSize(self, w=None, h=None):
        """Answers the (w, h) size for a given width, with the current text,
        measured from bottom em-size to top em-size (including ascender+ and
        descender+) and the string width (including margins).

        >>> from pagebot.toolbox.units import mm, uRound
        >>> from pagebot import getContext
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> context = getContext('DrawBot')
        >>> font = findFont('Bungee-Regular')
        >>> style = dict(font=font, fontSize=pt(12))
        >>> bs = context.newString('Example Text ' * 20, style=style)
        >>> #len(bs.getTextLines(w=100))
        #16
        >>> uRound(bs.textSize(w=300))
        [290pt, 130pt]
        """
        b = self.context.b

        if w is not None:
            wpt = upt(w)
            return b.textSize(self.s, width=wpt)
        if h is not None:
            hpt = upt(h)
            return b.textSize(self.s, height=hpt)

        return b.textSize(self.s)

    def bounds(self):
        """Answers the pixel-bounds rectangle of the text, if formatted by the
        option (w, h).

        NOTE that @by can be a negative value, if there is text (e.g.
        overshoot) below the baseline.
        @bh is the amount of pixels above the baseline.
        For the total height of the pixel-map, calculate @ph - @py.
        For the total width of the pixel-map, calculate @pw - @px."""

        # Sets the hyphenation flag and language from self; in DrawBot this
        # is set by a global function, not as FormattedString attribute.
        self.context.language(self.language)
        self.context.hyphenation(self.hyphenation)
        return pixelBounds(self.s)

    def fontContainsCharacters(self, characters):
        """Return a Boolean if the current font contains the provided
        characters. Characters is a string containing one or more
        characters."""
        return self.s.fontContainsCharacters(characters)

    def _get_fontFilePath(self):
        """Return the path to the file of the current font."""
        return self.s.fontFilePath()

    fontPath = property(_get_fontFilePath)

    def listFontGlyphNames(self):
        """Return a list of glyph names supported by the current font."""
        return self.s.listFontGlyphNames()

    def _get_ascender(self):
        """Returns the current font ascender as relative Em, based on the
        current font and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontAscender() / fontSize, base=fontSize)

    # Compatibility with DrawBot API.
    fontAscender = ascender = property(_get_ascender)

    def _get_descender(self):
        """Returns the current font descender as Em, based on the current font
        and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontDescender()/fontSize, base=fontSize)

    # Compatibility with DrawBot API.
    fontDescender = descender = property(_get_descender)

    def _get_xHeight(self):
        """Returns the current font x-height as Em, based on the current font
        and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontXHeight()/fontSize, base=fontSize)

    # Compatibility with DrawBot API.
    fontXHeight = xHeight = property(_get_xHeight)

    def _get_capHeight(self):
        """Returns the current font cap height as Em, based on the current font
        and fontSize."""
        fontSize = upt(self.fontSize)
        return em(self.s.fontCapHeight()/fontSize, base=fontSize)

    # Compatibility with DrawBot API.
    fontCapHeight = capHeight = property(_get_capHeight)

    def _get_leading(self):
        """Answers the current leading value."""
        #fontSize = upt(self.fontSize)
        #return em(self.s.fontLeading() / fontSize, base=fontSize)

        return self.style.get('leading', DEFAULT_LEADING)

    # Compatibility with DrawBot API.
    fontLeading = leading = property(_get_leading)

    def _get_lineHeight(self):
        """Returns the current line height, based on the current font and fontSize.
        If a lineHeight is set, this value will be returned."""
        #fontSize = upt(self.fontSize)
        return self.s.fontLineHeight()

    # Compatibility with DrawBot API.
    fontLineHeight = lineHeight = property(_get_lineHeight)

    def appendGlyph(self, *glyphNames):
        """Append a glyph by his glyph name using the current font. Multiple
        glyph names are possible."""
        self.s.appendGlyph(glyphNames)

    MARKER_PATTERN = '==%s@%s=='
    FIND_FS_MARKERS = re.compile('\=\=([a-zA-Z0-9_\:\.]*)\@([^=]*)\=\=')

    def appendMarker(self, markerId, arg):
        """Appends a formatted string with markerId that can be used as
        non-display marker. This way the Composer can find the position of
        markers in text boxes, after FS-slicing has been done. Note there is
        always a very small "white-space" added to the string, so there is a
        potential difference in width that matters. For that reason markers
        should not be changed after slicing (which would theoretically alter
        the flow of the FormattedString in an box) and the markerId and
        amount/length of args should be kept as small as possible.

        NOTE that there is a potential problem of slicing through the argument
        string at the end of a textBox. That is another reason to keep the
        length of the arguments short. And not to use any spaces, etc. inside
        the markerId. Possible slicing through line-endings is not a problem,
        as the raw string ignores them."""
        marker = self.MARKER_PATTERN % (markerId, arg or '')
        fs = self.context.b.FormattedString(marker, fill=noColor,
                stroke=noColor, fontSize=0.0000000000001)
        self.append(fs)

    def findMarkers(self, reCompiled=None):
        """Answers a dictionary of markers with their arguments in self.s."""
        if reCompiled is None:
            reCompiled= self.FIND_FS_MARKERS
        return reCompiled.findall(u'%s' % self.s)

    def textOverflow(self, w, h, align=LEFT):
        """Answers the overflowing of from the box (0, 0, w, h) as a new
        DrawBotString in the current context."""
        wpt, hpt = upt(w, h)
        box = (0, 0, wpt, hpt)

        # Sets the hyphenation flag from style. In DrawBot this is set by a
        # global function, not as FormattedString attribute.

        # TODO: Attributes don't seem to stay the same in the string or overfill copy.
        language = self.language or 'en'
        hyphenation = self.hyphenation or True
        self.context.b.language(language)
        self.context.b.hyphenation(hyphenation)
        overflow = self.__class__(self.context.b.textOverflow(self.s, box, align), self.context)

        # Pass on these parameters to the new constructed DrawBotString.
        overflow.language = language
        overflow.hyphenation = hyphenation
        return overflow

    def getBaselines(self, w, h=None):
        """Answers the dictionary of vertical baseline positions for the self.s
        FormattedString and for the given width and height. The value is the
        TextLine instance at that position.

        FIXME

        >>> from pagebot.toolbox.units import mm, uRound
        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> style = dict(font='Verdana', fontSize=pt(12))
        >>> bs = context.newString('Example Text ' * 10, style=style)
        >>> baselines = bs.getBaselines(w=200)
        >>> #baselines # FIXME: y-values too large
        """
        baselines = {}

        for textLine in self.getTextLines(w, h):
            baselines[textLine.y.pt] = textLine

        return baselines

    def getTextLines(self, w, h=None, align=LEFT):
        """Answers the dictionary of TextLine instances. Key is y position of
        the line.

        >>> from pagebot.toolbox.units import mm, uRound
        >>> from pagebot import getContext
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> context = getContext('DrawBot')
        >>> font = findFont('Bungee-Regular')
        >>> style = dict(font=font, fontSize=pt(12))
        >>> bs = context.newString('Example Text', style=style)
        >>> lines = bs.getTextLines(w=200, h=200)
        >>> len(lines)
        1
        >>> #lines # FIXME: baseline shift on Travis OSX.
        #[<TextLine #0 y:185.20 Runs:1>]
        >>> line = lines[0]
        >>> line.maximumLineHeight
        1.4em
        >>> #line.y # FIXME: baseline shift on Travis OSX.
        #185.2pt
        >>> #lines = bs.getTextLines(w=200, h=200)
        >>> attrString = bs.s.getNSObject()
        >>> len(attrString)
        12
        >>> setter = CTFramesetterCreateWithAttributedString(attrString)
        >>> path = CGPathCreateMutable()
        >>> CGPathAddRect(path, None, CGRectMake(0, 0, 200, 600))
        >>> ctBox = CTFramesetterCreateFrame(setter, (0, 0), path, None)
        >>> ctLines = CTFrameGetLines(ctBox)
        >>> from CoreText import CTLineGetGlyphRuns, CTRunGetAttributes
        >>> runs = CTLineGetGlyphRuns(ctLines[0])
        >>> attrs = CTRunGetAttributes(runs[0])
        >>> origins = CTFrameGetLineOrigins(ctBox, (0, len(ctLines)), None)
        >>> lineHeight = 16.8
        >>> oy = origins[0].y
        >>> #oy # FIXME: baseline shift on Travis OSX.
        #585.2
        >>> 600 - lineHeight
        583.2
        """
        assert w

        if h is None:
            h = 3 * w

        wpt, hpt = upt(w, h)
        textLines = []
        attrString = self.s.getNSObject()
        setter = CTFramesetterCreateWithAttributedString(attrString)
        path = CGPathCreateMutable()
        CGPathAddRect(path, None, CGRectMake(0, 0, wpt, hpt))
        ctBox = CTFramesetterCreateFrame(setter, (0, 0), path, None)
        ctLines = CTFrameGetLines(ctBox)
        origins = CTFrameGetLineOrigins(ctBox, (0, len(ctLines)), None)

        for lIndex, ctLine in enumerate(ctLines):
            origin = origins[lIndex]
            origin_y = origin.y
            textLine = TextLine(ctLine, pt(origin.x), pt(origin_y), lIndex)
            textLines.append(textLine)

        return textLines

    @classmethod
    def newString(cls, s, context, e=None, style=None, w=None, h=None, **kwargs):
        """Answers a DrawBotString instance from valid attributes in *style*.
        Set all values after testing their existence, so they can inherit from
        previous style formats in the string.

        If target width *w* or height *h* is defined, then *fontSize* is scaled
        to make the string fit *w* or *h*.
        TODO: restore pixelFit implementation.

        >>> from pagebot import getContext
        >>> context = getContext('DrawBot')
        >>> from pagebot.fonttoolbox.objects.font import findFont
        >>> font = findFont('Roboto-Regular')
        >>> font = findFont('Bungee-Regular')
        >>> font = findFont('Roboto-Black')
        >>> bs = context.newString('ABC', style=dict(font=font.path, fontSize=pt(22)))
        >>> bs.style['font'].endswith('Roboto-Black.ttf')
        True
        >>> bs
        ABC
        >>> bs = context.newString('ABC', style=dict(font=font.path, w=pt(100)))
        >>> int(round(bs.fontSize))
        12
        >>> # Use the font instance instead of path.
        >>> bs = context.newString('ABC ', style=dict(font=font, w=pt(100)))
        >>> int(round(bs.fontSize))
        12
        >>> bs1 = context.newString('DEF')
        >>> bs + bs1
        ABC DEF
        """
        assert isinstance(s, str)

        if style is None:
            style = {}
        else:
            assert isinstance(style, dict)

        attrs = cls.getStringAttributes(s, e=e, style=style, w=w, h=h)
        s = cls.addCaseToString(s, e, style)
        # Creates a new DrawBotString.
        return cls(s, context, style=attrs)

if __name__ == '__main__':
    import doctest
    import sys
    sys.exit(doctest.testmod()[0])
