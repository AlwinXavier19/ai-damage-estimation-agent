from app.services.azure_openai import AzureOpenAIService


def main():

    print("=" * 60)
    print("Creating Azure OpenAI Service...")
    print("=" * 60)

    try:
        client = AzureOpenAIService()

        print("\n✅ AzureOpenAIService created successfully!\n")

        print("Endpoint:")
        print(client.url)

        print("\nHeaders:")

        for key, value in client.headers.items():

            if key.lower() == "api-key":
                print(f"{key}: {value[:8]}********")
            else:
                print(f"{key}: {value}")

        print("\n✅ Configuration looks valid.")

    except Exception as e:

        print("\n❌ Failed to initialize AzureOpenAIService")
        print(e)


if __name__ == "__main__":
    main()