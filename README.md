# 🤖 AI Damage Estimation Agent

As device repair operations continue to scale, manual damage assessment and repair estimation become increasingly time-consuming. This project was initiated to explore how Artificial Intelligence could streamline the repair estimation workflow while integrating seamlessly into existing operational processes.

To address this challenge, I designed and implemented the foundational AI damage estimation agent for my company's internal after-sales operations portal. The project established the initial AI capability for repair estimation by introducing an intelligent workflow that supports two estimation paths.

For image-based estimation, the agent analyzes technician-uploaded pre-repair device images to identify visible external damages, predicts the required spare parts, generates technician-friendly repair summaries, and produces structured outputs that automatically populate the repair estimation workflow.

For brand estimation, the agent processes brand-issued estimate documents (PDFs or images), extracts structured repair information—including spare parts, quantities, pricing, labour charges, and other relevant details—and converts the extracted data into a standardized format for seamless integration with the existing workflow.

Rather than serving as a standalone AI demonstration, this repository showcases the core implementation and architectural foundation of the solution. It focuses on the engineering approach used to build the agent, orchestrate AI workflows, integrate asynchronous processing into an existing Django application, and validate AI-generated predictions before they are consumed by the user interface. While the production implementation continues to evolve, this repository represents the foundational design and implementation that enabled AI-assisted repair estimation within the platform.

The solution combines multimodal AI, cloud-native infrastructure, and asynchronous processing to build a scalable and maintainable workflow. Google Agent Development Kit (ADK) orchestrates the agent workflow, Vertex AI (Gemini) coordinates task execution, Azure OpenAI GPT-4o Vision performs damage analysis and document understanding, Celery and Azure Cache for Redis manage asynchronous background processing, Azure Blob Storage stores uploaded assets, and Docker with Azure Kubernetes Service (AKS) provides containerized deployment.

This repository showcases the **architecture**, **AI workflow**, and **engineering approach** behind the solution. **Company-specific details have been generalized** while preserving the overall technical design.
---

## 💼 Project Context & Goal

Repair estimation is a critical step in the device service lifecycle, directly influencing repair planning, spare part selection, and service turnaround time. Traditionally, this process relies on manual inspection of device images and supporting documents, making it time-consuming and requiring technicians to perform repetitive analysis before creating an estimation.

The goal of this project was to establish the foundation for AI-assisted repair estimation by introducing an intelligent workflow into my company's internal after-sales operations portal. Rather than replacing the existing process, the solution was designed to enhance it by assisting technicians with faster and more structured damage assessment.

The AI agent supports two complementary repair estimation workflows.

For **image-based estimation**, technicians upload multiple pre-repair device images. The agent analyzes the visible condition of the device, detects external damages such as cracked displays, damaged back panels, broken camera lenses, frame damage, or other observable issues, predicts the required spare parts, generates technician-friendly repair summaries, and returns structured outputs that automatically populate the repair estimation workflow.

For **brand estimation**, technicians upload a brand-issued estimate document (PDF or image). Instead of performing visual damage analysis, the agent extracts structured repair information—including spare parts, quantities, pricing, labour charges, customer complaints, remarks, and other relevant details—and converts it into a standardized format for seamless integration with the existing workflow.

Building this solution required more than integrating a single vision model. It involved designing a multi-step AI agent, orchestrating multimodal AI services, integrating asynchronous processing into an existing Django application, validating AI-generated predictions against business rules, and producing structured outputs reliable enough to integrate directly with the repair estimation interface without disrupting the existing workflow.

---

## ✨ Key Features

- **AI-powered damage analysis** from technician-uploaded pre-repair device images using multimodal vision models
- **Brand estimate document understanding** with intelligent extraction of structured repair information from scanned images and PDF documents
- **Spare part prediction** with validation and fuzzy matching against the existing inventory database
- **Technician-friendly repair summaries** generated from AI-detected damages and observations
- **Structured JSON responses** designed for seamless integration with existing repair estimation workflows and automatic UI population
- **Confidence scoring** for AI predictions to improve transparency and assist technician review
- **Asynchronous AI processing** using Celery and Redis, ensuring uploads and estimation requests never block the user interface
- **Cloud-native architecture** built with Docker, Kubernetes, Azure Blob Storage, and managed Redis for scalable production deployment
- **Modular AI agent design** enabling future enhancements, additional AI tools, and workflow expansion without disrupting the existing application

---
## 🧠 Technical Highlights

This project demonstrates the design and implementation of a production-oriented AI workflow by combining multimodal AI, cloud-native infrastructure, and asynchronous backend processing within an existing Django application.

- **Agentic AI Workflow** — Designed a multi-step AI agent using Google Agent Development Kit (ADK) to orchestrate damage analysis, document understanding, validation, summarization, and structured response generation.

- **Multimodal AI Integration** — Combined Vertex AI (Gemini) for workflow orchestration with Azure OpenAI GPT-4o Vision for device image analysis and intelligent document understanding.

- **Prompt Engineering & Structured Outputs** — Developed system prompts with strict JSON-based response contracts, enabling reliable downstream processing and seamless integration with application workflows.

- **Asynchronous Processing Architecture** — Implemented Celery and Azure Cache for Redis to execute AI workloads in the background, ensuring responsive user interactions and scalable request handling.

- **Data Validation & Business Rule Enforcement** — Built validation layers using Pydantic models, inventory-aware spare part mapping, fuzzy matching, and response normalization to convert AI-generated predictions into structured application data.

- **Production Integration** — Embedded the AI agent into an existing Django-based after-sales operations platform, integrating with established workflows without requiring major architectural changes or a separate deployment.

- **Cloud-Native Deployment** — Containerized the application using Docker and deployed it on Azure Kubernetes Service (AKS), leveraging Azure Blob Storage, Azure Cache for Redis, and Azure Container Registry (ACR) for scalable cloud infrastructure.

- **Scalable & Modular Architecture** — Designed the solution as a modular AI component, making it easy to extend with additional AI tools, workflows, validation layers, and future business capabilities.

---

## 🏗️ System Architecture

```text
Internal Operations Portal (Django)
        │
        ▼
Technician Uploads Device Images / Brand Document
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
        ├── Azure OpenAI GPT-4o / GPT-4o Vision — Brand Document OCR
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

### End-to-End Workflow

```text
                               Technician
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
         Manual Entry        AI Image Estimation    Brand Estimation
                │                   │                   │
                │                   │                   │
         ManualWorkflow()   generate_ai_estimation()  extract_brand_details()
                │                   │                   │
                │                   │                   │
                ▼                   ▼                   ▼
          Technician        Upload Images         Upload Brand Document
                                 │                      │
                                 ▼                      ▼
                     Azure Blob Storage         Azure Blob Storage
                                 │                      │
                                 ▼                      ▼
                  Celery Queue (Redis)       Celery Queue (Redis)
                                 │                      │
                                 ▼                      ▼
                     EstimationWorkflow()   BrandEstimationWorkflow()
                                 │                      │
                                 ▼                      ▼
                         VisionTool()          BrandOCRTool()
                                 │                      │
                                 ▼                      ▼
                   Azure OpenAI GPT-4o Vision   Azure OpenAI GPT-4o
                                 │                      │
                                 ▼                      ▼
                     AI Damage Prediction     Brand Document Extraction
                                 │                      │
                                 ▼                      ▼
                        SpareMapper()        Price / Data Cleanup
                                 │                      │
                                 ▼                      ▼
                     ValidationTool()      BrandEstimationPrediction
                                 │                      │
                                 ▼                      ▼
                       SummaryTool()        Structured JSON
                                 │                      │
                                 ▼                      ▼
                    ConfidenceTool()        Django Response
                                 │
                                 ▼
                    EstimationPrediction
                                 │
                                 ▼
                    Django JSON Response
                                 │
                                 ▼
               ERP Auto-Fills Estimation Screen
```

The agent runs as a module inside the same application — it's not a separately deployed service.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Agent Framework | Google Agent Development Kit (Google ADK), Google Agents CLI |
| LLM Orchestration | Vertex AI, Gemini 2.5 Flash |
| Vision AI | Azure OpenAI GPT-4o Vision |
| Document OCR | Azure OpenAI GPT-4o / GPT-4o Vision, pypdf |
| Backend | Python, Django, Django REST Framework |
| Storage | Azure Blob Storage |
| Background Processing | Celery |
| Task Coordination | Azure Cache for Redis (managed) |
| Deployment | Docker, Azure Kubernetes Service (AKS), Azure Container Registry (ACR) |

---

## ⚙️ Solution Workflow

### Image Estimation

1. A technician uploads device images, creating a repair request.
2. Images are validated, compressed, and stored in Azure Blob Storage.
3. Celery queues the processing job; Redis coordinates task execution.
4. The Google ADK agent is invoked, with Gemini 2.5 Flash orchestrating the workflow.
5. A vision tool sends images to Azure OpenAI GPT-4o Vision for damage analysis.
6. The agent detects visible damages and predicts required spare parts.
7. Predictions are validated against available inventory data.
8. The agent generates a confidence score, a repair summary, and a cost estimate.
9. A structured JSON response is returned and used to auto-fill the estimation screen.

### Brand Estimation

1. A technician uploads a brand-issued estimate document (PDF or image) instead of device images.
2. The document is validated and stored in Azure Blob Storage.
3. Celery queues the processing job; Redis coordinates task execution, same as the image pipeline.
4. The `BrandOCRTool` decides the extraction path:
   - **PDF with selectable text** → `pypdf` extracts the raw text, sent to Azure OpenAI GPT-4o as plain text.
   - **Image or scanned PDF with no extractable text** → the document is sent to Azure OpenAI GPT-4o Vision.
5. A detailed system prompt instructs the model to extract brand, customer complaint, remarks, a full spare parts table (name, part code, qty, unit price, total), and labour, returned strictly as JSON.
6. Prices are cleaned (e.g. `₹8,499.00` → `8499.0`) and validated into structured `BrandSpareItem` rows.
7. A structured `BrandEstimationPrediction` JSON response is returned and used to auto-fill the brand estimate fields.

### Why Background Processing

Image uploads and AI inference can take several seconds, and the UI shouldn't hang while that happens. Celery processes this asynchronously, with Redis coordinating things so AI processing only kicks off once all required images (or the brand document) are uploaded. This keeps the app responsive and makes the pipeline easy to scale horizontally.

---

## 🚀 Deployment

```text
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

The agent isn't deployed as a separate microservice — it's packaged into the same Django application, running in the web pod. The Celery worker runs in its own pod so AI processing doesn't compete with web traffic, and task coordination uses a managed Redis service rather than a Redis pod inside the cluster. Images and other container artifacts are built and stored in Azure Container Registry (ACR) and deployed on Azure Kubernetes Service (AKS).

---

## 🔌 API

### `POST /estimate`

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

### `POST /extract-brand-estimate`

**Input**

```json
{
  "document": "brand_estimate_url_or_file"
}
```

**Response**

```json
{
  "brand": "Oppo",
  "customer_complaint": "string",
  "remarks": "string",
  "spares": [
    {
      "name": "Display Assembly",
      "part_code": "5437870",
      "qty": 1,
      "unit_price": 9000.0,
      "total": 9000.0
    }
  ],
  "labour": 250.0,
  "confidence_score": 0.98,
  "document_type": "Estimate Receipt",
  "extraction_time": 1.42,
  "ai_model": "GPT-4o",
  "status": "success"
}
```

---

## 📄 Sample Input / Output

Below is a sanitized example based on an actual run.

**Input:** 6 pre-repair device images uploaded and stored via the background upload pipeline.

```text
image_1.jpg
image_2.jpg
image_3.jpg
image_4.jpg
image_5.jpg
image_6.jpg
```

**Output:** structured prediction returned by the agent.

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

Each predicted spare part name is fuzzy-matched against the available spares list (e.g. `Display Replacement` → 100% match) before returning the final response, so the output maps directly to real inventory items rather than free-text guesses.

---
## 🧱 Structured AI Responses

The AI agent returns schema-validated JSON responses rather than free-form text, allowing the output to integrate directly with the repair estimation workflow.

Before populating the user interface, every prediction is validated, normalized, and mapped to the application's business schema. This includes:

- Device damage predictions
- Predicted spare parts
- Technician-friendly repair summaries
- Brand estimation document data
- Confidence scores
- Validation metadata

Using structured response contracts ensures reliable downstream processing and seamless integration with the existing Django application.
```

---

## 📁 Project Structure

```text
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
│       ├── brand_ocr_tool.py
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

## 🧑‍💻 My Responsibilities

I was responsible for designing and implementing the foundational AI damage estimation solution from end to end. My work included designing the AI agent workflow, developing prompt engineering strategies for both vision-based damage analysis and brand document understanding, integrating the solution into the existing Django application, implementing asynchronous processing with Celery and Redis, designing structured data models and validation layers, and deploying the solution within the existing Azure Kubernetes Service (AKS) infrastructure.

The objective was not simply to integrate an LLM into an application, but to build a reliable AI-assisted workflow capable of producing structured, validated outputs that could be consumed directly by the repair estimation interface while fitting seamlessly into the existing production architecture.

---

## 📚 Engineering Learnings

Building this project provided practical experience in designing and integrating AI systems into an existing production application. Some of the key engineering takeaways include:

- Designing AI agents that generate structured, schema-validated outputs suitable for direct application integration rather than relying on unstructured natural language responses.
- Understanding the practical differences between multimodal image analysis and intelligent document understanding, and selecting the appropriate processing pipeline based on document type.
- Building asynchronous AI workflows using Celery and Redis to prevent long-running AI inference from impacting user experience.
- Validating and normalizing AI-generated predictions through business rules, Pydantic models, and inventory-aware spare part mapping before exposing results to end users.
- Designing modular AI components that can be extended with additional tools, workflows, and business capabilities without requiring major architectural changes.
- Integrating modern AI capabilities into an existing enterprise application while maintaining scalability, reliability, and compatibility with established operational workflows.

---

## 🛣️ Future Enhancements

The current implementation establishes the foundation for AI-assisted repair estimation. Future enhancements may include:

- Human-in-the-loop review and approval workflows for AI-generated repair estimates.
- Enhanced spare part validation and inventory synchronization across all estimation pipelines.
- Retrieval-Augmented Generation (RAG) using repair manuals, service documentation, and historical repair knowledge.
- Multi-agent workflows for specialized tasks such as damage analysis, document understanding, pricing, and quality assurance.
- Model evaluation and continuous improvement using technician feedback and production telemetry.
- Enterprise integrations through Model Context Protocol (MCP) and additional operational systems.
- Support for additional device categories and repair workflows.
- Advanced analytics and operational dashboards for AI-assisted repair insights and performance monitoring.
---

## 🎯 Project Outcome

This project established the initial AI foundation for repair estimation within the existing after-sales operations platform. By integrating multimodal AI directly into the repair workflow, the solution demonstrates how AI can assist technicians by reducing manual effort, accelerating estimation workflows, and producing structured outputs that integrate seamlessly with existing business processes.

Beyond the implementation itself, the project serves as a reference architecture for embedding AI capabilities into enterprise applications using modern cloud-native infrastructure, asynchronous processing, and modular agent design.

## License

This project is licensed under the MIT License.
