import numpy as np

class SovereignOmniKernel:
    """Core web3node Omni Math kernel"""
    def __init__(self, variance_retention=0.95, h_bar_mkt=0.01):
        self.variance_retention = variance_retention
        self.h_bar_mkt = h_bar_mkt

    def calculate_quantum_matrix(self, z_scores, deltas, base_vols):
        safe_bases = np.where(base_vols > 0, base_vols, self.h_bar_mkt)
        action_hats = deltas / safe_bases
        q_marks = 1.0 - np.exp(-(np.abs(z_scores) * action_hats))
        return np.round(q_marks, 4)