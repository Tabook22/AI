#source:https://www.youtube.com/watch?v=Cim1lNXvCzY

"""
follows a clear sequence of steps, starting from fetching the data using WikipediaLoader 
from the langchain_community package to creating embeddings and persisting them with Chroma, 
and finally setting up a retrieval-augmented question-answering model using RetrievalQA. 
"""


import os
from dotenv import load_dotenv
from langchain_community.document_loaders import WikipediaLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
import pprint

# Load environmental variables
load_dotenv()

"""
 First we are going to fetch information from Wikipedia regarding a specific topic, 
 in this case, "2023 Wimbledon Championships". 
"""
# Create a variable to  hold the information we are going to search for
search_term="2023 Wimbledon Championships"
# Here we are going to create an instance of the WikipediaLoader class
# load_max_docs=1: Limits the number of documents to retrieve to just one
docs=WikipediaLoader(query=search_term, load_max_docs=1).load()

# Split the text
# The reason we are splitting the whole docs, is we need to give LLM relvean infomraiton rather than giving it the whole docs, the idea is to imporve effeciency
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=100, #total number of characters in each chunks
    chunk_overlap=20, # overlapping characters from the previous and the next chunks meaning that the end of one chunk will overlap with the beginning of the next by 20 characters. Overlapping can help ensure that no context is lost at the boundaries of each chunk, which can be important for certain types of text analysis or processing.
    length_function=len, #This parameter is a function used to measure the length of the text. By default, and in this case, it uses Python's built-in len() function, which returns the number of characters in a string. This function is used by the splitter to determine when the chunk_size or chunk_overlap criteria are met.
    is_separator_regex=False, #This parameter indicates whether the splitter should interpret the chunk_size parameter as a regular expression for finding separators in the text (when True) or simply use the size value as the number of characters (when False). In this case, it's set to False, meaning the splitter will count characters directly rather than looking for pattern-based separators.
)

# look to the first three slices of the documents,
data=text_splitter.split_documents(docs)
result=data[:3]
print(result)

# Initialize the OpenAIEmbddings
embeddings= OpenAIEmbeddings()

# Lets create a store 
# Chroma is going to convert those text chunks of documents into vectors using the openai embeddings model
store = Chroma.from_documents(
    data, 
    embeddings, 
    ids = [f"{item.metadata['source']}-{index}" for index, item in enumerate(data)],
    collection_name="Wimbledon-Embeddings", 
persist_directory='db',
)
store.persist()

store.persist()

# Now we are going to ask questions about Wimbledon 2023
# Here we are going to use OpenaAI, Augmented by ChromaDB, to ask some questions about the tournament.
template = """You are a bot that answers questions about Wimbledon 2023, using only the context provided.
If you don't know the answer, simply state that you don't know.

{context}

Question: {question}"""

# Lets initialize the Openai model 
PROMPT= PromptTemplate(
    template=template, input_variables=["context", "question"]
)

llm=ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")

# Create a question and answer model in langchain
qa_with_source = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=store.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT, },
    return_source_documents=True,
)
# Ask simple question
pprint.pprint(
    qa_with_source("Did Russian players play?")
)