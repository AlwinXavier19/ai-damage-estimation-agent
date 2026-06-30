from app.services.azure_openai import AzureOpenAIService


def main():

    client = AzureOpenAIService()

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Reply with exactly: Azure GPT-4o Working"
        }
    ]

    print("=" * 60)
    print("Calling Azure OpenAI...")
    print("=" * 60)

    try:

        response = client.chat_completion(messages)

        print("\n✅ Raw Response\n")

        print(response)

        print("\n" + "=" * 60)

        print("Assistant Reply:")

        print(client.extract_content(response))

        print("=" * 60)

    except Exception as e:

        print("\n❌ Azure OpenAI Error\n")

        print(e)


if __name__ == "__main__":
    main()