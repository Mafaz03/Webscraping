# Set your OpenAI API key
# api_key = input("Enter api key: ")
import openai

api_key = input("Enter your api key: ")

openai.api_key = api_key

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "system", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message["content"]



def split_dict(dictionary, n_parts):
    # Calculate the number of items in each part
    items_per_part = len(dictionary) // n_parts
    
    # Split the dictionary keys and values into sub-lists
    keys_split = [list(dictionary.keys())[i:i + items_per_part] for i in range(0, len(dictionary), items_per_part)]
    values_split = [list(dictionary.values())[i:i + items_per_part] for i in range(0, len(dictionary), items_per_part)]
    
    # Create sub-dictionaries
    sub_dicts = [{k: v for k, v in zip(keys, values)} for keys, values in zip(keys_split, values_split)]
    
    return sub_dicts
