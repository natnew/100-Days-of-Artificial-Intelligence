from datetime import datetime

class ModelCard:
    """
    A unified data structure for Model Cards, supporting markdown export.
    """
    def __init__(self, name: str, version: str = "1.0"):
        self.meta = {
            "name": name,
            "version": version,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.intended_use = []
        self.limitations = []
        self.metrics = {}
        self.ethical_considerations = []

    def set_intended_use(self, usage: str):
        self.intended_use.append(usage)

    def add_limitation(self, limitation: str):
        self.limitations.append(limitation)

    def add_metric(self, name: str, value):
        self.metrics[name] = value

    def add_ethical_consideration(self, note: str):
        self.ethical_considerations.append(note)

    def validate(self) -> bool:
        """
        Checks if critical fields are populated.
        Returns True if valid, raises ValueError if missing critical info.
        """
        errors = []
        if not self.intended_use:
            errors.append("Missing Intended Use")
        if not self.limitations:
            errors.append("Missing Limitations")
        
        if errors:
            raise ValueError(f"Model Card Validation Failed: {', '.join(errors)}")
        return True

    def to_markdown(self) -> str:
        """
        Renders the Model Card as a Markdown string.
        """
        if not self.limitations: 
             # Safety warning in the card itself if not validated
             warn = "> [!WARNING]\n> This model card is incomplete.\n\n"
        else:
            warn = ""

        md = f"# Model Card: {self.meta['name']}\n\n"
        md += f"**Version**: {self.meta['version']}  \n"
        md += f"**Date**: {self.meta['date']}  \n\n"
        
        md += warn
        
        md += "## Intended Use\n"
        for use in self.intended_use:
            md += f"- {use}\n"
        md += "\n"
        
        md += "## Performance Metrics\n"
        if self.metrics:
            md += "| Metric | Value | \n|---|---|\n"
            for k, v in self.metrics.items():
                md += f"| {k} | {v} |\n"
        else:
            md += "*No metrics provided.*\n"
        md += "\n"
        
        md += "## Limitations & Risks\n"
        for lim in self.limitations:
            md += f"- {lim}\n"
        md += "\n"
        
        md += "## Ethical Considerations\n"
        for eth in self.ethical_considerations:
            md += f"- {eth}\n"
            
        return md
