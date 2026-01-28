from .ingestion import ResumeIngestor
from .preprocessing import TextPreprocessor
from .scoring import ResumeScorer
import os
from typing import List, Dict, Any

class ScreeningOrchestrator:
    """
    Orchestration Layer: Manages the workflow logic and state transitions between processing steps.
    """
    def __init__(self):
        self.ingestor = ResumeIngestor()
        self.preprocessor = TextPreprocessor()
        self.scorer = ResumeScorer()
        self.state = "IDLE"

    def run_screening_mission(self, jd_text: str, resume_dir: str) -> List[Dict[str, Any]]:
        self.state = "DISCOVERY"
        print(f"[{self.state}] Scanning {resume_dir} for resumes...")
        
        resume_paths = []
        for root, dirs, files in os.walk(resume_dir):
            for file in files:
                if file.lower().endswith(('.pdf', '.docx', '.txt')):
                    resume_paths.append(os.path.join(root, file))
        
        if not resume_paths:
            print("No resumes found.")
            return []

        self.state = "INGESTION_AND_PROCESSING"
        print(f"[{self.state}] Processing {len(resume_paths)} resumes...")
        
        processed_resumes = []
        valid_texts = []
        
        for path in resume_paths:
            try:
                # Ingestion
                raw_text = self.ingestor.extract_text(path)
                if not raw_text or not raw_text.strip():
                    print(f"Warning: Empty text for {os.path.basename(path)}")
                    continue
                
                # Preprocessing
                cleaned_text = self.preprocessor.clean_text(raw_text)
                final_text = self.preprocessor.tokenize_and_lemmatize(cleaned_text)
                
                if not final_text.strip():
                    print(f"Warning: No valid tokens for {os.path.basename(path)}")
                    continue

                # Store metadata
                processed_resumes.append({
                    "path": path,
                    "filename": os.path.basename(path),
                    "processed_text": final_text,
                    "raw_text_preview": raw_text[:100].replace('\n', ' ')
                })
                valid_texts.append(final_text)
            except Exception as e:
                print(f"Failed to process {path}: {e}")

        if not valid_texts:
            print("No valid text extracted from resumes.")
            return []

        self.state = "SCORING"
        print(f"[{self.state}] Calculating similarity...")
        
        # Process JD
        jd_clean = self.preprocessor.clean_text(jd_text)
        jd_final = self.preprocessor.tokenize_and_lemmatize(jd_clean)
        
        # Score
        scores = self.scorer.calculate_basic_similarity(jd_final, valid_texts)
        
        # Rank
        ranked_results = self.scorer.rank_resumes(processed_resumes, scores)
        self.state = "COMPLETED"
        
        return ranked_results
