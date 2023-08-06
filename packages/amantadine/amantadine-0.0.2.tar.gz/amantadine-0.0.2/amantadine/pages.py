# -*- coding: utf-8 -*-
"""
    ibuprofen
    ~~~~~~~~~~~~~~~~~~~

    Rendering HTML on server

    :copyright: 2020 ISCLUB
    :license: MIT LICENSE
"""
import cssutils


class OnlyText(object):
    def __init__(self, text):
        self.text = text


class Record(object):
    def __init__(self, recordname, body=[], classlist=[], attrs={}):
        self.recordname = recordname
        self.body = body
        self.classlist = classlist
        self.attrs = attrs

    def add(self, o):
        self.body.append(o)

    def add_attrs(self, name, value):
        self.attrs[name] = value

    def add_class(self, classname):
        self.classlist.append(classname)


class Pages(object):
    def __init__(self, body=[], head=[], attribute={}, css_static=[], lang="en"):
        self.body = body
        self.head = head
        self.css_static = css_static
        self.attribute = attribute
        self.lang = lang

    def add(self, o):
        self.body.append(o)

    def add_head(self, o):
        self.head.append(o)

    def add_attr(self, name, value):
        self.attribute[name] = value
