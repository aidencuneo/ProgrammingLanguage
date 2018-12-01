import textwrap


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


def do_split(s):
    comment = 0
    l = []
    o = ''
    for a in s:
        if a == '/':
            comment += 1
        elif 0 < comment < 2 and a != '/':
            comment -= 1
        if comment < 2:
            o += a
        if a == ';' or a == '\n' or a == '{' or a == '}':
            l.append(o[:-1])
            o = ''
        if a == '\n':
            comment = 0
            o = o[:-1]
    l.append(o)
    l = [textwrap.dedent(a) for a in l]
    #l = [a for a in l if len(a) > 0]
    print('Lines: ' + str(len(l)))
    exit()
    return l
