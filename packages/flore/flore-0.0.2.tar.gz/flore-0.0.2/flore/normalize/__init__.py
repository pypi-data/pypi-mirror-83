from .colon import normalize_colon_field
from .required import normalize_required_field


def normalize(fields: list) -> str:
    fields = normalize_required_field(fields)
    fields = normalize_colon_field(list(fields))
    return " ".join(fields)
