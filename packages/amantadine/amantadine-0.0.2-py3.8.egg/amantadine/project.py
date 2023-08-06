# -*- coding: utf-8 -*-
"""
    ibuprofen
    ~~~~~~~~~~~~~~~~~~~

    Rendering HTML on server

    :copyright: 2020 ISCLUB
    :license: MIT LICENSE
"""
from .render import renderDoc
from .render import renderRecord
import os

class Project(object):
    def __init__(self, project_name, baserender, renderlist):
        self.project_name = project_name
        self.baserender = baserender
        self.renderlist = renderlist

    def render(self):
        print("🎨 Build Production")

        try:
            os.mkdir("docs")
        except:
            pass

        for view in self.renderlist:
            now_pagesname = view.view.recordname
            now_pagesDoc = self.baserender(title=view.title,body=view.view.body)
            now_path = view.path
            
            with open("docs/" + str(now_path) + ".html","w+",encoding="utf-8") as f:
                f.write(renderDoc(now_pagesDoc))
        print(" ")
        print("All Chunk:")
        for pathfilename in os.listdir("docs/"):
            print("docs/" + str(pathfilename) + "  " + os.path.getsize("docs/" + str(pathfilename)))