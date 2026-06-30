from app.workflow import EstimationWorkflow
import json

workflow = EstimationWorkflow()

image_urls = [
    "https://example.com/images/pre-repair-image/1000328248.jpg",
    "https://example.com/images/pre-repair-image/1000328249.jpg",
    "https://example.com/images/pre-repair-image/1000328255.jpg",
    "https://example.com/images/pre-repair-image/1000328250.jpg",
    "https://example.com/images/pre-repair-image/1000328257.jpg",
    "https://example.com/images/pre-repair-image/1000328256.jpg",
]

available_spares = [
    "Display Replacement",
    "Battery Replacement",
    "Motherboard Replacement",
    "Charging Connector",
    "Back Camera",
    "Front Camera",
    "Rear Cover",
    "Battery Cover",
    "Back Housing",
    "Camera replacement",
    "Camera Glass",
    "PBA",
    "Sub PBA",
    "USB Subboard",
    "Fingerprint sensor",
    "Speaker",
]
prediction = workflow.run(
    image_urls=image_urls,
    available_spares=available_spares,
)

print("=" * 80)
print("AI Prediction")
print("=" * 80)

print(json.dumps(prediction.model_dump(), indent=4))