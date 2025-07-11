# compiler.py

import sys
from lexer import lexer, write_tokens_to_file
from parser import parser

def main():
    if len(sys.argv) != 2:
        print("Usage: python compiler.py <source_file.cppy>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not input_file.endswith('.cppy'):
        print("Error: Input file must have a .cppy extension")
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # 1. Lexical Analysis and Token File Generation
    lexer.input(source_code)
    token_output_filename = input_file.replace('.cppy', '_tokens.txt')
    write_tokens_to_file(lexer, token_output_filename)
    print(f"Token file generated: '{token_output_filename}'")

    # 2. Syntax Analysis and Python Code Generation
    # The parser can modify the lexer's state, so we reset it.
    lexer.input(source_code)
    python_code = parser.parse(lexer=lexer)

    if python_code:
        output_py_filename = input_file.replace('.cppy', '.py')
        with open(output_py_filename, 'w', encoding='utf-8') as f:
            f.write("# Code automatically generated by the cppy-compiler\n\n")
            f.write(python_code)
        print(f"Python code successfully generated: '{output_py_filename}'")
        print(f"\nTo run the generated code, use: python {output_py_filename}")
    else:
        print("Compilation failed. Check for syntax errors.")

if __name__ == '__main__':
    main()