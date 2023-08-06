# none/text/unicode.py
# ====================
#
# Copying
# -------
#
# Copyright (c) 2020 none authors and contributors.
#
# This file is part of the *none* project.
#
# None is a free software project. You can redistribute it and/or
# modify it following the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY
# KIND; including but not limited to the WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with
# *none*. If not, see <http://opensource.org/licenses/MIT>.
#
"""Common string operations."""
import re
import sys
import unicodedata

from collections import defaultdict


# Unicode ranges
# --------------

# The following regular expressions were taken from the Lodash project which is
# licensed under the MIT License.
# Source: https://github.com/lodash/lodash/blob/master/.internal/unicodeWords.js


#: Enumeration of Unicode characters grouped by their belonging category.
UNICODE_CATEGORY = defaultdict(list)
for c in map(chr, range(sys.maxunicode + 1)):
    _cat = unicodedata.category(c)
    UNICODE_CATEGORY[_cat[0]].append(c)
    UNICODE_CATEGORY[_cat].append(c)


# See also: https://en.wikipedia.org/wiki/Plane_(Unicode)

#: Unicode Basic Multilingual Plane (BMP) range with private use area excluded.
_UNICODE_BMP_RANGE = "\ud800-\udfff"

# See: https://en.wikipedia.org/wiki/Combining_character
#: Unicode Combining Diacritical Marks (CDM) range.
_UNICODE_CDM_RANGE = "\u0300-\u036f"
#: Unicode Combining Diacritical Marks Extended (CDMX) range.
_UNICODE_CDMX_RANGE = "\u1ab0-\u1aff"
#: Unicode Combining Diacritical Marks Supplement (CDMS).
_UNICODE_CDMS_RANGE = "\u1dc0-\u1dff"
#: Unicode Combining Diacritical Marks for Symbols range.
_UNICODE_SYM_CDM_RANGE = "\u20d0-\u20ff"
#: Unicode Combining Half Marks (CHM) range.
_UNICODE_CHM_RANGE = "\ufe20-\ufe2f"
#: Ranges of Unicode combining code points.
_UNICODE_COMBINING_RANGES = (
    _UNICODE_CDM_RANGE
    + _UNICODE_CDMX_RANGE
    + _UNICODE_CDMS_RANGE
    + _UNICODE_SYM_CDM_RANGE
    + _UNICODE_CHM_RANGE
)

# See: https://en.wikipedia.org/wiki/Dingbat
#: Unicode Dingbat range.
_UNICODE_DINGBAT_RANGE = "\u2700-\u27bf"

_UNICODE_LOWER = UNICODE_CATEGORY["Ll"]
_UNICODE_MATH = UNICODE_CATEGORY["Sm"]
_UNICODE_OTHER = UNICODE_CATEGORY["C"]
rsNonCharRange = '\\x00-\\x2f\\x3a-\\x40\\x5b-\\x60\\x7b-\\xbf'
rsPunctuationRange = '\\u2000-\\u206f'
rsSpaceRange = ' \\t\\x0b\\f\\xa0\\ufeff\\n\\r\\u2028\\u2029\\u1680\\u180e\\u2000\\u2001\\u2002\\u2003\\u2004\\u2005\\u2006\\u2007\\u2008\\u2009\\u200a\\u202f\\u205f\\u3000'
rsUpperRange = 'A-Z\\xc0-\\xd6\\xd8-\\xde'
rsVarRange = '\\ufe0e\\ufe0f'
rsBreakRange = _UNICODE_MATH + rsNonCharRange + rsPunctuationRange + rsSpaceRange

# Used to compose unicode capture groups.
rsApos = "['\u2019]"
rsBreak = f"[{rsBreakRange}]"
rsCombo = f"[{_UNICODE_COMBINING_RANGES}]"
rsDigit = '\\d'
rsDingbat = f"[{_UNICODE_DINGBAT_RANGE}]"
rsLower = f"[{_UNICODE_LOWER}]"
rsMisc = f"[^{_UNICODE_BMP_RANGE}{rsBreakRange + rsDigit + _UNICODE_DINGBAT_RANGE + _UNICODE_LOWER_RANGE + rsUpperRange}]"
rsFitz = '\\ud83c[\\udffb-\\udfff]'
rsModifier = f"(?:{rsCombo}|{rsFitz})"
rsNonAstral = f"[^{_UNICODE_BMP_RANGE}]"
rsRegional = '(?:\\ud83c[\\udde6-\\uddff]){2}'
rsSurrPair = '[\\ud800-\\udbff][\\udc00-\\udfff]'
rsUpper = f"[{rsUpperRange}]"
rsZWJ = '\\u200d'

# Used to compose unicode regexes.
rsMiscLower = f"(?:{rsLower}|{rsMisc})"
rsMiscUpper = f"(?:{rsUpper}|{rsMisc})"
rsOptContrLower = f"(?:{rsApos}(?:d|ll|m|re|s|t|ve))?"
rsOptContrUpper = f"(?:{rsApos}(?:D|LL|M|RE|S|T|VE))?"
reOptMod = f"{rsModifier}?"
rsOptVar = f"[{rsVarRange}]?"
rsOptJoin = f"(?:{rsZWJ}(?:${'|'.join([rsNonAstral, rsRegional, rsSurrPair])}){rsOptVar + reOptMod})*"
rsOrdLower = '\\d*(?:1st|2nd|3rd|(?![123])\\dth)(?=\\b|[A-Z_])'
rsOrdUpper = '\\d*(?:1ST|2ND|3RD|(?![123])\\dTH)(?=\\b|[a-z_])'
rsSeq = rsOptVar + reOptMod + rsOptJoin
rsEmoji = f"(?:{'|'.join([rsDingbat, rsRegional, rsSurrPair])}){rsSeq}"

UNICODE_WORD_RE = re.compile(
    "|".join([
      f"{rsUpper}?{rsLower}+{rsOptContrLower}(?={'|'.join([rsBreak, rsUpper, '$'])})",
      f"{rsMiscUpper}+{rsOptContrUpper}(?={'|'.join([rsBreak, rsUpper + rsMiscLower, '$'])})",
      f"{rsUpper}?{rsMiscLower}+{rsOptContrLower}",
      f"{rsUpper}+{rsOptContrUpper}",
      rsOrdUpper,
      rsOrdLower,
      f"{rsDigit}+",
      rsEmoji
  ])
)

#: Regular expression to catch an ASCII word.
ASCII_WORD_RE = re.compile(r"[^\x00-\x2f\x3a-\x40\x5b-\x60\x7b-\x7f]+")

