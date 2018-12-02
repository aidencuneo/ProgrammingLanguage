import error, func, lexer, parse_code, sys

if len(sys.argv) > 1:
    try:
        f = open(sys.argv[1])
        #if f.name.endswith('.yt'):
        src = f.read()
        f.close()
        #else:
        #    print('Invalid file type, must end with extension \'.yt\'.')
        #    exit()
    except FileNotFoundError if sys.version_info[0] > 2 else IOError:
        print('Input file not found.')
        exit()
else:
    print('Input file not given.')
    exit()

error.error_check(src.split('\n'))
pretokens = lexer.tokenize_file(src)
tokens = parse_code.process(pretokens)
s = src.split('\n')
compiled = parse_code.parse_code(tokens)
compiled += '\nif "Main" in globals():\n  a = Main()\nelse:\n  error.error_code(0, ' + str(len(s)) + ', ["' + s[len(s)-1] + '", "' + s[len(s)-2] + '", None])'
exec(compiled, {'error': error})
