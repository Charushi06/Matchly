import os
import argparse

from src.orchestrator import ScreeningOrchestrator

def main():
    parser = argparse.ArgumentParser(description="AI-Powered Resume Screening")
    parser.add_argument("--jd", help="Job Description text or path to file", default="")
    parser.add_argument("--dir", help="Directory containing resumes", default="./data/data/INFORMATION-TECHNOLOGY")
    parser.add_argument("--gui", action="store_true", help="Launch Streamlit GUI (Placeholder)")
    
    args = parser.parse_args()
    
    print("=== AI-Powered Resume Screening & Ranking System ===")
    
    jd_input = args.jd
    if not jd_input:
        print("Please enter the Job Description:")
        jd_input = input("> ") # interactive if not provided
        
    if os.path.isfile(jd_input):
        try:
            with open(jd_input, 'r', encoding='utf-8') as f:
                jd_text = f.read()
        except Exception:
            # Or try valid reading.
            jd_text = jd_input 
    else:
        jd_text = jd_input

    resume_target = args.dir
    # Handle relative paths check
    if not os.path.exists(resume_target):
        # Try full path if relative fails
        base_dir = os.path.dirname(os.path.abspath(__file__))
        proposed_path = os.path.join(base_dir, resume_target)
        if os.path.exists(proposed_path):
            resume_target = proposed_path
        else:
            print(f"Error: Directory {resume_target} does not exist.")
            # Fallback to current dir or ask user?
            resume_target = input("Enter valid resume directory path: ")
            
    if not os.path.exists(resume_target):
        print("Invalid directory. Exiting.")
        return

    orchestrator = ScreeningOrchestrator()
    results = orchestrator.run_screening_mission(jd_text, resume_target)
    
    print("\n=== RANKING RESULTS ===")
    print(f"{'Rank':<5} {'Score':<10} {'Filename':<50}")
    print("-" * 70)
    
    for i, res in enumerate(results[:20]): # Show top 20
        # Truncate filename if needed
        fname = (res['filename'][:47] + '..') if len(res['filename']) > 47 else res['filename']
        print(f"{i+1:<5} {res['score']:.4f}     {fname:<50}")
        
    # Option to save results
    save = input("\nSave results to CSV? (y/n): ")
    if save.lower().startswith('y'):
        import pandas as pd
        df = pd.DataFrame(results)
        # Drop heavy text columns for CSV
        df = df.drop(columns=['processed_text', 'raw_text_preview'], errors='ignore')
        df.to_csv("ranking_results.csv", index=False)
        print("Saved to ranking_results.csv")

if __name__ == "__main__":
    main()
