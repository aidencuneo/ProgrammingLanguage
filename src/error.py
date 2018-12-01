import lexer, textwrap


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
                if scope < 0:
                    error_code(4, i+1, [s[i], s[i-1], s[i+1]])
            if c[0][0] == 'RETURN_STATEMENT':
                if c[1][0] != 'LINEFEED':
                    if c[1][0] == 'IDENTIFIER':
                        pass
                else:
                    error_code(3, i+1, [s[i], s[i-1], s[i+1]])
    if scope != 0:
        error_code(2, len(s), [s[len(s)-2], s[len(s)-3], s[len(s)-1]])
    exit()


def error_code(code, l, e):
    if code == 0:
        print('Main method not found.')
    elif code == 1:
        print('Not enough arguments for variable creation.')
    elif code == 2:
        print('End of file without completed scope.')
    elif code == 3:
        print('Return statement requires at least one argument.')
    elif code == 4:
        print('Can not end a loop that does not exist. (Occurs when number of "}" is greater than number of "{")')
    else:
        print('Unknown error occurred.')
    if l-1 > 0 and len(e) > 1:
        print(str(l-1) + ': ' + str(e[1]))
    print(str(l) + ': ' + str(e[0]))
    if len(e) > 2:
        print(str(l+1) + ': ' + str(e[2]))
    exit()
