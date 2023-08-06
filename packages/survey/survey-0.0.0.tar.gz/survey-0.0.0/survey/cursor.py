import types
import re
import math

__all__ = ('Cursor',)


_CSI = b'\x1b'


ClearMode = types.SimpleNamespace(right = 0, left = 1, full = 2, extend = 3)


EraseMode = types.SimpleNamespace(right = 0, left = 1, full = 2)


class Cursor:

    __slots__ = ('_io',)

    def __init__(self, io):

        self._io = io

    def _send(self, code, *args, private = False):

        check = lambda value: not value is None
        params = ';'.join(map(str, filter(check, args)))
        if args:
            params = f'[{params}'
        params = params.encode()

        self._io.send(_CSI + params + code)

    def up(self, size = None, /):

        """
        Move `size` cells up.
        """

        if size == 0:
            return

        self._send(b'A', size)

    def down(self, size = None, /):

        """
        Move `size` cells down.
        """

        if size == 0:
            return

        self._send(b'B', size)

    def left(self, size = None, /):

        """
        Move `size` cells left.
        """

        if size == 0:
            return

        self._send(b'D', size)

    def right(self, size = None, /):

        """
        Move `size` cells right.
        """

        if size == 0:
            return

        self._send(b'C', size)

    def down(self, size = None, /):

        """
        Move to beginning of `size` lines down.
        """

        if size == 0:
            return

        self._send(b'E', size)

    def up(self, size = None, /):

        """
        Move to beginning of `size` lines up.
        """

        if size == 0:
            return

        self._send(b'F', size)

    def goto(self, x = None, /):

        """
        Move to `x` column.
        """

        self._send(b'G', x)

    def move(self, y, x, /):

        """
        Move to `x` and `y` coordinates:
        """

        self._send(b'f', y, x)

    def clear(self, mode = None, /):

        """
        Clear display.
        """

        self._send(b'J', mode)

    def erase(self, mode = None, /):

        """
        Erase in-line.
        """

        self._send(b'K', mode)

    def save(self):

        """
        Save current location.
        """

        self._send(b'7')

    def load(self):

        """
        Move to saved location.
        """

        self._send(b'8')

    def show(self):

        """
        Show.
        """

        self._send(b'h', '?25')

    def hide(self):

        """
        Hide.
        """

        self._send(b'l', '?25')

    _drs_re = re.compile(_CSI + b'\[(\d+);(\d+)R$')

    def locate(self):

        """
        Get current location.
        """

        buffer = bytearray()
        funnel = bytearray()

        self._send(b'n', '6')

        while True:
            data = self._io.recv()
            buffer.extend(data)
            if data == b'R':
                index = buffer.rindex(_CSI)
                portion = buffer[index:]
                match = self._drs_re.match(portion)
                if match:
                    break
                else:
                    funnel.extend(buffer)

        groups = match.groups()
        values = (groups[index] for index in range(2))

        return tuple(map(int, values))

    def measure(self):

        """
        Get screen size.
        """

        self.hide()

        self.save()

        self.move(999, 9999)

        size = self.locate()

        self.load()

        self.locate()

        self.show()

        return size
