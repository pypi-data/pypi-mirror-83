import enum
import types
import wrapio
import math

from . import abc


__all__ = ('Source', 'Translator', 'LineEditor', 'MultiLineEditor', 'Select',
           'MultiSelect')


class Source(abc.Handle):

    Event = enum.IntEnum(
        'Event',
        'move_left move_right jump_left jump_right move_up move_down '
        'delete_left delete_right escape indent enter insert'
    )

    _events = types.SimpleNamespace(
        arrows = {
            b'D': Event.move_left,
            b'C': Event.move_right,
            b'A': Event.move_up,
            b'B': Event.move_down
        },
        normal = {
            b'\x0d': Event.enter,
            b'\x0a': Event.enter,
            b'\x7f': Event.delete_left,
            b'\x08': Event.delete_right,
            b'\x09': Event.indent
        },
        special = {
            b'': Event.escape,
            b'b': Event.jump_left,
            b'f': Event.jump_right
        }
    )

    __slots__ = ('_io', '_done')

    def __init__(self, io, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._io = io

        self._done = False

    def _escape(self):

        key = self._io.recv(False)

        if key == b'[':
            key = self._io.recv()
            events = self._events.arrows
        else:
            events = self._events.special

        return (events, key)

    def _advance(self):

        key = self._io.recv()

        if key == b'\x1b':
            (events, key) = self._escape()
        else:
            events = self._events.normal

        event = events.get(key, self.Event.insert)

        self._dispatch(event.name, key)

    def done(self):

        self._done = True

    def stream(self):

        while not self._done:
            self._advance()

        self._done = False


class Abort(Exception):

    __slots__ = ()


class Translator(abc.Handle):

    """
    Combines related io events into single events with relevant info.

    .. code-block: python

        translator = Translator(callback = ...)
        source = Source(io, callback = translator.invoke)
    """

    def __init__(self, io, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._io = io

    def _move_x(self, size):

        self._dispatch('move_x', size)

    @wrapio.event('move_left')
    def _nnc(self, key):

        self._move_x(- 1)

    @wrapio.event('move_right')
    def _nnc(self, key):

        self._move_x(1)

    @wrapio.event('jump_left')
    def _nnc(self, key):

        self._move_x(- math.inf)

    @wrapio.event('jump_right')
    def _nnc(self, key):

        self._move_x(math.inf)

    def _move_y(self, up):

        self._dispatch('move_y', up)

    @wrapio.event('move_up')
    def _nnc(self, key):

        self._move_y(True)

    @wrapio.event('move_down')
    def _nnc(self, key):

        self._move_y(False)

    def _delete(self, left):

        self._dispatch('delete', left)

    @wrapio.event('delete_left')
    def _nnc(self, key):

        self._delete(True)

    @wrapio.event('delete_right')
    def _nnc(self, key):

        self._delete(False)

    def _insert(self, key):

        self._dispatch('insert', key)

    @wrapio.event('insert')
    def _nnc(self, key):

        self._insert(key)

    @wrapio.event('indent')
    def _nnc(self, key):

        self._insert(b'\t')

    def _enter(self, key):

        self._dispatch('enter', key)

    @wrapio.event('enter')
    def _nnc(self, key):

        self._enter(key)

    def invoke(self, *args, **kwargs):

        try:
            super().invoke(*args, **kwargs)
        except Abort:
            self._io.bell()


class Editor(abc.Handle):

    """
    ABC providing functions and attributes for all text editors.
    """

    def __init__(self,
                 io,
                 cursor,
                 *args,
                 limit = 0,
                 funnel = None,
                 **kwargs):

        super().__init__(*args, **kwargs)

        self._io = io
        self._cursor = cursor

        self._limit = limit
        self._funnel = funnel

        self._index = 0
        self._buffer = bytearray()

    @property
    def index(self):

        """
        Intenral buffer index and relative cursor position.
        """

        return self._index

    @property
    def buffer(self):

        """
        Internal data buffer.
        """

        return self._buffer

    def _show(self, key):

        """
        Should be used for sending data to stdin.
        """

        if self._funnel:
            rune = key.decode()
            if rune.isprintable():
                rune = self._funnel(rune)
                key = rune.encode()

        self._io.send(key)

    def _constrain(self):

        """
        Raises :exc:`Abort` if further insertion is disallowed.
        """

        if self._limit and len(self._buffer) == self._limit:
            raise Abort()


class LineEditor(Editor):

    """
    Use for editing a single line of text.

    Does not support line breaks or moving vertically.
    """

    def clear(self):

        """
        Clears screen text after origin.
        """

        self._cursor.left(self._index)
        self._cursor.erase()

    def reset(self):

        """
        Reverts index and clears buffer.
        """

        self._index = 0
        self._buffer.clear()

    def _draw(self):

        """
        Draw whatever comes after index.
        """

        self._cursor.save()

        self._cursor.erase()

        try:
            stop = self._buffer.index(b'\n', self._index)
        except ValueError:
            buffer = self._buffer[self._index:]
        else:
            buffer = self._buffer[self._index:stop + 1]

        for val in buffer:
            key = val.to_bytes(1, 'big')
            self._show(key)

        self._cursor.load()

    def move(self, size):

        """
        Move `size` spots horizontally. Negative for left.
        """

        index = self._index + size

        if index < 0 or index > len(self._buffer):
            raise Abort()

        self._index = index

        (self._cursor.left if size < 0 else self._cursor.right)(size)

        self._dispatch('move', size)

    @wrapio.event('move_x')
    def _nnc(self, size):

        self.move(size)

    def _insert(self, key):

        """
        Insert a key to internal buffer, increment index and show it.
        Redraw succeeding runes if not at end of line.
        """

        self._buffer.insert(self._index, ord(key))

        self._index += 1

        # moves cursor +1
        self._show(key)

        if not self._index == len(self._buffer):
            # not at end of stream;
            # need to redraw the rest as a rune has been overwritten
            self._draw()

    @wrapio.event('insert')
    def _nnc(self, key):

        if key == '\t':
            return

        self._constrain()

        self._insert(key)

        self._dispatch('insert', key)

    def _delete(self, left):

        """
        Move ``1`` spot left if ``left`` or right otherwise. Delete rune on
        index and use :meth:`draw`.
        """

        self.move(- left)

        rune = self._buffer.pop(self._index)

        self._dispatch('delete', left)

        self._draw()

        return rune

    @wrapio.event('delete')
    def _nnc(self, left):

        self._delete(left)

    def _submit(self):

        self._dispatch('submit')

    @wrapio.event('enter')
    def _nnc(self, key):

        self._submit()


class MultiLineEditor(LineEditor):

    """
    Use for editing multiple lines of text.

    Supports line breaks and moving vertically.
    """

    def __init__(self, *args, finish = 3, **kwargs):

        super().__init__(*args, **kwargs)

        self._finish = finish

    def _draw(self):

        """
        Same as :meth:`LineEditor.draw`, except accounts for line breaks.
        """

        self._cursor.save()

        buffer = self._buffer[self._index:]

        lines = buffer.split(b'\n')
        for (index, line) in enumerate(lines):
            if index:
                self._cursor.down(1)
            self._cursor.erase()
            self._show(line)

        self._cursor.load()

    def move(self, size):

        """
        Same as :meth:`LineEditor.move`, except accounts for line breaks.
        """

        index = self._index

        super().move(size)

        left = size < 0

        if left:
            buffer = self._buffer[self._index:index]
        else:
            buffer = self._buffer[index:self._index]

        count = buffer.count(b'\n')

        if count == 0:
            return

        try:
            start = self._buffer.rindex(b'\n', 0, self._index)
        except ValueError:
            start = 0
        else:
            start += 1
        size = self._index - start

        if left:
            func = self._cursor.up
        else:
            func = self._cursor.down

        func(count)

        self._cursor.right(size)

    def _move_up(self):

        """
        Moves cursor on same column of line above, or at end if no room.
        """

        try:
            enter = self._buffer.rindex(b'\n', 0, self._index)
        except ValueError:
            raise Abort()

        try:
            leave = self._buffer.rindex(b'\n', 0, enter)
        except ValueError:
            # moving to the "back" of a non-existent '\n'
            leave = - 1

        this_size = self._index - enter

        that_size = enter - leave

        size = max(this_size, that_size)

        self.move(- size)

    def _move_down(self):

        """
        Moves cursor on same column of line bellow, or at end if no room.
        """

        try:
            enter = self._buffer.rindex(b'\n', 0, self._index)
        except ValueError:
            enter = - 1

        try:
            anchor = self._buffer.index(b'\n', self._index)
        except ValueError:
            raise Abort()

        try:
            leave = self._buffer.index(b'\n', anchor + 1)
        except ValueError:
            leave = len(self._buffer)

        this_size = anchor - enter

        that_size = leave - self._index

        size = min(this_size, that_size)

        self.move(size)

    @wrapio.event('move_y')
    def _nnc(self, up):

        (self._move_up if up else self._move_down)()

    def _delete(self, left):

        """
        Same as :meth:`LineEditor._delete`, except accounts for line breaks.
        """

        rune = super()._delete(left)

        if not rune == ord(b'\n'):
            return

        buffer = self._buffer[self._index:]

        count = buffer.count(b'\n') + 1

        self._cursor.save()

        self._cursor.down(count)

        self._cursor.erase()

        self._cursor.load()

    @wrapio.event('enter')
    def _nnc(self, key):

        if not key == b'\n':
            return

        self._constrain()

        while True:
            # delete line-trailing "white"space
            try:
                current = self._buffer[self._index - 1]
            except IndexError:
                break
            if not current == 32:
                break
            self._delete(True)

        self._cursor.erase()

        self._insert(key)

        if not self._buffer.endswith(key * self._finish):
            return

        for _ in range(self._finish):
            self._buffer.pop()

        self._submit()


class Select(abc.Handle):

    """
    Use for cycling through and selecting options.
    """

    def __init__(self,
                 io,
                 cursor,
                 options,
                 *args,
                 prefix = b'> ',
                 indent = None,
                 funnel = None,
                 limit = 0,
                 **kwargs):

        super().__init__(*args, **kwargs)

        self._io = io

        self._cursor = cursor

        options = list(options)

        self._index = 0
        self._options = options

        self._prefix = prefix
        self._indent = len(prefix) if indent is None else indent

        self._funnel = funnel

        self._limit = limit
        self._upper = 0

    @property
    def index(self):

        """
        Internal options index.
        """

        return self._index

    @property
    def options(self):

        """
        Internal options.
        """

        return self._options

    @property
    def _size(self):

        """
        Amount of options.
        """

        return len(self._options)

    @property
    def _top(self):

        """
        Amount of lines to climb to reach the top.
        """

        return (self._limit or self._size) - 1

    @property
    def _lower(self):

        """
        Lower bound for display window.
        """

        return self._upper + self._limit

    def clear(self):

        """
        Clears scren text after origin.
        """

        self._cursor.up(self._top)

        self._cursor.clear()

    def reset(self):

        """
        Reverts index and clears options.
        """

        self._index = 0
        self._options.clear()

        self._upper = 0

    def space(self):

        """
        Add new lines to make room for options.
        """

        self._io.send(b'\n' * self._top)

    def _dress(self, index, option, current):

        """
        Use or processing of options after funneling.
        """

        return option

    def _make(self, index, option, current):

        """
        Get a line according to option and whether it's currently hovered over.
        """

        if self._funnel:
            option = self._funnel(index, option, current)

        prefix = self._prefix if current else b''
        prefix = prefix + b' ' * (self._indent - len(prefix))

        line = prefix + self._dress(index, option, current)

        return line

    def draw(self):

        """
        Clear screen and redraw options.
        """

        self._cursor.save()

        self._cursor.up(self._top)

        pairs = tuple(enumerate(self._options))
        judge = lambda pair: pair[0] == self._index
        currents = map(judge, pairs)
        pairs = tuple(zip(pairs, currents))

        if self._limit:
            pairs = pairs[self._upper:self._lower]

        for ((index, option), current) in pairs:
            self._cursor.erase()
            line = self._make(index, option, current)
            self._io.send(line)
            self._cursor.down(1)

        self._cursor.load()

    def move(self, up):

        """
        Hover next option if ``up`` or last otherwise.
        """

        index = self._index + (- 1 if up else 1)

        if index < 0:
            index = self._size - 1
        elif index == self._size:
            index = 0

        if index < self._upper:
            self._upper = index
        elif not index < self._lower:
            self._upper = index - self._limit + 1

        self._index = index

        self._dispatch('move', up)

        self.draw()

    @wrapio.event('move_y')
    def _nnc(self, up):

        self.move(up)

    def _submit(self):

        self._dispatch('submit')

    @wrapio.event('enter')
    def _nnc(self, key):

        self._submit()


class MultiSelect(Select):

    def __init__(self, *args, active = b'[X] ', inactive = b'[ ] ', **kwargs):

        super().__init__(*args, **kwargs)

        self._active = active
        self._inactive = inactive

        self._indexes = set()

    @property
    def indexes(self):

        return self._indexes

    def _dress(self, index, option, current):

        signal = self._active if index in self._indexes else self._inactive

        return signal + option

    def _add(self, full):

        if full:
            indexes = range(self._size)
            self._indexes.update(indexes)
        else:
            self._indexes.add(self._index)

    def _pop(self, full):

        if full:
            self._indexes.clear()
        else:
            self._indexes.remove(self._index)

    def _inform(self, new):

        exists = self._index in self._indexes
        full = exists if new else not new

        (self._add if new else self._pop)(full)

        self._dispatch('inform', new, full)

        self.draw()

    @wrapio.event('move_x')
    def _nnc(self, size):

        new = size > 0

        self._inform(new)
