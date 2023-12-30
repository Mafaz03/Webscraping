import nltk
from nltk.tokenize import sent_tokenize
from gensim.summarizer import summarize

# Download NLTK resources (if not downloaded)
nltk.download('punkt')

def extract_summary_by_keywords(text, keywords):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)

    # Initialize an empty summary
    summary = []

    # Extract sentences containing keywords
    for sentence in sentences:
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            summary.append(sentence)

    # Join the summary sentences
    summary_text = ' '.join(summary)
    return summary_text

# Get user input text
user_text = input("Enter the text: ")

# Get user input for keywords
keywords_input = input("Enter keywords separated by commas: ")
keywords = [keyword.strip() for keyword in keywords_input.split(",")]

# Extract summary based on user-input keywords (first filtering)
filtered_summary = extract_summary_by_keywords(user_text, keywords)

# Perform extractive summarization on the filtered summary
final_summary = summarize(filtered_summary)

# Print the extracted summary
print("\nSummary based on provided keywords (using extractive summarization):")
print(final_summary)