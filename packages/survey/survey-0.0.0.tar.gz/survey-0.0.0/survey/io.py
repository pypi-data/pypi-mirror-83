import io
import termios


__all__ = ('IO',)


class IO:

    __slots__ = ('_i', '_o', '_buffer', '_fd', '_save', '_mode', '_block')

    def __init__(self, i, o):

        self._i = i
        self._o = o

        self._buffer = bytearray()

        self._fd = i.fileno()

        self._save = None
        self._mode = None

        self._block = None

    def _fix(self, mode):

        termios.tcsetattr(self._fd, termios.TCSAFLUSH, mode)

    def start(self):

        """
        Save settings and enter cbreak mode.
        """

        self._save = termios.tcgetattr(self._fd)

        mode = termios.tcgetattr(self._fd)

        mode[3] &= ~(termios.ECHO | termios.ICANON)
        mode[6][termios.VTIME] = 0

        self._mode = mode

    def stop(self):

        """
        Restore initial settings.
        """

        self._fix(self._save)

    def send(self, value):

        """
        Write to output buffer.
        """

        self._o.write(value)
        self._o.flush()

    def recv(self, block = True):

        """
        Read from input buffer.
        """

        if not block is self._block:
            self._block = block
            self._mode[6][termios.VMIN] = int(block)
            self._fix(self._mode)

        try:
            return self._buffer.pop(0)
        except IndexError:
            pass

        return self._i.read(1)

    def feed(self, data):

        """
        Funnel additional data to be read before input buffer.
        """

        self._buffer.extend(data)

    def bell(self):

        self.send(b'\a')
