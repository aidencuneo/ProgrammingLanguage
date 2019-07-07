import error
import func
import re

scope_id = 0


def tokenise_line(line):
    global scope_id
    l = []
    for a in line:
        lf = comma = fstop = False
        if a.endswith(';') and a != ';':
            a = a[:-1]
            lf = True
        if a.endswith(',') and a != ',':
            a = a[:-1]
            comma = True
        if a.endswith('.') and a != '.':
            a = a[:-1]
            fstop = True
        if a.startswith('$'):
            l.append(['VARIABLE', a])
        elif a in ['if', 'else', 'elif', 'while']:
            l.append(['KEYWORD', a])
        elif a == 'for':
            l.append(['FOR_LOOP', a])
        elif a == 'import':
            l.append(['IMPORT_STATEMENT', a])
        elif a == 'raise':
            l.append(['RAISE_STATEMENT', a])
        elif a == 'return':
            l.append(['RETURN_STATEMENT', a])
        elif a in ['pass', 'break']:
            l.append(['STATIC_KEYWORD', a])
        elif a == 'fun':
            l.append(['FUNCTION_DEFINER', a])
        elif a == 'class':
            l.append(['CLASS_DEFINER', a])
        elif a == 'try':
            l.append(['TRY_DEFINER', a])
        elif a == 'catch':
            l.append(['CATCH_DEFINER', a])
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
        elif a.startswith('!{') and a.endswith('}'):
            l.append(['BOOL_REVERSE', a])
        elif a.startswith('!'):
            l.append(['FUNCTION_CALL', a])
        elif a == '{':
            scope_id += 1
            l.append(['SCOPE+1', a, scope_id])
        elif a == '}':
            l.append(['SCOPE-1', a, scope_id])
            scope_id -= 1
        elif a == '(':
            l.append(['SWITCH_BEGIN', a])
        elif a == ')':
            l.append(['SWITCH_END', a])
        elif a == '**':
            l.append(['COMMENT_DEFINER', a])
        elif a == '::':
            l.append(['KEY', a])
        elif a == ';':
            l.append(['LINEFEED', ';'])
        elif func.is_int(a):
            l.append(['INTEGER', a])
        elif func.is_float(a):
            l.append(['FLOAT', a])
        elif a == 'true' or a == 'false':
            l.append(['BOOL', a])
        elif (a.startswith('"') and a.endswith('"')) or (a.startswith("'") and a.endswith("'")):
            l.append(['STRING', a])
        elif a.startswith('[') and a.endswith(']'):
            l.append(['LIST', a])
        elif re.match('[a-z]', a) or re.match("[A-Z]", a):
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
        elif comma:
            l.append(['SYMBOL', ','])
        elif fstop:
            l.append(['FULL_STOP', '.'])
    return l


def tokenise_file(src):
    l = []
    for a in src.split('\n'):
        t = tokenise_line(func.split_line(a))
        for b in t:
            l += [b]
    return l
