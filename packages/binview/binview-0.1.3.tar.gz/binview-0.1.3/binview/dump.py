from functools import partial
from itertools import count


def converter(fmt, size, chunk):
    bytes = ' '.join([f'{b:{fmt}}' for b in chunk])
    return f'{bytes[:size]} {bytes[size:]}'


def spacer(b_len, chunk):
    if len(chunk)<16:
        ns = b_len*(16-len(chunk))+1
        return ' '*ns
    return ' '


def decode(chunk):
    return ''.join([chr(b) if 32 <= b <= 127 else '.' for b in chunk])


def mk_conv(format_letter, nb_digits):
    return (
        partial(converter,
            f'0{nb_digits}{format_letter}',
            ((nb_digits+1)*8)-1
        ),
        partial(spacer,
            nb_digits+1
        ),
    )


handlers = dict(
    hex = mk_conv('X', 2),
    oct = mk_conv('o', 3),
    dec = mk_conv('d', 3),
    bin = mk_conv('b', 8),
)


def dumper(path, fmt='hex'):
    convert, space = handlers[fmt]
    with open(path, 'rb') as inp:
        read = partial(inp.read, 16)
        for adr, chunk in zip(count(step=16), iter(read, b'')):
            yield f'{adr:08X} {convert(chunk)}{space(chunk)}{decode(chunk)}'

