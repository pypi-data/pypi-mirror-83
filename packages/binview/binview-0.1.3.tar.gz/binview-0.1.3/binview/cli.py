from pathlib import Path
from argparse import ArgumentParser, RawTextHelpFormatter

from .dump import dumper


def main():
    ''' Dumps the file given as arg.
    '''
    desc = 'Binary Dumper'
    parser = ArgumentParser(
        description = desc,
        formatter_class = RawTextHelpFormatter,
    )
    parser.add_argument(
        'file',
        help = 'File to be dumped.'
    )
    parser.add_argument(
        '--format',
        default = 'hex',
        help = '''
Output format.
May be :
    hex, oct, dec, bin
default is hex.
        '''
    )
    args = parser.parse_args()
    path = Path(args.file)
    fmt = args.format

    for line in dumper(path, fmt):
        print(line)
