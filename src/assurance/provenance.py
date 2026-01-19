
import time
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class DataArtifact:
    id: str
    content: Any
    checksum: str
    timestamp: float = field(default_factory=time.time)

@dataclass
class TransformationStep:
    operation: str
    input_ids: List[str]
    output_id: str
    parameters: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)

class ProvenanceTracker:
    """
    Day 80: Data Provenance Tracker.
    Maintains a verifiable lineage of data artifacts and transformations 
    to ensure scientific reproducibility.
    """
    def __init__(self):
        self.artifacts: Dict[str, DataArtifact] = {}
        self.lineage: List[TransformationStep] = []

    def _calculate_checksum(self, data: Any) -> str:
        """Simple checksum for data integrity."""
        return hashlib.sha256(str(data).encode()).hexdigest()

    def register_raw_data(self, name: str, content: Any) -> str:
        """Initializes the lineage with a raw artifact."""
        artifact_id = f"raw_{name}_{int(time.time())}"
        checksum = self._calculate_checksum(content)
        self.artifacts[artifact_id] = DataArtifact(artifact_id, content, checksum)
        return artifact_id

    def apply_transform(self, op_name: str, input_ids: List[str], transform_fn: Any, params: Dict[str, Any]) -> str:
        """
        Applies a transformation, logs the step, and registers the output.
        """
        # Collect input data
        inputs = [self.artifacts[aid].content for aid in input_ids]
        
        # Execute transform
        output_content = transform_fn(*inputs, **params)
        
        # Register output
        output_id = f"out_{op_name}_{int(time.time())}_{len(self.lineage)}"
        checksum = self._calculate_checksum(output_content)
        self.artifacts[output_id] = DataArtifact(output_id, output_content, checksum)
        
        # Log lineage
        self.lineage.append(TransformationStep(
            operation=op_name,
            input_ids=input_ids,
            output_id=output_id,
            parameters=params
        ))
        
        return output_id

    def get_lineage_graph(self, artifact_id: str) -> List[Dict[str, Any]]:
        """
        Returns the history of how a specific artifact was created.
        """
        history = []
        current_id = artifact_id
        
        # Traverse backwards through lineage
        while True:
            step = next((s for s in self.lineage if s.output_id == current_id), None)
            if not step:
                # Must be a raw artifact
                val = self.artifacts.get(current_id)
                if val:
                    history.append({"type": "raw", "id": current_id})
                break
            
            history.append({
                "type": "transform",
                "op": step.operation,
                "inputs": step.input_ids,
                "params": step.parameters
            })
            # For simplicity, follow first input
            current_id = step.input_ids[0]
            
        return history[::-1] # Return in chronological order
