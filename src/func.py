import sys, textwrap


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


def split_line(s, at=' '):
    comment = 0
    s_quote = d_quote = s_brack = include = False
    l = []
    o = ''
    for a in textwrap.dedent(s):
        if a == '/' and comment != 2:
            comment += 1
        elif 0 < comment < 2 and a != '/':
            comment -= 1
        if a == '"' and not s_quote:
            d_quote = not d_quote
        elif a == "'" and not d_quote:
            s_quote = not s_quote
        elif a == '[':
            s_brack = True
        elif a == ']':
            s_brack = False
        elif a == '`':
            include = not include
        if comment < 2:
            o += a
        if (a == at or a == ';') and not s_quote and not d_quote\
        and not s_brack and not include and comment < 2:
            if a == ';':
                o += ';'
            l.append(o[:-1])
            o = ''
        if comment == 2:
            o = o[:-1]
    l.append(o)
    l = list(filter(None, l))
    return l


def index_of(s, l, start=0):
    i = start
    while i < len(s):
        if s[i] in l:
            break
        i += 1
    return i
