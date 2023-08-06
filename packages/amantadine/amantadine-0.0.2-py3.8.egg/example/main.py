from amantadine import Project
from base import baserender

from src import hello

amantadine = Project(
    project_name=__name__, baserender=baserender, renderlist=[hello]
)

amantadine.render()
