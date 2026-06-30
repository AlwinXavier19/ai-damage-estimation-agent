"""
Vision Tool

Receives Azure Blob image URLs and asks GPT-4o Vision
to analyze visible damages.
"""
from estimation_agent.app.prompts import build_prompt

from  estimation_agent.app.services.azure_openai import AzureOpenAIService
from  estimation_agent.app.models.prediction import EstimationPrediction


class VisionTool:

    def __init__(self):
        self.client = AzureOpenAIService()

    def analyze(self,  available_spares,image_urls: list[str]) -> EstimationPrediction:

        if not image_urls:
            raise ValueError("At least 1 image is required.")

        content = [
            {
                "type": "text",
                "text": (
                    f"Analyze these {len(image_urls)} pre-repair images and return only "
                    "the JSON specified in the system prompt."
                ),
            }
        ]

        # Add every image
        for url in image_urls:

            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": url
                    }
                }
            )

        messages = [
            {
              "role": "system",
              "content": build_prompt(
                  available_spares
              ),
          },
            {
                "role": "user",
                "content": content
            }
        ]

        response = self.client.chat_completion(messages)

        prediction = self.client.extract_json(response)

        return EstimationPrediction(**prediction)