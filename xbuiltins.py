from xbc import *
from decimal import Decimal, setcontext, Context, ROUND_HALF_UP
c = Context(32, ROUND_HALF_UP)
c.clear_traps()
setcontext(c)
class XError(XBC):
    def __init__(self, message: XBC | str, filename: str, line: str, lineno: int):
        super().__init__()
        self.message = message
        self.filename, self.line, self.lineno = filename, line, lineno
    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return self.message == other.message
    def __str__(self):
        return f'{self.__class__.__name__}: {self.message}'
    def __xbc_str__(self):
        return f'{self.__class__.__name__.removeprefix("X")}: {self.message}'
    def __repr__(self):
        return f'{self.__class__.__name__}({self.message!r}) ~0x{self.id:0>7X}'
    def __xbc_repr__(self):
        return f'{self.__class__.__name__.removeprefix("X")}({xrepr(self.message)})'
class XWarning(XBC):
    def __init__(self, message: XBC):
        super().__init__()
        self.message = message
    def __eq__(self, other):
        if type(other) is not type(self):
            return False
        return self.message == other.message
    def __str__(self):
        return f'{self.__class__.__name__}: {self.message}'
    def __xbc_str__(self):
        return f'{self.__class__.__name__.removeprefix("X")}: {self.message}'
    def __repr__(self):
        return f'{self.__class__.__name__}({self.message!r}) ~0x{self.id:0>7X}'
    def __xbc_repr__(self):
        return f'{self.__class__.__name__.removeprefix("X")}({xrepr(self.message)})'
class XStr(XBC):
    def __init__(self, x='', /):
        super().__init__()
        self.__data = xstr(x)
    def __repr__(self):
        return f'XStr({xrepr(self)}) ~0x{self.id:0>7x}'
    def __xbc_repr__(self):
        return repr(self.__data)
    def cap(self):
        return self.__data.capitalize()
    def center(self, width, fill=' '):
        return self.__data.center(width, fill)
    def count(self, char):
        return self.__data.count(char)
    def cutprefix(self, prefix, delall=False):
        if isinstance(prefix, str):
            return XStr((self.__data.lstrip if delall else self.__data.removeprefix)(prefix))
        else:
            x = self.__data
            for p in prefix:
                x = (x.lstrip if delall else x.removeprefix)(p)
            return XStr(x)
    def endswith(self, s):
        return self.__data.endswith(s)
    def index(self, s, start=0):
        return XNum(self.__data.index(s, start))
    def lalign(self, width, fill=' '):
        return XStr(self.__data.ljust(width, fill))
    def lower(self):
        return XStr(self.__data.lower())
class XNum(XBC):
    def __new__(cls, x=0, /):
        if type(x) is cls:
            return x
        i = object.__new__(cls)
        return i
    def __init__(self, x, /):
        super().__init__()
        if isinstance(x, Decimal):
            self.__data = x.normalize()
        else:
            self.__data = Decimal(x).normalize()
    def __str__(self):
        s = str(self.__data)
        if '.' not in s: return s
        else:
            x = len(s.split('.')[1])
            if x <= 16:
                return s
        return str(self.__data.quantize(Decimal('1.' + '0'*16))).replace("E", "e")
    def __repr__(self):
        return f'{str(self.__data).replace("E", "e")} ~0x{self.id:0>7X}'
    def __xbc_repr__(self):
        return xstr(self)
    def __pos__(self):
        return self
    def __neg__(self):
        return self * -1
    def __add__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data + getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __sub__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data - getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __mul__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data * getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __truediv__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data / getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __mod__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data % getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __pow__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data ** getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __abs__(self):
        return type(self)(abs(self.__data))
    def __xbc_cmp__(self, other):
        if type(self) is type(other):
            x, y = self.__data, getattr(other, f'_{type(other).__name__}__data')
            return (x > y) - (x < y)
        return NotImplemented
class XFNum(XBC):
    def __new__(cls, x=0, /):
        if type(x) is cls:
            return x
        i = object.__new__(cls)
        return i
    def __init__(self, x, /):
        super().__init__()
        if isinstance(x, float):
            self.__data = x
        else:
            self.__data = float(x)
    def __str__(self):
        return str(self.__data).replace('nan', 'NaN').replace('inf', 'Infinity')
    def __repr__(self):
        return f'{self!s} ~0x{self.id:0>7X}'
    def __xbc_repr__(self):
        return xstr(self)
    def __pos__(self):
        return self
    def __neg__(self):
        return self * -1
    def __add__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data + getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __sub__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data - getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __mul__(self, other):
        if type(self) is type(other):
            return type(self)(self.__data * getattr(other, f'_{type(other).__name__}__data'))
        return NotImplemented
    def __truediv__(self, other):
        if type(self) is type(other):
            x, y = self.__data, getattr(other, f'_{type(other).__name__}__data')
            if y == 0:
                if x == 0:
                    return XFNum(float('NaN'))
                else:
                    return XFNum(float('Inf'))
            else:
                return type(self)(x / y)
        return NotImplemented
    def __mod__(self, other):
        if type(self) is type(other):
            x, y = self.__data, getattr(other, f'_{type(other).__name__}__data')
            if y == 0:
                return XFNum(float('NaN'))
            else:
                return type(self)(x % y)
        return NotImplemented
    def __pow__(self, other):
        if type(self) is type(other):
            x, y = self.__data, getattr(other, f'_{type(other).__name__}__data')
            if x == 0 and y == 0:
                return XFNum(float('NaN'))
            else:
                return type(self)(x ** y)
        return NotImplemented
    def __abs__(self):
        return type(self)(abs(self.__data))
    def __xbc_cmp__(self, other):
        if type(self) is type(other):
            x, y = self.__data, getattr(other, f'_{type(other).__name__}__data')
            return (x > y) - (x < y)
        return NotImplemented
