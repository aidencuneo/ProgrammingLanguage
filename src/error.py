import func
import lexer
import sys
import textwrap


def error_check(s):
    scope = 0
    for i in range(len(s)):
        e_args = [s[i], s[i-1] if i-1 >= 0 else None, s[i+1] if i+1 < len(s) else None]
        a = func.split_line(s[i], ' ')
        a = [b for b in a if b != '']
        if len(a) > 0:
            c = lexer.tokenise_line(a)
            for b in a:
                if b == '{':
                    scope += 1
                elif b == '}':
                    scope -= 1
                if scope < 0:
                    error_code(4, i+1, e_args)
            if c[0][0] == 'RETURN_STATEMENT':
                if c[1][0] == 'LINEFEED':
                    error_code(3, i+1, e_args)
            elif c[0][0] == 'IMPORT_STATEMENT':
                if c[1][0] != 'LINEFEED':
                    if c[1][0] != 'IDENTIFIER':
                        error_code(6, i+1, e_args)
                else:
                    error_code(5, i+1, e_args)
            elif c[0][0] == 'VARIABLE' and c[1:]:
                if c[1][0] == 'IDENTIFIER':
                    if len(c) > 2:
                        if c[2][0] == 'OPERATOR' or c[2][0] == 'INCREMENTAL_OPERATOR':
                            if c[3][0] == 'LINEFEED':
                                error_code(8, i+1, e_args)
                        elif c[2][0] == 'LINEFEED':
                            error_code(8, i+1, e_args)
                        else:
                            error_code(9, i+1, e_args)
                    else:
                        error_code(8, i+1, e_args)
                elif c[1][0] == 'LINEFEED':
                    error_code(8, i+1, e_args)
                else:
                    error_code(7, i+1, e_args)
            elif c[0][0] == 'VARIABLE':
                error_code(8, i+1, e_args)
    if scope != 0:
        error_code(2, len(s), [s[len(s)-1], s[len(s)-2], None])


def error_code(code, l, e):
    print('Error:')
    print('  At file "' + sys.argv[1] + '":')
    sys.stdout.write('    ')
    if code == 0:
        print('Expected "Main" method, but found EOF.')
    elif code == 1:
        print('Not enough arguments for variable creation.')
    elif code == 2:
        print('EOF without completed scope.')
    elif code == 3:
        print('Return statement requires at least one argument.')
    elif code == 4:
        print('Can not end a loop that does not exist. (Occurs when number of "}" in a file is greater than number of "{")')
    elif code == 5:
        print('Import statement requires at least one argument.')
    elif code == 6:
        print('Invalid type to import.')
    elif code == 7:
        print('Invalid name for variable.')
    elif code == 8:
        print('Variable statement incomplete. Requires: name, operator, value. Optional: type.')
    elif code == 9:
        print('Variable statement contains invalid operator.')
    else:
        print('Unknown error occurred.')
    print_error_info(l, e)
    exit()


def print_error_info(l, e):
    m = max([len(str(l)), len(str(l-1)), len(str(l+1))])
    i = [' ' * (m - len(a)) + a for a in [str(l), str(l-1), str(l+1)]]
    if l-1 > 0 and e[1] is not None:
        print(i[1] + ' | ' + str(e[1]))
    print(i[0] + ' > ' + str(e[0]))
    if e[2] is not None:
        print(i[2] + ' | ' + str(e[2]))


def custom_error(s):
    print('Error:')
    print('  At file "' + sys.argv[1] + '":')
    print('    ' + s)
    exit()


def env(*args):
    try:
        exec(*args)
    except Exception as e:
        custom_error(str(e))
