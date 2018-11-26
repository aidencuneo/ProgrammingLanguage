def is_int(i):
    try:
        int(i)
        return True
    except ValueError:
        return False


def is_float(i):
    try:
        float(i)
        return True
    except ValueError:
        return False


def do_split(s, at=' '):
    s_quote = False
    d_quote = False
    s_brack = False
    include = False
    l = []
    o = ''
    for a in s:
        if a == '"' and not s_quote:
            d_quote = not d_quote
            o += a
        elif a == "'" and not d_quote:
            s_quote = not s_quote
            o += a
        elif a == '[':
            s_brack = True
            o += a
        elif a == ']':
            s_brack = False
            o += a
        elif a == '`':
            include = not include
            o += a
        elif (a == at or a == '\n' or a == '\r' or a == ';')\
        and not s_quote and not d_quote and not s_brack and not include:
            if a == ';':
                o += ';'
            l.append(o)
            o = ''
        else:
            o += a
    l.append(o)
    l = list(filter(None, l))
    nl = []
    comment = False
    for a in l:
        if a == '**' or a.startswith('**') or a.endswith('**'):
            comment = not comment
        elif not comment:
            nl.append(a)
    return nl
