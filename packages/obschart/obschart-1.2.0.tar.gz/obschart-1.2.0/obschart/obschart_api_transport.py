import httpx
from httpx._config import UNSET
from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast
from .gql import GqlClientTransport
from .extract_files import extract_files
import json
import os.path
from typing import Any
from uuid import uuid4


class ObschartApiTransport(GqlClientTransport):
    _client: httpx.AsyncClient
    _url: str

    def __init__(
        self, url, *, headers={}, timeout=5,
    ):
        super().__init__()
        self._client = httpx.AsyncClient()
        self._url = url

    async def execute(self, document, variables=None, *, timeout=None):
        query_str = print_ast(document)
        payload = {"query": query_str, "variables": variables or {}}

        extracted_payload, files = extract_files(payload)

        response: httpx.Response
        if len(files):
            formData = dict()

            formData["operations"] = (None, json.dumps(extracted_payload))

            pathMap = {}
            i = 1
            for paths in files.values():
                pathMap[i] = paths
                i += 1
            formData["map"] = (None, json.dumps(pathMap))

            i = 1
            for file, paths in files.items():
                _file: Any = file
                if hasattr(_file, "name"):
                    file_name = os.path.basename(_file.name)
                else:
                    file_name = str(uuid4())
                formData[str(i)] = (file_name, file)
                i += 1

            response = await self._client.post(
                self._url, files=formData, timeout=(timeout or UNSET)
            )
        else:
            response = await self._client.post(self._url, json=payload, timeout=timeout or UNSET)

        response.raise_for_status()

        result = response.json()
        assert isinstance(result, dict) and (
            "errors" in result or "data" in result
        ), 'Received non-compatible response "{}"'.format(result)

        return ExecutionResult(errors=result.get("errors"), data=result.get("data"))
