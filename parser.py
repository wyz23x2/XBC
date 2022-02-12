from collections import deque
from main import *
from utils import *
from xbc import XBC
import xbuiltins as xb
from lexer import *
P = {ASSIGN: 0, IADD: 0, ISUB: 0, IMUL: 0, IDIV: 0,
     IMOD: 0, IPOW: 0, ILSHIFT: 0, IRSHIFT: 0, IAND: 0, IOR: 0,
     AND: 1, OR: 1, NOT: 1,
     GT: 2, GE: 2, EQ: 2, LE: 2, LT: 2,
     REF: 3,
     ADD: 4, SUB: 4,
     MUL: 5, DIV: 5, MOD: 5,
     POS: 6, NEG: 6,
     POW: 7, LSHIFT: 7, RSHIFT: 7}
class Action:
    pass
# Tokens are all in the token namespace of lexer,
# whereas all Actions subclass Action.
class ValueOf(Action):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f'ValueOf({self.name!r})'
class MemberOf(Action):
    def __init__(self, up: XBC, attr: str):
        self.up, self.attr = up, attr
    def __str__(self):
        return f'{self.up!s}.{self.attr!s}'
    def __repr__(self):
        return f'MemberOf(up={self.up!r}, attr={self.attr!r})'
class Call(Action):
    def __init__(self, caller: XBC, *args):
        self.caller, self.args = caller, args
    def __str__(self):
        return f'{self.caller!s}({", ".join(map(str, self.args))})'
    def __repr__(self):
        return f'Call(caller={self.caller!r}, args={self.args!r})'
class Operator(Action):
    def __init__(self, op: str, *sides):
        self.op = op
        self.sides = list(sides)
    def append(self, x, /):
        self.sides.append(x)
    def __repr__(self):
        return f'Operator({self.op!r}, {", ".join(map(repr, self.sides))})'
class Assign(Action):
    def __init__(self, name: str, value: XBC):
        self.name, self.value = name, value
    def __str__(self):
        return f'{self.name!s} = {self.value!s}'
    def __repr__(self):
        return f'Assign(name={self.name!r}, value={self.value!r})'
class IfTree(Action):
    def __init__(self, if_: XBC, /, *elseifselse):
        self.If = if_
        if elseifselse:
            self.elseifs, self.Else = elseifselse[:-1], elseifselse[-1]
        else:
            self.elseifs, self.Else = (), None
    def __repr__(self):
        return f'IfTree(if={self.If!r}, elseifs={self.elseifs!r}, else={self.Else!r})'
    def __getattr__(self, name: str, /):
        try:
            return getattr(self, {'if': 'If', 'if_': 'If',
                                  'Elseifs': 'elseifs',
                                  'else': 'Else', 'else_': 'Else'}[name])
        except (AttributeError, KeyError):
            pass
        return object.__getattribute__(self, name)
class Parser:
    # TODO
    def __init__(self, tokens: list[token.Token], flags: dict|None = None):
        self.tokens = tokens
        self.flags = flags
    def __iter__(self):
        # flake8: noqa
        raise NotImplementedError
        stack = []
        for tk in self.tokens:
            match type(tk):
                case _:
                    ...
        
    
