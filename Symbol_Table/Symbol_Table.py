import ast
from collections import defaultdict


class SymbolTableEntry:
    def __init__(
        self, index, name, type_, value, address, dimension, declaration, reference
    ):
        self.index = index
        self.name = name
        self.type = type_
        self.value = value
        self.address = address
        self.dimension = dimension
        self.declaration = declaration
        self.reference = reference

    def __str__(self):
        refs_str = ", ".join(map(str, self.reference))
        return f"   {self.index:<5} {self.name:<13} {self.type:<8} {self.value:<10} {self.address:<6} {self.dimension:<20} {self.declaration:<20} {refs_str}"


class SymbolTable:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

    def __str__(self):
        result = " Index   Name          Type    Value    Address     Dimension          Line Declaration        Reference\n"
        result += "-" * 111 + "\n"
        return result + "\n".join(map(str, self.entries))


def get_size(type_):
    type_sizes = {"int": 4, "float": 8, "bool": 1}
    return type_sizes.get(type_, 0)


def analyze_code(code):
    symbol_table = SymbolTable()
    references = defaultdict(list)
    address = 0
    index = 0
    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id
                    value = ast.literal_eval(node.value)
                    type_ = type(value).__name__
                    size = get_size(type_)
                    dimension = "None(not array)"
                    declaration = f"line:{node.lineno}, column:{node.col_offset}"
                    reference = references[name]
                    symbol_table.add_entry(
                        SymbolTableEntry(
                            index,
                            name,
                            type_,
                            value,
                            address,
                            dimension,
                            declaration,
                            reference,
                        )
                    )
                    address += size
                    index += 1
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, ast.Load):
                references[node.id].append(
                    f"line:{node.lineno}, column:{node.col_offset}"
                )
    return symbol_table


def main():
    file_name = "Symbol_Table/example-code.py"
    output_file_name = "Symbol_Table/Table"
    try:
        with open(file_name, "r") as file:
            code = file.read()
            symbol_table = analyze_code(code)
            with open(output_file_name, "w") as output_file:
                output_file.write(str(symbol_table))
            print("Symbol table has been written to", output_file_name)
    except FileNotFoundError:
        print("File not found.")


if __name__ == "__main__":
    main()
