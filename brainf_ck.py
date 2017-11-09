from sidekick import opt
from types import SimpleNamespace
from getch import getche
import click

final_code = SimpleNamespace(tokens=[], indent=1)

def construct(final_code, source_code):

    data = [0]
    ptr = 0
    counter = 0
    TAB = 9 # Tab in Ascii table

    final_code.indent = 0
    final_code.tokens.append('#include <stdio.h>\n')
    final_code.tokens.append('#include <stdlib.h>\n\n')
    final_code.tokens.append('int main() {\n\n')

    final_code.indent = 1

    final_code.tokens.append(chr(TAB) * final_code.indent + \
        'unsigned char data[100000];\n')
    final_code.tokens.append(chr(TAB) * final_code.indent + 'unsigned int ptr = 0;\n')

    while counter < len(source_code):
        character = source_code[counter]

        if character == '+':
            data[ptr] = (data[ptr] + 1) % 256
            x = ptr
            final_code.tokens.append(chr(TAB) * final_code.indent + \
                'data[ptr]++;\n')
        elif character == '-':
            data[ptr] = (data[ptr] - 1) % 256
            x = ptr
            final_code.tokens.append(chr(TAB) * final_code.indent + \
                'data[ptr]--;\n')
        elif character == '>':
            ptr += 1
            final_code.tokens.append(chr(TAB) * final_code.indent + 'ptr++;\n')
            if ptr == len(data):
                data.append(0)
        elif character == '<':
            ptr -= 1
            final_code.tokens.append(chr(TAB) * final_code.indent + 'ptr--;\n')
        elif character == '.':
            final_code.tokens.append(chr(TAB) * final_code.indent + \
                'putchar(data[ptr]);\n')
        elif character == ',':
            final_code.tokens.append(chr(TAB) * final_code.indent + \
                'data[ptr] = getchar();\n')
        elif character == '[':
            final_code.tokens.append(chr(TAB) * final_code.indent + \
                'while(data[ptr]) {\n')
            final_code.indent += 1
        elif character == ']':
            final_code.indent -= 1
            final_code.tokens.append(chr(TAB) * final_code.indent + '}\n')

        counter += 1

    final_code.indent = 0
    final_code.tokens.append('\n''    return 0;\n}')

    return ''.join(final_code.tokens)


@click.command()
@click.argument('filename')
@click.option('-o', nargs=1)
def build(o, filename):

    output = '%s' % o

    enter_arq = open(filename, 'r')

    code = SimpleNamespace(tokens=[])
    for line in enter_arq:
        code.tokens.append(line)

    enter_arq.close()

    source_code = construct(final_code, ''.join(code.tokens))

    exit_arq = open(output, 'w')
    exit_arq.write(source_code)
    exit_arq.close()

if __name__ == '__main__':
    build()
