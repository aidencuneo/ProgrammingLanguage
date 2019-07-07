import error
import func
import lexer

scope = 0


def process(tokens):
    i = 0
    l = []
    while i < len(tokens):
        a = tokens[i]
        if a[0] == 'IF_SHORTHAND':
            b = parse_if_shorthand(tokens, i)
            l.append(['PRECOMPILED', b[0]])
            i += b[1]
        elif a[0] == 'FUNCTION_CALL':
            b = parse_function_call(tokens, i)
            l.append(['PRECOMPILED', b[0][:-1]])
            i += b[1]
        elif a[0] == 'VARIABLE':
            #print(tokens[i:])
            b = parse_variable(tokens, i)
            l.append(['PRECOMPILED', b[0][:-1]])
            i += b[1]
        elif a[0] == 'KEYWORD':
            b = parse_keyword(tokens, a[1], i)
            l.append(['PRECOMPILED', b[0]])
            i += b[1]
        elif a[0] == 'BINARY_OPERATOR':
            if a[1] == '&&':
                l.append(['PRECOMPILED', 'and'])
            elif a[1] == '||':
                l.append(['PRECOMPILED', 'or'])
        elif a[0] == 'BOOL_REVERSE':
            l.append(['PRECOMPILED', 'not ' + a[1][2:-1]])
        elif a[0] == 'BOOL':
            l.append(['BOOL', a[1][0].upper() + a[1][1:]])
        else:
            l.append(a)
        i += 1
    return l


def parse_code(tokens):
    global scope
    i = 0
    o = ''
    while i < len(tokens):
        a = tokens[i]
        #print(a)
        if a[0] == 'KEYWORD':
            b = parse_keyword(tokens, a[1], i)
            o += b[0]
            i += b[1]
        elif a[0] == 'FOR_LOOP':
            b = parse_for_loop(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'IMPORT_STATEMENT':
            b = parse_import_statement(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'RAISE_STATEMENT':
            b = parse_raise_statement(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'RETURN_STATEMENT':
            b = parse_return_statement(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'STATIC_KEYWORD':
            o += scope * '  ' + a[1] + '\n'
        elif a[0] == 'FUNCTION_DEFINER':
            b = parse_function_definer(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'CLASS_DEFINER':
            b = parse_class_definer(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'TRY_DEFINER':
            o += scope * '  ' + 'try:\n'
        elif a[0] == 'CATCH_DEFINER':
            b = parse_catch_definer(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'IF_SHORTHAND':
            b = parse_if_shorthand(tokens, i)
            o += b[0]
            i += b[1]
        elif a[0] == 'SCOPE+1':
            scope += 1
        elif a[0] == 'SCOPE-1':
            scope -= 1
        elif a[0] == 'OPERATOR':
            o += a[1]
        elif a[0] == 'PRECOMPILED':
            o += scope * '  ' + a[1]
            if i+1 < len(tokens):
                if tokens[i+1][1] == ';':
                    o += '\n'
        elif a[0] == 'UNKNOWN':
            print('Unknown type: "' + a[1] + '" found.')
            exit()
        i += 1
    return o


def parse_variable(tokens, i):
    t = tokens[i][1][1:]
    n = tokens[i + 1][1].split('|')
    o = tokens[i + 2][1]
    if ['LINEFEED', ';'] in tokens[i + 2:]:
        v = tokens[i + 3:tokens.index(['LINEFEED', ';'], i + 2) + 1]
    else:
        v = tokens[i + 3:-1]
    v = ''.join([a[1] for a in process(v)]).replace(';', '')
    nt = ''
    if o == '=' and len(n) > 1:
        nn = ''
        for a in n:
            nn += a + '='
        nn = nn[:-1]
    else:
        nn = n[0]
    if t != 'var':
        nt = t + '('
    return [scope * '  ' + nn + o + nt + v + ')' * nt.count('(') + '\n', tokens.index(['LINEFEED', ';'], i + 2) - i - 1]


def parse_function_call(tokens, i):
    f = tokens[i][1][1:] + '('
    al = tokens[i+1:func.index_of(tokens, [['LINEFEED', ';'], ['SCOPE+1', '{'], ['KEY', '::']], i)]
    al = ''.join([a[1] for a in process(al)]).replace(';', '')
    return [scope * '  ' + f + al + ')' * f.count('(') + '\n', func.index_of(tokens, [['LINEFEED', ';'], ['SCOPE+1', '{'], ['KEY', '::']], i) - 1 - i]


def parse_keyword(tokens, k, i):
    global scope
    c = tokens[i + 1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i + 1)]
    c = ''.join([a[1] + ' ' for a in process(c)])
    a = tokens[i + 1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i + 1) + 1]
    j = tokens[func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i + 1):]
    if j[0] == ['KEY', '::']:
        j = j[:j.index(['LINEFEED', ';'])]
    elif j[0] == ['SCOPE+1', '{']:
        j = j[:j.index(['SCOPE-1', '}'])]
    if len(c) > 0:
        c = ' ' + c[:-1]
    if j:
        if j[-1] != ['LINEFEED', ';']:
            j.append(['LINEFEED', ';'])
    o = scope * '  ' + k + c + ':' + ('\n' if ['KEY', '::'] not in a and ['SCOPE+1', '{'] in a else '')
    scope += 1
    z = parse_code(process(j[1:]))
    scope -= 1
    o += z + ('\n' if ['KEY', '::'] not in a and ['SCOPE+1', '{'] in a else '')
    if j[0] == ['KEY', '::']:
        m = tokens.index(['LINEFEED', ';'], i + len(c)) - 1
    elif j[0] == ['SCOPE+1', '{']:
        m = tokens.index(['SCOPE-1', '}'], i + len(c)) - 1
    return [o, m]


def parse_import_statement(tokens, i):
    al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
    al = ''.join([a[1] for a in al]).replace(';', '')
    return [scope * '  ' + 'import ' + al + '\n', tokens.index(['LINEFEED', ';'], i) - i]


def parse_raise_statement(tokens, i):
    al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
    al = ''.join([a[1] for a in al]).replace(';', '')
    return [scope * '  ' + 'error.custom_error(' + al + ')\n', tokens.index(['LINEFEED', ';'], i) - i]


def parse_return_statement(tokens, i):
    al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
    al = ''.join([a[1] for a in al]).replace(';', '')
    return [scope * '  ' + 'return ' + al + '\n', tokens.index(['LINEFEED', ';'], i) - i]


def parse_function_definer(tokens, i):
    a = tokens[i+1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i+1)]
    n = a[0][1]
    al = a[1:]
    nal = ''
    for a in al:
        nal += a[1] + ','
    b = tokens[i+1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i+1)+1]
    o = scope * '  ' + 'def ' + n + '(' + nal[:-1] + '):' + ('\n' if ['KEY', '::'] not in b and ['SCOPE+1', '{'] in b else '')
    return [o, func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i) - 1 - i]


def parse_class_definer(tokens, i):
    global scope
    c = tokens[i + 1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i + 1)]
    d = ''.join([a[1] for a in process(c)])
    a = tokens[i + 1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i + 1) + 1]
    j = tokens[func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i + 1):]
    print(j)
    if j[0] == ['KEY', '::']:
        if ['LINEFEED', ';'] in j:
            j = j[:j.index(['LINEFEED', ';'])]
            m = tokens.index(['LINEFEED', ';'], i + len(c)) - i
            a = tokens[i + 1:tokens.index(['LINEFEED', ';'], i)]
        else:
            j = len(j)
            m = len(j)
            a = len(j)
    elif j[0] == ['SCOPE+1', '{']:
        j = j[:j.index(['SCOPE-1', '}'])]
        m = tokens.index(['SCOPE-1', '}'], i + len(c)) - i
        a = tokens[i + 1:tokens.index(['SCOPE-1', '}'], i)]
    o = scope * '  ' + scope * '  ' + 'class ' + d[1] + ':\n'
    scope += 1
    print(j[1:])
    p = parse_code(j[1:])
    scope -= 1
    n = a[0][1]
    al = a[1:]
    nal = ''
    for a in al:
        nal += a[1] + ','
    return [scope * '  ' + 'class ' + n + '(' + nal[:-1] + '):\n' + p, m]


def parse_catch_definer(tokens, i):
    c = tokens[i+1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i)]
    c = ''.join([a[1] for a in c])
    a = tokens[i+1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i)+1]
    o = scope * '  ' + 'except ' + c + ':' + ('\n' if ['KEY', '::'] not in a and ['SCOPE+1', '{'] in a else '')
    return [o, func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i) - 1 - i]


def parse_if_shorthand(tokens, i):
    s = tokens[i+1:func.index_of(tokens, [['LINEFEED', ';'], ['SCOPE+1', '{'], ['KEY', '::']], tokens.index(['KEY', '::'], i+1)+1)]
    c = s[:s.index(['KEY', '::'])]
    t = s[1+s.index(['KEY', '::']):s.index(['PIPE', '|'])]
    f = s[1+s.index(['PIPE', '|']):]
    c = ''.join([a[1] for a in c]).replace(';', '')
    t = ''.join([a[1] for a in t]).replace(';', '')
    f = ''.join([a[1] for a in f]).replace(';', '')
    return [scope * '  ' + t + ' if ' + c + ' else ' + f, len(s)]


def parse_for_loop(tokens, i):
    global scope
    c = tokens[i+1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i+1)]
    d = ''.join([a[1] for a in process(c)]).split(';')
    a = tokens[i+1:func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i+1)+1]
    j = tokens[func.index_of(tokens, [['SCOPE+1', '{'], ['KEY', '::']], i+1):]
    if j[0] == ['KEY', '::']:
        j = j[:j.index(['LINEFEED', ';'])]
    elif j[0] == ['SCOPE+1', '{']:
        j = j[:j.index(['SCOPE-1', '}'])]
    o = scope * '  ' + d[0] + '\n' + scope * '  ' + 'while ' + d[1] + ':\n'
    scope += 1
    p = parse_code(j[1:])
    scope -= 1
    o += p + '\n' + scope * '  ' + '  ' + d[2] + ('\n' if ['KEY', '::'] not in a and ['SCOPE+1', '{'] in a else '')
    if j[0] == ['KEY', '::']:
        m = tokens.index(['LINEFEED', ';'], i+len(c)) - i
    elif j[0] == ['SCOPE+1', '{']:
        m = tokens.index(['SCOPE-1', '}'], i+len(c)) - i
    return [o, m]
