import spacy
import re
import nltk
from nltk.corpus import stopwords

class TextPreprocessor:
    def __init__(self, model="en_core_web_sm"):
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"WARNING: Spacy model '{model}' not found. Falling back to blank 'en' model.")
            print(f"To fix: Run 'python -m spacy download {model}'")
            self.nlp = spacy.blank("en")
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except LookupError:
             nltk.download('stopwords', quiet=True)
             self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text: str) -> str:
        # Basic cleaning
        text = text.lower()
        text = re.sub(r'http\S+', '', text)  # remove urls
        text = re.sub(r'\s+', ' ', text)     # remove extra whitespace
        # Punctuation removal: allow +, #, and . for tech skills (C++, C#, Node.js)
        # We replace other punctuation with space to avoid merging words
        text = re.sub(r'[^\w\s\+\#\.]', ' ', text)  
        return text.strip()

    def tokenize_and_lemmatize(self, text: str) -> str:
        # Process with Spacy (limit length if needed, but resumes are usually short enough)
        doc = self.nlp(text[:1000000]) 
        # Fallback to token.text if lemma_ is missing (blank model)
        tokens = [token.lemma_ if token.lemma_ else token.text for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
        return " ".join(tokens)
    
    def extract_entities(self, text: str):
        # Basic NER from SpaCy
        doc = self.nlp(text[:1000000])
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)
        return entities
