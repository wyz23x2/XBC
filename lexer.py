from __future__ import annotations
from main import *
from utils import *
from sys import intern as i
from string import ascii_letters as _letters, whitespace as _ws
from collections import deque
try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache

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
RESERVED  = '\x03'
ESCAPE_MAPPING = {'\\\\': f'\\{RESERVED}',  # !! This must be the first.
                  r'\n': '\n',
                  r'\r': '\r',
                  r'\t': '\t'}
DIGITS    = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
NAMESET   = DIGITS | set(_letters) | {'$', '_'}
PAIRS     = {('(', ')'), ('[', ']'), ('{', '}')}
EB        = {p[1] for p in PAIRS}
MAXSTRLEN = None

def isdigit(s: str) -> bool:
    return s in DIGITS
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
    @staticmethod
    @cache
    def isname(s: str):
        if not s:
            return False
        if s[0] not in NAMESET - DIGITS:
            return False
        return not tuple(filter(lambda x: x not in NAMESET, s))
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
    @cache
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
        if not self.iskeyword(keyword):
            warning(f"Invalid keyword: {keyword!r}", stacklevel=5)
        self.keyword = keyword
    @property
    def content(self):
        return self.keyword
    @staticmethod
    @cache
    def iskeyword(s):
        return s in KEYWORDS
del Keyword
@token
class String(_Token):
    pass
del String
@token
class Integer(_Token):
    def __init__(self, n: str):
        if not self.isint(n):
            warning(f"Invalid integer: {n!r}", stacklevel=5)
        self.n = n
    @property
    def content(self):
        return self.n
    @staticmethod
    @cache
    def isint(s):
        if not s:
            return False
        return not tuple(filter(lambda x: not isdigit(x), s))
del Integer
@token
class Float(_Token):
    def __init__(self, f: str):
        if not self.isfloat(f):
            warning(f"Invalid float: {f!r}", stacklevel=5)
        self.f = f
    @property
    def content(self):
        return self.f
    @staticmethod
    @cache
    def isfloat(f: str):
        if '.' not in f:
            return False
        parts = tuple(filter(None, f.split('.')))
        if f.index('.') == 0:
            parts = ['0', *parts]
        elif f.index('.')+1 == len(f):
            parts = [*parts, '0']
        if len(parts) > 2:
            return False
        return token.Integer.isint(parts[0]) and token.Integer.isint(parts[1])
del Float
@token
class Group(_Token):
    def __init__(self, *tokens, bracket='('):
        self.tokens = list(tokens)
        self.bracket = bracket
    def add(self, *tokens):
        self.tokens.extend(tokens)
    @property
    def content(self):
        return self.tokens
    def __iter__(self):
        return self.tokens
    def __getitem__(self, idx):
        return self.tokens[idx]
    def __len__(self):
        return len(tuple(self))
    def __str__(self):
        return f'{self.__class__.__name__}({", ".join(map(str, self.tokens))}, bracket={self.bracket!r})'
    def __repr__(self):
        return f'{self._cls_name(self.__class__)}({", ".join(map(repr, self.tokens))}, bracket={self.bracket!r})'
del Group
MAPPING = {token.Op.isop: token.Op,
           token.Float.isfloat: token.Float,
           token.Integer.isint: token.Integer,
           token.Keyword.iskeyword: token.Keyword,
           token.Name.isname: token.Name}
def lex(code: str) -> list[token.Token]:
    if not code.strip():
        return []
    lc = len(code)
    tokens = deque(maxlen=lc)
    start = 0
    end = lc
    group_se = deque()
    depth = 0
    def append(x):
        nonlocal tokens, group_se
        if depth <= 0:
            tokens.append(x)
        else:
            t = tokens[-1]
            for _ in range(1, depth):
                t = t[-1]
            t.add(x)
    while True:
        if end > lc:
            break
        if end <= start:
            if start >= lc:
                break
            end = lc
            start += 1
        valid = 0
        s = code[start:end]
        # print(f'{start=!r} {end=!r} {s=!r}')
        if depth and start >= group_se[-1][1]:
            depth -= 1
            group_se.pop()
        if (s.startswith(STRSTART)  and
            s[0] == s[-1]           and
            (c:=s.count(s[0])) >= 2 and
            s.endswith(STREND)):
            # String token
            if '\\' not in s:
                if c > 2:
                    continue
                # No escapes
                append(token.String(s[1:-1]))
                valid = 1
            else:
                for o, n in ESCAPE_MAPPING.items():
                    if o in {f'\\{ss}' for ss in STREND}:
                        if o in s:
                            s = s.replace(o, n)
                            c -= 1
                        else:
                            continue
                    else:
                        s = s.replace(o, n)
                s = s.replace(RESERVED, '')
                if c == 2:
                    append(token.String(s[1:-1]))
                    valid = 1
        elif s[1:] and (s[0], s[-1]) in PAIRS:
            group_se.append((start, end))
            append(token.Group(bracket=s[0]))
            depth += 1
            valid = 2
        else:
            for func in MAPPING:
                if func(s):
                    append(MAPPING[func](s))
                    valid = 1
                    break
        if valid:
            if valid == 2:
                start += 1
                end -= 1
            elif depth:
                start = end
                if end < group_se[-1][1]-1:
                    end = group_se[-1][1]-1
                else:
                    start += 1
                    end = lc
            else:
                start = end
                end = lc
                while start < lc and (code[start] in _ws or code[start] in EB):
                    start += 1
        elif s in _ws or all(map(_ws.__contains__, s)):
            start += len(s)
            end = lc
        else:
            end -= 1
            while start < lc and (code[start] in _ws or code[start] in EB):
                start += 1
    return tokens
def Lex(code, showinput=False):
    from time import perf_counter
    t = perf_counter()
    x = lex(code)
    t = perf_counter()-t
    if showinput:
        print(f'  lex({code!r})\n>', end=' ')
    print(f'{x!r}\nTime used: {t:.8f}s')
    return x, t

if __name__ == '__main__' and DEBUG >= 2:
    # Lex(r'"\\\nx"+"y"')
    Lex('if (-156*-(.657>>3^+x*2.48)-15)*-394.48-3+(10945)*8-6>>2 > 59583*(455-(34858+int("34757")/int("7\\n")[0]))*474)-4958<<(50/5):')
