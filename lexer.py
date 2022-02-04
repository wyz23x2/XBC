from main import *
from utils import *
from sys import intern as i
from collections import deque

# Binary Operators #
ADD    = 0x1   #  +
SUB    = 0x2   #  -
MUL    = 0x3   #  *
DIV    = 0x4   #  /
MOD    = 0x5   #  %
POW    = 0x6   #  ^
LSHIFT = 0x7   #  <<
RSHIFT = 0x8   #  >>
LT     = 0x9   #  <
LE     = 0xA   #  <=
EQ     = 0xB   #  ==
NE     = 0xC   #  !=
GE     = 0xD   #  >=
GT     = 0xE   #  >
RANGE  = 0xF   #  ~
ASSIGN = 0x10  #  =
MEMBER = 0x11  #  .
AND    = 0x12  #  &
OR     = 0x13  #  |
# Unary Operators #
NOT    = 0x14  #  !
POS    = 0x15  #  +
NEG    = 0x16  #  -
REF    = 0x17  #  @
# Bitwise AND/OR/NOT are functions in XBC.
NDIC  = {1: {i("+"): POS, i("-"): NEG, i("!"): NOT, i("@"): REF},
         2: {i("+"): ADD, i("-"): NEG, i("*"): MUL, i("/"): DIV,
             i("%"): MOD, i("^"): POW, i("<<"): LSHIFT, i(">>"): RSHIFT,
             i("<"): LT, i("<="): LE, i("=="): EQ, i("!="): NE,
             i(">="): GE, i(">"): GT, i("~"): RANGE},
         }
KEYWORDS  = frozenset({"if"})
LCOMMENT  = "#"
SCOMMENT  = "#*"
ECOMMENT  = "*#"
STRSTART  = "'", '"'
STREND    = STRSTART
ESCAPE_MAPPING = {'\\\\': '\\',  # !! This must be the first.
                  r'\n': '\n',
                  r'\r': '\r',
                  r'\t': '\t'}
MAXSTRLEN = None

class _tokenns:
    def __init__(self, name='namespace'):
        self.__name = name
    def __call__(self, obj):
        if isinstance(obj, str):
            def inner(x):
                setattr(self, obj, x)
                x.in_token = True
                return x
            return inner
        else:
            setattr(self, obj.__name__, obj)
            obj.in_token = True
            return obj
    def __getattr__(self, name):
        if name == 'Kw':
            return self.Keyword
        raise AttributeError(f'Namespace {self.__name} has no attribute {name!r}')
token = _tokenns('token')
@token('Token')
class _Token:
    _tid = 0
    _id = 0
    def _setid(self):
        self.__id = self.__class__._id
        self.__tid = _Token._tid
        self.__class__._id += 1
        _Token._tid += 1
    def __init__(self, content: str):
        self._setid()
        self.cnt = content
    @staticmethod
    def _cls_name(cls):
        if getattr(cls, 'in_token', False):
            return f'token.{cls.__name__}'
        return cls.__name__
    def __str__(self):
        if type(self) is _Token:
            return f'Token({self.content!r})'
        return f'{self.__class__.__name__}({self.content!r})'
    def __repr__(self):
        if type(self) is _Token:
            return f'token.Token({self.content!r})'
        return f'{self._cls_name(self.__class__)}({self.content!r})'
    @property
    def id(self):
        return self.__id
    @property
    def tid(self):
        return self.__tid
    @property
    def content(self):
        return self.cnt
    def __eq__(self, other):
        return self.content == getattr(other, 'content', 0)
    def __hash__(self):
        return hash(self.content)
@token
class Name(_Token):
    def __init__(self, name: str):
        self._setid()
        self.name = name
    @property
    def content(self):
        return self.name
del Name
@token
class Op(_Token):
    def __init__(self, op: str, /):
        self._setid()
        self.op = i(op)
    # MV: The grouping of operators and sides should be done by the parser.
    # def __init__(self, op: str, left=None, right=None, middle=None, n=-1):
    #     self._setid()
    #     self.op = i(op)
    #     if n is None or n <= 0:
    #         n = (left is not None) + (middle is not None) + (right is not None)
    #     if n == 0:
    #         raise ValueError('No sides provided')
    #     try:
    #         self.type = NDIC[n][op]
    #     except KeyError as e:
    #         raise ValueError(f'Invalid operator {op!r} for n={n!r}') from e
    #     self.left, self.middle, self.right = left, middle, right
    @staticmethod
    def isop(s: str, n: int|None = None):
        s = i(s)
        if n is None:
            for x in NDIC:
                try:
                    NDIC[x][s]
                except KeyError:
                    pass
                else:
                    return True
            else:
                return False
        else:
            try:
                NDIC[n][s]
            except KeyError:
                return False
            else:
                return True
    def __str__(self):
        return f'{self.__class__.__name__}({self.op!r})'
    def __repr__(self):
        return f'{self._cls_name(self.__class__)}({self.op!r})'
    @property
    def content(self):
        return self.op
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.op == other.op
del Op
@token
class Keyword(_Token):
    def __init__(self, keyword: str):
        if keyword not in KEYWORDS:
            warning(f"Invalid keyword: {keyword!r}", stacklevel=5)
        self.keyword = keyword
    @property
    def content(self):
        return self.keyword
del Keyword
@token
class String(_Token):
    pass
del String

def lex(code: str) -> list[token.Token]:
    if not code.strip():
        return [code]
    tokens = deque()
    start = 0
    end = len(code)
    while True:
        if end > len(code):
            break
        if end <= start:
            break  # TODO
        valid = False
        s = code[start:end]
        if (s.startswith(STRSTART) and
            s[0] == s[-1]          and
            s.count(s[0]) == 2     and
            s.endswith(STREND)):
            # String token
            if '\\' not in s:
                # No escapes
                tokens.append(token.String(s[1:-1]))
                valid = True
        elif token.Op.isop(s):
            tokens.append(token.Op(s))
            valid = True
        if valid:
            start = end
            end = len(code)
        else:
            end -= 1
    return tokens
# def lex(code: str) -> list[token.Token]:
#     tokens = deque()
#     lines = code.splitlines()
#     in_string = False
#     in_comment = False
#     this_str = deque(maxlen=MAXSTRLEN)
#     str_escaping = False
#     str_start = None
#     prev = []
#     strpush = this_str.append
#     for line in lines:
#         if line.startswith(LCOMMENT) and not in_string: continue
#         for char in line:
#             prev.append(char)
#             ps = ''.join(prev)
#             if str_escaping:
#                 # FIXME: Multi char escapes unsupported
#                 match char:
#                     case 'n': strpush('\n')
#                     case 'r': strpush('\r')
#                     case 't': strpush('\t')
#                     case 'b': strpush('\b')
#                     case 'f': strpush('\f')
#                     case '"': strpush('"')
#                     case "'": strpush("'")
#                     case '\\': strpush('\\')
#                     case _:
#                         ...
#                         strpush('\\')
#                         strpush(char)
#             if in_string and not in_comment:
#                 if char == '\\':
#                     str_escaping = True
#                     continue
#                 if char == str_start:
#                     tokens.append(token.String(''.join(this_str)))
#                     this_str.clear()
#                     in_string = False
#                 else:
#                     strpush(char)
#             elif ps.endswith(ECOMMENT):
#                 in_comment = False
#                 prev.clear()
#                 continue
#             elif in_comment:
#                 continue
#             elif ps.endswith(SCOMMENT):
#                 in_comment = True
#             else:
#                 ...


if __name__ == '__main__' and DEBUG >= 2:
    x = token.Token("x")
    print(x)
    y = token.Name("y")
    print(y)
    z = token.Op("*")
    print(z)
    a = token.Kw('iXf')
    print(a)
    print(lex('"x"+"y"'))
