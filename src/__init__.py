import re, sys


class Main():

    def __init__(self, src):
        self.builtins = globals()
        del self.builtins['src'], self.builtins['f'], self.builtins['__file__'], self.builtins['Main']
        self.scope = 0
        self.src = src
        self.tokens = self.tokenize()
        self.compiled = self.compile()
        self.compiled += '\nif "Main" in globals():\n  a = Main()\nelse:\n  print("Main method not found.")\n  exit()'
        print(self.compiled)
        exec(self.compiled, self.builtins)

    def is_int(self, i):
        try:
            int(i)
            return True
        except ValueError:
            return False
    
    def is_float(self, i):
        try:
            float(i)
            return True
        except ValueError:
            return False

    def do_split(self, s, at=' '):
        s_quote = False
        d_quote = False
        s_brack = False
        include = False
        l = []
        o = ''
        for a in s:
            if a == '"' and not s_quote:
                d_quote = not d_quote
                o += a
            elif a == "'" and not d_quote:
                s_quote = not s_quote
                o += a
            elif a == '[':
                s_brack = True
                o += a
            elif a == ']':
                s_brack = False
                o += a
            elif a == '`':
                include = not include
                o += a
            elif (a == at or a == '\n' or a == '\r' or a == ';')\
            and not s_quote and not d_quote and not s_brack and not include:
                if a == ';':
                    o += ';'
                l.append(o)
                o = ''
            else:
                o += a
        l.append(o)
        l = list(filter(None, l))
        nl = []
        comment = False
        for a in l:
            if a == '**' or a.startswith('**') or a.endswith('**'):
                comment = not comment
            elif not comment:
                nl.append(a)
        return nl

    def tokenize(self, string=None):
        src = self.do_split(self.src if string is None else string)
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
            elif self.is_int(a):
                l.append(['INTEGER', a])
            elif self.is_float(a):
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

    def compile(self, tokens=None):
        tokens = self.tokens if tokens is None else tokens
        i = 0
        o = ''
        while i < len(tokens):
            a = tokens[i]
            if a[0] == 'VARIABLE':
                a = self.parse_variable(tokens, i)
                o += a[0]
                i += a[1]
            elif a[0] == 'FUNCTION_CALL':
                a = self.parse_function_call(tokens, i)
                o += a[0]
                i += a[1]
            elif a[0] == 'KEYWORD':
                a = self.parse_keyword(tokens, a[1], i)
                o += a[0]
                i += a[1]
            elif a[0] == 'SPECIAL_KEYWORD':
                a = self.parse_special_keyword(tokens, a[1], i)
                o += a[0]
                i += a[1]
            elif a[0] == 'STATIC_KEYWORD':
                o += self.scope * '  ' + a[1] + '\n'
            elif a[0] == 'FUNCTION_DEFINER':
                o += self.parse_function_definer(tokens, i)
            elif a[0] == 'CLASS_DEFINER':
                o += self.parse_class_definer(tokens, i)
            elif a[0] == 'SWITCH_DEFINER':
                a = self.parse_switch_definer(tokens, i)
                o += a[0]
                i += a[1]
            elif a[0] == 'TRY_DEFINER':
                o += self.scope * '  ' + 'try:\n'
            elif a[0] == 'CATCH_DEFINER':
                a = self.parse_catch_definer(tokens, i)
                o += a[0]
                i += a[1]
            elif a[0] == 'INCLUDE_STATEMENT':
                o += self.compile(self.tokenize(a[1][1:-1] + ';'))
            elif a[0] == 'SCOPE+1':
                self.scope += 1
            elif a[0] == 'SCOPE-1':
                self.scope -= 1
            elif a[0] == 'OPERATOR':
                o += a[1]
            elif a[0] == 'UNKNOWN':
                print('Unknown type: "' + a[1] + '" found during lexical analysis.')
                exit()
            i += 1
        return o

    def parse_variable(self, tokens, i):
        if len(tokens[:tokens.index(['LINEFEED', ';'], i)]) < 2:
            print('Not enough arguments for variable creation. ' +\
                  'Error found at line starting with: "' + tokens[i][1] + '".')
            exit()
        t = tokens[i][1][1:].split('::')
        n = tokens[i+1][1]
        o = tokens[i+2][1]
        v = tokens[i+3:tokens.index(['LINEFEED', ';'], i+2)+1]
        if '`' in ''.join([a[1] for a in v]):
            v = self.compile(v).replace('\n', '').replace('  ', '')
        else:
            v = ''.join([a[1] for a in v]).replace(';', '')
        if len(t) == 1 and t[0] == 'var':
            nt = ''
        else:
            nt = ''
            for a in t:
                nt += a + '('
        if len(tokens[i:tokens.index(['LINEFEED', ';'], i+2)]) < 3:
            o = '='
        return [self.scope * '  ' + n + o + nt + v + ')' * nt.count('(') + '\n', tokens.index(['LINEFEED', ';'], i+2) - i]
    
    def parse_function_call(self, tokens, i):
        f = tokens[i][1][1:].split('::')
        al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
        if '`' in ''.join([a[1] for a in al]):
            al = self.compile(al).replace('\n', '').replace('  ', '')
        else:
            al = ''.join([a[1] for a in al]).replace(';', '')
        nf = ''
        for a in f:
            nf += a + '('
        print(al)
        return [self.scope * '  ' + nf + al + ')' * nf.count('(') + '\n', tokens.index(['LINEFEED', ';'], i) - i]
    
    def parse_keyword(self, tokens, k, i):
        c = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
        if '`' in ''.join([a[1] for a in c]):
            c = self.compile(c).replace('\n', '').replace('  ', '')
        else:
            c = ''.join([a[1] for a in c]).replace(';', '')
        if len(c) > 0:
            c = ' ' + c
        return [self.scope * '  ' + k + c + ':\n', tokens.index(['SCOPE+1', '{'], i) - 1 - i]
    
    def parse_special_keyword(self, tokens, k, i):
        al = tokens[i+1:tokens.index(['LINEFEED', ';'], i)]
        if '`' in ''.join([a[1] for a in al]):
            al = self.compile(al).replace('\n', '').replace('  ', '')
        else:
            al = ''.join([a[1] + ',' for a in al]).replace(';', '')
        if al.endswith(','):
            al = al[:-1]
        return [self.scope * '  ' + k + ' ' + al + '\n', tokens.index(['LINEFEED', ';'], i) - i]
    
    def parse_function_definer(self, tokens, i):
        a = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
        n = a[0][1]
        al = a[1:]
        nal = ''
        for a in al:
            nal += a[1] + ','
        return self.scope * '  ' + 'def ' + n + '(' + nal + '):\n'
    
    def parse_class_definer(self, tokens, i):
        a = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
        n = a[0][1]
        al = a[1:]
        nal = ''
        for a in al:
            nal += a[1] + ','
        return self.scope * '  ' + 'class ' + n + '(' + nal + '):\n'
    
    def parse_switch_definer(self, tokens, i):
        section = tokens[i+1:tokens.index(['SWITCH_END', ')'], i+1)]
        v = section[0][1]
        section = section[2:]
        o = ''
        cases = []
        l = []
        for a in range(len(section)):
            l.append(section[a])
            if a+1 < len(section):
                if section[a+1][1] == 'case':
                    cases.append(l)
                    l = []
        cases.append(l)
        for a in cases:
            a = a[1:]
            o += 'if ' + v + ' '
            for b in a:
                if b[0] == 'KEY':
                    o += '{ '
                else:
                    o += b[1] + ' '
            o += '}\n'
        o = self.compile(self.tokenize(o))
        return [o, len(section)+2]

    def parse_catch_definer(self, tokens, i):
        c = tokens[i+1:tokens.index(['SCOPE+1', '{'], i)]
        if '`' in ''.join([a[1] for a in c]):
            c = self.compile(c).replace('\n', '').replace('  ', '')
        else:
            c = ''.join([a[1] for a in c]).replace(';', '')
        print(c)
        return [self.scope * '  ' + 'except ' + c + ':\n', tokens.index(['SCOPE+1', '{'], i) - 1 - i]


if len(sys.argv) > 1:
    try:
        f = open(sys.argv[1])
        if f.name.endswith('.yt'):
            src = f.read()
            f.close()
        else:
            print('Invalid file type, must end with extension \'.yt\'.')
            exit()
    except FileNotFoundError if sys.version_info[0] > 2 else IOError:
        print('Input file not found.')
        exit()
else:
    print('Input file not given.')
    exit()

m = Main(src)
