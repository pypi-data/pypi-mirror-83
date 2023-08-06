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
def table(widths, data):

    """
    Render and return a table.
    """

    tableString = ""

    format = "".join(["{:<" + str(w) + "}" for w in widths])
    for row in data:
        tableString += format.format(*row) + "\n"

    return tableString


def print_table(widths, data):
    print(table(widths, data))
