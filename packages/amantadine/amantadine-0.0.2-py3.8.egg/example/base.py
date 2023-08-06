from amantadine import Pages
from amantadine import Record
from amantadine import OnlyText
import requests

# Get CSS with Requests
gralig = requests.get("https://unpkg.com/gralig@0.5.0/dist/gralig.min.css").text


def baserender(title, body):
    return Pages(
        body=[],
        head=[Record("title", body=[OnlyText(title + " - Amantadine")])],
        css_static=[gralig],
    )
