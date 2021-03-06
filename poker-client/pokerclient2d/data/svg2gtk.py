#!/usr/bin/python
# -*- mode: python -*-
#
# Copyright (C) 2006 Mekensleep <licensing@mekensleep.com>
#                    24 rue vieille du temple, 75004 Paris
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#  Johan Euphrosine <johan@mekensleep.com>
#

import sys
from xml.sax import parseString
from xml.sax.handler import ContentHandler
import libxml2
import string
import re

class SVGParse(ContentHandler):
    def __init__(self, xml): 
        self.root = ""
        self.formats = []
        self.tuples = []
        self.doc = libxml2.parseMemory(xml, len(xml))
        parseString(xml, self)
    def __str__(self):
        return string.join(map(lambda format, tuple: format % tuple, self.formats, self.tuples), '')
    def startElement(self, name, node):
        nodeAttrs = dict([(key, value) for key, value in node._attrs.iteritems()])
        if name == "svg":
            self.startElementSvg(nodeAttrs)
        elif name == "image":
            self.startElementImage(nodeAttrs)            
        elif name == "use":
            self.startElementUse(nodeAttrs)
    def startElementUse(self, attrs):
        context = self.doc.xpathNewContext()
        path = '//g[@id="'+attrs['xlink:href'][1:]+'"]/image'
        nodes = context.xpathEval(path)
        for node in nodes:
            nodeAttrs = dict([(p.get_name(), p.get_content()) for p in node.properties])
            if nodeAttrs.has_key('href'): nodeAttrs['xlink:href'] = nodeAttrs['href']
            (groupPrefix, groupSuffix) = attrs['id'].split('_')
            (nodePrefix, nodeSuffix) = nodeAttrs['id'].split('_')
            nodeAttrs['id'] = nodeAttrs['id'].replace(nodeSuffix, groupSuffix)
            (nodeAttrs['x'], nodeAttrs['y']) = map(lambda x, tx: str(float(x) + float(tx)), (nodeAttrs['x'], nodeAttrs['y']), re.match('translate\((-?\d+\.?\d*),(-?\d+\.?\d*)\)', attrs['transform']).groups())
            self.startElementImage(nodeAttrs)

class SVG2Glade(SVGParse):
    def startElementSvg(self, attrs):
        self.formats.append('<glade-interface><widget class="GtkWindow" id="%s"><property name="width_request">%s</property><property name="height_request">%s</property><child><widget class="GtkFixed" id="%s_fixed">')
        self.tuples.append((attrs['id'], attrs['width'], attrs['height'], attrs['id']))
    def startElementImage(self, attrs):
        format = '<child><widget class="GtkButton" id="%s"><property name="width_request">%s</property><property name="height_request">%s</property><property name="label"/><signal name="clicked" handler="on_%s_clicked"/></widget><packing><property name="x">%s</property><property name="y">%s</property></packing></child>'
        self.formats.append(format)
        self.tuples.append((attrs['id'], attrs['width'], attrs['height'], attrs['id'], attrs['x'], attrs['y']))
    def endElement(self, name):
        if name == "svg":
            self.formats.append('</widget></child></widget></glade-interface>')
            self.tuples.append(())

class SVG2Rc(SVGParse):
    def startElementSvg(self, attrs):
        self.root = attrs['id']
    def startElementImage(self, attrs):
        format = 'style "%s_style" {engine "pixmap" {image {function = BOX file = "%s"}}} widget "*%s*%s" style "%s_style"\n'
        self.formats.append(format)
        self.tuples.append((attrs['id'], attrs['xlink:href'], self.root, attrs['id'], attrs['id']))           

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        if sys.argv[1] == "--glade":
            print SVG2Glade(sys.stdin.read())
        elif sys.argv[1] == "--gtkrc":
            print SVG2Rc(sys.stdin.read())
