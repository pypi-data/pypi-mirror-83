# Amantadine


<strong>Amantadine</strong> is a framework for rendering HTML on the server

## Introduce

The heavy HTML, CSS and JS files are rendered into independent HTML files, and asynchronous data collection through network requests is supported, and functions are defined as parameters. Only render CSS tags used in HTML to reduce volume

## Install

``` bash
pip install -U amantadine
```

## Usage

``` python
import amantadine

pages = amantadine.Pages(
    body=[amantadine.Record("h1", [amantadine.OnlyText("Amantadine")])],
    head=[
        amantadine.Record("meta", attrs={"charset": "UTF-8"}),
        amantadine.Record("title", [amantadine.OnlyText("Amantadine")]),
    ],
)

print(amantadine.renderDoc(pages))
```

After rendering:

``` html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta class='' charset=UTF-8></meta>
    <title class=''>Amantadine</title>
</head>

<body>
    <h1 class=''>Amantadine</h1>
</body>

</html>
```

## License
MIT LICENSE