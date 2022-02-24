__all__ = 'VERSION', 'VEROCT', 'XBC', 'xstr', 'xrepr', 'xcmp', 'xis', 'xin'
VERSION = '0.1.0a1'
#          Minor Level (dev->0, a->1, b->2, c->3, final->4)
#             vv  v
VEROCT  = 0o00010011
#           ^^  ^^ ^ Serial
#        Major Micro
from utils import *
import sys
Xid = 0
class XBC:
    def __init__(self):
        global Xid
        self.id = Xid
        Xid += 1
    def __repr__(self):
        return f'<{self.__class__.__name__} 0x{self.id:0>7X}>'
    def __xbc_str__(self):
        return str(self)
    def __xbc_repr__(self):
        return f'<object 0x{self.id:0>7x}>'
    def __eq__(self, other):
        return self.id == other.id
    def __xbc_cmp__(self, other):
        if self == other: return 0
        return (self > other) - (self < other)
    def __xbc_is__(self, other):
        return self == other
    def __xbc_in__(self, other):
        return self in other
def xstr(obj: XBC, /):
    return obj.__xbc_str__()
def xrepr(obj: XBC, /):
    return obj.__xbc_repr__()
def xcmp(a: XBC, b: XBC, /):
    if a.__xbc_cmp__ is XBC.__xbc_cmp__ and b.__xbc_cmp__ is not XBC.__xbc_cmp__:
        return -(b.__xbc_cmp__(a))
    return a.__xbc_cmp__(b)
def xis(a: XBC, b: XBC, /):
    return a.__xbc_is__(b)
def xin(a: XBC, b: XBC, /):
    return a.__xbc_in__(b)
from xbuiltins import *
def xerr(e: XError, /):
    printf(f'$b$R!$r$R  Error occurred. Traceback:\nFile "{e.filename}", line {e.lineno}:\n  {e.line}\n{xstr(e)}$r', file=sys.stderr)
    ...
def xwarn(e, /):
    from xbuiltins import XError
    ...
if __name__ == '__main__':
    print(VEROCT)
