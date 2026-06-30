"""
Validation Tool

Ensures AI only returns spare parts that exist
in the database.
"""

from  estimation_agent.app.models.prediction import EstimationPrediction


class ValidationTool:

    def __init__(self, available_spares: list[str]):
        self.available_spares = {
            spare.lower().strip()
            for spare in available_spares
        }

    def process(
        self,
        prediction: EstimationPrediction
    ) -> EstimationPrediction:

        valid_spares = []

        for spare in prediction.spares:

            if spare.name.lower().strip() in self.available_spares:
                valid_spares.append(spare)

        prediction.spares = valid_spares

        return prediction