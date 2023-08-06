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

html_base = """
<!DOCTYPE html>
<html lang="{lang}">

<head>
    <meta charset="utf-8">
    <meta name="generator" content="Amantadine">
    {head}
</head>

<body>
    {body}
</body>

<style>
    {style}
</style>

</html>
"""

record_base = """
<{recordname} {classlist}{attrs}>
    {body}
</{recordname}>"""


def renderDoc(amantadineDoc: Pages):
    headString = ""
    for obj in amantadineDoc.head:
        headString = headString + renderRecord(obj) + " "

    bodyString = ""
    for obj in amantadineDoc.body:
        bodyString = bodyString + renderRecord(obj) + " "

    return html_base.format(
        lang=amantadineDoc.lang,
        head=headString,
        body=bodyString,
        style=amantadineDoc.css_static[0],
    )


def renderRecord(amantadineRecord: Record):
    if amantadineRecord.classlist == list():
        classString = ""
    else:
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
