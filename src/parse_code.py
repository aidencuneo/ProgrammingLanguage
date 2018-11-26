import lexer

scope = 0


def parse_code(tokens):
    global scope
    tokens = tokens
    i = 0
    o = ''
    while i < len(tokens):
        a = tokens[i]
        if a[0] == 'VARIABLE':
            a = parse_variable(tokens, i)
            o += a[0]
            i += a[1]
        elif a[0] == 'FUNCTION_CALL':
            a = parse_function_call(tokens, i)
            o += a[0]
            i += a[1]
        elif a[0] == 'KEYWORD':
            a = parse_keyword(tokens, a[1], i)
            o += a[0]
            i += a[1]
        elif a[0] == 'SPECIAL_KEYWORD':
            a = parse_special_keyword(tokens, a[1], i)
            o += a[0]
            i += a[1]
        elif a[0] == 'STATIC_KEYWORD':
            o += scope * '  ' + a[1] + '\n'
        elif a[0] == 'FUNCTION_DEFINER':
            o += parse_function_definer(tokens, i)
        elif a[0] == 'CLASS_DEFINER':
            o += parse_class_definer(tokens, i)
        elif a[0] == 'SWITCH_DEFINER':
            a = parse_switch_definer(tokens, i)
            o += a[0]
            i += a[1]
        elif a[0] == 'TRY_DEFINER':
            o += scope * '  ' + 'try:\n'
        elif a[0] == 'CATCH_DEFINER':
            a = parse_catch_definer(tokens, i)
            o += a[0]
            i += a[1]
        elif a[0] == 'INCLUDE_STATEMENT':
            o += parse_code(lexer.tokenize(a[1][1:-1] + ';'))
        elif a[0] == 'SCOPE+1':
            scope += 1
        elif a[0] == 'SCOPE-1':
            scope -= 1
        elif a[0] == 'OPERATOR':
            o += a[1]
        elif a[0] == 'UNKNOWN':
            print('Unknown type: "' + a[1] + '" found during lexical analysis.')
            exit()
        i += 1
    return o


def parse_variable(tokens, i):
    if len(tokens[:tokens.index(['LINEFEED', ';'], i)]) < 2:
        print('Not enough arguments for variable creation. ' +\
                'Error found at line starting with: "' + tokens[i][1] + '".')
        exit()
    t = tokens[i][1][1:].split('::')
    n = tokens[i+1][1]
    o = tokens[i+2][1]
    v = tokens[i+3:tokens.index(['LINEFEED', ';'], i+2)+1]
    if '`' in ''.join([a[1] for a in v]):
        v = parse_code(v).replace('\n', '').replace('  ', '')
    else:
        v = ''.join([a[1] for a in v]).replace(';', '')
    if len(t) == 1 and t[0] == 'var':
        nt = ''
    else:
        nt = ''
        for a in t:
            nt += a + '('
    if len(tokens[i:tokens.index(['LINEFEED', ';'], i+2)]) < 3:
        o = '='
    return [scope * '  ' + n + o + nt + v + ')' * nt.count('(') + '\n', tokens.index(['LINEFEED', ';'], i+2) - i]


def parse_function_call(tokens, i):
    f = tokens[i][1][1:].split('::')
    al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
    if '`' in ''.join([a[1] for a in al]):
        al = parse_code(al).replace('\n', '').replace('  ', '')
    else:
        al = ''.join([a[1] for a in al]).replace(';', '')
    nf = ''
    for a in f:
        nf += a + '('
    return [scope * '  ' + nf + al + ')' * nf.count('(') + '\n', tokens.index(['LINEFEED', ';'], i) - i]


def parse_keyword(tokens, k, i):
    c = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
    if '`' in ''.join([a[1] for a in c]):
        c = parse_code(c).replace('\n', '').replace('  ', '')
    else:
        c = ''.join([a[1] for a in c]).replace(';', '')
    if len(c) > 0:
        c = ' ' + c
    return [scope * '  ' + k + c + ':\n', tokens.index(['SCOPE+1', '{'], i) - 1 - i]


def parse_special_keyword(tokens, k, i):
    al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
    if '`' in ''.join([a[1] for a in al]):
        al = parse_code(al).replace('\n', '').replace('  ', '')
    else:
        al = ''.join([a[1] + ',' for a in al]).replace(';', '')
    if al.endswith(','):
        al = al[:-1]
    return [scope * '  ' + k + ' ' + al + '\n', tokens.index(['LINEFEED', ';'], i) - i]


def parse_function_definer(tokens, i):
    a = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
    n = a[0][1]
    al = a[1:]
    nal = ''
    for a in al:
        nal += a[1] + ','
    return scope * '  ' + 'def ' + n + '(' + nal + '):\n'


def parse_class_definer(tokens, i):
    a = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
    n = a[0][1]
    al = a[1:]
    nal = ''
    for a in al:
        nal += a[1] + ','
    return scope * '  ' + 'class ' + n + '(' + nal + '):\n'


def parse_switch_definer(tokens, i):
    section = tokens[i+1:tokens.index(['SWITCH_END', ')'], i+1)]
    v = section[0][1]
    section = section[2:]
    o = ''
    cases = []
    l = []
    for a in range(len(section)):
        l.append(section[a])
        if a+1 < len(section):
            if section[a+1][1] == 'case':
                cases.append(l)
                l = []
    cases.append(l)
    for a in cases:
        a = a[1:]
        o += 'if ' + v + ' '
        for b in a:
            if b[0] == 'KEY':
                o += '{ '
            else:
                o += b[1] + ' '
        o += '}\n'
    o = parse_code(lexer.tokenize(o))
    return [o, len(section)+2]


def parse_catch_definer(tokens, i):
    c = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
    if '`' in ''.join([a[1] for a in c]):
        c = parse_code(c).replace('\n', '').replace('  ', '')
    else:
        c = ''.join([a[1] for a in c]).replace(';', '')
    return [scope * '  ' + 'except ' + c + ':\n', tokens.index(['SCOPE+1', '{'], i) - 1 - i]
