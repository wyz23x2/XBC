## Special comment meanings:
#  TODO:   Something planned.
#  BUG:    More severe problem.
#  FIXME:  More mild problem.
#  XXX:    Highlight a possible problem spot.
#  UNDONE: A rollback of previous code/commits.
#  HACK:   A workaround. Can be combined with FIXME/XXX if the workaround is considered fragile and needs to be rewritten.
#  MAGIC:  A workaround. Considered clever and safe so it will likely stay as is.
#  NOTE:   Other types of notes.
#  !!:     Attention needed.
#  !!!:    Very important information.
#  ?:      Help wanted.
#  ??:     Needs to be immediately solved.
#  BC:     Build Change, i.e. changed between different builds.
#  May include the date the comment was written,
#  and the first 8 along with ?? may include the date due.

DEBUG   = 2          # BC
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
