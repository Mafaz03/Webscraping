import openai

def get_completion1(prompt, model="gpt-3.5-turbo"):
    openai.api_key = "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"
    messages = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]


# def get_completion2(prompt, model="gpt-3.5-turbo"):
#     openai.api_key = ""
#     messages = [{"role": "system", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0,
#     )
#     return response.choices[0].message["content"]


def get_completion2(prompt, model="gpt-3.5-turbo"):
    openai.api_key = ""
    messages = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]



def gpt1(question, content_list_complete, data_idx, result_queue):
    result1 = get_completion1(prompt=f""" 
        Data is in the form of tuples inside list: {content_list_complete[data_idx]} \n\n\n 
        Question: {question} \n\n\n
        Method of reply: 100 - 200 word sentences, clear reply,
        provide url if necessary.
        """)
    result_queue.put(result1)

def gpt2(question, content_list_complete, data_idx, result_queue):
    result2 = get_completion2(prompt=f""" 
        Data is in the form of tuples inside list: {content_list_complete[data_idx + 1]} \n\n\n 
        Question: {question} \n\n\n
        Method of reply: 100 - 200 word sentences, clear reply,
        provide url if necessary.
        """)
    result_queue.put(result2)

# def gpt3(question, content_list_complete, data_idx, result_queue):
#     result3 = get_completion3(prompt=f""" 
#         Data is in the form of tuples inside list: {content_list_complete[data_idx + 2]} \n\n\n 
#         Question: {question} \n\n\n
#         Method of reply: 100 - 200 word sentences, clear reply,
#         provide url if necessary.
#         """)
#     result_queue.put(result3)


