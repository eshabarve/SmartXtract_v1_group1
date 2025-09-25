import ollama


def llm_structuring(prompt):

    response = ollama.chat(
        model='llama3.1',
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    return response['message']['content']