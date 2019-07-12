import error
import func
import re
import string
import sys

alphabet = string.letters if sys.version_info[0] < 3 else string.ascii_letters
digits = string.digits
symbols = string.punctuation
whitespace = string.whitespace
scope_id = 0


def tokenise(src):
    global scope_id
    l = []
    if isinstance(src, str):
        src = split_src(src)
    for a in src:
        lf = False
        if a.endswith(';') and a != ';':
            a = a[:-1]
            lf = True
        if a.startswith('$'):
            l.append(['VARIABLE', a])
        elif a in ['if', 'else', 'elif', 'while']:
            l.append(['KEYWORD', a])
        elif a == 'for':
            l.append(['FOR_LOOP', a])
        elif a == 'include':
            l.append(['INCLUDE', a])
        elif a == 'class':
            l.append(['CLASS_DEFINER', a])
        elif a == 'fun':
            l.append(['FUNCTION_DEFINER', a])
        elif a == 'try':
            l.append(['TRY_DEFINER', a])
        elif a == 'catch':
            l.append(['CATCH_DEFINER', a])
        elif a == 'do':
            l.append(['FUNCTION_CALL', a])
        elif a == 'return':
            l.append(['RETURN', a])
        elif a == '?':
            l.append(['IF_SHORTHAND', a])
        elif a == '|':
            l.append(['PIPE', a])
        elif a == '+=' or a == '-=' or a == '*=' or a == '/=' or a == '%=':
            l.append(['INCREMENTAL_OPERATOR', a])
        elif a in ['*', '-', '/', '+', '%', '=']:
            l.append(['OPERATOR', a])
        elif a == '&&' or a == '||':
            l.append(['BINARY_OPERATOR', a])
        elif a == '==' or a == '!=' or a == '>' or a == '<' or a == '<=' or a == '>=':
            l.append(['COMPARISON_OPERATOR', a])
        elif a == '!':
            l.append(['BOOL_REVERSE', a])
        elif a == '{':
            scope_id += 1
            l.append(['SCOPE+1', a, scope_id])
        elif a == '}':
            l.append(['SCOPE-1', a, scope_id])
            scope_id -= 1
        elif a == ';':
            l.append(['LINEFEED', ';'])
        elif a in symbols:
            l.append(['SYMBOL', a])
        elif func.is_int(a):
            l.append(['INTEGER', a])
        elif func.is_float(a):
            l.append(['FLOAT', a])
        elif a == 'true' or a == 'false':
            l.append(['BOOL', a])
        elif (a.startswith('"') and a.endswith('"')) or (a.startswith("'") and a.endswith("'")):
            l.append(['STRING', a])
        elif re.match('[a-z]', a) or re.match('[A-Z]', a):
            l.append(['IDENTIFIER', a])
        elif a.startswith('__') and a.endswith('__'):
            l.append(['SPECIAL_IDENTIFIER', a])
        elif (re.match('[a-z]', a[1:]) or re.match('[A-Z]', a[1:])) and a[0] == '*':
            l.append(['ARGS_IDENTIFIER', a])
        elif (re.match('[a-z]', a[2:]) or re.match('[A-Z]', a[2:])) and a[0] + a[1] == '**':
            l.append(['KWARGS_IDENTIFIER', a])
        else:
            l.append(['UNKNOWN', a])
        if lf:
            l.append(['LINEFEED', ';'])
    return l


def split_src(s):
    sq = False
    dq = False
    l = []
    o = ''
    p = ''
    t = ''
    for a in s.strip():
        q = p
        if a in alphabet:
            p = 'A'
        elif a in digits:
            p = 'D'
        elif a in symbols:
            p = 'S'
        elif a in whitespace:
            p = 'W'
        con = (q != p and p != 'W' or p == 'S')\
            and not (sq or dq)
        if con:
            l.append(o.strip())
            o = ''
        if a == "'":
            sq = not sq
        elif a == '"':
            dq = not dq
        o += a
        t = a
    l.append(o)
    l = list(filter(None, l))
    k = []
    pair = []
    for a in l:
        pair.append(a)
        if pair[1:]:
            if pair[0] == pair[1] == '&':
                del k[-1]
                k.append('&&')
            elif pair[0] == pair[1] == '|':
                del k[-1]
                k.append('||')
            elif pair[0] == pair[1] == ';':
                del k[-1]
                k.append(';')
            elif pair[0] == pair[1] == '+':
                del k[-1]
                k += ['+=', '1']
            elif pair[0] == pair[1] == '-':
                del k[-1]
                k += ['-=', '1']
            elif pair[1] == '=':
                if pair[0] == '+':
                    del k[-1]
                    k.append('+=')
                elif pair[0] == '-':
                    del k[-1]
                    k.append('-=')
                elif pair[0] == '*':
                    del k[-1]
                    k.append('*=')
                elif pair[0] == '/':
                    del k[-1]
                    k.append('/=')
                elif pair[0] == '=':
                    del k[-1]
                    k.append('==')
                else:
                    k.append(a)
            else:
                k.append(a)
            del pair[0]
        else:
            k.append(a)
    return k
