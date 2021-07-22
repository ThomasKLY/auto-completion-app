from transformers import GPT2LMHeadModel, GPT2Tokenizer

import torch
import torch.nn.functional as F
from tqdm import tqdm, trange

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model_dict = {}
device = 'cuda'


def generate_text(model_name, prompt, max_suggestion_length=20, top_p=0.8, num_return_sequences=3):
    model = model_dict.get(model_name)
    if model is None:
        model = GPT2LMHeadModel.from_pretrained(f"savedModel/{model_name}")
        model = model.to(device)
        model.eval()
        model_dict[model_name] = model

    generated = torch.tensor(tokenizer.encode(prompt)).unsqueeze(0).to(device)
    prompt_size = generated.shape[1]
    sample_outputs = model.generate(
        generated,
        do_sample=True,
        top_k=50,
        max_length=max_suggestion_length + prompt_size,
        top_p=top_p,
        num_return_sequences=num_return_sequences
    )

    results = [tokenizer.decode(output, skip_special_tokens=True) for output in sample_outputs]
    return results
