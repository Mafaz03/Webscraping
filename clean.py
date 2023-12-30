import re

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove newline characters
    text = text.replace('\n', ' ')

    # Remove extra white spaces
    text = re.sub(r'\s+', ' ', text)

    # Remove any text inside brackets (inclusive)
    text = re.sub(r'\[.*?\]', '', text)

    # Remove any text inside parentheses (inclusive)
    text = re.sub(r'\(.*?\)', '', text)

    return text.strip()

# Prompt the user for input
user_input = input("Please enter the text you want to clean: ")

# Clean the user's input
cleaned_text = clean_text(user_input)

# Print the cleaned text
print("Cleaned text: ",cleaned_text)