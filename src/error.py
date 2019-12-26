import func
import lexer
import os
import sys
import textwrap


def error_check(pretokens):
    scope = 0
    tokens = lexer.tokenise(pretokens)
    trees = []
    ct = []
    for t in tokens:
        ct.append(t)
        if t[1] in [';', '{', '}']:
            trees.append(ct)
            ct = []
    for t in trees:
        if t[1:]:
            if t[0][0] == 'INCLUDE':
                if t[1][1] == ';':
                    error_code(5, t[0][1] + ';')
                if t[1][0] != 'STRING':
                    error_code(10, t[0][1] + ';')
                for a in t[1:-1]:
                    if a[0] != 'STRING':
                        error_code(10, ' '.join([b[1] for b in t[:-1]]) + ';')
            elif t[0][0] == 'FUNCTION_CALL':
                if t[1][0] not in ['IDENTIFIER']:
                    error_code(11, t[0][1] + ' ' + t[1][1])
                for a in t[2:-1]:
                    if a[0] not in ['INTEGER', 'STRING', 'IDENTIFIER', 'OPERATOR', 'FUNCTION_CALL']\
                        and a[1] != ',':
                        error_code(12, ' '.join([b[1] for b in t[:-1]]) + ';')
            elif t[0][0] == 'VARIABLE':
                if t[1][0] != 'IDENTIFIER':
                    error_code(1, t[0][1] + t[1][1])
                if t[2:]:
                    if t[2][0] != 'IDENTIFIER':
                        error_code(6, t[0][1] + t[1][1] + ' ' + t[2][1])
            elif t[0][0] == 'IDENTIFIER':
                if t[1][0] not in ['INCREMENTAL_OPERATOR', 'OPERATOR', 'LINEFEED']:
                    error_code(8, t[0][1] + ' ' + t[1][1])
                if t[1][0] in ['INCREMENTAL_OPERATOR', 'OPERATOR']:
                    if t[2][0] not in ['INTEGER', 'STRING', 'IDENTIFIER', 'FUNCTION_CALL']:
                        error_code(13, t[0][1] + ' ' + t[1][1])
            elif t[0][0] == 'FUNCTION_DEFINER':
                if t[1][0] != 'IDENTIFIER':
                    error_code(14, t[0][1] + ' ' + t[1][1])
                last = t[1]
                if t[2][0] not in ['IDENTIFIER', 'SCOPE+1']:
                    error_code(15, ' '.join([b[1] for b in t]))
                for a in t[2:]:
                    if a[0] not in ['IDENTIFIER', 'SCOPE+1', 'OPERATOR', 'INTEGER', 'STRING']\
                        or (a[0] == 'OPERATOR' and a[1] != '='):
                        error_code(15, ' '.join([b[1] for b in t]))
                    if last[0] == 'IDENTIFIER':
                        if a[0] not in ['IDENTIFIER', 'SCOPE+1', 'OPERATOR']:
                            print(2)
                            error_code(15, ' '.join([b[1] for b in t]))
                    if last[0] == 'OPERATOR':
                        if a[0] not in ['IDENTIFIER', 'INTEGER', 'STRING']:
                            error_code(15, ' '.join([b[1] for b in t]))
                    last = a


def error_code(c, loc):
    codes = [
        # 0:
        'Expected "Main" method, but found EOF',
        # 1:
        'Invalid variable type',
        # 2:
        'EOF without completed scope',
        # 3:
        'Return statement requires at least one arguments',
        # 4:
        'Can not end a loop that does not exist (occurs when number of "}" in a file is greater than number of "{")',
        # 5:
        'Include statement requires at least one argument',
        # 6:
        'Invalid variable name',
        # 7:
        'Invalid name for variable',
        # 8:
        'Invalid type after an identifier',
        # 9:
        'Variable statement contains invalid operator',
        # 10:
        'Include statement arguments must be of type string',
        # 11:
        'Invalid function name to call',
        # 12:
        'Invalid type in function arguments',
        # 13:
        'Missing value after an operator',
        # 14:
        'Invalid function name to define',
        # 15:
        'Invalid syntax for function arguments',
    ]
    s = 'Invalid syntax'
    if 0 <= c < len(codes):
        s = codes[c] if codes[c] else s
    call_error(s, loc)


def call_error(e, loc):
    print('ERROR:')
    print('  At file "' + os.path.abspath(sys.argv[1]) + '":')
    if loc:
        print('    -> ' + loc)
        print('    :: ' + e)
    else:
        print('    <exception>: ' + e)
    sys.exit()


def env(*args):
    try:
        exec(*args)
    except BaseException as e:
        call_error(str(e))
