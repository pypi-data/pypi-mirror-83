

__all__ = ()


def paint(value, color, null = b'\x1b[0m'):

    return color + value + null
