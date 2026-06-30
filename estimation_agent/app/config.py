
"""
Application configuration.
"""

import os
from dotenv import load_dotenv

# Load .env during local development
load_dotenv()

DJANGO_ENV = os.getenv("DJANGO_ENV", "local").lower()
USE_KEYVAULT = os.getenv("USE_KEYVAULT", "true" if DJANGO_ENV != "local" else "false").lower() == "true"

if USE_KEYVAULT:
    from core.azure_secrets import get_secret

    def secret(name):
        return get_secret(name)
else:
    def secret(name):
        value = os.getenv(name)

        if value is None:
            raise RuntimeError(
                f"Environment variable '{name}' not found."
            )

        return value


class Settings:

    AZURE_OPENAI_KEY = secret("AZURE_OPENAI_KEY")

    AZURE_OPENAI_ENDPOINT = secret(
        "AZURE_OPENAI_ENDPOINT"
    ).rstrip("/")

    AZURE_OPENAI_DEPLOYMENT = secret(
        "AZURE_OPENAI_DEPLOYMENT"
    )

    AZURE_OPENAI_API_VERSION = secret(
        "AZURE_OPENAI_API_VERSION"
    )

    GPT_MODEL = "gpt-4o"

    REQUEST_TIMEOUT = 120

    MAX_RETRIES = 3

    TEMPERATURE = 0.2

    MAX_TOKENS = 1800


settings = Settings()