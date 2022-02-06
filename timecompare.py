import sys
import subprocess
if sys.argv[1:]:
    fn = sys.argv[1]
else:
    fn = 'lexer.py'
ct, ft, pt = [], [], []
for c in range(2):
    stream = subprocess.getoutput(f'py -OO ./{fn}')
    cpython = stream.split(' ')[-1].rstrip().rstrip('s')
    stream = subprocess.getoutput(fr'"D:\Download\cpython-3.10.0a6\cpython-3.10.0a6\PCbuild\amd64\python.exe" -OO ./{fn}')
    fpy = stream.split(' ')[-1].rstrip().rstrip('s')
    stream = subprocess.getoutput(f'pypy3 -OO ./{fn}')
    pypy = stream.split(' ')[-1].rstrip().rstrip('s')
    ct.append(float(cpython))
    ft.append(float(fpy))
    pt.append(float(pypy))
cpython = sum(ct)
fpy = sum(ft)
pypy = sum(pt)
base = sorted((cpython, fpy, pypy))[1]
print(f'CPython:      {cpython:>9.6f}/{len(ct)}={cpython/len(ct):>9.6f}  {cpython/base:>7.2%}')
print(f'FCPython:     {fpy:>9.6f}/{len(ft)}={fpy/len(ft):>9.6f}  {fpy/base:>7.2%}')
print(f'PyPy:         {pypy:>9.6f}/{len(pt)}={pypy/len(pt):>9.6f}  {pypy/base:>7.2%}')
