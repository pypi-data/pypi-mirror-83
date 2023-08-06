from ..node import Node

imageFragment = """
fragment Image on Image {
    id
    url
    width
    height
}
"""


class Image(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)

    @property
    def url(self):
        return self._data["url"]

    @property
    def width(self):
        return self._data["width"]

    @property
    def height(self):
        return self._data["height"]
