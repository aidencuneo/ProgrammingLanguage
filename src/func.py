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


def index_of(s, l, start=0):
    i = start
    while i < len(s):
        if s[i] in l:
            break
        i += 1
    return i


def remove_comments(src):
    o = ''
    lc = 0
    bc = 0
    for a in src:
        if a == '/' and lc < 3:
            lc += 1
        elif a != '/' and lc == 1:
            lc = 0
        elif a == '#' and not bc:
            bc = 1
        elif a == '#' and bc == 1:
            bc = 2
        elif a == '\n':
            lc = 0
        elif a != '#' and bc == 1:
            bc = 0
        elif a == '#' and bc == 2:
            bc = 3
        elif a == '#' and bc == 3:
            bc = 0
            a = ''
        if lc < 1 and bc < 1 or a == '\n':
            o += a
    return o
