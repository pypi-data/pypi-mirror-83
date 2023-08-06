from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .obschart_api_client import ObschartApiClient


class Context(object):
    client: "ObschartApiClient"
    data: dict

    def __init__(self, client, data={}):
        super().__init__()

        self.client = client
        self.data = data
