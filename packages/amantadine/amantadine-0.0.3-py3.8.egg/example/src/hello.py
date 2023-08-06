from amantadine import Record
from amantadine import OnlyText

title = "Welcome"
path = "index"

view = Record(
    recordname="hello",
    body=[Record("h2", body=[OnlyText("Welcome to You Amantadine App")])],
)

__all__ = ["title", "view", "path"]
