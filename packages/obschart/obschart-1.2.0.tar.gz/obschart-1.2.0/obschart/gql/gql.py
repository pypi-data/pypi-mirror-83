from graphql.language.parser import parse
from graphql.language.source import Source


def gql(source_body: str):
    source = Source(source_body, "GraphQL request")
    return parse(source)
