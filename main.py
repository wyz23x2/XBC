DEBUG   = 2
VERSION = '0.1.0a1'
if __name__ == '__main__':
    import argparse as ap
    parser = ap.ArgumentParser('XBC', allow_abbrev=False)
    parser.add_argument('-V', '--version', action='version', version=VERSION)
    if DEBUG < 2:
        parser.add_argument('-d', '--debug', action='store_true', help='debug mode, DEBUG = 1')
    else:
        parser.add_argument('-d', '--debug', action='store_true', help='ignored in debug builds')
    ns = parser.parse_args()
