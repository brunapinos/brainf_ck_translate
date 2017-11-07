from sidekick import opt
from types import SimpleNamespace
from getch import getche
import click

ctx = SimpleNamespace(tokens=[], indent=1)

def construct(ctx, source):

    data = [0]
    ptr = 0
    code_ptr = 0
    breakpoints = []

    op_b = 0
    pilha = []
    enter = 0
    ctx.indent = 0
    ctx.tokens.append('#include <stdio.h>\n')
    ctx.tokens.append('#include <stdlib.h>\n\n')
    ctx.tokens.append('int main() {\n\n')

    ctx.indent = 1

    ctx.tokens.append('    ' * ctx.indent + 'unsigned char data[100000];\n')
    ctx.tokens.append('    ' * ctx.indent + 'int ptr = 0;\n')

    while code_ptr < len(source):
        cmd = source[code_ptr]

        if cmd == '+':
            data[ptr] = (data[ptr] + 1) % 256
            x = ptr
            ctx.tokens.append('    ' * ctx.indent + 'data[' + str(x) + '] += 1;\n')
        elif cmd == '-':
            data[ptr] = (data[ptr] - 1) % 256
            x = ptr
            ctx.tokens.append('    ' * ctx.indent + 'data[' + str(x) + '] -= 1;\n')
        elif cmd == '>':
            ptr += 1
            ctx.tokens.append('    ' * ctx.indent + 'ptr++;\n')
            if ptr >= len(data):
                data.append(0)
        elif cmd == '<':
            ctx.tokens.append('    ' * ctx.indent + 'ptr--;\n')
            ptr -= 1
        elif cmd == '.':
            ctx.tokens.append('    ' * ctx.indent + 'putchar(data[ptr]);\n')
        elif cmd == ',':
            ctx.tokens.append('    ' * ctx.indent + 'scanf("%hhu",&data[ptr]);\n')
        elif cmd == '[':
            ctx.tokens.append('    ' * ctx.indent + 'while(data[ptr]) {\n')
            ctx.indent += 1
        elif cmd == ']':
            ctx.indent -= 1
            ctx.tokens.append('    ' * ctx.indent + '}\n')
        else:
            enter = 0

        code_ptr += 1

    ctx.indent = 0
    ctx.tokens.append('\n''    return 0;\n}')
    return ''.join(ctx.tokens)


@click.command()
@click.argument('filename')
@click.option('-o', nargs=1)
def build(o, filename):

    output = '%s' % o

    enter_arq = open(filename, 'r')

    code = SimpleNamespace(tokens=[])
    for linha in enter_arq:
        code.tokens.append(linha)

    enter_arq.close()

    source = construct(ctx, ''.join(code.tokens))

    exit_arq = open(output, 'w')
    exit_arq.write(source)
    exit_arq.close()

if __name__ == '__main__':
    build()
