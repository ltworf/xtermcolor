from os import isatty, environ, write
from sys import stdout

from xtermcolor.ColorMap import XTermColorMap, VT100ColorMap

_cmap = None

def _init():
    global _cmap
    term = environ.get('TERM')
    if term.startswith('xterm'):
        _cmap = XTermColorMap()
    elif term == 'vt100':
        _cmap = VT100ColorMap()
_init()


def cprint(value, *args, sep=' ', end='\n', file=stdout, flush=False, fg=None, bg=None, ansifg=None, ansibg=None):
    '''
    This function is similar to print, but adds named parameters for
    the colors.
    '''
    outstring = ' '.join(str(i) for i in (value,) + args)
    if any([fg, bg, ansifg, ansibg]) and file.isatty() and _cmap:
        outstring = _cmap.colorize(outstring, fg, ansifg, bg, ansibg)

    print(outstring, sep=sep, end=end, file=file, flush=flush)


def colorize(string, rgb=None, ansi=None, bg=None, ansi_bg=None, fd=1):
    '''Returns the colored string to print on the terminal.

    This function detects the terminal type and if it is supported and the
    output is not going to a pipe or a file, then it will return the colored
    string, otherwise it will return the string without modifications.

    string = the string to print. Only accepts strings, unicode strings must
             be encoded in advance.
    rgb    = Rgb color for the text; for example 0xFF0000 is red.
    ansi   = Ansi for the text
    bg     = Rgb color for the background
    ansi_bg= Ansi color for the background
    fd     = The file descriptor that will be used by print, by default is the
             stdout
    '''
    if isatty(fd):
        string = _cmap.colorize(string, rgb, ansi, bg, ansi_bg)

    return string
