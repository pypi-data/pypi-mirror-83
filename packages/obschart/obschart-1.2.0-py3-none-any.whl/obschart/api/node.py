from typing import TYPE_CHECKING, Any, Dict

if TYPE_CHECKING:
    from .context import Context

NodeData = Dict[str, Any]


class Node(object):
    _data: NodeData
    _context: "Context"

    def __init__(self, data: NodeData, context: "Context"):
        super().__init__()

        self._data = data
        self._context = context

    def _execute(self, query, variables):
        if not self._context:
            raise Exception("Expected context")

        return self._context.client._execute(query, variables)

    def __repr__(self):
        clean_data = dict(self._data)
        clean_data.pop("id")
        return f"{self.__class__.__name__} (ID: {self.id}) {clean_data}"

    @property
    def id(self):
        return self._data["id"]
