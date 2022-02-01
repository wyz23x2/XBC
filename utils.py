__all__ = ['printf', 'Signal', 'signals', 'warning', 'fail']
import traceback as t
import warnings as w
from typing import Callable as C, NoReturn
import sys
import os
from main import *

COLOR_DICT = {'BLACK': '\033[30m',
              'R': '\033[31m', 'RED': '\033[31m',
              'Y': '\033[33m', 'YELLOW': '\033[33m',
              'G': '\033[32m', 'GREEN': '\033[33m',
              'C': '\033[36m', 'CYAN': '\033[36m',
              'B': '\033[34m', 'BLUE': '\033[34m',
              'P': '\033[35m', 'PURPLE': '\033[35m',
              'W': '\033[37m', 'WHITE': '\033[37m',
              'b': '\033[1m', 'BOLD': '\033[1m',
              'r': '\033[0m', 'RESET': '\033[0m'}
def _translate(a):
    for c in COLOR_DICT:
        if c in {'b', 'B', 'R', 'r'}:
            a =  a.replace(f'${c} ', COLOR_DICT[c]).replace(f'${c}', COLOR_DICT[c])
        else:
            a = (a.replace(f'${c} ', COLOR_DICT[c])
                  .replace(f'${c}', COLOR_DICT[c])
                  .replace(f'${c} '.lower(), COLOR_DICT[c])
                  .replace(f'${c}'.lower(), COLOR_DICT[c])
                  .replace(f'${c} '.title(), COLOR_DICT[c])
                  .replace(f'${c}'.title(), COLOR_DICT[c]))
def printf(*args, **kwargs):
    """Print translating color codes in strings."""
    args = list(args)
    for i, a in enumerate(args):
        if isinstance(a, str):
            args[i] = _translate(a)
    if 'sep' in kwargs and isinstance(kwargs['sep'], str):
        kwargs['sep'] = _translate(kwargs['sep'])
    if 'end' in kwargs and isinstance(kwargs['end'], str):
        kwargs['end'] = _translate(kwargs['end'])
    return print(*args, **kwargs)
class Signal:
    def __init__(self, name: str, *callbacks: C):
        self.name, self.callbacks = name, [*callbacks]
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.name!r})'
    def add_callback(self, *callbacks: C, append: bool=False):
        if append:
            self.callbacks.extend(callbacks)
        else:
            self.callbacks = [*callbacks, *self.callbacks]
    def __call__(self, *args, **kwargs):
        if not self.callbacks:
            return
        x = self.callbacks[-1](*args, **kwargs)
        for c in self.callbacks[:-1][::-1]:
            c()
        return x
class signals:
    def __repr__(self) -> str:
        return self.__qualname__
    def register(self, name: str, *funcs: C):
        if not funcs:
            def _inner(func: C):
                setattr(self, name, Signal(name, func))
            return _inner
        else:
            setattr(self, name, Signal(name, *funcs))
            return getattr(self, name)
    def __setattr__(self, name: str, value, /) -> None:
        if not isinstance(value, Signal):
            warning(Warning, f'Attribute {name!r} not a Signal')
        object.__setattr__(self, name, value)
signals = signals()
@signals.register('abort')
def abort_handler(message: str='$b$R Process aborted.$r', *, force: bool=False) -> NoReturn:
    printf(message)
    if force:
        os._exit(2)
    signals.exit(2)
def abort(message: str='$b$R Process aborted.$r', *, force: bool=False):
    signals.abort(message, force=force)
@signals.register('exit')
def exit_handler(exitcode: int=0) -> NoReturn:
    try:
        sys.exit(exitcode)
    except (KeyboardInterrupt, InterruptedError):
        os._exit(exitcode)
    except Exception:
        abort_handler('$b$R Error occurred while exiting; process aborted.$r', force=True)
@signals.register('warning')
def warning_handler(message: str=None, type: Warning=Warning, *, stacklevel: int=2):
    if DEBUG <= 0:
        return
    w.warn(f'\033[33m{message}\033[m', type, stacklevel)
def warning(message: str=None, type: Warning=Warning, *, stacklevel: int=2):
    signals.warning(message, type, stacklevel=stacklevel)
@signals.register('fail')
def fail_handler(exc: BaseException, /) -> NoReturn:
    if DEBUG == 0:
        printf(f'$b$R Core error! {exc.__class__.__name__}: {exc!s}$r')
    else:
        printf('$b$R Core error!')
        print(t.format_exception(exc), end='')
        printf('$r')
    abort()
def fail(exc: BaseException, /):
    signals.fail(exc)
