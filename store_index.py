from src.helpers import data_load,tex_split,download_embeddings
# from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os

load_dotenv()

PINE_CONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINE_CONE_API_KEY

documents  = data_load("Data/")
text_chunks = tex_split(documents)
embedding_model = download_embeddings()


from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=PINE_CONE_API_KEY, environment="us-west1-gcp")

index_name = "medibot-pinecone"


pc.create_index(
name = index_name,
dimension=  384,
metric="cosine",
spec=ServerlessSpec(cloud="aws", region="us-east-1")

)



from langchain_pinecone import PineconeVectorStore


docsearch   = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embedding_model,
    index_name=index_name,
)





