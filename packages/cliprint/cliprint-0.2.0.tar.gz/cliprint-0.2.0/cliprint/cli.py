import re
import json as lib_json

# JSON
def json(data):

    """
    Prettify and return JSON.
    """

    jsonString = str(data)

    return lib_json.dumps(
        lib_json.loads(jsonString.replace("'", '"')),
        indent=4,
        sort_keys=True,
    )


def print_json(data):
    print(json(data))


# Table
def table(widths, data, compensate_ansi=True):

    """
    Render and return a table.
    """

    if isinstance(widths, int):
        if len(data):
            widths = [widths for i in range(len(data[0]))]
        else:
            widths = []

    tableString = ""

    # Create table formats
    formats = []
    for d in data:
        format = ""
        for n in range(len(widths)):
            width = widths[n]
            cellData = d[n]
            if compensate_ansi and isinstance(cellData, str):
                width += len(cellData) - len(
                    re.sub("(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", cellData)
                )
            format += "{:<" + str(width) + "}"
        formats += [format]

    # format data
    for n in range(len(data)):
        row = data[n]
        tableString += formats[n].format(*row) + "\n"

    return tableString


def print_table(widths, data):
    print(table(widths, data))
