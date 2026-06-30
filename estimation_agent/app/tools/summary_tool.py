"""
Summary Tool

Cleans and normalizes the AI prediction before it is
returned to Django.
"""

from  estimation_agent.app.models.prediction import EstimationPrediction


class SummaryTool:

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Remove extra whitespace and normalize text.
        """

        if not text:
            return ""

        return " ".join(text.strip().split())


    def process(
        self,
        prediction: EstimationPrediction
    ) -> EstimationPrediction:

        prediction.engineer_observation = self.clean_text(
            prediction.engineer_observation
        )

        prediction.repair_summary = self.clean_text(
            prediction.repair_summary
        )

        prediction.cause_of_damage = self.clean_text(
            prediction.cause_of_damage
        )

        return prediction