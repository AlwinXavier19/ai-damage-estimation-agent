# 🤖 AI Damage Estimation Agent

**An AI agent I built to automate device damage assessment and repair estimation, built into our internal operations portal.**

This project analyzes pre-repair device images, detects visible damages, predicts required spare parts, generates repair summaries, estimates repair costs, and returns a structured JSON response. It runs as part of our internal operations portal rather than as a separately deployed service — packaged into the same application and deployed together on Kubernetes.

## How I Integrated It

I built this into our internal operations portal. When a technician creates a repair request and uploads device images through the portal, the upload-and-predict flow kicks off the estimation pipeline in the background (via Celery/Redis) instead of blocking the request. Once the agent returns its structured prediction, the portal automatically populates the repair estimation screen with the detected damages, predicted spare parts, summary, cost estimate, and confidence score.

---

## ✨ Features

- AI-powered damage detection from device images
- Spare part prediction
- Repair summary generation
- Repair cost estimation
- Confidence scoring on predictions
- Inventory-aware spare part validation
- Structured JSON output for easy downstream integration
- Asynchronous background processing for scalability
- Containerized, cloud-native deployment

---

## 🏗️ Architecture

This is how the agent fits into our internal operations portal:

```
Internal Operations Portal (Django)
        │
        ▼
Technician Uploads Device Images
        │
        ▼
Azure Blob Storage
        │
        ▼
Celery Background Processing
        │
        ▼
AI Damage Estimation Agent (Google ADK)
        │
        ├── Vertex AI (Gemini) — Orchestration
        ├── Azure OpenAI GPT-4o Vision — Damage Analysis
        ├── Spare Part Prediction
        ├── Inventory Validation
        ├── Confidence Scoring
        └── Repair Cost Estimation
        │
        ▼
Structured JSON Response
        │
        ▼
Portal Auto-Fills Repair Estimation Screen
```

The agent runs as a module inside the same application — it's not a separately deployed service.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Agent Framework | Google Agent Development Kit (Google ADK), Google Agents CLI |
| LLM Orchestration | Vertex AI, Gemini 2.5 Flash |
| Vision AI | Azure OpenAI GPT-4o Vision |
| Backend | Python, Django, Django REST Framework |
| Storage | Azure Blob Storage |
| Background Processing | Celery |
| Task Coordination | Azure Cache for Redis (managed) |
| Deployment | Docker, Azure Kubernetes Service (AKS), Azure Container Registry (ACR) |

---

## ⚙️ How It Works

1. A technician uploads device images through our internal operations portal, creating a repair request.
2. Images are validated, compressed, and stored in Azure Blob Storage.
3. Celery queues the processing job; Redis coordinates task execution.
4. The Google ADK agent is invoked, with Gemini 2.5 Flash orchestrating the workflow.
5. A vision tool sends images to Azure OpenAI GPT-4o Vision for damage analysis.
6. The agent detects visible damages and predicts required spare parts.
7. Predictions are validated against available inventory data.
8. The agent generates a confidence score, a repair summary, and a cost estimate.
9. A structured JSON response is returned, and the portal auto-fills the repair estimation screen.

### Why I Used Background Processing

Image uploads and AI inference can take several seconds, and I didn't want the portal request to hang while that happened. I used Celery to process this asynchronously, with Redis coordinating things so AI processing only kicks off once all required images are uploaded. This keeps the portal responsive and makes the whole pipeline easier to scale.

---

## 🚀 Deployment

```
Azure Container Registry (ACR)
        │
        ▼
Azure Kubernetes Service (AKS)
        │
        ├── Portal Pod (Django + AI Agent)
        │       ├── Google ADK Runtime
        │       ├── Vertex AI (Gemini)
        │       └── Azure OpenAI GPT-4o Vision
        │
        └── Celery Worker Pod
        │
        ▼
Azure Cache for Redis (managed)
        │
        ▼
Azure Blob Storage
```

The agent isn't deployed as a separate microservice — it's part of the same Django application as the internal operations portal, so it runs in the portal's pod. Images and other container artifacts are built and stored in Azure Container Registry (ACR) and deployed on Azure Kubernetes Service (AKS). The Celery worker runs in its own pod (so AI processing doesn't compete with the portal's web traffic), and task coordination uses Azure Cache for Redis as a managed service rather than a Redis pod inside the cluster.

---

## 🔌 API

This is exposed as an internal endpoint within the operations portal (not a separately hosted service):

**POST** `/estimate`

**Input**
```json
{
  "images": ["url_1", "url_2", "url_3", "url_4", "url_5", "url_6"]
}
```

**Response**
```json
{
  "damages": [...],
  "spare_parts": [...],
  "summary": "string",
  "estimated_cost": 0,
  "confidence_score": 0.0
}
```

---

## 📄 Sample Input / Output

Below is a sanitized example based on an actual run.

**Input:** 6 pre-repair device images uploaded and stored via the background upload pipeline.

```
image_1.jpg
image_2.jpg
image_3.jpg
image_4.jpg
image_5.jpg
image_6.jpg
```

**Output:** structured prediction returned by the agent and cached for the portal to consume.

```json
{
  "engineer_observation": "The device has visible damage to the front screen, back camera lens, and internal components.",
  "repair_summary": "The device requires replacement of the front screen, back camera lens, and inspection of internal components for further damage.",
  "cause_of_damage": "The damages appear to be caused by physical impact, likely due to dropping the device.",
  "damages": [
    {
      "damage": "Cracked front screen",
      "location": "Front panel",
      "confidence": 0.95
    },
    {
      "damage": "Cracked back camera lens",
      "location": "Back panel",
      "confidence": 0.95
    },
    {
      "damage": "Potential damage to internal components",
      "location": "Internal hardware",
      "confidence": 0.85
    }
  ],
  "spares": [
    {
      "name": "Display Replacement",
      "qty": 1,
      "confidence": 0.95
    },
    {
      "name": "Back Camera Lens",
      "qty": 1,
      "confidence": 0.95
    }
  ],
  "overall_confidence": 0.95
}
```

The agent matches each predicted spare part name against the available spares list (fuzzy-matched, e.g. `Display Replacement` → 100% match) before returning the final response, so the output maps directly to real inventory items rather than free-text guesses.

---

## 📁 Project Structure

```
estimation_agent/
│
├── .gitignore
├── agents-cli-manifest.yaml
├── Dockerfile
├── GEMINI.md
├── pyproject.toml
├── README.md
├── __init__.py
│
├── app/
│   │
│   ├── agent.py
│   ├── config.py
│   ├── fast_api_app.py
│   ├── prompts.py
│   ├── workflow.py
│   ├── __init__.py
│   │
│   ├── app_utils/
│   │   ├── telemetry.py
│   │   └── typing.py
│   │
│   ├── models/
│   │   └── prediction.py
│   │
│   ├── services/
│   │   ├── azure_openai.py
│   │   ├── blob_service.py
│   │   └── __init__.py
│   │
│   └── tools/
│       ├── analyze_damage_tool.py
│       ├── confidence_tool.py
│       ├── spare_mapper.py
│       ├── summary_tool.py
│       ├── validation_tool.py
│       ├── vision_tool.py
│       └── __init__.py
│
└── tests/
    │
    ├── eval/
    │   ├── eval_config.yaml
    │   │
    │   └── datasets/
    │       ├── basic-dataset.json
    │       └── README.md
    │
    ├── integration/
    │   ├── test_agent.py
    │   └── test_agent_runtime_app.py
    │
    └── unit/
        └── test_dummy.py
```

---

## 🔗 Integration Notes

This agent lives inside our internal operations portal — it isn't deployed or run as a separate service. It runs in the portal pod on AKS, while the Celery worker runs in its own pod so background AI processing doesn't impact the portal's web traffic. Task coordination uses Azure Cache for Redis (a managed Azure service, not a pod in the cluster). Everything is built and pushed through Azure Container Registry (ACR) and deployed on AKS. The modular structure under `estimation_agent/` keeps the agent code self-contained within the portal codebase, even though it's not deployed separately.

---

## 🛣️ Future Enhancements

Things I'm planning to add:

- Human-in-the-loop review and approval workflow
- MCP integration for enterprise tool connectivity
- Multi-agent collaboration
- RAG over repair manuals and service documentation
- Multi-device support
- Advanced analytics dashboard

---

## License

This project is licensed under the [MIT License](./LICENSE).
