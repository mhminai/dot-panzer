#!/usr/bin/env python

"""
mhminai: Taken from https://gist.github.com/bpj/f591a9e29fe974fa791f#file-pandoc-collect-floats-py

Pandoc filter which emulate the LaTeX endfloat package by extracting all
elements which would be LaTeX floats (figures and tables) from a
document and putting them in div with the id "figures" or "tables"
respectively. You must mark the points in the document where you want
the floats to go with a paragraph containing *only* the text
"FiguresHere" or "TablesHere" -- exactly as written here in CamelCase --
or you will lose the floats! If there are several paragraphs with the
sentinel texts only the one first found will be replaced with a div
containing the figures/tables.
Additionally a paragraph with the text "[Figure %d about here.]" or
"[Table %d about here.]" is inserted into the document where the
figure/table used to be, with "%d" being the number of figures/tables
found so far; thus it is not and cannot be guaranteed to be the same
number as LaTeX would have assigned!
Reference: <https://groups.google.com/d/topic/pandoc-discuss/jLUuYFcRDtk/discussion>
This filter requires the pandocfilters module to be installed. You can
clone or download it from GitHub (with instructions for installing and
how to use filters): https://github.com/jgm/pandocfilters or install
from PyPI::
    pip install pandocfilters
If you have an earlier version installed you may need to do::
    pip install -U pandocfilters
"""

from pandocfilters import toJSONFilter, Div, Image, Para, Str, Table

floats = {
    'figures': [],
    'saw_figures': None,
    'tables': [],
    'saw_tables': None
}

def collect_floats(eltype, eldata, fmt, meta):
    global floats
    if eltype == 'Para':
        if len(eldata) != 1:
            return None
        elem = eldata[0];
        if elem['t'] == 'Image':
            if elem['c'][-1][1].startswith('fig:'): # title
                floats['figures'].append(Para(eldata))
                filler = "[Figure %d about here.]" % len(floats['figures'])
                return Para([Str(filler)])
        elif elem['t'] == 'Str':
            text = elem['c']
            if elem['c'] == 'FiguresHere':
                if floats['saw_figures']:
                    return None
                floats['saw_figures'] = True
                key = 'figures'
            elif elem['c'] == 'TablesHere':
                if floats['saw_tables']:
                    return None
                floats['saw_tables'] = True
                key = 'tables'
            else:
                return None
            return [Div(['collected-' + key , [], []], floats[key])]
    elif eltype == 'Table':
        floats['tables'].append(Table(*eldata))
        filler = "[Table %d about here.]" % len(floats['tables'])
        return Para([Str(filler)])
    return None

if __name__ == "__main__":
    toJSONFilter(collect_floats)

