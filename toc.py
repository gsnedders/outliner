# coding=UTF-8
# Copyright (c) 2008 Geoffrey Sneddon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from lxml import etree
from copy import deepcopy

from anolislib.processes import outliner
from anolislib import utils

# These are all the attributes to be removed
remove_attributes_from_toc = frozenset([u"id", ])

def buildToc(ElementTree, **kwargs):
    # Create root element of TOC
    toc = etree.Element(u"ol")
    
    # Build the outline of the document
    outline_creator = outliner.Outliner(ElementTree, **kwargs)
    outline = outline_creator.build(**kwargs)

    # Get a list of all the top level sections, and their depth (0)
    sections = [(section, 0) for section in reversed(outline)]

    # Loop over all sections in a DFS
    while sections:
        # Get the section and depth at the end of list
        section, depth = sections.pop()

        # If we have a header, regardless of how deep we are
        if section.header is not None:
            # Get the element that represents the section header's text
            if section.header.tag == u"hgroup":
                i = 1
                while i <= 6:
                    header_text = section.header.find(u".//h" + unicode(i))
                    if header_text is not None:
                        break
                    i += 1
                else:
                    header_text = None
            else:
                header_text = section.header
        else:
            header_text = None

        # Find the appropriate section of the TOC
        i = 0
        toc_section = toc
        while i < depth:
            try:
                # If the final li has no children, or the last
                # children isn't an ol element
                if len(toc_section[-1]) == 0 or \
                   toc_section[-1][-1].tag != u"ol":
                    toc_section[-1].append(etree.Element(u"ol"))
            except IndexError:
                # If the current ol has no li in it
                toc_section.append(etree.Element(u"li"))
                toc_section[0].append(etree.Element(u"ol"))
            # TOC Section is now the final child (ol) of the final
            # item (li) in the previous section
            assert toc_section[-1].tag == u"li"
            assert toc_section[-1][-1].tag == u"ol"
            toc_section = toc_section[-1][-1]
            i += 1
        # Add the current item to the TOC
        item = etree.Element(u"li")
        toc_section.append(item)

        # If we have a header
        if header_text is not None:
            item.text = utils.textContent(header_text)
        else:
            italics = etree.Element(u"i")
            italics.text = "Untitled Section"
            item.append(italics)
        
        # Add subsections in reverse order (so the next one is executed
        # next) with a higher depth value
        sections.extend([(child_section, depth + 1)
                         for child_section in reversed(section)])
    
    return toc
