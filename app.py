from flask import Flask, render_template, request
from langchain.vectorstores import Pinecone
# from langchain.chains import create_retireval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
# from langchain.chains.retrieval_qa.base import create_retrieval_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from src.prompt import *
from src.helpers import *
import os



app = Flask(__name__)

load_dotenv()


PINE_CONE_API_KEY = os.environ.get("PINECONE_API_KEY")
HUGGINGFACEHUB_API_TOKEN =os.environ["HUGGINGFACEHUB_API_TOKEN"]



os.environ["PINECONE_API_KEY"] = PINE_CONE_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

embedding_model = download_embeddings()


# #Initializing the Pinecone
# Pinecone.init(api_key=PINE_CONE_API_KEY,
#               )


index_name = "medibot-pinecone"

docsearch = PineconeVectorStore.from_existing_index(
    embedding=embedding_model,
    index_name=index_name,
)


retriver = docsearch.as_retriever(search_type = 'similarity',search_kwargs={"k": 5})
# retrived_docs = retriver.invoke("What is the use of  Flood Insurance Policy?")

llm = HuggingFaceEndpoint(huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    provider="hf-inference",
)

chat_model = ChatHuggingFace(llm=llm)

prompt  = ChatPromptTemplate.from_messages(


    [
("system", system_prompt),
("human", "{input}")
    ]
)   

question_answer_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)

rag_chain = create_retrieval_chain(retriver,question_answer_chain)
# responce = rag_chain.invoke({"input":" Auto Insurance ? ?"})

# print(responce['answer'])




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get', methods=['POST','GET'])
def chat():
    msg = request.form['msg']
    input=msg
    print(input)
    # Perform the retrieval and question-answering
    response = rag_chain.invoke({"input": input})
    print("Response : ",response['answer'])
    return str(response['answer'])



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)