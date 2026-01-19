class NERFilter:
    """
    A guardrail that uses Named Entity Recognition (NER) to find and redact PII.
    This mock implementation uses a keyword-based dictionary to simulate NER
    for demonstration purposes, avoiding the need for heavy models like Spacy/BERT.
    """
    def __init__(self):
        # Mock "Knowledge Base" of entities
        self.entities = {
            "John Doe": "PERSON",
            "Jane Smith": "PERSON",
            "Google": "ORG",
            "OpenAI": "ORG",
            "New York": "LOC",
            "Paris": "LOC",
            "Alice": "PERSON",
            "Bob": "PERSON"
        }

    def detect(self, text: str) -> list:
        """
        Scans text for known entities.
        Returns a list of dicts: {'text': 'John Doe', 'label': 'PERSON', 'start': 0, 'end': 8}
        """
        found = []
        for entity_text, label in self.entities.items():
            # Check if entity is in text (case sensitive for "NER" feel)
            # A real NER model would use context, not just string matching.
            if entity_text in text:
                start_idx = text.find(entity_text)
                while start_idx != -1:
                    found.append({
                        "text": entity_text,
                        "label": label,
                        "start": start_idx,
                        "end": start_idx + len(entity_text)
                    })
                    # Find next occurrence
                    start_idx = text.find(entity_text, start_idx + 1)
        
        # Sort by start position to handle overlaps nicely (simple greedy approach)
        found.sort(key=lambda x: x['start'])
        return found

    def redact(self, text: str) -> str:
        """
        Replaces detected entities with [LABEL].
        """
        entities = self.detect(text)
        
        # Process from end to start to avoid messing up indices
        entities.sort(key=lambda x: x['start'], reverse=True)
        
        redacted_text = text
        for ent in entities:
             replacement = f"[{ent['label']}]"
             start = ent['start']
             end = ent['end']
             # Simple string slice replacement
             redacted_text = redacted_text[:start] + replacement + redacted_text[end:]
             
        return redacted_text
