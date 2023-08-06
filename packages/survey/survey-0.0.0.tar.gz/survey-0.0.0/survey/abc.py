import wrapio


__all__ = ('Handle',)


class Handle(wrapio.Handle):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs, sync = True)

    def invoke(self, *args, safe = True, **kwargs):

        try:
            super().invoke(*args, **kwargs)
        except KeyError:
            done = False
        else:
            done = True

        return done
