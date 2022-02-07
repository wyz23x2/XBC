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
class Assign(Action):
    def __init__(self, name: str, value: Action):
        self.name, self.value = name, value
    def __str__(self):
        return f'{self.name!s} = {self.value!s}'
    def __repr__(self):
        return f'Assign(name={self.name!r}, value={self.value!r})'
class Parser:
    # TODO
    def __init__(self, tokens: list[token.Token], flags: dict|None = None):
        for tk in tokens:
            ...
    def __next__(self):
        ...
