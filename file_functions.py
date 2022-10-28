from Token import Token


def read_file(filepath: str):
    with open(filepath, 'r') as f:
        content = f.read()
        return content


def write_to_file(filepath: str, values: list[Token]):
    with open(filepath, 'w') as f:
        f.write('(class_part, value_part, line_number)\n')
        for value in values:
            f.write(f'{value}\n')
    return 'file write completed'
