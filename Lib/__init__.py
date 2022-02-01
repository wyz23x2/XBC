import os
import sys
d = os.path.dirname(os.path.realpath(__file__))
if '\\' in d:
    sys.path.append('\\'.join(d.split('\\')[:-1]))
else:
    sys.path.append('/'.join(d.split('/')[:-1]))
