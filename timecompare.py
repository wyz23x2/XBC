import sys
import subprocess
if sys.argv[1:]:
    fn = sys.argv[1]
else:
    fn = 'lexer.py'
ct, pt = [], []
for i in range(5):
    stream = subprocess.getoutput(f'py ./{fn}')
    cpython = stream.split(' ')[-1].rstrip().rstrip('s')
    stream = subprocess.getoutput(f'pypy3 ./{fn}')
    pypy = stream.split(' ')[-1].rstrip().rstrip('s')
    ct.append(float(cpython))
    pt.append(float(pypy))
cpython = sum(ct)/len(ct)
pypy = sum(pt)/len(pt)
print(f'CPython:      {cpython:.6f}')
print(f'PyPy:         {pypy:.6f}')
print(f'CPython/PyPy: {cpython/pypy:.2%}')
print(f'PyPy/CPython: {pypy/cpython:.2%}')
