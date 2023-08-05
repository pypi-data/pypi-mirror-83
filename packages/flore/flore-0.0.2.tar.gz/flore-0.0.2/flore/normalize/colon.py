import re


REGEX_FOUND_COLON = r"(\w+)\:(\d+)"


def normalize_colon_field(fields):
    """when the field comes varchar:120, it be converted to varchar(120)"""

    if re.search(REGEX_FOUND_COLON, " ".join(fields)):
        return re.sub(
            REGEX_FOUND_COLON, "\\1(\\2)", " ".join(fields)
        ).splitlines()
    return fields
