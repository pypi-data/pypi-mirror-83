from ..node import Node

programTrackEventFragment = """
fragment ProgramTrackEvent on ProgramTrackEvent {
    id
}
"""


class ProgramTrackEvent(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
