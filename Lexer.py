import re

# Token types
TOKEN_KEYWORD = "KEYWORD"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_NUMBER = "NUMBER"
TOKEN_STRING = "STRING"

# Operators
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MULTI = "MULTI"
TOKEN_DIVISION = "DIVISION"
TOKEN_MODULUS = "MODULUS"
TOKEN_ASSIGNMENT = "ASSIGNMENT"
TOKEN_EQUALITY = "EQUALITY"

# Punctuations
TOKEN_LPAREN = "LPAREN"
TOKEN_RPAREN = "RPAREN"
TOKEN_COMMA = "COMMA"
TOKEN_COLON = "COLON"

# Regular expressions
patterns = [
    (r"\b(if|else|print)\b", TOKEN_KEYWORD),  # Keywords
    (r'"(?:\\.|[^"\\])*"', TOKEN_STRING),  # Strings (double-quoted)
    (
        r"[a-zA-Z_][\w\s]*",
        TOKEN_IDENTIFIER,
    ),  # Identifiers (allowing spaces and special characters)
    (r"\d+", TOKEN_NUMBER),
    (r"\+", TOKEN_PLUS),
    (r"-", TOKEN_MINUS),
    (r"\*", TOKEN_MULTI),
    (r"/", TOKEN_DIVISION),
    (r"%", TOKEN_MODULUS),
    (r"==", TOKEN_EQUALITY),  # Equality operator
    (r"(?<!\=)=+(?!=)", TOKEN_ASSIGNMENT),  # Assignment operator
    (r"\(", TOKEN_LPAREN),  # Left parenthesis
    (r"\)", TOKEN_RPAREN),  # Right parenthesis
    (r",", TOKEN_COMMA),
    (r":", TOKEN_COLON),
]


# Function that tokenize code from a file
def tokenize_file(input_file, output_file):
    with open(input_file, "r") as file:
        code = file.read()
    tokens = tokenize(code)
    with open(output_file, "w") as file:
        for token in tokens:
            file.write(f"{token[0]}: {token[1]}\n")


# Function that tokenize code
def tokenize(code):
    tokens = []
    code = code.strip()
    while code:
        matched = False
        for pattern, token_type in patterns:
            match = re.match(pattern, code)
            if match:
                value = match.group(0)
                tokens.append((value, token_type))
                code = code[len(value) :].strip()
                matched = True
                break
        if not matched:
            code = code[1:].strip()  # If there is no match found, skip the character
    return tokens


input_file = "example.py"
output_file = "tokens.txt"
tokenize_file(input_file, output_file)
