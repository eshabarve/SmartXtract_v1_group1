from llama_cpp import Llama

llm = Llama(
    model_path="path/to/your/model.gguf",  # e.g., llama-3-8b-instruct.Q4_K_M.gguf
    n_ctx=2048,
    logits_all=True  # <--- needed to get logits/logprobs
)


prompt = "Part: Drill motor, Quantity: 1, Price: $99.00"

output = llm(
    prompt,
    temperature=0.0,
    top_p=1.0,
    max_tokens=50,
    stop=["\n"],
    echo=True  # <-- include the prompt in the output
)

tokens = output["tokens"]           # list of tokens
token_strs = output["token_strs"]   # actual strings
logits = output["logits"]           # raw logits per token

import numpy as np

# Softmax to get probabilities
def softmax(logits):
    e = np.exp(logits - np.max(logits))
    return e / e.sum()

# Get top predicted token probabilities
for i, token in enumerate(token_strs):
    probs = softmax(logits[i])
    prob = probs[output["tokens"][i]]  # actual token's prob
    logprob = np.log(prob)
    print(f"Token: {token} | LogProb: {logprob:.4f}")


