import sys
import subprocess
if sys.argv[1:]:
    fn = sys.argv[1]
else:
    fn = 'lexer.py'
ct, pt = [], []
for c in range(50):
    stream = subprocess.getoutput(f'py -OO ./{fn}')
    cpython = stream.split(' ')[-1].rstrip().rstrip('s')
    stream = subprocess.getoutput(f'pypy3 -OO ./{fn}')
    pypy = stream.split(' ')[-1].rstrip().rstrip('s')
    ct.append(float(cpython))
    pt.append(float(pypy))
cpython = sum(ct)
pypy = sum(pt)
print(f'CPython:      {cpython:.6f}/{len(ct)}={cpython/len(ct):.6f}')
print(f'PyPy:         {pypy:.6f}/{len(pt)}={pypy/len(pt):.6f}')
print(f'CPython/PyPy: {cpython/pypy:.2%}')
print(f'PyPy/CPython: {pypy/cpython:.2%}')
