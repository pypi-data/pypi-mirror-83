from ..node import Node
from .program_track_action import ProgramTrackAction, programTrackActionFragment

programTrackActionResponseFragment = (
    """
fragment ProgramTrackActionResponse on ProgramTrackActionResponse {
    id
    createdAt
    action {
        ...ProgramTrackAction
    }
    response
}
"""
    + programTrackActionFragment
)


class ProgramTrackActionResponse(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)

    @property
    def action(self):
        return ProgramTrackAction(self._data["action"], self._context)

    @property
    def data(self):
        return self._data["response"]

    @property
    def values(self):
        responses = self.data["steps"][0]["fields"]
        blocks = self.action.data["steps"][0]["action"]["blocks"]

        values = {}
        for index, block in enumerate(blocks):
            id = block.get("id")
            if id:
                values[id] = responses[index]

        return values
