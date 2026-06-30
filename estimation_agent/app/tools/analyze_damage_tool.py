from  estimation_agent.app.workflow import EstimationWorkflow


def analyze_damage(
    image_urls: list[str],
    available_spares: list[str],
):
    """
    Analyze six pre-repair images and return a structured estimation.
    """

    workflow = EstimationWorkflow()

    prediction = workflow.run(
        image_urls=image_urls,
        available_spares=available_spares,
    )

    return prediction.model_dump()