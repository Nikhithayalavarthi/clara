
# Clara AI Automation Pipeline

## Overview
This project is creating an automation workflow for transforming call recordings/transcripts into a structured AI voice agent configuration for Clara Answers.

The workflow involves processing demo calls for creating an initial agent configuration (v1) and onboarding calls for updating the agent configuration (v2).

The aim is to take raw and unstructured human conversations and turn them into structured operational rules and a deployable AI voice agent.

---

# Architecture

Pipeline Flow:

Audio/Transcript Input  
↓  
Speech Transcription (Vosk)  
↓  
Information Extraction  
↓  
Account Memo JSON  
↓  
Agent Prompt Generation  
↓  
Versioned Agent Config (v1 / v2)

---

# Project Structure
clara-ai-automation/
│
├── data/
│ ├── demo/ # demo call transcripts/audio
│ └── onboarding/ # onboarding transcripts
│
├── models/
│ └── vosk-model-small-en-us-0.15/
│
├── scripts/
│ ├── run_pipeline.py
│ ├── onboarding_pipeline.py
│ ├── extract.py
│ ├── generate_agent.py
│ └── transcribe_audio.py
│
├── outputs/
│ └── accounts/
│ └── <account_id>/
│ ├── v1/
│ └── v2/
│
└── README.md


---

# Features

- Processes **demo call transcripts or audio**
- Extracts operational business rules
- Generates structured **Account Memo JSON**
- Generates **AI Agent configuration**
- Supports **versioning (v1 → v2)**
- Handles **missing data safely**
- Works with **audio or transcript inputs**

---

# Installation

## 1. Clone Repository


git clone <your_repo_link>
cd clara-ai-automation


## 2. Create Virtual Environment


python -m venv venv
venv\Scripts\activate


## 3. Install Dependencies


pip install vosk
pip install soundfile


---

# Speech Model Setup

Download the Vosk model


---

# Running the Demo Pipeline

Place transcripts or audio files inside:


data/demo/


Run:


python -m scripts.run_pipeline


Outputs are generated in:


outputs/accounts/<account_id>/v1


---

# Running the Onboarding Update

Place onboarding transcripts in:


data/onboarding/


Run:


python -m scripts.onboarding_pipeline


Outputs are generated in:


outputs/accounts/<account_id>/v2


---

# Output Files

Each account produces:

### Account Memo


account_memo.json


Contains structured operational configuration.

### Agent Draft Spec


agent_draft_spec.json


Contains AI voice agent prompt and routing logic.

---

# Versioning

Demo calls create:


v1/


Onboarding updates create:


v2/


Changes between versions are recorded in a changelog.

---

# Supported Input Types


.txt → transcript
.wav → audio recording
.mp3 → audio recording
.m4a → audio recording


Audio is transcribed using **Vosk speech recognition**.

---

# Design Principles

- No hallucinated data
- Missing fields recorded as `questions_or_unknowns`
- Safe automation pipeline
- Structured agent configuration
- Reproducible workflow

---

# Future Improvements

- Improved speech recognition accuracy
- Automatic conflict resolution
- Dashboard for account monitoring
- Integration with Retell API

---

# Author

Lakshmi Nikhitha Yalavarthi