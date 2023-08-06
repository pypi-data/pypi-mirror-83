# -*- coding: utf-8 -*-
"""
    ibuprofen
    ~~~~~~~~~~~~~~~~~~~

    Rendering HTML on server

    :copyright: 2020 ISCLUB
    :license: MIT LICENSE
"""
from .pages import Pages
from .pages import Record
from .pages import OnlyText

html_base = """<!DOCTYPE html><html lang="{lang}"><head>{head}</head><body>{body}</body></html>"""

record_base = """<{recordname} {classlist} {attrs}>{body}</{recordname}>"""


def renderDoc(amantadineDoc: Pages):
    headString = ""
    for obj in amantadineDoc.head:
        headString = headString + renderRecord(obj) + " "

    bodyString = ""
    for obj in amantadineDoc.body:
        bodyString = bodyString + renderRecord(obj) + " "

    return html_base.format(lang=amantadineDoc.lang, head=headString, body=bodyString)


def renderRecord(amantadineRecord: Record):
    classString = """class='"""
    for classname in amantadineRecord.classlist:
        classString = classString + classname + " "
    classString = classString + """'"""

    attrsString = ""
    for attrname, attrvalue in amantadineRecord.attrs.items():
        attrsString = attrname + "=" + attrvalue + " "

    bodyString = ""
    for obj in amantadineRecord.body:
        if isinstance(obj, Record):
            bodyString = bodyString + renderRecord(obj)
        elif isinstance(obj, OnlyText):
            bodyString = bodyString + obj.text
        else:
            pass

    return record_base.format(
        recordname=amantadineRecord.recordname,
        classlist=classString,
        attrs=attrsString,
        body=bodyString,
    )
