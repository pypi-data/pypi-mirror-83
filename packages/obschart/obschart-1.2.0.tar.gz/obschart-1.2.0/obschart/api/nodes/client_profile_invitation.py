from ..node import Node

clientProfileInvitationFragment = """
fragment ClientProfileInvitation on ClientProfileInvitation {
    id
    name
    token
    firebaseShortLink
    clientProfile {
        id
    }
}
"""


class ClientProfileInvitation(Node):
    def __init__(self, data, context):
        super().__init__(data, context=context)
