from llama_cpp import Llama
import numpy as np

llm = Llama(
     model_path="C:/Users/Nitin/models/llama3_8b_q5/meta-llama-3.1-8b-Q5_K_M.gguf",
     logits_all=True
     )

response = llm.create_completion(
     prompt="What is AI?",
     max_tokens=5,
     logprobs=1,
     echo=True
)

# Extract tokens and logprobs
tokens = response["choices"][0]["logprobs"]["tokens"]
logprobs = response["choices"][0]["logprobs"]["token_logprobs"]

probs = [np.exp(lp) if lp is not None else 0.0 for lp in logprobs]

print(tokens, probs)


for token, prob in zip(tokens, probs):
    print(f"{token:<15} | {prob*100:.2f}%")

# for token, logprob in zip(
#     response["choices"][0]["logprobs"]["tokens"],
#     response["choices"][0]["logprobs"]["token_logprobs"]
# ):
#     print(f"{token}: {logprob}")

# for token, logprob in zip(tokens, logprobs):
#     conf = math.exp(logprob) if logprob is not None else 0.0
#     print(f"{token:<20} | confidence: {conf:.4f}")

# # Average confidence
# avg_conf = np.mean([math.exp(lp) for lp in logprobs if lp is not None])
# print(f"\nAverage confidence: {avg_conf:.4f}")