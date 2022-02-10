from main import *
from utils import *
from lexer import token
from sys import intern as i
class Action:
    pass
# Tokens are all in the token namespace of lexer,
# while all Actions subclass Action.
class ValueOf(Action):
    def __init__(self, name: str):
        self.name = name
    def __repr__(self):
        return f'ValueOf({self.name!r})'
class MemberOf(Action):
    def __init__(self, up: Action, attr: str):
        self.up, self.attr = up, attr
    def __str__(self):
        return f'{self.up!s}.{self.attr!s}'
    def __repr__(self):
        return f'MemberOf(up={self.up!r}, attr={self.attr!r})'
class Call(Action):
    def __init__(self, caller: Action, *args):
        self.caller, self.args = caller, args
    def __str__(self):
        return f'{self.caller!s}({", ".join(map(str, self.args))})'
    def __repr__(self):
        return f'Call(caller={self.caller!r}, args={self.args!r})'
class Operator(Action):
    def __init__(self, op: str, *sides):
        self.op = op
        self.sides = sides
    def __repr__(self):
        return f'Operator({self.op!r}, {", ".join(map(repr, self.sides))})'
class Assign(Action):
    def __init__(self, name: str, value: Action):
        self.name, self.value = name, value
    def __str__(self):
        return f'{self.name!s} = {self.value!s}'
    def __repr__(self):
        return f'Assign(name={self.name!r}, value={self.value!r})'
class IfTree(Action):
    def __init__(self, if_: Action, /, *elseifselse):
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
        for tk in tokens:
            ...
    def __next__(self):
        ...
