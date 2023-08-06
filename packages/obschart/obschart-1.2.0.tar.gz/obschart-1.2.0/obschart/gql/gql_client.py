import logging

log = logging.getLogger(__name__)

from .gql_client_transport import GqlClientTransport


class RetryError(Exception):
    """Custom exception thrown when retry logic fails"""

    def __init__(self, retries_count, last_exception):
        message = "Failed %s retries: %s" % (retries_count, last_exception)
        super(RetryError, self).__init__(message)
        self.last_exception = last_exception


class GqlClient(object):
    _transport: GqlClientTransport
    _retries: int

    def __init__(
        self, transport, retries=0,
    ):
        self._transport = transport
        self._retries = retries

    async def execute(self, document, *args, **kwargs):
        result = await self._get_result(document, *args, **kwargs)
        if result.errors:
            raise Exception(str(result.errors[0]))

        return result.data

    async def _get_result(self, document, *args, **kwargs):
        if not self._retries:
            return await self._transport.execute(document, *args, **kwargs)

        last_exception = None
        retries_count = 0
        while retries_count < self._retries:
            try:
                result = await self._transport.execute(document, *args, **kwargs)
                return result
            except Exception as e:
                last_exception = e
                log.warning(
                    "Request failed with exception %s. Retrying for the %s time...",
                    e,
                    retries_count + 1,
                    exc_info=True,
                )
            finally:
                retries_count += 1

        raise RetryError(retries_count, last_exception)
