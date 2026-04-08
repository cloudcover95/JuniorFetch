# juniorfetch/core/llm_sandbox.py
import mlx.core as mx
from mlx_lm import load, generate
from typing import List, Dict

class SovereignAgenticSandbox:
    """
    Local LLM Controller for active inference over TDA meshes.
    Designed for zero-cloud, strictly local execution on M-series chips.
    """
    def __init__(self, model_path: str = "mlx-community/Meta-Llama-3-8B-Instruct-4bit"):
        print(f"[INIT] Loading Sovereign Sandbox Model: {model_path} into unified memory...")
        self.model, self.tokenizer = load(model_path)

    def generate_context_prompt(self, query: str, mesh_results: List[Dict]) -> str:
        """Constructs the RAG injection prompt."""
        context_block = "\n---\n".join(
            [f"Path: {r['metadata']['path']}\nContent: {r['content'][:2000]}" for r in mesh_results]
        )
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are the JuniorCloud LLC AI Assistant. Answer the query using ONLY the provided local system files context. Do not hallucinate.
<|eot_id|><|start_header_id|>user<|end_header_id|>
Context:
{context_block}

Query: {query}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        return prompt

    def execute_inference(self, query: str, mesh_results: List[Dict], max_tokens: int = 512) -> str:
        """Executes terminal-ready LLM inference based on retrieved local mesh data."""
        prompt = self.generate_context_prompt(query, mesh_results)
        response = generate(self.model, self.tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False)
        return response
