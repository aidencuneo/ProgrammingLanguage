import error
import func
import lexer
import sys

scope = 0


'''
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
            o += parse_class_definer(tokens, i)
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
            sys.exit()
        i += 1
    return o
'''
