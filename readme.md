# 🤖 Persona-Adaptive Customer Support Agent

A Gemini-powered AI Customer Support Agent that combines **Persona Classification**, **Retrieval-Augmented Generation (RAG)**, and **Human Escalation Workflows** to provide intelligent and context-aware customer support responses.

---

## 📌 Project Overview

This project classifies incoming customer queries into different personas, retrieves relevant knowledge from a local document repository using vector search, generates adaptive responses using Google's Gemini API, and escalates unresolved or sensitive issues to a human support specialist.

The system is built using:

- Google Gemini API
- ChromaDB Vector Database
- Streamlit
- Python

---

## 🚀 Features

### 1. Persona Classification

The system classifies users into one of the following personas:

#### Technical Expert

Users discussing:

- APIs
- Authentication
- Databases
- Debugging
- Deployments
- Configuration issues

#### Frustrated User

Users expressing:

- Frustration
- Anger
- Urgency
- Dissatisfaction

#### Business Executive

Users focused on:

- Business impact
- Revenue
- Customers
- Timelines
- Operations

---

### 2. Retrieval-Augmented Generation (RAG)

The application retrieves relevant information from a local knowledge base.

Supported document types:

- TXT
- MD
- PDF

Retrieved documents are converted into embeddings and stored in ChromaDB for semantic search.

---

### 3. Adaptive Response Generation

Responses are generated using:

- User Persona
- Retrieved Context
- Gemini LLM

This allows the system to tailor responses based on user needs.

---

### 4. Human Escalation Workflow

Sensitive or unresolved issues are automatically escalated.

Examples:

- Refund requests
- Billing disputes
- Legal complaints
- Low-confidence responses

The system generates a structured handoff JSON for support teams.

---

## 🏗️ Project Structure

```text
Persona_Classification/
│
├── app.py
│
├── data/
│   ├── api_troubleshooting.md
│   ├── billing_policy.txt
│   └── password_reset_guide.txt
│
├── src/
│   ├── classifier.py
│   ├── rag_pipeline.py
│   ├── generator.py
│   ├── escalator.py
│   └── config.py
│
├── chroma_db/
│
├── requirements.txt
│
├── .env
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd Persona_Classification
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## ▶️ Running the Application

Start Streamlit:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

## 📚 Knowledge Base Documents

Example documents:

### Password Reset Guide

Contains instructions for resetting passwords.

### API Troubleshooting Guide

Contains solutions for:

- 401 Unauthorized
- 500 Internal Server Error

### Billing Policy

Contains:

- Refund policy
- Billing dispute procedures
- Duplicate charge handling

---

## 🧪 Sample Test Queries

### Password Reset

```text
How do I reset my password?
```

Expected:

- RAG Retrieval
- Automatic Resolution

---

### Technical Expert

```text
Our API is returning 401 Unauthorized errors after updating authentication headers.
```

Expected:

- Technical Expert Persona
- API Troubleshooting Response

---

### Frustrated User

```text
I am extremely frustrated. Login has not worked for hours and I need this fixed immediately.
```

Expected:

- Frustrated User Persona
- Escalation Triggered

---

### Business Executive

```text
What is the business impact of the authentication outage and how quickly can it be resolved?
```

Expected:

- Business Executive Persona
- Executive-Level Response

---

### Billing Escalation

```text
I was charged twice and need a refund immediately.
```

Expected:

- Human Escalation
- Handoff JSON Generated

---

## 🔄 Workflow

```text
User Query
     │
     ▼
Persona Classification
     │
     ▼
RAG Retrieval (ChromaDB)
     │
     ▼
Adaptive Response Generation
     │
     ▼
Confidence Evaluation
     │
 ┌───┴───┐
 │       │
 ▼       ▼
Resolved  Escalated
 │       │
 ▼       ▼
Response  Human Handoff JSON
```

---

## 🛠️ Technologies Used

- Python 3.11+
- Streamlit
- Google Gemini API
- ChromaDB
- PyPDF
- LangChain Text Splitters
- dotenv

---

## 📈 Future Enhancements

- Multi-turn conversation memory
- Sentiment analysis
- Admin dashboard
- Ticket generation system
- Support analytics
- Multi-language support

---

## 👨‍💻 Author

Harshal Payghan

AI-Powered Persona Adaptive Customer Support Agent using Gemini + RAG + ChromaDB.
