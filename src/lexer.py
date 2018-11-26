import func, re


def tokenize(string):
    src = func.do_split(string)
    l = []
    for a in src:
        lf = False
        if a.endswith(';') and a != ';':
            a = a[:-1]
            lf = True
        if a.startswith('$'):
            l.append(['VARIABLE', a])
        elif a in ['if', 'else', 'elif', 'while', 'for']:
            l.append(['KEYWORD', a])
        elif a in ['import', 'raise', 'return']:
            l.append(['SPECIAL_KEYWORD', a])
        elif a in ['pass', 'break']:
            l.append(['STATIC_KEYWORD', a])
        elif a == 'fun':
            l.append(['FUNCTION_DEFINER', a])
        elif a == 'class':
            l.append(['CLASS_DEFINER', a])
        elif a == 'switch':
            l.append(['SWITCH_DEFINER', a])
        elif a == 'case':
            l.append(['CASE_DEFINER', a])
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
        elif a in ',':
            l.append(['SYMBOL', a])
        elif a in '*-/+%=':
            l.append(['OPERATOR', a])
        elif a == '&&' or a == '||':
            l.append(['BINARY_OPERATOR', a])
        elif a == '==' or a == '!=' or a == '>' or a == '<' or a == '<=' or a == '>=':
            l.append(['COMPARISON_OPERATOR', a])
        elif a.startswith('!'):
            l.append(['FUNCTION_CALL', a])
        elif a == '{':
            l.append(['SCOPE+1', a])
        elif a == '}':
            l.append(['SCOPE-1', a])
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
        elif (a.startswith('"') and a.endswith('"')) or (a.startswith("'") and a.endswith("'")):
            l.append(['STRING', a])
        elif a.startswith('[') and a.endswith(']'):
            l.append(['LIST', a])
        elif a.startswith('`') and a.endswith('`'):
            l.append(['INCLUDE_STATEMENT', a])
        elif re.match("[a-z]", a) or re.match("[A-Z]", a):
            l.append(['INDENTIFIER', a])
        elif a.startswith('__') and a.endswith('__'):
            l.append(['SPECIAL_IDENTIFIER', a])
        else:
            l.append(['UNKNOWN', a])
        if lf:
            l.append(['LINEFEED', ';'])
    return l
