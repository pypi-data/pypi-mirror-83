class colors_fg:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    WHITE = "\033[37m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class colors_bg:
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    WHITE = "\033[47m"


class colors:
    ENDC = "\033[0m"


status_colors = {
    "new": colors_fg.YELLOW,
    "maintained": colors_fg.GREEN,
    "discontinued": colors_fg.RED,
    "completed": colors_fg.BLUE,
}


def printTable(widths, data):

    row_format = "".join(["{:<" + str(w) + "}" for w in widths])

    for row in data:
        print(row_format.format(*row))
