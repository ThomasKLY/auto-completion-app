from transformers import GPT2LMHeadModel, GPT2Tokenizer

import torch
import torch.nn.functional as F
from tqdm import tqdm, trange

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model_dict = {}


def generate(
        model_name,
        prompt,
        entry_count=10,
        entry_length=20,  # maximum number of words
        top_p=0.8,
        temperature=1.):

    model = model_dict.get(model_name)
    if model is None:
        model = GPT2LMHeadModel.from_pretrained(f"savedModel/{model_name}")
        model.eval()
        model_dict[model_name] = model

    generated_num = 0
    generated_list = []

    filter_value = -float("Inf")

    with torch.no_grad():

        for entry_idx in trange(entry_count):

            entry_finished = False
            input_ids = tokenizer.encode(prompt)
            prompt_length = len(input_ids)
            generated = torch.tensor(input_ids).unsqueeze(0)

            for i in range(entry_length + prompt_length):
                outputs = model(generated, labels=generated)
                loss, logits = outputs[:2]
                logits = logits[:, -1, :] / (temperature if temperature > 0 else 1.0)

                sorted_logits, sorted_indices = torch.sort(logits, descending=True)
                cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

                sorted_indices_to_remove = cumulative_probs > top_p
                sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[
                                                    ..., :-1
                                                    ].clone()
                sorted_indices_to_remove[..., 0] = 0

                indices_to_remove = sorted_indices[sorted_indices_to_remove]
                logits[:, indices_to_remove] = filter_value

                next_token = torch.multinomial(F.softmax(logits, dim=-1), num_samples=1)
                generated = torch.cat((generated, next_token), dim=1)

                if next_token in tokenizer.encode("<|endoftext|>"):
                    entry_finished = True

                if entry_finished:
                    generated_num = generated_num + 1

                    output_list = list(generated.squeeze().numpy())
                    output_text = tokenizer.decode(output_list[prompt_length:])
                    generated_list.append(output_text)
                    break

            if not entry_finished:
                output_list = list(generated.squeeze().numpy())
                output_text = f"{tokenizer.decode(output_list[prompt_length:])}"
                generated_list.append(output_text)

    return generated_list
