import sys
import subprocess
try:
    import matplotlib.pyplot as plt  # type: ignore
except Exception:
    plt = None
if sys.argv[1:]:
    fn = sys.argv[1]
else:
    fn = 'lexer.py'
lines = ['a & b & c & d & e & f & g & h & i & j & k & (!m) | n\n',
         'if 3377-(-156*-(.657>>3^+x*2.48)-15)*-394.48-3+(10945)*8-6>>2 > 59583*(455-(34858+int("34757")/int("7\\n")[0]))*474)-4958<<(50/5):\n',
         '    print(50+59583*(455-(34858+int("34757")/int("7\\n")[0]))*474)',
        '-4958<<(50/5+59583*(455-(34858+int("34757")/int("7\\n")[0]))*474)-4958<<(50/5)))\n',
        '(4585842348586<<39/5)^(577667405820-58.394+3939+" 5\\n"[1]-485821.3948-59*4)+7747028.494+(((((((717779688)-6)*5)^27)%4983)-21039)+39485<<2)',
        '\n77.5+((((((((((((((((8<<1))))))))))))))))\nprint("\\r\\n\\\\\\n")',
        '((((((((((((((((((((((((((((3<<7))))))))))))))))))))))))))))\n',
        '[([{([{[((([{[[[[((({{[([(({{[]}}))])]}})))]]]]}])))]}])}])]\n',
        '1[2[3[4[5[6[7[8[9[10[11[12[13[14[15]16]17]18]19]20]21]22]23]24]25]26]27]28]29\n',
        '((((((((((((((((((((((((((((3<<7))))))))))))))))))))))))))))\n',
        'a + b - c + d - e + f - g + h - i + j - k + m * n / o * p / q * r / s * t / u * v / w * x / y * z\n',
        '(a+(b+(c+(d+(e+(f+g)+h)+i)+j)+k)+m)\n',
        'print(20+(69-get(5875*(627<<5))+[195, 2883, x, y, z][a])-u)\n',
        'export(459585-28388*(2848-(28-(3847-2847-(48)))))\n',
        'export(459585-28388*(2848-(28-(3847-2847-(48)))))\n',
        'r = 5 + $R - xor(66, and(y, 45))\n',
        '1 ++++ 1 ---- 1 ++++ 2 ---- 2 * 5 +++-- 7\n',
        'r = x = y = t = a = q = b = ((((((((((50))))))))))',
        '[([{([{[((([{[x[[[((({{[([(({{[x+1-5<<2]}}))])]}})))]]]]}])))]}])y}])]\n']
lines = ['[([{([{[((([{[x[[[((({{[([(({{[x+%d-5<<%d]}}))])]}})))]]]]}])))]}])y}])]\n' % (i, i+7) for i in range(30)]
plt.grid(axis='both')
with open('.content.txt', 'w', encoding='utf-8') as f:
    i = 1
    prev = [0, 0, 0]
    for ln in lines:
        f.write(ln)
        f.flush()
        stream = subprocess.getoutput(f'py -OO ./{fn}')
        cpython = float(stream.split(' ')[-1].rstrip().rstrip('s'))
        stream = subprocess.getoutput(fr'"D:\Download\cpython-3.10.0a6\cpython-3.10.0a6\PCbuild\amd64\python.exe" -OO ./{fn}')
        fpy = float(stream.split(' ')[-1].rstrip().rstrip('s'))
        stream = subprocess.getoutput(f'pypy3 -OO ./{fn}')
        pypy = float(stream.split(' ')[-1].rstrip().rstrip('s'))
        if 0:
            stream = subprocess.getoutput(f'py -OO ./{fn}')
            cpython += float(stream.split(' ')[-1].rstrip().rstrip('s'))
            stream = subprocess.getoutput(fr'"D:\Download\cpython-3.10.0a6\cpython-3.10.0a6\PCbuild\amd64\python.exe" -OO ./{fn}')
            fpy += float(stream.split(' ')[-1].rstrip().rstrip('s'))
            stream = subprocess.getoutput(f'pypy3 -OO ./{fn}')
            pypy += float(stream.split(' ')[-1].rstrip().rstrip('s'))
            cpython /= 2
            fpy /= 2
            pypy /= 2
        av = (cpython+fpy+pypy) / 3
        if 0:
            cpython = av-cpython
            fpy = av-fpy
            pypy = av-pypy
        if i == 1:
            plt.plot([i], [cpython], 'r.-', label='CPython')
            plt.plot([i], [fpy], '.-', label='FPython', color='#FFD700')
            plt.plot([i], [pypy], 'b.-', label='PyPy')
        else:
            if i == 2: plt.clf(); plt.grid()  # noqa
            plt.plot([i-1, i], [prev[0], cpython], 'r-', label='CPython')
            plt.plot([i-1, i], [prev[1], fpy], '-', label='FPython', color='#FFD700')
            plt.plot([i-1, i], [prev[2], pypy], 'b-', label='PyPy')
            plt.plot([i-1, i], [prev[0]/(i-1), cpython/i], 'r--', label='CPython')
            plt.plot([i-1, i], [prev[1]/(i-1), fpy/i], '--', label='FPython', color='#FFD700')
            plt.plot([i-1, i], [prev[2]/(i-1), pypy/i], 'b--', label='PyPy')
        prev = [cpython, fpy, pypy]
        plt.legend(('CPython', 'FPython', 'PyPy'))
        print(i)
        plt.pause(.05)
        i += 1
plt.show()
