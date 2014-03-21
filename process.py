#!/usr/bin/env python
# coding=UTF-8
# Copyright (c) 2009 Geoffrey Sneddon
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
import cgi
import cgitb
cgitb.enable()

import sys
sys.path[0:0] = ['/home/gsnedders/.python/lib/python2.5/site-packages/setuptools-0.6c11-py2.5.egg',
                 '/home/gsnedders/.python/lib/python2.5/site-packages/lxml-2.2.6-py2.5-linux-x86_64.egg',
                 '/home/gsnedders/.python/lib/python2.5/site-packages/html5lib-0.95_dev-py2.5.egg',
                 '/home/gsnedders/.python/lib/python2.5/site-packages']

import urllib2

import html5lib
from html5lib import treewalkers, serializer

import toc

walker = treewalkers.getTreeWalker("lxml")
s = serializer.HTMLSerializer(inject_meta_charset=False,
                                  omit_optional_tags=False,
                                  quote_attr_values=True)

def main():
    form = cgi.FieldStorage()
    if "upload" in form and form["upload"].file:
        tree = html5lib.parse(form["upload"].file, "lxml", namespaceHTMLElements=False)
        fromTree(tree)
    elif "input" in form:
        tree = html5lib.parse(form["input"].value, "lxml", namespaceHTMLElements=False)
        fromTree(tree)
    elif "url" in form and form["url"].value.strip().startswith("http"):
        tree = html5lib.parse(urllib2.urlopen(form["url"].value), "lxml", namespaceHTMLElements=False)
        fromTree(tree)
    else:
        print """Content-Type: text/html

<!doctype html>
<title>Error</title>
<style>
html { font:1.5em/1.2 Verdana, sans-serif; text-align: center;}
</style>
<h1>Error!</h1>
<p>Please provide an input file or a URL!
<p><a href=".">Return to input form.</a>"""


def fromTree(tree):
    treeToc = toc.buildToc(tree)
    print """Content-Type: text/html;charset=utf-8

<!doctype html>
<title>Outline</title>
<style>
html { font:1.5em/1.2 Verdana, sans-serif; }
</style>"""
    print s.render(walker(treeToc), encoding="utf-8")
    

if __name__ == "__main__":
    main()
