DEBUG   = 2
VERSION = '0.1.0a1'
if __name__ == '__main__':
    import argparse as ap
    parser = ap.ArgumentParser('XBC', allow_abbrev=False)
    parser.add_argument('-V', '--version', action='version', version=VERSION)
    if DEBUG < 2:
        parser.add_argument('-d', '--debug', action='store_true', help='debug mode, DEBUG = 1')
        parser.add_argument('--ld', '--lower-debug', action='count', help='ignored in normal builds')
    else:
        parser.add_argument('-d', '--debug', action='store_true', help='ignored in debug builds')
        parser.add_argument('--ld', '--lower-debug', action='count', help='DEBUG = 1; if specified twice, DEBUG = 0')
    ns = parser.parse_args()
    if DEBUG < 2 and ns.debug:
        DEBUG = 1
    elif ns.ld:
        DEBUG = max(2-ns.ld, 0)
