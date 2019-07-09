import error
import func
import lexer
import parse_code
import sys

if not sys.argv[1:]:
    print('Input file not given.')
    sys.exit()
try:
    with open(sys.argv[1]) as f:
    #if f.name.endswith('.yt'):
        src = f.read()
    #else:
    #    print('Invalid file type, must end with extension \'.yt\'.')
    #    exit()
except FileNotFoundError if sys.version_info[0] > 2 else IOError:
    print('Input file could not be opened.')
    sys.exit()

s = src.split('\n')
src = func.remove_comments(src)
#error.error_check(s)
pretokens = lexer.tokenise(lexer.split_src(src))
print(pretokens)
#tokens = parse_code.process(pretokens)
#compiled = parse_code.parse_code(tokens)
#compiled += '\nif "Main" in globals():\n  a = Main(*sys.argv[1:])\nelse:\n  error.error_code(0, ' + str(len(s)) + ', ["' + s[len(s)-1] + '", "' + s[len(s)-2] + '", None])'
#error.env(compiled, {'error': error})
