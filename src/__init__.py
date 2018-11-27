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

tokens = lexer.tokenize(src)
compiled = parse_code.parse_code(tokens)
compiled += '\nif "Main" in globals():\n  a = Main()\nelse:\n  error.error_code(0)'
exec(compiled, {})
