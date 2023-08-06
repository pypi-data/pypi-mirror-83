from .nodes import *
from .context import Context
from typing import Optional, Dict, Any, List
import datetime
import asyncio
import time
from ..gql import GqlClient, gql
import logging
import httpx

log = logging.getLogger(__name__)


class ObschartApiClient(object):
    _gql_client: GqlClient
    _context: Context

    def __init__(
        self, gql_client,
    ):
        super().__init__()

        self._gql_client = gql_client
        self._context = Context(self)

    def _execute(self, query, variables: Optional[Dict[str, Any]] = None, *, timeout=None):
        return self._gql_client.execute(query, variables, timeout=timeout)

    def _execute_mutation(self, query, input: Optional[Dict[str, Any]] = None, *, timeout=None):
        variables = {"input": input}
        return self._execute(query, variables)

    async def create_session(self, email: str, password: str):
        query = gql(
            """
          mutation CreateSessionMutation($input: CreateSessionInput) {
            createSession(input: $input) {
              token
              session {
                id
              }
            }
          }
          """
        )

        input = {"password": password, "email": email}
        result = await self._execute_mutation(query, input)

        authentication_token = result["createSession"]["token"]
        session = Session(result["createSession"]["session"], Context(self))

        return (authentication_token, session)

    async def poll_program_track_action_responses(self, filter: dict):
        query = gql(
            """
          query OnResponseQuery($filter: ProgramTrackActionResponseFilterInput) {
            programTrackActionResponses(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramTrackActionResponse
                }
              }
            }
          }
        """
            + programTrackActionResponseFragment
        )

        now = datetime.datetime.utcnow()
        variables = {
            "filter": {
                **filter,
                "createdAt": {"after": now.replace(tzinfo=datetime.timezone.utc).isoformat()},
            }
        }

        while True:
            start = time.monotonic()
            try:
                response = await self._execute(query, variables, timeout=1)
                edges = response["programTrackActionResponses"]["edges"]

                if len(edges) > 0:
                    break
            except httpx.TimeoutException as exception:
                log.warn(f"Polling timed out: {exception.__class__.__name__}")
            except:
                log.exception("Polling failed")

            duration = time.monotonic() - start
            await asyncio.sleep(max(1 - duration, 0))

        responses: List[ProgramTrackActionResponse] = [
            ProgramTrackActionResponse(edge["node"], self._context) for edge in edges
        ]

        return responses

    async def create_program_track_action(self, data: Any, waits_for_feedback: bool):
        query = gql(
            """
          mutation CreateProgramTrackActionMutation($input: CreateProgramTrackActionInput!) {
            createProgramTrackAction(input: $input) {
              programTrackAction  {
                ...ProgramTrackAction
              }
            }
          }
          """
            + programTrackActionFragment
        )

        input = {"data": data, "waitsForFeedback": waits_for_feedback}
        result = await self._execute_mutation(query, input)

        return ProgramTrackAction(
            result["createProgramTrackAction"]["programTrackAction"], self._context
        )

    async def create_image(self, image: Any):
        query = gql(
            """
          mutation CreateImageMutation($input: CreateImageInput!) {
            createImage(input: $input) {
              image  {
                ...Image
              }
            }
          }
          """
            + imageFragment
        )

        input = {"image": image}
        result = await self._execute_mutation(query, input)

        return Image(result["createImage"]["image"], self._context)

    async def create_program_invitation(self, program_id: str):
        query = gql(
            """
          mutation CreateProgramInvitationMutation($input: CreateProgramInvitationInput!) {
            createProgramInvitation(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          """
        )

        input = {"programId": program_id}
        result = await self._execute_mutation(query, input)

        return ProgramInvitation(
            result["createProgramInvitation"]["programInvitation"], self._context
        )

    async def send_program_invitation_sms(self, program_invitation_id: str, phone_number: str):
        query = gql(
            """
          mutation SendProgramInvitationSmsMutation($input: SendProgramInvitationSmsInput) {
            sendProgramInvitationSms(input: $input) {
              programInvitation  {
                id
              }
            }
          }
          """
        )

        input = {"id": program_invitation_id, "phoneNumber": phone_number}
        result = await self._execute(query, input)

        return ProgramInvitation(
            result["sendProgramInvitationSms"]["programInvitation"], self._context
        )

    async def get_current_session(self):
        query = gql(
            """
          query CurrentSessionQuery {
            currentSession {
              id
              user {
                id
                name
                email
              }
            }
          }
          """
        )

        result = await self._execute(query)

        return Session(result["currentSession"], self._context)

    async def get_program_track_action_response(self, id):
        query = gql(
            """
          query ProgramTrackActionResponseQuery($id: ID) {
            programTrackActionResponse(id: $id) {
              ...ProgramTrackActionResponse
            }
          }
          """
            + programTrackActionResponseFragment
        )

        variables = {"id": id}
        result = await self._execute(query, variables)

        return ProgramTrackActionResponse(result["programTrackActionResponse"], self._context)

    async def update_program_track_action_response(self, id: str, *, input: Dict[str, Any]):
        query = gql(
            """
            mutation UpdateProgramTrackActionResponseMutation($input: UpdateProgramTrackActionResponseInput!)  {
                updateProgramTrackActionResponse(input: $input) {
                    programTrackActionResponse {
                        ...ProgramTrackActionResponse
                    }
                }
            }
        """
            + programTrackActionResponseFragment
        )

        input = {"id": id, **input}
        result = await self._context.client._execute_mutation(query, input)

        return ProgramTrackActionResponse(
            result["updateProgramTrackActionResponse"]["programTrackActionResponse"], self._execute,
        )

    async def list_program_modules(self, filter: dict):
        query = gql(
            """
          query ListProgramModules($filter: ProgramModuleFilterInput) {
            programModules(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ProgramModule
                }
              }
            }
          }
        """
            + programModuleFragment
        )

        variables = {"filter": filter}
        response = await self._execute(query, variables)

        nodes: List[ProgramModule] = [
            ProgramModule(edge["node"], self._context)
            for edge in response["programModules"]["edges"]
        ]

        return nodes

    async def list_tags(self, filter: dict):
        query = gql(
            """
          query ListTags($filter: TagFilterInput) {
            tags(filter: $filter, first: 9999) {
              edges {
                node {
                  ...Tag
                }
              }
            }
          }
        """
            + tagFragment
        )

        variables = {"filter": filter}
        response = await self._execute(query, variables)

        nodes: List[Tag] = [Tag(edge["node"], self._context) for edge in response["tags"]["edges"]]

        return nodes

    async def list_chat_channels(self, filter: dict):
        query = gql(
            """
          query ListChatChannels($filter: ChatChannelFilterInput) {
            chatChannels(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ChatChannel
                }
              }
            }
          }
        """
            + chatChannelFragment
        )

        variables = {"filter": filter}
        response = await self._execute(query, variables)

        nodes: List[ChatChannel] = [
            ChatChannel(edge["node"], self._context) for edge in response["chatChannels"]["edges"]
        ]

        return nodes

    async def list_client_profile_invitations(self, filter: dict):
        query = gql(
            """
          query ListClientProfileInvitations($filter: ClientProfileInvitationFilterInput) {
            clientProfileInvitations(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ClientProfileInvitation
                }
              }
            }
          }
        """
            + clientProfileInvitationFragment
        )

        variables = {"filter": filter}
        response = await self._execute(query, variables)

        nodes: List[ClientProfileInvitation] = [
            ClientProfileInvitation(edge["node"], self._context)
            for edge in response["clientProfileInvitations"]["edges"]
        ]

        return nodes

    async def update_program_module(self, id: str, is_public: bool):
        query = gql(
            """
            mutation UpdateProgramModuleMutation($input: UpdateProgramModuleInput!)  {
                updateProgramModule(input: $input) {
                    programModule {
                        ...ProgramModule
                    }
                }
            }
        """
            + programModuleFragment
        )

        input = {
            "id": id,
            "isPublic": is_public,
        }
        result = await self._context.client._execute_mutation(query, input)

        return ProgramModule(result["updateProgramModule"]["programModule"], self._execute,)

    async def delete_node(self, id: str):
        query = gql(
            """
            mutation DeleteNodeMutation($input: DeleteNodeInput!)  {
                deleteNode(input: $input) {
                    node {
                        id
                    }
                }
            }
        """
        )

        input = {
            "id": id,
        }
        await self._context.client._execute_mutation(query, input)

    async def get_application(self, id: str = None, token: str = None):
        query = gql(
            """
          query ApplicationQuery($id: ID, $token: String) {
            application(id: $id, token: $token) {
              id
            }
          }
          """
        )

        variables = {"id": id, "token": token}
        result = await self._execute(query, variables)

        return Application(result["application"], self._context)

    async def update_program_track_action(self, id: str, *, input: Dict[str, Any]):
        query = gql(
            """
            mutation UpdateProgramTrackActionMutation($input: UpdateProgramTrackActionInput!)  {
                updateProgramTrackAction(input: $input) {
                    programTrackAction {
                        ...ProgramTrackAction
                    }
                }
            }
        """
            + programTrackActionFragment
        )

        input = {"id": id, **input}
        result = await self._context.client._execute_mutation(query, input)

        return ProgramTrackAction(
            result["updateProgramTrackAction"]["programTrackAction"], self._execute,
        )

    async def update_application_request(self, id: str, *, input: Dict[str, Any]):
        query = gql(
            """
            mutation UpdateApplicationRequestMutation($input: UpdateApplicationRequestInput!)  {
                updateApplicationRequest(input: $input) {
                    applicationRequest {
                        ...ApplicationRequest
                    }
                }
            }
        """
            + applicationRequestFragment
        )

        input = {"id": id, **input}
        result = await self._context.client._execute_mutation(query, input)

        return ApplicationRequest(
            result["updateApplicationRequest"]["applicationRequest"], self._execute,
        )

    async def poll_application_requests(self, filter: dict):
        query = gql(
            """
          query PollApplicationRequestsQuery($filter: ApplicationRequestFilterInput) {
            applicationRequests(filter: $filter, first: 9999) {
              edges {
                node {
                  ...ApplicationRequest
                }
              }
            }
          }
        """
            + applicationRequestFragment
        )

        now = datetime.datetime.utcnow()
        variables = {
            "filter": {
                **filter,
                "createdAt": {"after": now.replace(tzinfo=datetime.timezone.utc).isoformat()},
            }
        }

        while True:
            start = time.monotonic()
            try:
                response = await self._execute(query, variables, timeout=1)
                edges = response["applicationRequests"]["edges"]

                if len(edges) > 0:
                    break
            except httpx.TimeoutException as exception:
                log.warn(f"Polling timed out: {exception.__class__.__name__}")
            except:
                log.exception("Polling failed")

            duration = time.monotonic() - start
            await asyncio.sleep(max(1 - duration, 0))

        requests: List[ApplicationRequest] = [
            ApplicationRequest(edge["node"], self._context) for edge in edges
        ]

        return requests

    async def create_program_track_action_response(self, *, input: Dict[str, Any]):
        query = gql(
            """
          mutation CreateProgramTrackActionResponseMutation($input: CreateProgramTrackActionResponseInput!) {
            createProgramTrackActionResponse(input: $input) {
              programTrackActionResponse  {
                ...ProgramTrackActionResponse
              }
            }
          }
          """
            + programTrackActionResponseFragment
        )

        result = await self._execute_mutation(query, input)

        return ProgramTrackActionResponse(
            result["createProgramTrackActionResponse"]["programTrackActionResponse"], self._context
        )
