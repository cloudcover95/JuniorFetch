import numpy as np
from juniorfetch.core.omni_math import SovereignOmniKernel
from juniorfetch.config import settings

class TDAMemoryMesh:
    def __init__(self):
        self.kernel = SovereignOmniKernel()
        self.capacity = 100000
        self.dim = settings.embedding_dim
        self.mesh_tensors = np.zeros((self.capacity, self.dim), dtype=np.float32)
        self.mesh_signatures = np.zeros((self.capacity, self.dim), dtype=np.int8)
        self.head_pointer = 0

    def _quantize_signature(self, x):
        return np.where(x > 0, 1, -1).astype(np.int8)

    def encode(self, signal_tensor: np.ndarray, z_score: float = 1.8):
        q_mark = self.kernel.calculate_quantum_matrix(
            np.array([z_score]), np.array([0.5]), np.array([0.1])
        )[0]
        if q_mark < settings.etch_threshold:
            return False

        signal_t = signal_tensor.reshape(1, self.dim).T
        q, r = np.linalg.qr(signal_t)
        projected = (q @ r).flatten()
        signature = self._quantize_signature(projected)

        idx = self.head_pointer % self.capacity
        self.mesh_tensors[idx] = projected
        self.mesh_signatures[idx] = signature
        self.head_pointer += 1
        return True

    def bit_drift_search(self, query_tensor: np.ndarray, threshold: float = 0.18):
        query_sig = self._quantize_signature(query_tensor.flatten())
        active = min(self.head_pointer, self.capacity)
        if active == 0:
            return np.array([])
        scores = np.mean(np.abs(self.mesh_signatures[:active] - query_sig) / 2, axis=1)
        return np.where(scores < threshold)[0]