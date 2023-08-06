from .obschart_api_transport import ObschartApiTransport
from typing import Optional, Union, Any, Callable
from .blocks_action_builder import BlocksActionBuilder
from .step_builder import StepBuilder
from typing import Awaitable
import asyncio
from .gql import GqlClient
from .api import ObschartApiClient
import io
import logging
from .application_request_handler import Request

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

OnRequestCallback = Callable[[Request], Awaitable[None]]

log = logging.getLogger(__name__)


class ObschartClient(ObschartApiClient):
    _authentication_token: str
    _transport: ObschartApiTransport

    def __init__(
        self,
        authentication_token: Optional[str] = None,
        api_url: Optional[str] = "https://api.obschart.com/",
    ):

        self._transport = ObschartApiTransport(api_url)
        gql_client = GqlClient(transport=self._transport)
        super().__init__(gql_client=gql_client)

        if authentication_token:
            self.set_authentication_token(authentication_token)

    def set_authentication_token(self, authentication_token: str):
        self._authentication_token = authentication_token
        self._transport._client.headers["Authorization"] = f"Bearer {authentication_token}"

    async def login(self, email: str, password: str):
        authentication_token, session = await self.create_session(email, password)
        self.set_authentication_token(authentication_token)
        return session

    async def run(self, on_request_callback: OnRequestCallback) -> Any:
        application = await self.get_application(token=self._authentication_token)

        while True:
            application_requests = await self.poll_application_requests(
                {"applicationId": {"eq": application.id}}
            )

            for application_request in application_requests:
                request = Request(application_request, self)

                async def task():
                    try:
                        log.debug("Handling request...")
                        inner_task = on_request_callback(request)
                        await asyncio.wait_for(inner_task, timeout=5 * 60)
                        log.debug("Request handled")
                    except:
                        log.exception("Could not handle request: %s", request)

                asyncio.ensure_future(task())

    def on_request(self, on_request_callback: OnRequestCallback):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run(on_request_callback))
        # https://stackoverflow.com/a/37345564/11225752
        # loop.run_until_complete(asyncio.Task.all_tasks())

    def build_feedback_data(self):
        return BlocksActionBuilder()

    def build_step(self, title: str):
        return StepBuilder(title)

    # def create_image(self, image_like: Union[plt.Figure, str, Any]):
    def create_image(self, image_like: Union[Any, str, Any]):
        if isinstance(image_like, str):
            file_path = image_like
            image = open(file_path, "rb")
        elif plt and isinstance(image_like, plt.Figure):
            figure = image_like

            buffer = io.BytesIO()
            figure.savefig(buffer, format="png")
            buffer.seek(0)

            image = buffer
        else:
            image = image_like

        return super().create_image(image)
