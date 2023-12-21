import os
import pandas as pd
import matplotlib.pyplot as plt

def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie

# create a list to store the text files
texts=[]

domain = "openai.com"

# get all the text files in the text directory
for file in os.listdir(f"text/{domain}/"):

    # open the file and read the text
    with open(f"text/{domain}/{file}", "r", encoding="UTF-8") as f:
        text = f.read()

        # Omit the first 11 and last 4 lines, then replace -, _ and update with spaces.
        texts.append((file[11:-4].replace('-',' ').replace('_', ' ').replace('#update',''), text))

# create a dataframe from the list of texts
df = pd.DataFrame(texts, columns = ['fname', 'text'])

# set the text column to be the raw text with the newlines removed
df['text'] = df.fname + ". " + remove_newlines(df.text)
df.to_csv('processed/scraped.csv')
df.head()

import tiktoken

# load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('processed/scraped.csv', index_col=0)
df.columns = ['title', 'text']

# tokenize the text and save the number of tokens to a new column
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

# Visualize the distribution of the number of tokens per row using a histogram
df.n_tokens.hist()
# plt.show()

max_tokens = 500

# function to split the text into chunks of a maximum number of tokens
def split_into_many(text, max_tokens = max_tokens):

    # split text into sentences
    sentences = text.split('. ')

    # get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # loop through the sentences and toekns joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # if the number of tokens so far plus the number of tokens in the current sentence
        # than the max number of tokens, thena dd the chunk to list of chunks and
        # reset the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            toeksn_so_far = 0

        # if the number of tokens in the current sentence is greater than the 
        # max number of tokens, go to the next sentence
        if token > max_tokens:
            continue

        # otherwise add the sentence to the chunk and increment total
        chunks.append(sentence)
        tokens_so_far += token + 1

    return chunks

shortened = []

# Loop through the dataframe
for row in df.iterrows():

    # if the text is None, go to next row
    if row[1]['text'] is None:
        continue

    # if the number of tokens > max number of tokens
    if row[1]['n_tokens'] > max_tokens:
        shortened += split_into_many(row[1]['text'])
    # otherwise, add the text to the list of shortened texts

    else:
        shortened.append(row[1]['text'])

# visualize the update histogram again to confirm the rows are split!
df = pd.DataFrame(shortened, columns = ['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
df.n_tokens.hist()
# plt.show()

from openai import OpenAI
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def embedding_with_backoff(*args, **kwargs):
    print("calling embedding with backoff function")
    return client.embeddings.create(*args, **kwargs).data[0].embedding

df['embeddings'] = df.text.apply(lambda x: embedding_with_backoff(input=x, model='text-embedding-ada-002'))

df.to_csv('processed/embeddings.csv')
df.head()
