from main import *
from utils import *
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
NDIC  = {1: {"+": POS, "-": NEG, "!": NOT, "@": REF},
         2: {"+": ADD, "-": NEG, "*": MUL, "/": DIV,
             "%": MOD, "^": POW, "<<": LSHIFT, ">>": RSHIFT,
             "<": LT, "<=": LE, "==": EQ, "!=": NE,
             ">=": GE, ">": GT, "~": RANGE},
         }
KEYWORDS  = frozenset({"if"})
LCOMMENT  = "#"
SCOMMENT  = "#*"
ECOMMENT  = "*#"
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
    def __init__(self, op: str, left=None, right=None, middle=None, n=-1):
        self._setid()
        self.op = op
        if n is None or n <= 0:
            n = (left is not None) + (middle is not None) + (right is not None)
        if n == 0:
            raise ValueError('No sides provided')
        try:
            self.type = NDIC[n][op]
        except KeyError as e:
            raise ValueError(f'Invalid operator {op!r} for n={n!r}') from e
        self.left, self.middle, self.right = left, middle, right
    @staticmethod
    def isop(s: str, n: int|None = None):
        if n is None:
            for i in NDIC:
                try:
                    NDIC[i][s]
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
        lis = [repr(self.op)]
        if self.left is not None:
            lis.append(f'left={self.left!s}')
        if self.middle is not None:
            lis.append(f'middle={self.middle!s}')
        if self.right is not None:
            lis.append(f'right={self.right!s}')
        return f'{self.__class__.__name__}({", ".join(lis)})'
    def __repr__(self):
        return f'{self._cls_name(self.__class__)}({self.op!r}, left={self.left!r}, middle={self.middle!r}, right={self.right!r})'
    @property
    def content(self):
        return self.op
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return ((self.left, self.middle, self.right, self.op) ==
                (other.left, other.middle, other.right, other.op))
del Op
@token
class Keyword(_Token):
    def __init__(self, keyword: str):
        if keyword not in KEYWORDS:
            warning(f"Invalid keyword: {keyword!r}")
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
    tokens = deque()
    lines = code.splitlines()
    in_string = False
    in_comment = False
    this_str = deque(maxlen=MAXSTRLEN)
    str_start = None
    prev = []
    for line in lines:
        if line.startswith(LCOMMENT) and not in_string: continue
        for char in line:
            prev.append(char)
            ps = ''.join(prev)
            if in_string and not in_comment:
                # TODO
                if char == '\\':
                    ...
                if char == str_start:
                    tokens.append(token.String(''.join(this_str)))
                    this_str.clear()
                    in_string = False
                else:
                    this_str.append(char)
            elif ps.endswith(ECOMMENT):
                in_comment = False
                prev.clear()
                continue
            elif in_comment:
                continue
            elif ps.endswith(SCOMMENT):
                in_comment = True
            else:
                ...


if __name__ == '__main__' and DEBUG >= 2:
    x = token.Token("x")
    print(x)
    y = token.Name("y")
    print(y)
    z = token.Op("*", x, y)
    print(z)
    a = token.Kw('iXf')
    print(a)
