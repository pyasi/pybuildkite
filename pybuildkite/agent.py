from pybuildkite.client import AgentClient as Client
from pybuildkite.constants import APIVersion
from pybuildkite.decorators import requires_agent_token
from pybuildkite.metrics import Metrics


class Agent(object):
    """
    Public API for the Agent REST API, https://buildkite.com/docs/apis/agent-api
    """

    def __init__(self, api_version: APIVersion = APIVersion.V3) -> None:
        """
        Create a new client
        :param api_version: The version of the Agent API
        """
        self.client = Client(api_version)
        self.base_url = f"https://agent.buildkite.com/{api_version.value}"

    def set_agent_token(self, agent_token: str) -> None:
        """
        Set the agent registration token to be used to authenticate the requests
        :param agent_token: The agent token
        """
        self.client.set_client_agent_token(agent_token)

    @requires_agent_token
    def metrics(self) -> Metrics:
        """
        Get Metrics operations for the Agent API
        """
        return Metrics(self.client, self.base_url)
