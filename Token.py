class Token:
    class_part: str
    value_part: str
    line_number: int

    def __init__(self, class_part: str, value_part: str, line_number: int):
        self.class_part = class_part
        self.value_part = value_part if(class_part != value_part) else "_"
        self.line_number = line_number

    def __str__(self):
        return f"({self.class_part}, {self.value_part}, {self.line_number})"
