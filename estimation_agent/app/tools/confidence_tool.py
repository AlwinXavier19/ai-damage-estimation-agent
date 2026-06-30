"""
Confidence Tool

Filters low-confidence AI predictions before they are
returned to Django.
"""

from  estimation_agent.app.models.prediction import EstimationPrediction


class ConfidenceTool:

    def __init__(
        self,
        spare_threshold: float = 0.80,
        damage_threshold: float = 0.75,
        overall_threshold: float = 0.70,
    ):
        self.spare_threshold = spare_threshold
        self.damage_threshold = damage_threshold
        self.overall_threshold = overall_threshold

    def process(
        self,
        prediction: EstimationPrediction,
    ) -> EstimationPrediction:

        # Filter spare parts
        prediction.spares = [
            spare
            for spare in prediction.spares
            if spare.confidence is None
            or spare.confidence >= self.spare_threshold
        ]

        # Filter damages
        prediction.damages = [
            damage
            for damage in prediction.damages
            if damage.confidence is None
            or damage.confidence >= self.damage_threshold
        ]

        return prediction

    def is_prediction_reliable(
        self,
        prediction: EstimationPrediction,
    ) -> bool:

        if prediction.overall_confidence is None:
            return True

        return (
            prediction.overall_confidence
            >= self.overall_threshold
        )