from ..node import Node
from .program_module import ProgramModule
from ...gql import gql
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .program_track_action_response import ProgramTrackActionResponse

programTrackActionFragment = """
fragment ProgramTrackAction on ProgramTrackAction {
    id
    sourceProgramModule {
        id
    }
    data
    waitsForFeedback
}
"""


class ProgramTrackAction(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)

    @property
    def waits_for_feedback(self) -> bool:
        return self._data["waitsForFeedback"]

    @property
    def data(self):
        return self._data["data"]

    @property
    def module(self):
        if not self._data["sourceProgramModule"]:
            return None

        return ProgramModule(self._data["sourceProgramModule"], self._context)

    async def list_responses(self):
        from .program_track_action_response import (
            ProgramTrackActionResponse,
            programTrackActionResponseFragment,
        )

        query = gql(
            """
          query ProgramTrackActionResponsesQuery($programTrackActionId: ID)  {
            programTrackAction(id: $programTrackActionId) {
              responses(first: 9999) {
                edges {
                  node {
                    ...ProgramTrackActionResponse
                  }
                }
              }
            }
          }
          """
            + programTrackActionResponseFragment
        )

        variables = {}
        variables["programTrackActionId"] = self.id
        response = await self._execute(query, variables)

        responses: List[ProgramTrackActionResponse] = []
        for edge in response["programTrackAction"]["responses"]["edges"]:
            responses.append(ProgramTrackActionResponse(edge["node"], self._context))

        return responses

    async def poll_responses(self) -> List["ProgramTrackActionResponse"]:
        return await self._context.client.poll_program_track_action_responses(
            {"programTrackActionId": {"eq": self.id}}
        )

    async def wait_for_response(self) -> "ProgramTrackActionResponse":
        responses = await self.poll_responses()
        return responses[0]
