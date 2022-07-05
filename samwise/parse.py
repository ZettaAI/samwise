"""Functions for parsing command files."""


def parsecmd(filename: str) -> list[str]:
    with open(filename) as f:
        lines = f.readlines()

    cleaned = [
        line.replace("\\\n", "").replace("\n", "").replace("\\", "") for line in lines
    ]

    args = list()
    for line in cleaned:
        for arg in line.split():
            if arg != "":
                args.append(arg)

    return args
