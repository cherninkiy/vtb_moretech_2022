from glob import glob
from os import stat
from stat import S_ISREG


def ls(path, wildcards='*'):
    def fmt(arg):
        size, mode = stat(arg).st_size, S_ISREG(stat(arg).st_mode)
        for unit, num in zip([' B', 'kB', 'MB', 'GB', 'TB'], [size / (1000.0**i) for i in range(5)]):
            if num < 1000.0:
                return ('1', arg, f'{num:.1f} {unit}'.rjust(8)) if mode else ('0', arg, 'DIR'.ljust(8))
    print('\n'.join(f'{x[2]} {x[1]}' for x in sorted(map(fmt, glob(f'{path}/{wildcards}')))))


def cat(path, num_lines=3):
    with open(path, 'r') as f:
        print(''.join(next(f) for _ in range(num_lines)), '\n...' if f.read() else '')