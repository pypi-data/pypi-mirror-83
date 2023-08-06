import types
import sys
import wrapio
import itertools

from . import io
from . import cursor
from . import abc
from . import base
from . import utils


__all__ = ('Input', 'Password', 'Question', 'Confirm', 'Select')


_colors = types.SimpleNamespace(
    info = b'\x1b[38;5;6m',
    done = b'\x1b[38;5;10m',
    fail = b'\x1b[38;5;9m',
    hint = b'\x1b[38;5;7m'
)


_io = io.IO(sys.stdin.buffer, sys.stdout.buffer)


_cursor = cursor.Cursor(_io)


class Interactive:

    # __slots__ = ('_io', '_cursor')

    def __init__(self, io = _io, cursor = _cursor):

        self._io = io

        self._cursor = cursor

    def _enter(self):

        self._io.start()

    def _leave(self):

        self._io.stop()

    def __enter__(self):

        self._enter()

        return self

    def __exit__(self, type, value, traceback):

        self._leave()


class Aware(Interactive, abc.Handle):

    __slots__ = ()

    def __init__(self):

        Interactive.__init__(self)
        abc.Handle.__init__(self)


class Editor(Aware):

    __slots__ = ('_editor', '_source')

    def __init__(self, multi = False, /, **config):

        super().__init__()

        cls = base.MultiLineEditor if multi else base.LineEditor

        editor = self._editor = cls(
            self._io,
            self._cursor,
            **config,
            callback = self.invoke
        )

        translator = base.Translator(
            self._io,
            callback = editor.invoke
        )

        self._source = base.Source(
            self._io,
            callback = translator.invoke
        )

    @wrapio.event('submit')
    def _nnc(self):

        self._source.done()

    def _done(self):

        self._io.send(b'\n')

    def get(self, prompt = '', /, *, hint = '', draw = True):

        if draw:
            buffer = prompt.encode()
            if hint:
                hint = hint.encode()
                buffer += utils.paint(hint, _colors.hint)
            self._io.send(buffer)

        self._source.stream()

        result = self._editor.buffer.decode()

        return result


class Input(Editor):

    __slots__ = ()

    def get(self, *args, **kwargs):

        result = super().get(*args, **kwargs)

        self._editor.reset()

        self._done()

        return result


class Password(Input):

    __slots__ = ()

    def __init__(self, *args, rune = '*', **config):
        super().__init__(*args, **config, funnel = self._conceal)

        self._rune = rune

    def _conceal(self, rune):

        return self._rune


class Responsive(Editor):

    __slots__ = ('_pull',)

    def get(self, prompt, /, *args, hint = '', **kwargs):

        self._pull = len(hint)

        result = super().get(prompt, *args, hint = hint, **kwargs)

        return result

    def _respond(self, color, buffer):

        self._cursor.hide()

        self._cursor.left(self._editor.index + self._pull)

        self._cursor.erase()

        buffer = utils.paint(buffer, color)

        self._io.send(buffer)

        self._editor.reset()

        self._done()

        self._cursor.show()


class Question(Responsive):

    __slots__ = ()

    def _respond(self, color):

        super()._respond(color, self._editor.buffer)

    def accept(self):

        return self._respond(_colors.done)

    def reject(self):

        return self._respond(_colors.fail)


sentiments = (
    {'n', 'no', '0', 'false', 'f'},
    {'y', 'ye', 'yes', '1', 'true', 't'}
)


class Confirm(Responsive):

    __slots__ = ()

    def get(self,
            *args,
            sentiments = sentiments,
            answers = ('No', 'Yes'),
            **kwargs):

        for index in itertools.count():
            value = super().get(*args, **kwargs, draw = not index)
            value = value.lower()
            for (index, sentiment) in enumerate(sentiments):
                if not value in sentiment:
                    continue
                break
            else:
                self._io.bell()
                continue
            break

        answer = answers[index]
        answer = answer.encode()

        self._respond(_colors.info, answer)

        return bool(index)


class Select(Aware):

    @staticmethod
    def _get_funnel(funnel, color):

        funnels = [funnel]

        @funnels.append
        def funnel_encode(index, option, current):
            option = str(option).encode()
            return option

        if color:
            @funnels.append
            def funnel_paint(index, option, current):
                if current:
                    option = utils.paint(option, color)
                return option

        funnels = tuple(filter(bool, funnels))

        def funnel_mix(index, option, current):
            for funnel in funnels:
                option = funnel(index, option, current)
            return option

        return funnel_mix

    def __init__(self,
                 options,
                 multi = False,
                 /,
                 color = _colors.info,
                 **config):

        super().__init__()

        funnel = config.get('funnel')
        config['funnel'] = self._funnel = self._get_funnel(funnel, color)

        for key in ('prefix', 'active', 'inactive'):
            try:
                value = config[key]
            except KeyError:
                continue
            config[key] = b'' if value is None else value.encode()

        cls = base.MultiSelect if multi else base.Select

        select = self._select = cls(
            self._io,
            self._cursor,
            options,
            **config,
            callback = self.invoke
        )

        translator = base.Translator(
            self._io,
            callback = select.invoke
        )

        self._source = base.Source(
            self._io,
            callback = translator.invoke
        )

    def _submit(self):

        self._source.done()

    @wrapio.event('submit')
    def _nnc(self):

        self._submit()

    def _draw(self, prompt):

        if prompt:
            self._io.send(prompt + b'\n')

        self._select.space()

        self._select.draw()

    def _reset(self, indent, result):

        self._select.clear()

        if indent and result:
            self._cursor.up(1)
            self._cursor.right(indent)
            buffer = self._funnel(self._select.index, result, True)
            self._io.send(buffer + b'\n')

        self._select.reset()

    def _get_m_i(self):

        return tuple(sorted(self._select.indexes))

    def _get_m(self):

        indexes = self._get_m_i()

        options = tuple(self._select.options[index] for index in indexes)

        result = tuple(zip(indexes, options))

        return (result, None)

    def _get_s_i(self):

        return self._select.index

    def _get_s(self):

        index = self._get_s_i()

        option = self._select.options[index]

        result = (index, option)

        return (result, option)

    def get(self, prompt = '', /):

        prompt = prompt.encode()

        self._cursor.hide()

        self._draw(prompt)

        try:
            self._source.stream()
        finally:
            self._cursor.show()

        multi = isinstance(self._select, base.MultiSelect)

        (result, show) = (self._get_m if multi else self._get_s)()

        self._reset(len(prompt), show)

        return result
