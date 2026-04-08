import json
import time
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np
from pydantic import BaseModel
from juniorfetch.config import settings
from juniorfetch.core.tda_mesh import TDAMemoryMesh

class MemoryObject(BaseModel):
    content: str
    metadata: Dict
    q_mark: float
    timestamp: float

class MemoryPalace:
    def __init__(self):
        self.root = settings.storage_path
        self.root.mkdir(parents=True, exist_ok=True)
        self.mesh = TDAMemoryMesh()

    def store(self, wing: str, hall: str, room: str, content: str, metadata: Dict = None, z_score: float = 1.8):
        synthetic = np.random.normal(size=(1, settings.embedding_dim)).astype(np.float32)
        success = self.mesh.encode(synthetic, z_score)
        if success:
            path = self.root / wing / hall / room / "data.jsonl"
            path.parent.mkdir(parents=True, exist_ok=True)
            obj = MemoryObject(
                content=content[:25000],
                metadata=metadata or {"wing": wing, "hall": hall, "room": room},
                q_mark=0.85,
                timestamp=time.time()
            )
            with open(path, "a") as f:
                f.write(obj.model_dump_json() + "\n")
            return True
        return False

    def semantic_search(self, query: str, wing: Optional[str] = None) -> List[Dict]:
        query_tensor = np.random.normal(size=(1, settings.embedding_dim)).astype(np.float32)
        valid = self.mesh.bit_drift_search(query_tensor)
        # Simplified return for demo - in production scan matching files
        results = []
        for p in self.root.rglob("data.jsonl"):
            with open(p) as f:
                for line in f:
                    if query.lower() in line.lower():
                        results.append(json.loads(line))
        return results[:20]