from ..base import BlockingBase, AwaitingBase


class Blocking(BlockingBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args, **kwargs
        )


class Awaiting(AwaitingBase):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args, **kwargs
        )
