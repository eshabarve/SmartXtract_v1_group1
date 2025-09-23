import ollama


def llmStructuring(extracted_text, prompt):

    response = ollama.chat(
        model='llama3.1',
        messages=[
            {"role": "user", "content": prompt}
        ],
        
    )

    print(response['message']['content'])

    return response['message']['content']