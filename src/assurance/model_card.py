
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import datetime

@dataclass
class ModelDetails:
    name: str
    version: str
    date: str = field(default_factory=lambda: datetime.date.today().isoformat())
    description: str = ""
    license: str = ""
    developers: List[str] = field(default_factory=list)

@dataclass
class IntendedUse:
    primary_uses: List[str] = field(default_factory=list)
    primary_users: List[str] = field(default_factory=list)
    out_of_scope_uses: List[str] = field(default_factory=list)

@dataclass
class Metric:
    name: str
    value: float
    description: str = ""
    confidence_interval: Optional[str] = None

@dataclass
class QuantitativeAnalysis:
    performance_metrics: List[Metric] = field(default_factory=list)
    graphics: List[str] = field(default_factory=list) # paths to images

@dataclass
class EthicalConsiderations:
    risks: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)

@dataclass
class ModelCard:
    model_details: ModelDetails
    intended_use: IntendedUse
    metrics: List[Metric] = field(default_factory=list)
    ethical_considerations: EthicalConsiderations = field(default_factory=lambda: EthicalConsiderations())
    caveats_and_recommendations: str = ""

class ModelCardGenerator:
    """
    Generates a Markdown representation of a ModelCard.
    """
    @staticmethod
    def generate_markdown(card: ModelCard) -> str:
        md = []
        
        # Header
        md.append(f"# Model Card: {card.model_details.name}")
        md.append(f"**Version**: {card.model_details.version} | **Date**: {card.model_details.date}")
        if card.model_details.developers:
            md.append(f"**Developers**: {', '.join(card.model_details.developers)}")
        if card.model_details.license:
            md.append(f"**License**: {card.model_details.license}")
        md.append("")
        md.append(f"{card.model_details.description}")
        md.append("")

        # Intended Use
        md.append("## Intended Use")
        if card.intended_use.primary_uses:
            md.append("### Primary Uses")
            for use in card.intended_use.primary_uses:
                md.append(f"- {use}")
        if card.intended_use.out_of_scope_uses:
            md.append("### Out-of-Scope Use Cases")
            for use in card.intended_use.out_of_scope_uses:
                md.append(f"- {use}")
        md.append("")

        # Metrics
        md.append("## Quantitative Analysis")
        md.append("| Metric | Value | Description |")
        md.append("| --- | --- | --- |")
        for m in card.metrics:
            md.append(f"| {m.name} | {m.value} | {m.description} |")
        md.append("")

        # Ethics
        md.append("## Ethical Considerations")
        if card.ethical_considerations.risks:
            md.append("### Risks")
            for risk in card.ethical_considerations.risks:
                md.append(f"- {risk}")
        
        if card.ethical_considerations.mitigations:
            md.append("### Mitigations")
            for mitigation in card.ethical_considerations.mitigations:
                md.append(f"- {mitigation}")
        md.append("")

        # Caveats
        md.append("## Caveats and Recommendations")
        md.append(card.caveats_and_recommendations)

        return "\n".join(md)
