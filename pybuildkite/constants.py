import enum


AGENT_V3_BASE_URL = "https://agent.buildkite.com/v3"


class APIVersion(enum.Enum):
    V2 = "v2"
    V3 = "v3"
