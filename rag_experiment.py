import voyageai
import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

voyage_client = voyageai.Client()

DATA_PATH = "./data"

loader = PyPDFDirectoryLoader(DATA_PATH)
raw_documents = loader.load()

db = chromadb.PersistentClient(path="./chroma_db")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False
)

chunks = text_splitter.split_documents(raw_documents)

data = []
metadata = []
ids = []

for chunk in chunks:
    data.append(chunk.page_content)
    metadata.append(chunk.metadata)
    ids.append("ID_" + str(len(ids)))


def embed(text):
    response = voyage_client.embed(
        texts=[text],
        model="voyage-4",
    )
    return response.embeddings[0]


collection = db.get_or_create_collection("docker_docs")

embeddings = [embed(d) for d in data]
collection.upsert(
    documents=data,
    embeddings=embeddings,
    metadatas=metadata,
    ids=ids
)


def search_docs(query, collection):
    query_vector = embed(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3
    )
    docs = results['documents']
    return docs[0] if docs and docs[0] else ["No relevant documents found."]
