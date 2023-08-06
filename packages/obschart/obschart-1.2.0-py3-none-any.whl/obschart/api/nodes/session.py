from ..node import Node


class Session(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
