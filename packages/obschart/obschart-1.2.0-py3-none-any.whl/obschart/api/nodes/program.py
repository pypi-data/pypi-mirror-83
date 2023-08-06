from ..node import Node


class Program(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
