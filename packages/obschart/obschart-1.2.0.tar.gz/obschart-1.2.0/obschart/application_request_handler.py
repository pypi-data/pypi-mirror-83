from .api.nodes import *
from .step_builder import StepBuilder
from .blocks_action_builder import BlocksActionBuilder
from typing import Union, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .obschart_client import ObschartClient


class Request(object):
    _client: "ObschartClient"
    _last_request: Optional[Union[ApplicationRequest, ProgramTrackActionResponse]] = None
    application_request: ApplicationRequest

    def __init__(self, application_request: ApplicationRequest, client: "ObschartClient"):
        super().__init__()

        self._client = client
        self.application_request = application_request

    @property
    def action(self):
        return self.application_request.action

    @property
    def event(self):
        return self.application_request.event

    @property
    def lastRequest(self):
        if not self._last_request:
            return self.application_request
        return self._last_request

    @lastRequest.setter
    def lastRequest(self, lastRequest):
        self._last_request = lastRequest

    async def prompt(self, step: Union[dict, StepBuilder]):
        if isinstance(step, StepBuilder):
            step = step.build()

        data = {
            "type": "multiStep",
            "steps": [step],
        }
        pta = await self._client.create_program_track_action(data, waits_for_feedback=True)

        if isinstance(self.lastRequest, ApplicationRequest):
            await self._client.update_application_request(
                self.lastRequest.id, input={"responseProgramTrackActionId": pta.id}
            )
        else:
            await self._client.update_program_track_action_response(
                self.lastRequest.id, input={"feedbackProgramTrackActionId": pta.id}
            )

        response = await pta.wait_for_response()

        self.lastRequest = response

        return response.values

    async def set_output(self, blocks_action: Union[dict, BlocksActionBuilder], fields: list):
        # Update action with shape
        if isinstance(blocks_action, BlocksActionBuilder):
            blocks_action = blocks_action.build()

        data = {
            "type": "multiStep",
            "steps": [{"name": "", "action": blocks_action}],
        }
        await self._client.update_program_track_action(self.action.id, input={"data": data})

        # Create response with values
        response = {"steps": [{"fields": fields}]}
        await self._client.create_program_track_action_response(
            input={
                "programTrackActionId": self.action.id,
                "programTrackEventId": self.event and self.event.id or None,
                "response": response,
            },
        )

    async def end(self, step: Union[dict, StepBuilder] = None):
        if isinstance(step, StepBuilder):
            step = step.build()

        steps: list
        if step:
            steps = [step]
        else:
            steps = []

        data = {"type": "multiStep", "steps": steps}
        pta = await self._client.create_program_track_action(data, waits_for_feedback=False)

        if isinstance(self.lastRequest, ApplicationRequest):
            await self._client.update_application_request(
                self.lastRequest.id, input={"responseProgramTrackActionId": pta.id}
            )
        else:
            await self._client.update_program_track_action_response(
                self.lastRequest.id, input={"feedbackProgramTrackActionId": pta.id}
            )


class ApplicationRequestHandler(object):
    _client: "ObschartClient"

    def __init__(self, client):
        super().__init__()

        self._client = client

    @property
    def client(self) -> "ObschartClient":
        return self._client

    def on_request(self, request: Request):
        raise NotImplementedError
