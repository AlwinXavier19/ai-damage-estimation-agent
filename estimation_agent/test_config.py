from app.config import settings

print("=" * 50)
print("Azure Configuration")
print("=" * 50)

print(settings.AZURE_OPENAI_ENDPOINT)
print(settings.AZURE_OPENAI_DEPLOYMENT)
print(settings.AZURE_OPENAI_API_VERSION)
print(settings.AZURE_OPENAI_KEY[:8] + "********")