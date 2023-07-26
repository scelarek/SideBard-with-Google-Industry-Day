# imports
import ast  # for converting embeddings saved as strings back to arrays
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
import re  # for cleaning text
from scipy import spatial  # for calculating vector similarities for search
from scipy import __version__ as scipy_version
import os
import openai
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Markdown
from matplotlib.collections import LineCollection
import numpy as np
import requests

# Replace with the raw GitHub URL of the Python file
import io

# Replace with the raw GitHub URL of the CSV file
csv_url = "https://raw.githubusercontent.com/scelarek/Google-Industry-Day/95878152539660a5f5fe54659a2c226a0a075606/SideBard%20Chatbot/google_docs.csv"
response = requests.get(csv_url)

# Use io.StringIO to convert the response content to a file-like object
df = pd.read_csv(io.StringIO(response.text))


# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

# # # get the answer from the response
# df = pd.read_csv('google_docs.csv')

# convert embeddings from CSV str type back to list type
df['embedding'] = df['embedding'].apply(ast.literal_eval)




# search function
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]


# intergrating the Information of the user into the question

age = {
    "0-9": "I'm 0 to 9 years old.",
    "10-19": "I'm 10 to 19 years old.",
    "20-29": "I'm 20 to 29 years old.",
    "30-39": "I'm 30 to 39 years old.",
    "40-49": "I'm 40 to 49 years old.",
    "50-59": "I'm 50 to 59 years old.",
    "60-69": "I'm 60 to 69 years old.",
    "70 and above": "I'm 70 years old or above."
}

ai_familiarity = {
    "beginner": "I have basic knowledge about AI.",
    "moderate": "I have some experience and understanding about AI.",
    "expert": "I am highly knowledgeable and experienced about AI."
}

# Demo Personas
name = 'Samir'
input_age = "40-49"
input_ai_familiarity = "beginner"
custom_intro = f'{age[input_age]} {ai_familiarity[input_ai_familiarity]} Use the below articles on Google\'s help and user experience documentation to answer the subsequent question. If the answer cannot be found in the articles, answer to the best of your abilities but convey that you were unable to find the information with the Google Help dataset you were provided. Please say hello to {name} before offering your answer"'


# Model Parameters for Safety and Reliability
max_response_tokens = 300
temperature = 0.3
diversity_penlty = 0.5
Echo = True


def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = f'{custom_intro}'
    question = f"\n\nQuestion: {query}"
    message = introduction
    for string in strings:
        next_article = f'\n\Google Help article section:\n"""\n{string}\n"""'
        if (
            num_tokens(message + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message + question

def ask(
    query: str,
    df: pd.DataFrame = df,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
    max_response_tokens: int = max_response_tokens,
    temperature: float = temperature,
    diversity_penalty: float = diversity_penlty,
    top_p_value: float = 0.9
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You answer questions about the Google AI Powered Products."},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=max_response_tokens,
        top_p=top_p_value
    )
    response_message = response["choices"][0]["message"]["content"]
    return response_message
def display_answer_in_markdown(question: str, category: str):
    """Displays the answer in a user-friendly format using Markdown."""
    answer = ask(question)
    markdown_output = f"""
### Category: {category}  
### Question:  
{question}
    ---
### Answer:  
{answer} 
    ---
    """
    display(Markdown(markdown_output))


def plot_relatedness(answers: pd.DataFrame, colors: list = ['blue', 'red', 'yellow', 'green']) -> None:
    """
    Plots the relatedness of documents to a query using a bar chart.
    
    Parameters:
    - answers: A DataFrame with columns 'Relatedness' and 'Answer'.
    - colors: A list of colors for the bars.
    """
    
    # Define a set of colors and create a custom colormap
    num_colors = len(colors)
    bins = np.linspace(answers.Relatedness.min(), answers.Relatedness.max(), num_colors)
    segment_colors = np.array([colors[np.digitize(val, bins=bins) - 1] for val in answers.Relatedness])

    plt.figure(figsize=(10, 6))

    # Create the bar plot
    plt.bar(answers.index, answers.Relatedness, color=segment_colors, alpha=0.7)

    # Beautify the plot
    plt.title("Relatedness of Documents to Query", fontsize=16, fontweight='bold')
    plt.xlabel("Documents", fontsize=14)
    plt.ylabel("Relatedness (Cosine Similarity)", fontsize=14)
    plt.grid(axis='y', which='both', linestyle='--', linewidth=0.5)
    plt.xticks(ticks=answers.index, labels=answers['Answer'].str.split(',').str[0], rotation=90, ha='right')  # Set x-axis labels as the answers
    plt.tight_layout()
    plt.ylim(answers.Relatedness.min() * 0.95, answers.Relatedness.max() * 1.05)

    # Display the plot
    plt.show()

# Usage example
# plot_relatedness(answers_dataframe)




print("OpenAI version: ", openai.__version__)
print("Pandas version: ", pd.__version__)
print("Seaborn version: ", sns.__version__)
print("Numpy version: ", np.__version__)
print("Matplotlib version: ", plt.matplotlib.__version__)
print("Scipy version: ", scipy_version)

print('Other Libraries: requests, ast, tiktoken, os, IPython.display, re')
