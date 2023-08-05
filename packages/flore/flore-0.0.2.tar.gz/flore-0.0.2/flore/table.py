from .normalize import normalize


def compose(table_name, columns):
    tables = ""
    for name, fields in columns.items():
        tables += "%s %s, " % (name, normalize(fields))
    return mount_table(table_name, tables)


def mount_table(table_name, tables):
    table = "CREATE TABLE if not exists {0} ({1});".format(table_name, tables)
    return table.replace(", )", ")")


def create_id():
    return "id integer autoincrement unsigned"


def set_index():
    return "primary key(id)"
