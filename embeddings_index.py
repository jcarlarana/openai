import os
import pandas as pd

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

# print the df
print(df)
print(df['text'][0])
