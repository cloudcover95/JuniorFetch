# juniorfetch/core/tda_mesh.py
import mlx.core as mx
import numpy as np
from juniorfetch.core.omni_math import SovereignOmniKernel
from juniorfetch.config import settings

class TDAMemoryMesh:
    def __init__(self):
        self.kernel = SovereignOmniKernel()
        self.capacity = 100000
        self.dim = settings.embedding_dim
        # Maintain in numpy for easy serialization, move to MLX for fast bitwise ops
        self.mesh_tensors = np.zeros((self.capacity, self.dim), dtype=np.float32)
        self.mesh_signatures = np.zeros((self.capacity, self.dim), dtype=np.int8)
        self.head_pointer = 0

    def _quantize_signature(self, x: mx.array) -> mx.array:
        return mx.where(x > 0, 1, -1)

    def encode(self, signal_tensor: mx.array, z_score: float = 1.8) -> bool:
        """
        Encodes a genuine MLX tensor into the topological mesh.
        """
        # Execute Metal-accelerated Q-Mark filtering
        z_mx = mx.array([z_score])
        q_mark = self.kernel.calculate_quantum_matrix(z_mx, mx.array([0.5]), mx.array([0.1]))[0].item()
        
        if q_mark < settings.etch_threshold:
            return False

        # Project and quantize
        projected = self.kernel.qr_manifold_projection(mx.reshape(signal_tensor, (1, self.dim)))
        signature = self._quantize_signature(projected)

        idx = self.head_pointer % self.capacity
        self.mesh_tensors[idx] = np.array(projected.tolist())
        self.mesh_signatures[idx] = np.array(signature.tolist(), dtype=np.int8)
        self.head_pointer += 1
        return True

    def bit_drift_search(self, query_tensor: mx.array, threshold: float = 0.18) -> np.ndarray:
        """Accelerated Hamming distance search over the mesh."""
        query_sig = self._quantize_signature(query_tensor)
        active = min(self.head_pointer, self.capacity)
        if active == 0:
            return np.array([])
            
        # Push signatures to unified memory for fast distance calculation
        mesh_sigs_mx = mx.array(self.mesh_signatures[:active])
        
        # Calculate bit drift (normalized Hamming distance)
        differences = mx.abs(mesh_sigs_mx - query_sig) / 2
        scores = mx.mean(differences, axis=1)
        
        # Pull back to numpy for indexing
        scores_np = np.array(scores.tolist())
        return np.where(scores_np < threshold)[0]
