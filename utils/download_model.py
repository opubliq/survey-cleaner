# download_model.py
from huggingface_hub import hf_hub_download
import os

def download_llm(model_id="TheBloke/CodeLlama-7B-Instruct-GGUF", 
                 filename="codellama-7b-instruct.Q4_K_M.gguf",
                 cache_dir="models"):
    """Télécharge le modèle LLM depuis Hugging Face."""
    os.makedirs(cache_dir, exist_ok=True)
    
    model_path = hf_hub_download(
        repo_id=model_id,
        filename=filename,
        cache_dir=cache_dir
    )
    
    print(f"Modèle téléchargé: {model_path}")
    return model_path

if __name__ == "__main__":
    download_llm()