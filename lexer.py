from __future__ import annotations
__all__ = ['token', 'pypy']
from main import *
from utils import *
from sys import intern as i, implementation
from itertools import chain
from string import ascii_letters as _letters, whitespace as _ws
from collections import deque
if implementation.name == 'pypy':
    # cache is much slower on PyPy
    cache = (lambda x: x)
    pypy = True
    import __pypy__  # type: ignore
    __all__.append('__pypy__')
else:
    try:
        from functools import cache
    except ImportError:
        from functools import lru_cache as cache
    pypy = False

__all__.extend(filter(str.isupper, globals()))
# Bitwise AND/OR/NOT are functions in XBC.
OPSET = {'+', '-', '*', '/', '%', '^', '<<', '>>', '<', '<=', '==', '>=', '>',
         '=', '+=', '-=', '*=', '/=', '%=', '^=', '<<=', '>>=', '~=', '&=', '|=',
         '.', '&', '|', '!', '+', '-', '@'}
KEYWORDS  = frozenset(("if", "else", "load", "del", "func",
                       "global", "local", "inner", "outer",
                       "private", "public", "async", "task"))
LCOMMENT  = "#"
SCOMMENT  = "#*"
ECOMMENT  = "*#"
STRSTART  = "'", '"'
STREND    = STRSTART
RESERVED  = '\x06'
if pypy:
    ESCAPE_MAPPING = __pypy__.newdict('strdict')
else:
    ESCAPE_MAPPING = {}
ESCAPE_MAPPING.update({i('\\\\'): f'\\{RESERVED}',  # !! This must be the first.
                       i(r'\n'): '\n',
                       i(r'\r'): '\r',
                       i(r'\t'): '\t'})
PUREDIGITS = frozenset(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))
DIGITS     = PUREDIGITS | frozenset(('_',))
NAMESET    = PUREDIGITS | frozenset(_letters) | frozenset(('$', '_'))
NDNS = NAMESET - DIGITS
PAIRS      = frozenset((('(', ')'), ('[', ']'), ('{', '}')))
EB         = frozenset(p[1] for p in PAIRS)
CAPTURE    = frozenset((':', ',', '\n', ';'))
del implementation, chain, _letters

@cache
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
    __slots__ = '_Token__tid', '_Token__id', 'cnt'
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
    def _cls_name(cls) -> str:
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
    __slots__ = '_Token__tid', '_Token__id', 'name'
    def __init__(self, name: str):
        self._setid()
        self.name = name
    @property
    def content(self):
        return self.name
    @staticmethod
    @cache
    def isname(s: str):
        if (not s) or (s[0] not in NDNS):
            return False
        for x in s[1:]:
            if x not in NAMESET:
                return False
        return True
del Name
@token
class Op(_Token):
    __slots__ = '_Token__tid', '_Token__id', 'op'
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
    def isop(s: str):
        return s in OPSET
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
    __slots__ = '_Token__tid', '_Token__id', 'keyword'
    def __init__(self, keyword: str):
        self._setid()
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
    __slots__ = '_Token__tid', '_Token__id', 'n'
    def __init__(self, n: str):
        self._setid()
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
        for x in s:
            if not isdigit(x):
                return False
        return True
        # return not tuple(filter(lambda x: not isdigit(x), s))
del Integer
@token
class Float(_Token):
    __slots__ = '_Token__tid', '_Token__id', 'f'
    def __init__(self, f: str):
        self._setid()
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
        c = 0
        for x in f:
            if f == '.':
                c += 1
                if c > 1:
                    return False
            elif not isdigit(x):
                return False
        return True
del Float
@token
class Group(_Token):
    __slots__ = '_Token__tid', '_Token__id', 'tokens', 'bracket'
    def __init__(self, *tokens, bracket='('):
        self._setid()
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
MAPPING = {token.Keyword.iskeyword: token.Keyword,
           token.Op.isop: token.Op,
           token.Integer.isint: token.Integer,
           token.Float.isfloat: token.Float,
           token.Name.isname: token.Name}
@cache
def lex(code: str) -> list[token.Token]:
    if not code.strip():
        return []
    lc = len(code)
    tokens = deque(maxlen=lc)
    ta, start, end, group_se, depth = tokens.append, 0, lc, deque(), 0
    def append(x):
        if depth <= 0:
            ta(x)
        else:
            t = tokens[-1]
            for _ in range(1, depth):
                t = t[-1]
            t.add(x)
    prevse = -1, -1
    while 1:
        if (start, end) == prevse:
            end -= 1
        prevse = start, end
        if end > lc:
            break
        if end <= start:
            if start >= lc:
                break
            end = lc
            start += 1
        valid = 0
        s = code[start:end]
        if depth and start >= group_se[-1][1]:
            depth -= 1
            group_se.pop()
        if (s.startswith(STRSTART)  and
            s[0] == s[-1]           and
            s.endswith(STREND)      and
            (c:=s.count(s[0])) >= 2
            ):
            # String token
            if '\\' not in s:
                if c > 2:
                    continue
                # No escapes
                append(token.String(s[1:-1]))
                valid = 1
            else:
                for o, n in ESCAPE_MAPPING.items():
                    if o in frozenset(i(f'\\{ss}') for ss in STREND):
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
            else:
                if s in CAPTURE:
                    append(token.Token(s))
                    valid = 1
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
        elif s.isspace():
            start += len(s)
            end = lc
        else:
            end -= 1
            while start < lc and (code[start] in _ws or code[start] in EB):
                start += 1
    if pypy:
        import gc
        gc.collect()
    return tokens
def Lex(code, showinput=False, showoutput=True, showtime=True):
    from time import perf_counter
    t = perf_counter()
    x = lex(code)
    t = perf_counter()-t
    if showinput:
        print(f'  lex({code!r})\n', end=('> ' if showoutput else ''))
    if showoutput:
        print(f'{x!r}')
    if showtime:
        print(f'Time used: {t:.8f}s')
    return x, t

if __name__ == '__main__' and DEBUG >= 2:
    # Lex(r'"\\\nx"+"y"')
    with open('.content.txt', encoding='UTF-8') as f:
        content = f.read()
    Lex(content, showoutput=False)
