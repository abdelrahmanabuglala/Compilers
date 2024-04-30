# program -> assignment_statement print_statement

# assignment_statement -> identifier "=" expression

# print_statement -> "print" expression

# expression -> identifier
#             | number
#             | "(" expression ")"

# identifier -> [a-zA-Z_][a-zA-Z0-9_]*
# number -> [0-9]+


class Token:  # convert input to Tokens
    def __init__(self, lexeme, token_type):
        self.lexeme = lexeme
        self.token_type = token_type

    def __repr__(self):
        return f"{self.lexeme}: {self.token_type}"


class ParseError(Exception):  # catch error
    pass


class ParseTreeNode:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children if children is not None else []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.label}"


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        return self.program()

    def program(self):  # program: assignment_statement print_statement
        assignment = self.assignment_statement()
        print_statement = self.print_statement()
        return ParseTreeNode("program", [assignment, print_statement])

    def assignment_statement(self):  # assignment statement: identifier "=" expression
        identifier = self.identifier()
        if self.tokens[self.current_token_index].lexeme != "=":
            raise ParseError("Expected '=' after identifier")
        self.current_token_index += 1
        expression = self.expression()
        return ParseTreeNode("assignment", [identifier, expression])

    def print_statement(self):  # print statement: "print" expression
        if self.tokens[self.current_token_index].lexeme != "print":
            raise ParseError("Expected 'print' keyword")
        self.current_token_index += 1
        expression = self.expression()
        return ParseTreeNode("print", [expression])

    def expression(self):  # expression: identifier | number | "(" expression ")"
        token = self.tokens[self.current_token_index]
        if token.token_type == "IDENTIFIER":
            self.current_token_index += 1
            return ParseTreeNode("identifier", [token])
        elif token.token_type == "NUMBER":
            self.current_token_index += 1
            return ParseTreeNode("number", [token])
        elif token.lexeme == "(":
            self.current_token_index += 1
            expression = self.expression()
            if self.tokens[self.current_token_index].lexeme != ")":
                raise ParseError("Expected ')' after expression")
            self.current_token_index += 1
            return expression
        else:
            raise ParseError(f"Unexpected token: {token}")

    def identifier(self):  # identifier
        token = self.tokens[self.current_token_index]
        if token.token_type == "IDENTIFIER":
            self.current_token_index += 1
            return ParseTreeNode("identifier", [token])
        else:
            raise ParseError("Expected an identifier")

    def number(self):  # number
        token = self.tokens[self.current_token_index]
        if token.token_type == "NUMBER":
            self.current_token_index += 1
            return ParseTreeNode("number", [token])
        else:
            raise ParseError("Expected a number")


def print_tree(node, indent=""):  # print
    if isinstance(node, ParseTreeNode):
        print(indent + str(node))
        for child in node.children:
            print_tree(child, indent + "  ")
    else:
        print(indent + str(node))


def read_tokens_from_file(filename):  # take input
    tokens = []
    with open(filename, "r") as file:
        for line in file:
            lexeme, token_type = line.strip().split(": ")
            tokens.append(Token(lexeme, token_type))
    return tokens


filename = "tokens.txt"
tokens = read_tokens_from_file(filename)
parser = Parser(tokens)

# Parse the input
try:
    parse_tree = parser.parse()
    print("Parse tree: \n")
    print_tree(parse_tree)
except ParseError as e:  # catch an error
    print("Parse error:", e)
