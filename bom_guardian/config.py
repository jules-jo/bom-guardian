"""Central configuration. All tunables live here, loaded from env where secret."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

SEARCH_URL = "https://ydc-index.io/v1/search"
CONTENTS_URL = "https://ydc-index.io/v1/contents"
RESEARCH_URL = "https://api.you.com/v1/research"

# Valid values: ulow, lite, standard, deep, exhaustive, frontier.
# Below "standard", lifecycle verdicts get flaky (miss vendor PDN/PCN notices).
# Soft ranking preference for searches where official vendor documents should
# outrank mirrors/forums (errata lookups). Users can override in the UI.
VENDOR_BOOST_DOMAINS = (
    "st.com",
    "microchip.com",
    "ti.com",
    "nxp.com",
    "infineon.com",
    "analog.com",
    "renesas.com",
)

RESEARCH_EFFORT = "standard"
SEARCH_RESULT_COUNT = 5
MAX_CONCURRENT_COMPONENTS = 4
HTTP_TIMEOUT_SECONDS = 30
RESEARCH_TIMEOUT_SECONDS = 300
NEWS_FRESHNESS = "month"


class ConfigError(RuntimeError):
    """Raised when required configuration is missing."""


def get_api_key() -> str:
    api_key = os.environ.get("YDC_API_KEY", "")
    if not api_key:
        raise ConfigError(
            "YDC_API_KEY is not set. Copy .env.example to .env and add your key "
            "from https://you.com/platform"
        )
    return api_key
