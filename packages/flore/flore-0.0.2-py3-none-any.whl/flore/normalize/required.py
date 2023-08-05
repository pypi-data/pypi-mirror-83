def normalize_required_field(fields):
    """when the field comes required, it be converted to not null"""

    if "required" in fields:
        return map(lambda field: field.replace("required", "not null"), fields)
    return fields
