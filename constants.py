keywords: dict[str, list[str]] = {
    "data_type": ["number", "string", "bool"],
    "class": ["class"],
    "this": ["this"],
    "super": ["super"],
    "access_modifier": ["public", "hidden"],
    "type_modifier": ["static", "final", "abstract"],
    "new": ["new"],
    "try": ["try"],
    "catch": ["catch"],
    "finally": ["finally"],
    "extends": ["extends"],
    "function": ["function"],
    "return": ["return"],
    "void": ["void"],
    "if": ["if"],
    "else": ["else"],
    "furthermore": ["furthermore"],
    "for": ["for"],
    "while": ["while"],
    "jump_statements": ["break", "continue", "pass"],
    "arr_dec": ["[]"],
    "construct": ["Constructor"]
}

operators: dict[str, list[str]] = {
    "inc_dec": ["++", "--"],
    "plus_minus": ["+", "-"],
    "multiply_divide_mod": ["*", "/", "%"],
    "assignment": ["="],
    "compound_assignment": ["+=", "-=", "*=", "/="],
    "relational_operators": [">", "<", "==", ">=", "<=", "!="],
    "and_operator": ["&&"],
    "or_operator": ["||"],
    "not_operator": ["!"],
}

punctuators: list[str] = [":", ",", "(", ")", "{", "}", "[", "]", "."]
