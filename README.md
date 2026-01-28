# Resume Screening System

An AI-powered system to streamline recruitment by screening and ranking resumes against job descriptions.

## Structure
- `src/ingestion.py`: Handles PDF/DOCX parsing.
- `src/preprocessing.py`: NLP with SpaCy (NER, Lemmatization).
- `src/scoring.py`: TF-IDF and Cosine Similarity.
- `src/orchestrator.py`: The Main Controller (Orchestration Layer).
- `main.py`: CLI entry point.
- `app.py`: Streamlit Dashboard.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI (Command Line Interface)

### Web Dashboard
Launch the visual interface to upload new resumes:
```bash
streamlit run app.py
```

## Features (Phase 1 MVP)
- **Multi-Format Parsing**: Supports PDF and text extraction.
- **NLP Engine**: automated tokenization and extensive cleaning.
- **Scoring Logic**: TF-IDF Vectorization & Cosine Similarity ranking.
- **Workflow Orchestration**: State-managed processing pipeline.
