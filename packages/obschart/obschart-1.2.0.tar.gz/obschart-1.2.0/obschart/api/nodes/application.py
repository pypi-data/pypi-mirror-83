from ..node import Node

applicationFragment = """
fragment Application on Application {
    id
    name
}
"""


class Application(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
