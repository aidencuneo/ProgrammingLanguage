import error
import func
import lexer
import sys
import textwrap

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
            l.append(['PRECOMPILED', b[0]])
            i += b[1]
        elif a[0] == 'VARIABLE':
            b = parse_variable(tokens, i)
            l.append(['PRECOMPILED', b[0][:-1]])
            i += b[1]
        elif a[0] == 'BINARY_OPERATOR':
            if a[1] == '&&':
                l.append(['PRECOMPILED', 'and'])
            elif a[1] == '||':
                l.append(['PRECOMPILED', 'or'])
        elif a[0] == 'CLASS_DEFINER':
            b = parse_keyword(tokens, 'class', i, True, True)
            l.append(['PRECOMPILED', b[0]])
            i += b[1]
        elif a[0] == 'FUNCTION_DEFINER':
            b = parse_keyword(tokens, 'def', i, True, True)
            l.append(['PRECOMPILED', b[0]])
            i += b[1]
        elif a[0] == 'BOOL_REVERSE':
            l.append(['PRECOMPILED', 'not ' + a[1][2:-1]])
        elif a[0] == 'BOOL':
            l.append(['BOOL', a[1][0].upper() + a[1][1:]])
        elif a[0] == 'SCOPE+1':
            b = create_compound_statement(tokens, i)
            l.append(['COMPOUND_BLOCK', b[0]])
            i += b[1]
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
        if a[0] == 'KEYWORD':
            b = parse_keyword(tokens, a[1], i, True)
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
            o += scope * '  ' + textwrap.dedent(a[1])
            if i + 1 < len(tokens):
                if tokens[i + 1][1] == ';':
                    o += '\n'
        elif a[0] == 'UNKNOWN':
            print('Unknown type: "' + a[1] + '" found.')
            sys.exit()
        i += 1
    return o


def create_compound_statement(tokens, i):
    global scope
    s = tokens[i][2]
    a = i
    while a < len(tokens):
        if len(tokens[a]) > 2 and tokens[a][0] == 'SCOPE-1':
            if tokens[a][2] == s:
                break
        a += 1
    c = tokens[i+1:a]
    scope += 1
    o = parse_code(process(c))
    scope -= 1
    return [o, len(c)+1]


def parse_variable(tokens, i):
    t = tokens[i][1][1:]
    n = tokens[i + 1][1].split('|')
    o = tokens[i + 2][1]
    if ['LINEFEED', ';'] in tokens[i + 2:]:
        v = tokens[i + 3:tokens.index(['LINEFEED', ';'], i + 2) + 1]
    else:
        v = tokens[i + 3:-1]
    v = ''.join([a[1].strip() for a in process(v)]).replace(';', '')
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
    a = i
    while a < len(tokens):
        if tokens[a][0] in ['LINEFEED', 'SCOPE+1', 'COMPOUND_BLOCK'] or tokens[a] == ['SYMBOL', ',']:
            break
        a += 1
    al = ''.join([b[1] for b in process(tokens[i+1:a])])
    return [scope * '  ' + f + al + ')\n', a - i]


def parse_keyword(tokens, k, i, forcelf=False, brackets=False):
    global scope
    b = i
    while b < len(tokens):
        if tokens[b][0] in ['SCOPE+1', 'COMPOUND_BLOCK', 'PRECOMPILED', 'KEY']:
            break
        b += 1
    c = tokens[i + 1:b]
    n = c[0][1] if c else ''
    a = tokens[i + 1:b + 1]
    j = tokens[b:]
    linefeed = (['KEY', '::'] not in a and ['SCOPE+1', '{', scope + 1] in a) or forcelf
    if j[0] == ['KEY', '::']:
        a = b
        while a < len(tokens):
            if tokens[a][0] in ['LINEFEED', 'PRECOMPILED']:
                break
            a += 1
        j = tokens[b:a + 1]
    elif j[0] == ['SCOPE+1', '{', scope + 1]:
        j = j[:j.index(['SCOPE-1', '}', scope + 1])]
    elif j[0][0] == 'COMPOUND_BLOCK':
        j = ['PRECOMPILED', j[0][1]]
    elif j[0][0] == 'PRECOMPILED':
        j = [j[0]]
    if j[0] == ['KEY', '::']:
        if j[-1] != ['LINEFEED', ';']:
            j.append(['LINEFEED', ';'])
    nal = ''.join([a[1] + (',' if brackets else ' ') for a in process(c[1:])])
    nal = ('(' if brackets else '') + nal[:-1] + (')' if brackets else '')
    o = scope * '  ' + k + (' ' if n else '') + n + nal + ':' + ('\n' if linefeed else '')
    scope += 1
    z = parse_code(process(j[1:] if j[0][0] in ['KEY', 'SCOPE+1'] else j))
    scope -= 1
    if z.endswith('\n'):
        z = z[:-1]
    o += z + ('\n' if linefeed else '')
    m = 1
    if j[0] == ['KEY', '::']:
        m = len(j) - 1
    elif j[0] == ['SCOPE+1', '{', scope + 1]:
        m = len(j) - 1
    elif j[0][0] == 'PRECOMPILED':
        a = 0
        while a < len(tokens):
            if tokens[a][0] != 'PRECOMPILED':
                break
            a += 1
        m = a
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
    a = 0
    while a < len(tokens):
        if a > i and tokens[a][0] == 'COMPOUND_BLOCK':
            break
        a += 1
    f = [b[1] for b in process(tokens[i+1:a])]
    print(f)
    v = ''.join(f[:f.index(';')])
    f = f[f.index(';')+1:]
    c = ''.join(f[:f.index(';')])
    f = ''.join(f[f.index(';')+1:])
    o = scope * '  ' + v + '\n' + scope * '  ' + 'while ' + c + ':\n' + tokens[a][1] + scope * '  ' + '  ' + f + '\n'
    return [o, len(tokens[i:a])]
