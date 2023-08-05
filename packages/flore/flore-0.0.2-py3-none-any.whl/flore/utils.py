def open_yaml_file(filename):
    with open(f"migrations/{filename}", mode="r") as f:
        return f.read()
