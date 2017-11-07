from sidekick import opt
from types import SimpleNamespace
from getch import getche
import click

ctx = SimpleNamespace(tokens=[], indent=1)
code_p = SimpleNamespace(tokens=[], indent=1)

def n(code_p, source):

    data = [0]
    ptr = 0
    code_ptr = 0
    breakpoints = []

    while code_ptr < len(source):
        cmd = source[code_ptr]

        if cmd == '+':
            data[ptr] = (data[ptr] + 1) % 256
            x = ptr
            code_p.tokens.append('    ' * code_p.indent + 'data[' + str(x) + '] += 1;\n')
        elif cmd == '-':
            data[ptr] = (data[ptr] - 1) % 256
            x = ptr
            code_p.tokens.append('    ' * code_p.indent + 'data[' + str(x) + '] -= 1;\n')
        elif cmd == '>':
            ptr += 1
            code_p.tokens.append('    ' * code_p.indent + 'ptr++;\n')
            if ptr >= len(data):
                data.append(0)
        elif cmd == '<':
            ptr -= 1
            code_p.tokens.append('    ' * code_p.indent + 'ptr--;\n')
        elif cmd == '.':
            code_p.tokens.append('    ' * code_p.indent + 'putchar(' + str(data[ptr]) + ');\n')
        elif cmd == ',':
            x = ord(getche())
            code_p.tokens.append('    ' * code_p.indent + 'data[' + str(x) +'] = getchar();\n')
        elif cmd == '[':
            code_p.tokens.append('    ' * code_p.indent + 'while(data[ptr]) {\n')
            code_p.indent += 1
        elif cmd == ']':
            code_p.indent -= 1
            code_p.tokens.append('    ' * code_p.indent + '}\n')

        code_ptr += 1

    return ''.join(code_p.tokens)

def construct(ctx, source):

    data = [0]
    ptr = 0
    code_ptr = 0
    breakpoints = []

    op_b = 0
    pilha = []
    enter = 0

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
            if ptr >= len(data):
                data.append(0)
        elif cmd == '<':
            ptr -= 1
        elif cmd == '.':
            ctx.tokens.append('    ' * ctx.indent + 'putchar(' + str(data[ptr]) + ');\n')
        elif cmd == ',':
            x = ord(getche())
            ctx.tokens.append('    ' * ctx.indent + 'data[' + str(x) +'] = getchar();\n')
        elif cmd == '[':

            if enter == 0:
                armazena = code_ptr
                while True:

                    pilha.append(source[armazena])

                    if source[armazena] == '[':
                        op_b += 1

                    if source[armazena] == ']':
                        op_b -= 1

                    if source[armazena] == ']' and op_b == 0:
                        break;

                    armazena += 1

                while_code = ''.join(pilha)

                code_pilha = n(code_p, while_code)

                ctx.tokens.append(code_pilha)
                pilha = []

                code_p.tokens = []

                enter = 1

            if data[ptr] == 0:
                open_brackets = 1
                while open_brackets != 0:
                    code_ptr += 1
                    if source[code_ptr] == '[':
                        open_brackets += 1
                    elif source[code_ptr] == ']':
                        open_brackets -= 1

            else:
                breakpoints.append(code_ptr)
        elif cmd == ']':
            # voltar para o colchete correspondente
            code_ptr = breakpoints.pop() - 1
        else:
            enter = 0

        code_ptr += 1

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
