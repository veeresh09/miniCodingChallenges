import re

def tokenize(json_string):
    # Regular expressions for different JSON tokens
    token_specification = [
        ("NUMBER",   r'\d+(\.\d*)?'),  # Integer or decimal number
        ("STRING",   r'\"(.*?)\"'),    # String
        ("BRACE_L",  r'\{'),           # Left brace
        ("BRACE_R",  r'\}'),           # Right brace
        ("BRACKET_L",r'\['),           # Left bracket
        ("BRACKET_R",r'\]'),           # Right bracket
        ("COMMA",    r','),            # Comma
        ("COLON",    r':'),            # Colon
        ("BOOLEAN",  r'true|false'),   # Booleans
        ("NULL",     r'null'),         # Null
        ("SKIP",     r'[ \t\n\r]+'),   # Skip over spaces and newlines
    ]
    regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(regex, json_string):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            value = float(value) if '.' in value else int(value)
        elif kind == "STRING":
            value = value[1:-1]  # Remove quotation marks
        elif kind in ["BOOLEAN", "NULL"]:
            value = {"true": True, "false": False, "null": None}[value]
        elif kind == "SKIP":
            continue
        yield kind, value

def parse_object(token_gen):
    obj = {}
    token_type, token_value = next(token_gen, (None, None))

    while token_type != "BRACE_R":
        if token_type != "STRING":
            raise SyntaxError("Expected string key")

        key = token_value
        token_type, _ = next(token_gen)  # Skip colon
        if (token_type != "COLON") :
            raise SyntaxError("Expected a colon")
        obj[key] = parse_value(token_gen)
        token_type, token_value = next(token_gen, (None, None))

        if token_type == "COMMA":
            token_type, token_value = next(token_gen, (None, None))
        elif token_type != "BRACE_R":
            print(token_type)
            raise SyntaxError("Expected a comma or closing brace")
    return obj

def parse_array(token_gen):
    array = []
    token_type, token_value = next(token_gen, (None, None))

    if token_type == "BRACKET_R":
        return array  # Empty array
    else:
        if token_type in ["BOOLEAN", "NULL", "NUMBER","STRING"]:
            array.append(token_value)
        else:
            raise SyntaxError("Expected a comma or closing brace")
    while token_type != "BRACKET_R" :
        token_type, token_value = next(token_gen, (None,None))
        if token_type == "COMMA":
            array.append(parse_value(token_gen))
        elif token_type != "BRACKET_R":
            raise SyntaxError("Expected a comma or closing brace")
    return array

def parse_value(token_gen):
    token_type, token_value = next(token_gen, (None, None))

    if token_type == "NUMBER":
        return token_value
    elif token_type == "STRING":
        return token_value
    elif token_type in ["BOOLEAN", "NULL"]:
        return token_value
    elif token_type == "BRACE_L":
        return parse_object(token_gen)
    elif token_type == "BRACKET_L":
        return parse_array(token_gen)
    else:
        raise SyntaxError("Unexpected token type")

def is_valid_json(json_string):
    try:
        tokens = tokenize(json_string)
        parse_value(iter(tokens))
        return True
    except SyntaxError:
        return False

def read_and_parse_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json_string = file.read()

        if is_valid_json(json_string):
            tokens = tokenize(json_string)
            return parse_value(iter(tokens))  # Using our own parser function
        else:
            return "Invalid JSON format."

    except FileNotFoundError:
        return "File not found."

    except Exception as e:
        return f"An error occurred: {str(e)}"

jsonObj = read_and_parse_json("test2.json")
print(jsonObj)
