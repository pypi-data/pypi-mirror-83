from ..node import Node

chatChannelFragment = """
fragment ChatChannel on ChatChannel {
    id
    twilioSid
    twilioLastMessageSid
    twilioLastMessageDateCreated
    # members(first: 9999) {
    #     edges {
    #         node {
    #             id
    #             name
    #         }
    #     }
    # }
    object {
        __typename
        id
    }
}
"""


class ChatChannel(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
