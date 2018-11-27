def error_code(code, at=''):
    if code == 0:
        print('Main method not found.')
    elif code == 1:
        print('Not enough arguments for variable creation.')
    else:
        print('Unknown error occurred.')
    if len(at) > 0:
        print('At: ' + at)
    exit()
