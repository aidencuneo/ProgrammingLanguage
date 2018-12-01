import lexer


def error_check(s):
    scope = 0
    for i in range(len(s)):
        a = s[i].split(' ')
        a = [b for b in a if b != '']
        if len(a) > 0:
            c = lexer.tokenize_line(a)
            print(c)
            for b in a:
                if b == '{':
                    scope += 1
                elif b == '}':
                    scope -= 1
    if scope != 0:
        error_code(2, len(s))
    exit()


def error_code(code, l=0):
    if code == 0:
        print('Main method not found.')
    elif code == 1:
        print('Not enough arguments for variable creation.')
    elif code == 2:
        print('End of file without completed scope.')
    else:
        print('Unknown error occurred.')
    if l > 0:
        print('At: Line ' + str(l))
    exit()
