# utils/llm_interface.py

from llama_cpp import Llama
import os

# Initialiser une seule fois
_model_path = "models/models--TheBloke--CodeLlama-7B-Instruct-GGUF/snapshots/2f064ee0c6ae3f025ec4e392c6ba5dd049c77969/codellama-7b-instruct.Q4_K_M.gguf"
llm = Llama(model_path=_model_path, n_ctx=2048)

def generate_r_script(prompt: str) -> str:
    output = llm(prompt, max_tokens=1024, stop=["</s>"])
    return output["choices"][0]["text"].strip()
