import numpy as np
from openai.embeddings_utils import distance_from_embeddings

df=pd.read_csv('processed/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

df.head()

def create_context(question, df, max_len=1800, size="ada"):
    '''
    create a context for a question by finding the most similar context in the df
    '''
    
    # get the embeddings for the question
    q_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002')['data'][0]['embedding']

    # get the distances from the embeddings
    df['distance'] = distances_from_embeddings(q_embeddings, df['embeddings'].valuse, distnace_metric='cosine')

    returns = []
    cur_len = 0

    # sort by distance and add the text to the context until the context is too long
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        
        # add the length of the text to the current length
        cur_len += row['n_tokens'] + 4

        # if the context is too long, break
        if cur_len > max_len:
            break

        # else add it to the text that is being returned
        returns.append(row["text"])

    # return the context
    return "\n\n###\n\n".join(returns)

def answer_question(
    df,
    model="gpt-3.5-turbo",
    question="Am I allowed to publish model outputs to Twitter, without a human review?",
    max_len=1800,
    size="ada",
    debug=False,
    max_tokens=150,
    sto_sequence=None
):
    '''
    answer a question based on the most similar context from the dataframe texts
    '''

    context = create_context(question, df, max_len=max_len, size=size)

    # if debug, print the raw model response
    if debug:
        print("Context:\n" + context)
        print("\n\n")

    try:
        # create a chat completion using the question and context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Answer the question based on the context below and if the question can't be answered based on the context, say \"I don't know\"\n\n"},
                {"role": "user", "content": f"Context: {context}\n\n---\n\nQuestion: {question}\nAnswer:"}
            ],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            pressence_penalty=0,
            stop=stop_sequence,
        )
        return response.choices[0].message.strip()
    except Exception as e:
        print(e)
        return ""

answer_question(df, question="What day is it?", debug=False)

answer_question(df, question="What is our newest embeddings model?")

answer_question(df, question="What is ChatGPT?")
