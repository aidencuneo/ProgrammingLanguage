'''

Programming language created by Aiden Blishen Cuneo.
First started on: 22/11/18.

'''

import error
import func
import lexer
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

src = func.remove_comments(src)
pretokens = lexer.tokenise(src)
print(pretokens)
error.error_check(src)
tokens = process(pretokens)
#compiled = parse_code(tokens)
#compiled += '\nif "Main" in globals():\n  a = Main(*sys.argv[1:])\nelse:\n  error.error_code(0, ' + str(len(s)) + ', ["' + s[len(s)-1] + '", "' + s[len(s)-2] + '", None])'
#error.env(compiled, {'error': error})
