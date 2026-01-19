class ContextOverflowGenerator:
    """
    Generates 'Needle in a Haystack' attack prompts.
    """
    def __init__(self, filler_text: str = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "):
        self.filler_text = filler_text

    def generate_haystack(self, needle: str, length_tokens: int = 1000, position: str = "middle") -> str:
        """
        Creates a large context with a hidden directive (needle).
        position: 'start', 'middle', 'end'
        """
        # Crude token approximation (1 word = 1 token for mock)
        words_needed = length_tokens
        filler_words = self.filler_text.split()
        
        # Repeat filler to match length
        generated_filler = []
        while len(generated_filler) < words_needed:
            generated_filler.extend(filler_words)
        
        # Trim to exact length
        generated_filler = generated_filler[:words_needed]
        
        # Insert needle
        if position == "start":
            final_text = needle + " " + " ".join(generated_filler)
        elif position == "end":
            final_text = " ".join(generated_filler) + " " + needle
        else: # middle
            mid_point = len(generated_filler) // 2
            final_text = " ".join(generated_filler[:mid_point]) + " " + needle + " " + " ".join(generated_filler[mid_point:])
            
        return final_text
