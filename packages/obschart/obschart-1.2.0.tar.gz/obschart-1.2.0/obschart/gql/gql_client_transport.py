from graphql.execution import ExecutionResult


class GqlClientTransport(object):
    async def execute(self, document, *args, **kwargs) -> ExecutionResult:
        raise NotImplementedError
